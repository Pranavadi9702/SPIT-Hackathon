import { useEffect, useState } from "react";
import StatsCard from "../components/StatsCard";
import ForecastChart from "../components/ForecastChart";
import SegmentsChart from "../components/SegmentsChart";
import {
  statsCards as defaultStatsCards,
  weeklySalesData as defaultWeeklySalesData,
  customerSegmentsData as defaultCustomerSegmentsData,
} from "../data/mockData";

// Change this if your backend runs on a different host/port
const API_BASE_URL = "http://127.0.0.1:5000";

function Overview() {
  // Start with placeholders for values + percentages (fully runtime later)
  const [stats, setStats] = useState(
    defaultStatsCards.map((card) => ({
      ...card,
      value: "----",
      change: "---",
      changeLabel: card.changeLabel ?? "", // keep labels if defined
    }))
  );

  // Charts can start with mock data so layout is not empty
  const [weeklyData, setWeeklyData] = useState(defaultWeeklySalesData);

  const [loading, setLoading] = useState(true);

  const [segmentData, setSegmentData] = useState(defaultCustomerSegmentsData);
  const [totalCustomers, setTotalCustomers] = useState(null);

  useEffect(() => {
    async function fetchDashboardData() {
      try {
        // 1) Forecast summary for KPIs + line chart
        const resForecast = await fetch(`${API_BASE_URL}/api/forecast-summary`);
        const dataForecast = await resForecast.json();

        if (dataForecast.status === "success") {
          const apiWeekly = Array.isArray(dataForecast.weeklySalesData)
            ? dataForecast.weeklySalesData
            : [];

          // -------- Line chart data --------
          setWeeklyData(apiWeekly.length ? apiWeekly : defaultWeeklySalesData);

          // -------- KPI #1: Total Sales (Last 4 Weeks) --------
          const last4 = apiWeekly.slice(-4);
          const totalSalesNum = last4.reduce(
            (sum, d) => sum + (Number(d.actual) || 0),
            0
          );

          const totalSalesFormatted =
            totalSalesNum > 0
              ? `₹${Math.round(totalSalesNum).toLocaleString("en-IN")}`
              : "₹0";

          // % growth vs previous 4 weeks (if we have >= 8 data points)
          let totalSalesChangeText = "---";
          if (apiWeekly.length >= 8) {
            const prev4 = apiWeekly.slice(-8, -4);
            const prevSalesNum = prev4.reduce(
              (sum, d) => sum + (Number(d.actual) || 0),
              0
            );
            if (prevSalesNum > 0) {
              const growth =
                ((totalSalesNum - prevSalesNum) / prevSalesNum) * 100;
              const sign = growth > 0 ? "+" : growth < 0 ? "" : "";
              totalSalesChangeText = `${sign}${growth.toFixed(1)}%`;
            }
          }

          // -------- KPI #2: Forecasted Sales (Next 4 Weeks) --------
          const forecastFormatted =
            dataForecast.total_forecast_formatted || "₹0";

          const totalForecastNum =
            typeof dataForecast.total_forecast === "number"
              ? dataForecast.total_forecast
              : null;

          let forecastChangeText = "---";
          if (totalForecastNum != null && totalSalesNum > 0) {
            const growth =
              ((totalForecastNum - totalSalesNum) / totalSalesNum) * 100;
            const sign = growth > 0 ? "+" : growth < 0 ? "" : "";
            forecastChangeText = `${sign}${growth.toFixed(1)}%`;
          }

          // -------- Update KPI cards #1 and #2 (fully runtime) --------
          setStats((prev) =>
            prev.map((card) => {
              if (card.id === 1) {
                return {
                  ...card,
                  value: totalSalesFormatted,
                  change: totalSalesChangeText,
                  changeLabel: "vs previous 4 weeks",
                };
              }
              if (card.id === 2) {
                return {
                  ...card,
                  value: forecastFormatted,
                  change: forecastChangeText,
                  changeLabel: "vs last 4 weeks",
                };
              }
              return card;
            })
          );
        }

        // 2) Segments summary for pie chart + Total Customers + Top Segment
        const resSegments = await fetch(
          `${API_BASE_URL}/api/segments-summary`
        );
        const dataSegments = await resSegments.json();

        if (
          dataSegments.status === "success" &&
          Array.isArray(dataSegments.segments)
        ) {
          // -------- Pie chart data --------
          const segData = dataSegments.segments.map((s) => ({
            name: s.name,
            value: s.value,
          }));
          setSegmentData(segData.length ? segData : defaultCustomerSegmentsData);

          // -------- Base metrics from backend --------
          const totalCustomersCount =
            Array.isArray(dataSegments.customers) &&
            dataSegments.customers.length > 0
              ? dataSegments.customers.length
              : null;

          setTotalCustomers(totalCustomersCount);

          let topSegmentName = null;
          let topSegmentCount = null;

          if (segData.length > 0) {
            const topSeg = segData.reduce((a, b) =>
              b.value > a.value ? b : a
            );
            topSegmentName = topSeg.name;
            topSegmentCount = topSeg.value;
          }

          // High-value segments for KPI #3 change (Champions, Loyal, Potential)
          let pctHighValue = null;
          if (totalCustomersCount && totalCustomersCount > 0) {
            const highValueNames = [
              "Champions",
              "Loyal Customers",
              "Potential Loyalists",
            ];
            const highValueCount = segData
              .filter((s) => highValueNames.includes(s.name))
              .reduce((sum, s) => sum + (s.value || 0), 0);
            pctHighValue = (highValueCount / totalCustomersCount) * 100;
          }

          // Top segment share for KPI #4 change
          let pctTopSegment = null;
          if (
            totalCustomersCount &&
            totalCustomersCount > 0 &&
            topSegmentCount != null
          ) {
            pctTopSegment = (topSegmentCount / totalCustomersCount) * 100;
          }

          // -------- Update KPI #3 and #4 (fully runtime) --------
          setStats((prev) =>
            prev.map((card) => {
              // Total Customers card (id 3)
              if (card.id === 3 && totalCustomersCount != null) {
                const formattedTotal =
                  totalCustomersCount.toLocaleString("en-IN");
                return {
                  ...card,
                  value: formattedTotal,
                  change:
                    pctHighValue != null
                      ? `${pctHighValue.toFixed(1)}%`
                      : "---",
                  changeLabel: "in high-value segments",
                };
              }

              // Top Segment card (id 4)
              if (card.id === 4 && topSegmentName) {
                return {
                  ...card,
                  value: topSegmentName,
                  change:
                    pctTopSegment != null
                      ? `${pctTopSegment.toFixed(1)}%`
                      : "---",
                  changeLabel: "of total customers",
                };
              }

              return card;
            })
          );
        }
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
        // Fallback to mock data if backend fails completely
        setWeeklyData(defaultWeeklySalesData);
        setSegmentData(defaultCustomerSegmentsData);
        setStats(defaultStatsCards);
      } finally {
        setLoading(false);
      }
    }

    fetchDashboardData();
  }, []);

  return (
    <div className="space-y-6 text-slate-900 dark:text-slate-100">
      {/* Top header row */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
            Overview
          </h1>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            LSTM-powered demand forecasting, RFM segmentation, and campaign
            insights for your retail data.
          </p>
        </div>
      </div>

      {/* Optional inline "loading" info – this does NOT block clicks */}
      {loading && (
        <div className="rounded-3xl border border-slate-100 bg-white/70 dark:border-slate-800 dark:bg-slate-900/80 px-4 py-3 text-xs flex items-center gap-3 shadow-sm">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
          <div>
            <p className="font-medium text-slate-700 dark:text-slate-100">
              Running forecast pipeline...
            </p>
            <p className="text-[11px] text-slate-500 dark:text-slate-400">
              Fetching LSTM forecasts and customer segments
            </p>
          </div>
        </div>
      )}

      {/* Filter / toolbar row */}
      <div className="flex flex-col gap-3 rounded-3xl border border-slate-100 bg-white/70 p-4 shadow-sm backdrop-blur md:flex-row md:items-center md:justify-between dark:border-slate-800 dark:bg-slate-900/80">
        <div className="flex items-center gap-3">
          <div className="flex h-9 items-center gap-2 rounded-full border border-slate-200 bg-slate-50/70 px-3 dark:border-slate-700 dark:bg-slate-900/80">
            <span className="text-xs font-medium text-slate-500 dark:text-slate-400">
              Store
            </span>
            <select className="bg-transparent text-xs font-medium text-slate-900 outline-none dark:text-slate-100">
              <option>Main Store</option>
              <option>All Channels</option>
            </select>
          </div>

          <div className="flex h-9 items-center gap-2 rounded-full border border-slate-200 bg-slate-50/70 px-3 dark:border-slate-700 dark:bg-slate-900/80">
            <span className="text-xs font-medium text-slate-500 dark:text-slate-400">
              Horizon
            </span>
            <select className="bg-transparent text-xs font-medium text-slate-900 outline-none dark:text-slate-100">
              <option>Next 4 weeks</option>
              <option>Next 8 weeks</option>
              <option>Next 12 weeks</option>
            </select>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <div className="flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50/70 px-3 py-1 dark:border-slate-700 dark:bg-slate-900/80">
            <input
              type="text"
              placeholder="Filter segments..."
              className="flex-1 bg-transparent text-xs text-slate-600 outline-none placeholder:text-slate-400 dark:text-slate-200 dark:placeholder:text-slate-500"
            />
            <span className="text-lg text-slate-400 dark:text-slate-500">
              🔍
            </span>
          </div>

          <button className="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 shadow-sm dark:border-slate-700 dark:bg-slate-900/80 dark:text-slate-100">
            Last 4 weeks
          </button>
        </div>
      </div>

      {/* Stats cards row */}
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {stats.map((card) => (
          <StatsCard key={card.id} {...card} />
        ))}
      </div>

      {/* Charts row */}
      <div className="grid gap-4 lg:grid-cols-3">
        <div className="lg:col-span-2">
          {/* height similar to reference so it fits on screen */}
          <div className="h-[360px] rounded-3xl border border-slate-100 bg-white/80 p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900/80">
            <ForecastChart data={weeklyData} />
          </div>
        </div>
        <div>
          <div className="h-[360px] rounded-3xl border border-slate-100 bg-white/80 p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900/80">
            <SegmentsChart data={segmentData} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Overview;
