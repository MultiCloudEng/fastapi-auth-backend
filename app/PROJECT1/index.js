import React, { useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Home, Bookmark, Bell, Gift, Plus, Moon, Sun, MapPin, ChevronLeft } from "lucide-react";

const productData = [
  { id: 1, name: "XAPP Lime", accent: "from-lime-300 to-lime-500", text: "text-lime-700" },
  { id: 2, name: "XAPP Energy", accent: "from-yellow-300 to-lime-300", text: "text-yellow-700" },
  { id: 3, name: "XAPP Punch", accent: "from-pink-400 to-rose-500", text: "text-pink-700" },
  { id: 4, name: "XAPP Recovery", accent: "from-red-300 to-red-500", text: "text-red-700" },
  { id: 5, name: "XAPP Zero", accent: "from-violet-300 to-violet-500", text: "text-violet-700" },
];

const streakData = [12.6, 8.2, 2.9, 2.9];

function Stat({ label, value, unit, dark }) {
  return (
    <div className="flex-1 min-w-0">
      <p className={`text-[13px] font-semibold ${dark ? "text-white/90" : "text-slate-900"}`}>{label}</p>
      <div className="mt-2 flex items-end gap-1">
        <span className={`text-[38px] font-extrabold leading-none tracking-tight ${dark ? "text-indigo-300" : "text-indigo-900"}`}>
          {value}
        </span>
        <span className={`mb-1 text-sm ${dark ? "text-indigo-200" : "text-blue-500"}`}>{unit}</span>
      </div>
    </div>
  );
}

function CanMock({ accent, label, dark }) {
  return (
    <div className={`relative h-44 w-16 shrink-0 rounded-[20px] border ${dark ? "border-white/10 bg-zinc-900" : "border-slate-200 bg-zinc-900"} shadow-lg`}>
      <div className={`absolute inset-x-0 top-0 h-5 rounded-t-[20px] bg-gradient-to-r ${accent}`} />
      <div className="absolute left-1/2 top-7 -translate-x-1/2 text-[10px] font-bold tracking-[0.35em] text-white/85">XAPP</div>
      <div className={`absolute bottom-4 left-1/2 w-12 -translate-x-1/2 text-center text-[9px] font-medium ${dark ? "text-white/75" : "text-white/80"}`}>
        {label}
      </div>
      <div className="absolute inset-y-8 left-1/2 w-[2px] -translate-x-1/2 bg-white/15" />
    </div>
  );
}

function MainScreen({ dark, setDark, openEmptyPage }) {
  const stepGoal = 8000;
  const currentSteps = 6412;
  const progress = Math.min((currentSteps / stepGoal) * 100, 100);

  const containerClasses = dark
    ? "bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-white"
    : "bg-[#f6f7fb] text-slate-900";

  return (
    <div className={`relative mx-auto h-[812px] w-[375px] overflow-hidden rounded-[38px] border border-black/10 shadow-2xl ${containerClasses}`}>
      {!dark && (
        <>
          <div className="absolute -left-16 top-0 h-[360px] w-[280px] rounded-full bg-slate-200/55" />
          <div className="absolute -right-24 bottom-0 h-[220px] w-[280px] rounded-full bg-slate-200/35" />
        </>
      )}

      {dark && (
        <>
          <div className="absolute -left-20 top-0 h-[340px] w-[280px] rounded-full bg-indigo-500/10" />
          <div className="absolute -right-24 bottom-0 h-[220px] w-[300px] rounded-full bg-fuchsia-500/10" />
        </>
      )}

      <div className="relative z-10 flex h-full flex-col px-6 pb-6 pt-8">
        <div className="mb-4 flex items-start justify-between gap-3">
          <div>
            <h1 className="text-[22px] font-extrabold tracking-tight">Good morning Erkin</h1>
            <p className={`mt-3 text-[14px] ${dark ? "text-white/80" : "text-slate-800"}`}>
              You walked <span className="font-semibold text-fuchsia-500">6412</span> steps today, keep going!
            </p>
          </div>

          <button
            onClick={() => setDark(!dark)}
            className={`mt-1 flex h-11 w-11 items-center justify-center rounded-full border transition ${
              dark
                ? "border-white/10 bg-white/5 text-yellow-300"
                : "border-slate-200 bg-white/80 text-slate-700 shadow-sm"
            }`}
            aria-label="Toggle dark mode"
          >
            {dark ? <Sun size={18} /> : <Moon size={18} />}
          </button>
        </div>

        <div className="mb-10 mt-4 flex items-center gap-3">
          <div className={`relative h-4 flex-1 overflow-hidden rounded-full ${dark ? "bg-white/10" : "bg-slate-300"}`}>
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              className="h-full rounded-full bg-gradient-to-r from-indigo-700 to-blue-400"
            />
          </div>
          <div className="text-fuchsia-500">
            <Gift size={20} fill="currentColor" />
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <Stat label="Average:" value="4.2" unit="km" dark={dark} />
          <Stat label="Goal:" value="8" unit="km" dark={dark} />
          <Stat label="Total:" value="62.4" unit="km" dark={dark} />
        </div>

        <div className={`mt-10 rounded-[24px] p-5 shadow-2xl ${dark ? "bg-white/5 shadow-black/30 backdrop-blur-sm" : "bg-white shadow-slate-300/70"}`}>
          <h2 className="text-[16px] font-extrabold text-fuchsia-500">You’re on 12 day streaks!</h2>
          <div className="mt-4 flex items-center gap-4 overflow-x-auto pb-1">
            {streakData.map((item, index) => (
              <div
                key={index}
                className={`flex h-22 w-22 shrink-0 flex-col justify-center rounded-2xl border-2 p-3 ${
                  index === streakData.length - 1
                    ? "border-dashed border-fuchsia-400 bg-transparent text-fuchsia-500"
                    : "border-transparent bg-fuchsia-500 text-white shadow-lg shadow-fuchsia-500/20"
                }`}
              >
                <span className="text-[20px] font-extrabold leading-none">{item}</span>
                <span className="mt-1 text-[12px] font-semibold">km</span>
              </div>
            ))}
          </div>
        </div>

        <div className={`mt-8 rounded-[24px] p-4 ${dark ? "bg-white/5" : "bg-white"} shadow-xl`}>
          <div className="mb-3 flex items-center justify-between">
            <div>
              <p className={`text-sm font-semibold ${dark ? "text-white/85" : "text-slate-700"}`}>Energy drinks</p>
              <p className={`text-xs ${dark ? "text-white/50" : "text-slate-400"}`}>Swipe horizontally</p>
            </div>
          </div>
          <div className="flex gap-4 overflow-x-auto pb-2">
            {productData.map((product) => (
              <CanMock key={product.id} accent={product.accent} label={product.name} dark={dark} />
            ))}
          </div>
        </div>

        <div className="mt-auto flex items-end justify-between pt-4">
          <div className={`grid h-20 w-[280px] grid-cols-3 rounded-[24px] px-3 ${dark ? "bg-white/5 backdrop-blur-sm" : "bg-white/90 shadow-lg"}`}>
            {[
              { icon: MapPin, label: "Explore", active: true },
              { icon: Bookmark, label: "Saved" },
              { icon: Bell, label: "Updates" },
            ].map((item) => (
              <button key={item.label} className="flex flex-col items-center justify-center gap-1">
                <div className={`rounded-full p-2 ${item.active ? (dark ? "bg-violet-400/20 text-violet-300" : "bg-violet-100 text-violet-700") : dark ? "text-white/65" : "text-slate-500"}`}>
                  <item.icon size={18} />
                </div>
                <span className={`text-[11px] ${dark ? "text-white/75" : "text-slate-700"}`}>{item.label}</span>
              </button>
            ))}
          </div>

          <motion.button
            whileTap={{ scale: 0.96 }}
            whileHover={{ scale: 1.03 }}
            onClick={openEmptyPage}
            className="flex h-18 w-18 items-center justify-center rounded-full bg-violet-600 text-white shadow-2xl shadow-violet-500/30"
            aria-label="Open empty page"
          >
            <Plus size={34} />
          </motion.button>
        </div>
      </div>
    </div>
  );
}

function EmptyScreen({ dark, goBack }) {
  return (
    <div className={`relative mx-auto flex h-[812px] w-[375px] flex-col overflow-hidden rounded-[38px] border border-black/10 shadow-2xl ${dark ? "bg-slate-950 text-white" : "bg-[#f8f9fc] text-slate-900"}`}>
      <div className="flex items-center justify-between px-6 pt-8">
        <button
          onClick={goBack}
          className={`flex h-11 w-11 items-center justify-center rounded-full ${dark ? "bg-white/5" : "bg-white shadow"}`}
          aria-label="Go back"
        >
          <ChevronLeft size={20} />
        </button>
        <p className={`text-sm font-semibold ${dark ? "text-white/70" : "text-slate-500"}`}>Empty Page</p>
        <div className="w-11" />
      </div>

      <div className="flex flex-1 items-center justify-center px-8">
        <div className={`w-full rounded-[32px] border border-dashed p-10 text-center ${dark ? "border-white/15 bg-white/5" : "border-slate-300 bg-white/70"}`}>
          <div className={`mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full ${dark ? "bg-violet-400/15 text-violet-300" : "bg-violet-100 text-violet-700"}`}>
            <Plus size={28} />
          </div>
          <h2 className="text-xl font-bold">Second screen</h2>
          <p className={`mt-3 text-sm leading-6 ${dark ? "text-white/65" : "text-slate-500"}`}>
            This page is intentionally empty to match the assignment prototype requirement.
          </p>
        </div>
      </div>
    </div>
  );
}

export default function StepCounterAssignmentPrototype() {
  const [dark, setDark] = useState(false);
  const [screen, setScreen] = useState("home");

  const background = useMemo(
    () => (dark ? "bg-slate-950" : "bg-slate-100"),
    [dark]
  );

  return (
    <div className={`min-h-screen w-full ${background} flex items-center justify-center p-6`}>
      <AnimatePresence mode="wait">
        {screen === "home" ? (
          <motion.div
            key="home"
            initial={{ opacity: 0, y: 20, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.98 }}
            transition={{ duration: 0.28 }}
          >
            <MainScreen dark={dark} setDark={setDark} openEmptyPage={() => setScreen("empty")} />
          </motion.div>
        ) : (
          <motion.div
            key="empty"
            initial={{ opacity: 0, x: 24 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -24 }}
            transition={{ duration: 0.28 }}
          >
            <EmptyScreen dark={dark} goBack={() => setScreen("home")} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
