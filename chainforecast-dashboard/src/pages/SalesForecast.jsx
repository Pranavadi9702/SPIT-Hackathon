import ForecastChart from "../components/ForecastChart";
import { weeklySalesData, statsCards } from "../data/mockData";

function SalesForecast() {
  const totalForecast = statsCards[1]?.value || "₹13,20,000";

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-2">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">
            Sales Forecast
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            AI-powered projections for the next 4 weeks based on historical
            trends, seasonality and demand patterns.
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs">
          <button className="rounded-full border border-slate-200 bg-white px-3 py-1.5 font-medium text-slate-700 shadow-sm">
            Last 12 weeks
          </button>
          <button className="rounded-full bg-indigo-500 px-3.5 py-1.5 font-medium text-white shadow-sm hover:bg-indigo-600 transition">
            Export Forecast
          </button>
        </div>
      </div>

      {/* Summary + chart layout */}
      <div className="grid gap-4 lg:grid-cols-3">
        {/* AI Forecast summary card */}
        <div className="lg:col-span-1">
          <div className="relative overflow-hidden rounded-3xl bg-white border border-slate-100 shadow-[0_18px_45px_rgba(15,23,42,0.06)] p-5 flex flex-col gap-4">
            {/* Accent bar */}
            <div className="absolute inset-x-5 top-0 h-0.5 rounded-b-full bg-gradient-to-r from-indigo-500/80 via-sky-500/70 to-emerald-500/70" />

            <div>
              <h2 className="text-sm font-semibold text-slate-900">
                AI Forecast Summary
              </h2>
              <p className="text-xs text-slate-500 mt-1">
                High-confidence sales forecast generated from your recent
                transaction history and customer behavior.
              </p>
            </div>

            <div className="rounded-2xl bg-indigo-50/70 border border-indigo-100 px-4 py-3 text-sm">
              <div className="text-[11px] uppercase tracking-wide text-indigo-500 font-semibold mb-1">
                Next 4-week forecast
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-xl font-semibold text-slate-900">
                  {totalForecast}
                </span>
                <span className="text-xs text-emerald-600 font-medium">
                  +5.1% projected
                </span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="rounded-2xl border border-slate-100 bg-slate-50/60 px-3 py-2">
                <div className="text-[11px] text-slate-500 mb-0.5">
                  Model accuracy
                </div>
                <div className="font-semibold text-slate-900">94%</div>
              </div>
              <div className="rounded-2xl border border-slate-100 bg-slate-50/60 px-3 py-2">
                <div className="text-[11px] text-slate-500 mb-0.5">
                  Confidence band
                </div>
                <div className="font-semibold text-slate-900">
                  ± 6.5% variance
                </div>
              </div>
            </div>

            <div className="text-[11px] text-slate-500">
              Updated{" "}
              <span className="font-medium text-slate-900">2 hours ago</span>.
              Next refresh scheduled in 24 hours.
            </div>
          </div>
        </div>

        {/* Chart card */}
        <div className="lg:col-span-2">
          <div className="rounded-3xl border border-indigo-50 bg-gradient-to-b from-indigo-50/60 via-white to-white shadow-[0_18px_45px_rgba(15,23,42,0.06)] p-3 h-full">
            <div className="rounded-2xl bg-white border border-slate-100 h-full flex flex-col">
              {/* Chart header row */}
              <div className="px-5 pt-4 pb-2 flex items-center justify-between">
                <div>
                  <h2 className="text-sm font-semibold text-slate-900">
                    4-Week Sales Forecast
                  </h2>
                  <p className="text-xs text-slate-500 mt-0.5">
                    Compare AI-predicted revenue against actual performance to
                    spot gaps early.
                  </p>
                </div>
                <div className="flex items-center gap-3 text-[11px] text-slate-600">
                  
                </div>
              </div>

              {/* Chart body */}
              <div className="flex-1 px-3 pb-3">
                <div className="h-72 md:h-80">
                  <ForecastChart data={weeklySalesData} />
                </div>
              </div>

              {/* Chart footer */}
              <div className="px-5 pb-4 flex items-center justify-between text-[11px] text-slate-500">
                <div className="flex items-center gap-4">
                </div>
                <div>
                  Model window:{" "}
                  <span className="font-medium text-slate-900">
                    last 12 weeks
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* “How to use this” card */}
      <div className="bg-white rounded-3xl shadow-[0_18px_45px_rgba(15,23,42,0.04)] border border-slate-100 p-5 lg:p-6 text-xs text-slate-600">
        <h3 className="font-semibold text-slate-900 mb-2">
          How to act on this forecast
        </h3>
        <div className="grid md:grid-cols-3 gap-3">
          <ul className="list-disc pl-4 space-y-1">
            <li>Align inventory and staffing with upcoming demand peaks.</li>
            <li>Prepare buffer stock for products with volatile history.</li>
          </ul>
          <ul className="list-disc pl-4 space-y-1">
            <li>Trigger campaigns when forecast dips below revenue targets.</li>
            <li>Bundle low-performing SKUs with high-velocity ones.</li>
          </ul>
          <ul className="list-disc pl-4 space-y-1">
            <li>
              Combine with customer segments to focus on high-value cohorts.
            </li>
            <li>Share insights with sales teams for weekly planning.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default SalesForecast;
