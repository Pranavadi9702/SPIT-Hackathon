function Settings() {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-4 lg:p-6 text-sm">
        <h2 className="text-sm font-semibold text-slate-900 mb-2">
          Settings (UI only)
        </h2>
        <p className="text-xs text-slate-500 mb-3">
          This page is a placeholder for future API-driven configuration options.
        </p>

        <div className="grid gap-4 md:grid-cols-2">
          <div className="border border-slate-100 rounded-2xl p-4">
            <h3 className="text-xs font-semibold text-slate-900 mb-1">
              Forecast Horizon
            </h3>
            <p className="text-xs text-slate-500 mb-2">
              Configure how many weeks ahead the AI model should forecast.
            </p>
            <select className="text-xs border border-slate-200 rounded-xl px-2 py-1.5 bg-slate-50">
              <option>4 weeks</option>
              <option>8 weeks</option>
              <option>12 weeks</option>
            </select>
          </div>

          <div className="border border-slate-100 rounded-2xl p-4">
            <h3 className="text-xs font-semibold text-slate-900 mb-1">
              Notifications
            </h3>
            <p className="text-xs text-slate-500 mb-2">
              Control email alerts for anomalies and forecast deviations.
            </p>
            <label className="flex items-center gap-2 text-xs text-slate-700">
              <input type="checkbox" className="rounded border-slate-300" defaultChecked />
              Weekly forecast summary
            </label>
            <label className="flex items-center gap-2 text-xs text-slate-700 mt-1">
              <input type="checkbox" className="rounded border-slate-300" />
              Anomaly alerts
            </label>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Settings;
