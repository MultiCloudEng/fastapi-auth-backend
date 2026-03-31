from sqlalchemy import text
from app.db.session import engine

with engine.connect() as conn:
    conn.execute(text("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS is_admin BOOLEAN NOT NULL DEFAULT FALSE
    """))
    conn.commit()

print("is_admin column added successfully")