import { useState } from "react";
import StatsCard from "../components/StatsCard";
import ForecastChart from "../components/ForecastChart";
import {
  statsCards,
  weeklySalesData,
  customerSegmentsData,
} from "../data/mockData";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

// Colors consistent with other charts
const SEGMENT_COLORS = [
  "#4f46e5", // Champions
  "#22c55e", // Loyal Customers
  "#0ea5e9", // At-Risk
  "#f97316", // New Customers
  "#9ca3af", // Others (if any)
];

function Overview() {
  // week range state for 4, 6, 12 weeks
  const [weekRange, setWeekRange] = useState(4);

  // slice the weekly data according to selected range
  const filteredWeeklySales = weeklySalesData.slice(0, weekRange);

  // segment data for donut
  const totalSegmentValue = customerSegmentsData.reduce(
    (sum, s) => sum + (s.value || 0),
    0
  );

  const segments = customerSegmentsData.map((s, index) => {
    const percent =
      totalSegmentValue > 0 ? (s.value / totalSegmentValue) * 100 : 0;
    return {
      ...s,
      percent,
      color: SEGMENT_COLORS[index % SEGMENT_COLORS.length],
    };
  });

  return (
    <div className="space-y-6">
      {/* Top header row */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Overview</h1>
          <p className="text-sm text-slate-500 mt-1">
            Interactive sales insights — range:{" "}
            <span className="font-medium">{weekRange}w</span>
          </p>
        </div>

        {/* Search + filters */}
        <div className="flex items-center gap-3">
          <div className="hidden md:flex items-center rounded-full border border-slate-200 bg-white px-3 py-1.5 text-sm shadow-sm min-w-[220px]">
            <input
              type="text"
              placeholder="Filter segments..."
              className="flex-1 outline-none text-xs text-slate-600 placeholder:text-slate-400 bg-transparent"
            />
            <span className="text-slate-400 text-lg">🔍</span>
          </div>

          {/* Week range dropdown */}
          <select
            value={weekRange}
            onChange={(e) => setWeekRange(Number(e.target.value))}
            className="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value={4}>Last 4 weeks</option>
            <option value={6}>Last 6 weeks</option>
            <option value={12}>Last 12 weeks</option>
          </select>

          <button className="rounded-full bg-indigo-500 px-3.5 py-1.5 text-xs font-medium text-white shadow-sm hover:bg-indigo-600 transition">
            Export CSV
          </button>
        </div>
      </div>

      {/* Stats cards row */}
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {statsCards.map((card) => (
          <StatsCard key={card.id} {...card} />
        ))}
      </div>

      {/* Charts row */}
      <div className="grid gap-4 lg:grid-cols-3">
        {/* Left: forecast chart */}
        <div className="lg:col-span-2">
          <div className="h-[360px]">
            <ForecastChart data={filteredWeeklySales} />
          </div>
        </div>

        {/* Right: Customer Segments donut – styled like Segment Share card */}
        <div>
          <div className="bg-white rounded-3xl border border-slate-100 shadow-sm p-5 flex flex-col h-[320px]">
            {/* Header */}
            <div className="flex items-start justify-between mb-3">
              <div>
                <h2 className="text-sm font-semibold text-slate-900">
                  Customer Segments
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  RFM distribution
                </p>
              </div>
              <div className="text-right text-[11px] text-slate-500">
                Total{" "}
                <span className="font-semibold text-slate-900">
                  {totalSegmentValue.toLocaleString()}
                </span>
              </div>
            </div>

            {/* Donut + legend */}
            <div className="flex-1 flex items-center gap-3">
              {/* Donut chart – same proportions as Segment Share card */}
              <div className="w-1/2 h-full min-h-[220px] flex items-center justify-center">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={segments}
                      dataKey="value"
                      nameKey="name"
                      innerRadius={50}
                      outerRadius={70}
                      paddingAngle={3}
                      stroke="#ffffff"
                      strokeWidth={3}
                    >
                      {segments.map((entry) => (
                        <Cell
                          key={entry.name}
                          fill={entry.color}
                        />
                      ))}
                    </Pie>
                    <Tooltip
                      formatter={(value, _name, props) => {
                        const val = Number(value) || 0;
                        const percent =
                          totalSegmentValue > 0
                            ? ((val / totalSegmentValue) * 100).toFixed(0)
                            : 0;
                        return [`${percent}% of base`, props.payload.name];
                      }}
                      contentStyle={{
                        borderRadius: 12,
                        borderColor: "#e5e7eb",
                        fontSize: 12,
                      }}
                    />
                    {/* no Recharts Legend – we use custom legend on right */}
                  </PieChart>
                </ResponsiveContainer>
              </div>

              {/* Legend list */}
              <div className="w-1/2 flex flex-col gap-1.5 text-xs">
                {segments.map((segment) => (
                  <div
                    key={segment.name}
                    className="flex items-center justify-between rounded-xl px-2 py-1.5 hover:bg-slate-50 transition"
                  >
                    <div className="flex items-center gap-2">
                      <span
                        className="w-2.5 h-2.5 rounded-full"
                        style={{ backgroundColor: segment.color }}
                      />
                      <div className="flex flex-col">
                        <span className="text-xs font-semibold text-slate-900">
                          {segment.name}
                        </span>
                        <span className="text-[11px] text-slate-500">
                          {segment.percent.toFixed(0)}% of base
                        </span>
                      </div>
                    </div>
                    <span className="text-xs font-semibold text-slate-900">
                      {segment.percent.toFixed(0)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Overview;
