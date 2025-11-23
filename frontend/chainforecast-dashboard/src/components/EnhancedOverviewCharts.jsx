// src/components/EnhancedOverviewCharts.jsx
import React, { useMemo, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
} from "recharts";

const SEGMENT_COLORS = ["#6366F1", "#10B981", "#60A5FA", "#F97316", "#9CA3AF"];

// simple moving average smoothing (window 2)
function smoothen(data, key) {
  return data.map((d, i, arr) => {
    const prev = arr[i - 1] ? arr[i - 1][key] : d[key];
    return { ...d, [key]: Math.round((prev + d[key]) / 2) };
  });
}

/**
 * EnhancedOverviewCharts
 * - uses your existing weeklySalesData + customerSegmentsData
 * - gives you:
 *   • Sales: Actual vs Forecast chart with toggles
 *   • Customer Segments donut with legend + actions
 */
export default function EnhancedOverviewCharts({
  weeklySalesData,
  segmentsData,
  totalCustomers = 8452,
  accuracy = 94,
}) {
  const [showForecast, setShowForecast] = useState(true);
  const [smoothForecast, setSmoothForecast] = useState(false);
  const [segmentSearch, setSegmentSearch] = useState("");

  const lineData = useMemo(() => {
    if (!smoothForecast) return weeklySalesData;
    return smoothen(weeklySalesData, "forecast");
  }, [smoothForecast, weeklySalesData]);

  const filteredSegments = useMemo(() => {
    const q = segmentSearch.trim().toLowerCase();
    if (!q) return segmentsData;
    return segmentsData.filter((s) => s.name.toLowerCase().includes(q));
  }, [segmentSearch, segmentsData]);

  const totalSegmentValue = filteredSegments.reduce(
    (sum, s) => sum + s.value,
    0
  );

  return (
    <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Sales chart card */}
      <div className="lg:col-span-2 bg-white rounded-3xl p-5 shadow-sm border border-gray-100">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h3 className="text-sm sm:text-base font-semibold text-slate-900">
              4-Week Sales Forecast
            </h3>
            <p className="text-xs text-slate-500">
              Actual vs AI-predicted sales performance
            </p>
          </div>

          <div className="flex flex-col items-end gap-1">
            <div className="text-[11px] text-slate-400">
              Updated{" "}
              <span className="font-medium text-slate-500">2 hours ago</span>
            </div>
            <div className="flex items-center gap-3 text-[11px] text-slate-600">
              <label className="flex items-center gap-1 cursor-pointer">
                <input
                  type="checkbox"
                  checked={showForecast}
                  onChange={(e) => setShowForecast(e.target.checked)}
                  className="rounded border-slate-300"
                />
                <span>Show forecast</span>
              </label>
              <label className="flex items-center gap-1 cursor-pointer">
                <input
                  type="checkbox"
                  checked={smoothForecast}
                  onChange={(e) => setSmoothForecast(e.target.checked)}
                  className="rounded border-slate-300"
                />
                <span>Smooth forecast</span>
              </label>
            </div>
          </div>
        </div>

        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={lineData}
              margin={{ top: 10, right: 20, left: -10, bottom: 0 }}
            >
              <CartesianGrid strokeDasharray="4 6" stroke="#F1F5F9" />
              <XAxis
                dataKey="week"
                tickLine={false}
                axisLine={false}
                tick={{ fontSize: 12, fill: "#94a3b8" }}
              />
              <YAxis
                tickFormatter={(v) => `${v / 1000}k`}
                tick={{ fontSize: 12, fill: "#94a3b8" }}
                axisLine={false}
              />
              <Tooltip
                formatter={(value) => `₹${value.toLocaleString()}`}
                labelStyle={{ fontSize: 12 }}
              />
              <Legend
                verticalAlign="top"
                align="center"
                wrapperStyle={{ fontSize: 12, paddingBottom: 8 }}
              />

              <Line
                type="monotone"
                dataKey="actual"
                name="Actual Sales"
                stroke="#6366F1"
                strokeWidth={2.5}
                dot={{ r: 3 }}
                activeDot={{ r: 5 }}
              />
              {showForecast && (
                <Line
                  type="monotone"
                  dataKey="forecast"
                  name="Forecasted Sales"
                  stroke="#10B981"
                  strokeWidth={2.5}
                  strokeDasharray="5 5"
                  dot={false}
                />
              )}
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-3 flex items-center gap-4 text-[11px] text-slate-500">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-indigo-500" />
            Actual Sales
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            Forecasted Sales
          </div>
          <div className="ml-auto">
            Accuracy:{" "}
            <span className="font-semibold text-slate-900">
              {accuracy}%
            </span>
          </div>
        </div>
      </div>

      {/* Customer Segments card */}
      <div className="bg-white rounded-3xl p-5 shadow-sm border border-gray-100 flex flex-col">
        <div className="flex items-start justify-between mb-3">
          <div>
            <h3 className="text-sm sm:text-base font-semibold text-slate-900">
              Customer Segments
            </h3>
            <p className="text-xs text-slate-500">
              Distribution of customers by RFM segments
            </p>
          </div>
          <div className="text-right">
            <div className="text-[11px] text-slate-400">Monthly</div>
            <div className="text-[11px] text-slate-500">
              Total{" "}
              <span className="font-semibold text-slate-900">
                {totalCustomers.toLocaleString()}
              </span>
            </div>
          </div>
        </div>

        {/* Search inside segments */}
        <div className="mb-3">
          <input
            value={segmentSearch}
            onChange={(e) => setSegmentSearch(e.target.value)}
            placeholder="Filter segments..."
            className="w-full rounded-full border border-slate-200 px-3 py-1.5 text-[11px] focus:outline-none focus:ring-2 focus:ring-indigo-100"
          />
        </div>

        <div className="flex gap-4 items-center flex-1">
          {/* Donut */}
          <div className="w-32 h-32 sm:w-36 sm:h-36 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={filteredSegments}
                  dataKey="value"
                  nameKey="name"
                  innerRadius={35}
                  outerRadius={55}
                  paddingAngle={4}
                  strokeWidth={0}
                >
                  {filteredSegments.map((entry, index) => (
                    <Cell
                      key={entry.name}
                      fill={SEGMENT_COLORS[index % SEGMENT_COLORS.length]}
                    />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Legend */}
          <div className="flex-1">
            <ul className="space-y-2">
              {filteredSegments.map((seg, idx) => {
                const percent =
                  totalSegmentValue > 0
                    ? (seg.value / totalSegmentValue) * 100
                    : 0;
                return (
                  <li
                    key={seg.name}
                    className="flex items-center justify-between"
                  >
                    <div className="flex items-center gap-2">
                      <span
                        className="w-2.5 h-2.5 rounded-full"
                        style={{
                          backgroundColor:
                            SEGMENT_COLORS[idx % SEGMENT_COLORS.length],
                        }}
                      />
                      <div>
                        <div className="text-xs font-medium text-slate-900">
                          {seg.name}
                        </div>
                        <div className="text-[10px] text-slate-400">
                          {seg.value}% of base
                        </div>
                      </div>
                    </div>
                    <div className="text-xs font-semibold text-slate-900">
                      {percent.toFixed(0)}%
                    </div>
                  </li>
                );
              })}
            </ul>
          </div>
        </div>

        <div className="mt-4 flex justify-end">
          <button className="inline-flex items-center justify-center rounded-full px-4 py-1.5 text-[11px] font-medium text-white bg-gradient-to-r from-indigo-500 to-indigo-600 shadow-sm hover:shadow-md transition">
            View Segment Details
          </button>
        </div>
      </div>
    </section>
  );
}
