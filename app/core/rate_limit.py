"""In-memory rate limiting for login attempts (brute-force protection).

Failed attempts are counted per email and per client IP inside a sliding
time window. When a limit is reached, login returns 429 until the window passes.

Limitation: state lives in process memory, so it resets on restart and is not
shared between multiple instances. That is fine for a single small instance;
with several instances, use a shared store such as Redis.
"""
import threading
import time
from collections import defaultdict, deque


class LoginRateLimiter:
    def __init__(self, max_per_email: int, max_per_ip: int, window_seconds: int):
        self.max_per_email = max_per_email
        self.max_per_ip = max_per_ip
        self.window = window_seconds
        self._failures: dict[str, deque] = defaultdict(deque)
        self._lock = threading.Lock()

    def _prune(self, key: str, now: float) -> deque:
        q = self._failures[key]
        while q and now - q[0] >= self.window:
            q.popleft()
        return q

    def retry_after(self, email: str, ip: str) -> int:
        """Seconds until another attempt is allowed (0 = allowed now)."""
        now = time.monotonic()
        wait = 0.0
        with self._lock:
            for key, limit in ((f"email:{email}", self.max_per_email), (f"ip:{ip}", self.max_per_ip)):
                q = self._prune(key, now)
                if len(q) >= limit:
                    wait = max(wait, self.window - (now - q[0]))
        return int(wait) + 1 if wait > 0 else 0

    def record_failure(self, email: str, ip: str) -> None:
        now = time.monotonic()
        with self._lock:
            self._failures[f"email:{email}"].append(now)
            self._failures[f"ip:{ip}"].append(now)

    def reset_email(self, email: str) -> None:
        with self._lock:
            self._failures.pop(f"email:{email}", None)

    def clear(self) -> None:
        with self._lock:
            self._failures.clear()
