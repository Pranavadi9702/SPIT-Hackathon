// src/pages/SalesForecast.jsx
import { useEffect, useState } from "react";
import ForecastChart from "../components/ForecastChart";
import {
  weeklySalesData as mockWeeklySalesData,
  statsCards,
} from "../data/mockData";
import { fetchForecastSummary } from "../api/backend";

function SalesForecast() {
  const [chartData, setChartData] = useState(mockWeeklySalesData);
  const [totalForecast, setTotalForecast] = useState(
    statsCards[1]?.value || "₹13,20,000"
  );
  const [modelAccuracy, setModelAccuracy] = useState("—");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        setError("");
        const data = await fetchForecastSummary();

        if (data.total_forecast_formatted) {
          setTotalForecast(data.total_forecast_formatted);
        } else if (data.total_forecast) {
          setTotalForecast(
            `₹${Math.round(data.total_forecast).toLocaleString()}`
          );
        }

        if (data.metrics && data.metrics.accuracy_pct != null) {
          setModelAccuracy(`${data.metrics.accuracy_pct.toFixed(2)}%`);
        }

        if (data.weeklySalesData && data.weeklySalesData.length > 0) {
          setChartData(data.weeklySalesData);
        }
      } catch (err) {
        console.error(err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-2">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
            Sales Forecast
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            AI-powered projections for the next 4 weeks based on historical
            trends, seasonality and demand patterns.
          </p>
          {loading && (
            <p className="text-xs text-slate-500 mt-1">
              Updating forecast from backend...
            </p>
          )}
          {error && (
            <p className="text-xs text-red-500 mt-1">Backend error: {error}</p>
          )}
        </div>

        <div className="flex items-center gap-2 text-xs">
          <button className="rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-1.5 font-medium text-slate-700 dark:text-slate-100 shadow-sm">
            Last 12 weeks
          </button>
          <button className="rounded-full bg-indigo-500 px-3.5 py-1.5 font-medium text-white shadow-sm hover:bg-indigo-600 dark:hover:bg-indigo-400 transition">
            Export Forecast
          </button>
        </div>
      </div>

      {/* Summary + chart layout */}
      <div className="grid gap-4 lg:grid-cols-3">
        {/* AI Forecast summary card */}
        <div className="lg:col-span-1">
          <div className="relative overflow-hidden rounded-3xl bg-white/90 dark:bg-slate-900/80 border border-slate-100 dark:border-slate-700 shadow-[0_18px_45px_rgba(15,23,42,0.06)] dark:shadow-none p-5 flex flex-col gap-4">
            {/* Accent bar */}
            <div className="absolute inset-x-5 top-0 h-0.5 rounded-b-full bg-gradient-to-r from-indigo-500/80 via-sky-500/70 to-emerald-500/70" />

            <div>
              <h2 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                AI Forecast Summary
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                High-confidence sales forecast generated from your recent
                transaction history and customer behavior.
              </p>
            </div>

            <div className="rounded-2xl bg-indigo-50/70 dark:bg-indigo-500/15 border border-indigo-100 dark:border-indigo-500/40 px-4 py-3 text-sm">
              <div className="text-[11px] uppercase tracking-wide text-indigo-500 font-semibold mb-1">
                Next 4-week forecast
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-xl font-semibold text-slate-900 dark:text-slate-100">
                  {totalForecast}
                </span>
                {/* This projected percentage is presentational — you can compute or replace it */}
                <span className="text-xs text-emerald-600 dark:text-emerald-400 font-medium">
                  +5.1% projected
                </span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="rounded-2xl border border-slate-100 dark:border-slate-700 bg-slate-50/60 dark:bg-slate-800/80 px-3 py-2">
                <div className="text-[11px] text-slate-500 dark:text-slate-400 mb-0.5">
                  Model accuracy
                </div>
                <div className="font-semibold text-slate-900 dark:text-slate-100">
                  {/* show runtime modelAccuracy (falls back to placeholder if "—") */}
                  {modelAccuracy === "—" ? "94%" : modelAccuracy}
                </div>
              </div>
              <div className="rounded-2xl border border-slate-100 dark:border-slate-700 bg-slate-50/60 dark:bg-slate-800/80 px-3 py-2">
                <div className="text-[11px] text-slate-500 dark:text-slate-400 mb-0.5">
                  Confidence band
                </div>
                <div className="font-semibold text-slate-900 dark:text-slate-100">
                  ± 6.5% variance
                </div>
              </div>
            </div>

            <div className="text-[11px] text-slate-500 dark:text-slate-400">
              Updated{" "}
              <span className="font-medium text-slate-900 dark:text-slate-100">
                2 hours ago
              </span>
              . Next refresh scheduled in 24 hours.
            </div>
          </div>
        </div>

        {/* Chart card */}
        <div className="lg:col-span-2">
          <div className="rounded-3xl border border-indigo-50 dark:border-slate-700 bg-gradient-to-b from-indigo-50/60 via-white to-white dark:from-slate-900 dark:via-slate-950 dark:to-slate-950 shadow-[0_18px_45px_rgba(15,23,42,0.06)] dark:shadow-none p-3 h-full">
            <div className="rounded-2xl bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-700 h-full flex flex-col">
              {/* Chart header row */}
              <div className="px-5 pt-4 pb-2 flex items-center justify-between">
                <div>
                  <h2 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                    4-Week Sales Forecast
                  </h2>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                    Compare AI-predicted revenue against actual performance to
                    spot gaps early.
                  </p>
                </div>
                <div className="flex items-center gap-3 text-[11px] text-slate-600 dark:text-slate-400"></div>
              </div>

              {/* Chart body */}
              <div className="flex-1 px-3 pb-3">
                <div className="h-72 md:h-80">
                  {/* IMPORTANT: use runtime chartData (keeps all logic intact) */}
                  <ForecastChart data={chartData} />
                </div>
              </div>

              {/* Chart footer */}
              <div className="px-5 pb-4 flex items-center justify-between text-[11px] text-slate-500 dark:text-slate-400">
                <div className="flex items-center gap-4" />
                <div>
                  Model window:{" "}
                  <span className="font-medium text-slate-900 dark:text-slate-100">
                    last 12 weeks
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* “How to use this” card */}
      <div className="bg-white/90 dark:bg-slate-900/80 rounded-3xl shadow-[0_18px_45px_rgba(15,23,42,0.04)] dark:shadow-none border border-slate-100 dark:border-slate-700 p-5 lg:p-6 text-xs text-slate-600 dark:text-slate-300">
        <h3 className="font-semibold text-slate-900 dark:text-slate-100 mb-2">
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
            <li>Combine with customer segments to focus on high-value cohorts.</li>
            <li>Share insights with sales teams for weekly planning.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default SalesForecast;