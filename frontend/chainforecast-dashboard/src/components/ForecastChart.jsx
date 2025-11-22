import React, { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
  CartesianGrid,
} from "recharts";

function ForecastChart({ data }) {
  // toggles
  const [showForecast, setShowForecast] = useState(true);
  const [smoothForecast, setSmoothForecast] = useState(true);

  // NEW: week dropdown state
  const [weekRange, setWeekRange] = useState(4);

  // Slice data based on selected week range
  const filteredData = data.slice(0, weekRange);

  return (
    <div className="bg-white rounded-3xl border border-slate-100 shadow-sm h-full flex flex-col">
      {/* Header */}
      <div className="px-6 pt-5 pb-3 flex items-center justify-between">
        <div>
          <h2 className="text-sm font-semibold text-slate-900">
            Sales: Actual vs Forecast
          </h2>
        </div>

        {/* Right controls: Dropdown + Toggles */}
        <div className="flex items-center gap-4 text-xs text-slate-600">
          
          {/* Weeks Dropdown */}
          <select
            value={weekRange}
            onChange={(e) => setWeekRange(Number(e.target.value))}
            className="border border-slate-300 rounded-lg px-2 py-1 text-xs focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value={4}>Last 4 weeks</option>
            <option value={8}>Last 8 weeks</option>
            <option value={12}>Last 12 weeks</option>
          </select>

          {/* Toggles */}
          <label className="inline-flex items-center gap-1">
            <input
              type="checkbox"
              className="accent-indigo-500"
              checked={showForecast}
              onChange={() => setShowForecast((prev) => !prev)}
            />
            <span>Show forecast</span>
          </label>

          <label className="inline-flex items-center gap-1">
            <input
              type="checkbox"
              className="accent-indigo-500"
              checked={smoothForecast}
              onChange={() => setSmoothForecast((prev) => !prev)}
            />
            <span>Smooth forecast</span>
          </label>
        </div>
      </div>

      {/* Chart */}
      <div className="flex-1 px-4 pb-4">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={filteredData}
            margin={{ top: 10, right: 24, left: 0, bottom: 8 }}
          >
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis
              dataKey="week"
              tick={{ fontSize: 12, fill: "#94a3b8" }}
              axisLine={{ stroke: "#e5e7eb" }}
            />
            <YAxis
              tick={{ fontSize: 12, fill: "#94a3b8" }}
              tickFormatter={(v) => `${v / 1000}k`}
              axisLine={{ stroke: "#e5e7eb" }}
            />
            <Tooltip
              formatter={(value) => `₹${value.toLocaleString()}`}
              labelStyle={{ fontSize: 12 }}
              contentStyle={{
                borderRadius: 12,
                borderColor: "#e5e7eb",
                fontSize: 12,
              }}
            />

            <Legend
              verticalAlign="top"
              align="center"
              wrapperStyle={{ fontSize: 12, paddingBottom: 12 }}
            />

            {/* Actual Line */}
            <Line
              type="monotone"
              dataKey="actual"
              name="Actual"
              stroke="#4f46e5"
              strokeWidth={2.2}
              dot={{ r: 3.5 }}
              activeDot={{ r: 5 }}
            />

            {/* Forecast Line */}
            {showForecast && (
              <Line
                type={smoothForecast ? "monotone" : "linear"}
                dataKey="forecast"
                name="Forecast"
                stroke="#22c55e"
                strokeWidth={2.2}
                strokeDasharray="4 4"
                dot={{ r: 3.5 }}
              />
            )}
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Footer */}
      <div className="px-6 pb-4 flex justify-between items-center text-xs text-slate-500">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-[#4f46e5]" />
            <span>Actual</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-[#22c55e]" />
            <span>Forecast</span>
          </div>
        </div>

        <span>
          Displaying last{" "}
          <span className="font-medium text-slate-900">{weekRange} weeks</span>
        </span>
      </div>
    </div>
  );
}

export default ForecastChart;
