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
          <h1 className="text-2xl font-semibold text-slate-900">
            Sales Forecast
          </h1>
          <p className="text-sm text-slate-500 mt-1">
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

        <div className="text-right">
          <p className="text-sm text-slate-500">
            Forecasted Sales (Next 4 Weeks)
          </p>
          <p className="text-2xl font-semibold text-emerald-600">
            {totalForecast}
          </p>
          <p className="text-xs text-slate-400 mt-1">LSTM-based chain forecast</p>
        </div>
      </div>

      {/* Summary + chart layout */}
      <div className="grid gap-4 lg:grid-cols-3">
        {/* Left: AI summary card */}
        <div className="lg:col-span-1">
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-b from-slate-900 via-slate-900 to-slate-950 text-slate-50 p-5 h-full flex flex-col gap-4">
            {/* Glow background */}
            <div className="pointer-events-none absolute inset-0">
              <div className="absolute -top-24 -left-10 w-40 h-40 rounded-full bg-indigo-500/20 blur-3xl" />
              <div className="absolute -bottom-20 right-0 w-52 h-52 rounded-full bg-emerald-500/20 blur-3xl" />
            </div>

            <div className="relative flex items-center justify-between">
              <div>
                <p className="text-xs text-slate-400">AI Summary</p>
                <p className="text-lg font-semibold mt-1">
                  Next 4-week forecast
                </p>
              </div>
              <div className="flex items-center gap-2 text-xs bg-slate-800/80 border border-slate-600/70 rounded-full px-3 py-1">
                <span className="inline-flex h-2 w-2 rounded-full bg-emerald-400" />
                <span>Model: LSTM</span>
              </div>
            </div>

            <div className="relative">
              <p className="text-[11px] uppercase tracking-wide text-slate-400 mb-1">
                Predicted Total
              </p>
              <div className="flex items-baseline gap-2">
                <span className="text-2xl font-semibold">{totalForecast}</span>
              </div>
            </div>

            <div className="relative grid grid-cols-2 gap-3 text-xs">
              <div className="rounded-2xl border border-slate-700/70 bg-slate-900/60 px-3 py-2">
                <div className="text-[11px] text-slate-400 mb-0.5">
                  Model accuracy
                </div>
                <div className="font-semibold text-slate-50">
                  {modelAccuracy}
                </div>
              </div>
              <div className="rounded-2xl border border-slate-700/70 bg-slate-900/60 px-3 py-2">
                <div className="text-[11px] text-slate-400 mb-0.5">
                  Confidence band
                </div>
                <div className="font-semibold text-slate-50">
                  ±10–15% (heuristic)
                </div>
              </div>
            </div>

            <div className="relative text-xs text-slate-300 space-y-2">
              <p className="font-medium text-slate-200">How to use this:</p>
              <ul className="list-disc pl-4 space-y-1">
                <li>Align inventory planning with forecasted demand.</li>
                <li>Prioritize campaigns in high-performing weeks.</li>
                <li>
                  Monitor deviations between actual vs forecast to refine the
                  model.
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Right: Chart */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-3xl shadow-sm border border-slate-200 p-4 h-full">
            <ForecastChart data={chartData} />
          </div>
        </div>
      </div>

      {/* Usage tips / explanation */}
      <div className="grid gap-4 md:grid-cols-2">
        <div className="bg-white rounded-3xl border border-slate-200 p-4 text-sm space-y-2">
          <h2 className="font-semibold text-slate-900">
            Model & Data Assumptions
          </h2>
          <ul className="list-disc pl-4 space-y-1 text-slate-600">
            <li>Weekly aggregation from your transaction history.</li>
            <li>Outliers and cancelled invoices are cleaned.</li>
            <li>Forecast horizon: exactly 4 weeks ahead.</li>
          </ul>
        </div>

        <div className="bg-white rounded-3xl border border-slate-200 p-4 text-sm space-y-2">
          <h2 className="font-semibold text-slate-900">
            Best practices using this forecast
          </h2>
          <ul className="list-disc pl-4 space-y-1">
            <li>Align marketing spends around expected peaks.</li>
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
