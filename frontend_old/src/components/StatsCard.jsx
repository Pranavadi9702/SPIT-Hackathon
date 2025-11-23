function StatsCard({ title, value, change, changeLabel, icon }) {
  const isNegative = change?.trim().startsWith("-");

  return (
    <div className="relative overflow-hidden rounded-3xl bg-white/90 dark:bg-slate-900/80 border border-slate-100 dark:border-slate-700 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all p-4 lg:p-5 flex flex-col gap-3">
      {/* subtle top accent */}
      <div className="absolute inset-x-4 top-0 h-0.5 rounded-b-full bg-gradient-to-r from-indigo-500/70 via-sky-500/70 to-emerald-500/70" />

      <div className="flex items-start justify-between">
        <div className="text-[11px] font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wide leading-snug max-w-[70%]">
          {title}
        </div>

        <div className="h-9 w-9 rounded-2xl bg-gradient-to-br from-indigo-500/10 via-sky-500/10 to-emerald-500/10 dark:from-indigo-500/20 dark:via-sky-500/20 dark:to-emerald-500/20 border border-slate-100 dark:border-slate-700 flex items-center justify-center text-lg">
          <span className="drop-shadow-sm">{icon}</span>
        </div>
      </div>

      <div className="flex items-baseline justify-between gap-2">
        <div className="text-2xl md:text-3xl font-semibold text-slate-900 dark:text-slate-100">
          {value}
        </div>
      </div>

      <div className="flex items-center gap-1.5 text-xs mt-1">
        <span
          className={`inline-flex items-center rounded-full px-2 py-0.5 font-medium ${
            isNegative
              ? "bg-rose-50 text-rose-600 dark:bg-rose-500/15 dark:text-rose-300"
              : "bg-emerald-50 text-emerald-600 dark:bg-emerald-500/15 dark:text-emerald-300"
          }`}
        >
          <span
            className={`mr-1 h-1.5 w-1.5 rounded-full ${
              isNegative ? "bg-rose-500" : "bg-emerald-500"
            }`}
          />
          {change}
        </span>
        <span className="text-slate-500 dark:text-slate-400">
          {changeLabel}
        </span>
      </div>
    </div>
  );
}

export default StatsCard;