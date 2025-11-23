import { useEffect, useMemo, useState } from "react";
import CustomersTable from "../components/CustomersTable";
import { customers as mockCustomers } from "../data/mockData";
import { fetchSegmentsSummary } from "../api/backend";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

const SEGMENT_COLORS = [
  "#4f46e5", // Champions
  "#22c55e", // Loyal
  "#0ea5e9", // New
  "#f97316", // At-Risk
  "#9ca3af", // Others
];

function CustomerSegmentation() {
  // ---- Logic (kept exactly as in your logic file) ----
  const [customers, setCustomers] = useState(mockCustomers);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        setError("");
        const data = await fetchSegmentsSummary();
        if (data.customers && data.customers.length > 0) {
          setCustomers(data.customers);
        }
      } catch (err) {
        console.error(err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);
  // ----------------------------------------------------

  // UI needs some derived values from customers — computed with useMemo
  const {
    totalCustomers,
    avgMonetary,
    segmentDistribution,
  } = useMemo(() => {
    const total = customers.length;

    const champs = customers.filter((c) => c.segment === "Champions").length;

    const atRisk = customers.filter((c) => c.segment === "At-Risk").length;

    const monetarySum = customers.reduce((sum, c) => {
      // handle values like "₹52,000" or 52000
      const raw =
        typeof c.monetary === "string"
          ? c.monetary.replace(/[^\d.-]/g, "")
          : c.monetary;
      const num = Number(raw) || 0;
      return sum + num;
    }, 0);

    const avgMon = total > 0 ? monetarySum / total : 0;

    const segMap = new Map();
    customers.forEach((c) => {
      const key = c.segment || "Others";
      segMap.set(key, (segMap.get(key) || 0) + 1);
    });

    const segArray = Array.from(segMap.entries()).map(([name, value]) => ({
      name,
      value,
    }));

    return {
      totalCustomers: total,
      championsCount: champs,
      atRiskCount: atRisk,
      avgMonetary: avgMon,
      segmentDistribution: segArray,
    };
  }, [customers]);

  // build a normalized lookup from the segmentDistribution so KPI cards use the same numbers as charts
  const normalize = (s) => (s || "").toString().replace(/\W/g, "").toLowerCase();
  const segLookup = {};
  segmentDistribution.forEach((s) => {
    const raw = normalize(s.name);
    segLookup[raw] = s.value;
    if (raw.endsWith("customers")) segLookup[raw.replace(/customers$/, "")] = s.value;
    if (raw.endsWith("s")) segLookup[raw.slice(0, -1)] = s.value;
  });

  const cardSegments = [
    { key: "champions", label: "Champions", icon: "🏆", subLabel: "Most engaged & valuable" },
    { key: "loyal", label: "Loyal Customers", icon: "💚", subLabel: "Repeat buyers" },
    { key: "atrisk", label: "At-Risk customers", icon: "⚠", subLabel: "Need re-engagement" },
    { key: "lost", label: "Lost Customers", icon: "🧡", subLabel: "No recent activity" },
    { key: "potentialloyalists", label: "Potential Loyalists", icon: "🌱", subLabel: "Could be nurtured" },
  ];

  const statsCards = [
    {
      id: "total",
      label: "Total customers",
      value: totalCustomers.toLocaleString(),
      subLabel: "Across all RFM segments",
      icon: "👥",
    },
    ...cardSegments.map((seg, i) => ({
      id: `seg-${i}`,
      label: seg.label,
      value: (segLookup[seg.key] || 0).toLocaleString(),
      subLabel: seg.subLabel,
      icon: seg.icon,
    })),
    {
      id: "avg",
      label: "Avg revenue / customer",
      value: `₹${Math.round(avgMonetary).toLocaleString()}`,
      subLabel: "Based on monetary value",
      icon: "💰",
    },
  ];

  // Pagination: client-side paging of the customers table
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const pageSizes = [10, 25, 50, 100];
  const totalPages = Math.max(1, Math.ceil(customers.length / pageSize));
  // toast for toggles
  // reset page when data or pageSize changes
  useEffect(() => {
    setPage(1);
  }, [customers, pageSize]);

  const paginatedCustomers = useMemo(() => {
    const start = (page - 1) * pageSize;
    return customers.slice(start, start + pageSize);
  }, [customers, page, pageSize]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
        <div className="flex flex-col md:flex-row md:items-center md:gap-6">
          {/* Rows per page now sits beside the title (desktop) */}
          <div className="hidden md:flex flex-col items-start gap-1 text-xs">
            <div className="text-[11px] text-slate-500 dark:text-slate-400">Rows per page</div>
            <select
              value={pageSize}
              onChange={(e) => {
                setPageSize(Number(e.target.value));
                setPage(1);
              }}
              className="text-sm px-2 py-1 bg-white/90 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded text-slate-700 dark:text-slate-100"
            >
              {pageSizes.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>

          <div>
            <h1 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
              Customer Segmentation
            </h1>
            <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
              RFM-based segments with behavioral metrics and cohort insights.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="hidden md:flex items-center rounded-full border border-slate-200/80 dark:border-slate-700 bg-white/90 dark:bg-slate-900/70 px-3 py-1.5 text-sm shadow-sm min-w-[260px]">
            <input
              type="text"
              placeholder="Search by name, ID or segment..."
              className="flex-1 outline-none text-xs text-slate-600 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 bg-transparent"
            />
            <span className="text-slate-400 dark:text-slate-500 text-lg">
              🔍
            </span>
          </div>

          <button className="rounded-full bg-indigo-500 px-3.5 py-1.5 text-xs font-medium text-white shadow-sm hover:bg-indigo-600 dark:hover:bg-indigo-400 transition">
            Export segment report
          </button>
        </div>
      </div>

      {/* Show loading / error from logic (kept) */}
      {loading && (
        <p className="text-xs text-slate-500">Loading customers from backend...</p>
      )}
      {error && <p className="text-xs text-red-500">Backend error: {error}</p>}

      {/* Stat cards */}
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {statsCards.map((card) => (
          <div
            key={card.id}
            className="relative overflow-hidden rounded-3xl bg-white/90 dark:bg-slate-900/80 border border-slate-100 dark:border-slate-700 shadow-[0_18px_45px_rgba(15,23,42,0.06)] dark:shadow-none p-4 flex flex-col gap-3 transition-all duration-300 ease-out hover:shadow-[0_25px_55px_rgba(15,23,42,0.12)] hover:-translate-y-1 hover:scale-[1.02]"
          >
            <div className="absolute inset-x-4 top-0 h-0.5 rounded-b-full bg-gradient-to-r from-indigo-500 via-sky-500 to-emerald-500" />
            <div className="flex items-start justify-between">
              <div className="text-[11px] uppercase tracking-wide text-slate-500 dark:text-slate-400 font-medium">
                {card.label}
              </div>
              <div className="h-9 w-9 rounded-2xl bg-indigo-50 dark:bg-indigo-500/15 border border-indigo-100 dark:border-indigo-500/40 flex items-center justify-center text-lg">
                <span>{card.icon}</span>
              </div>
            </div>
            <div className="text-xl font-semibold text-slate-900 dark:text-slate-100">
              {card.value}
            </div>
            <div className="text-xs text-slate-500 dark:text-slate-400">
              {card.subLabel}
            </div>
          </div>
        ))}
      </div>

      {/* Charts row */}
      <div className="grid gap-4 lg:grid-cols-3">
        {/* Bar chart: customers by segment */}
        <div className="lg:col-span-2 bg-white/90 dark:bg-slate-900/80 rounded-3xl border border-slate-100 dark:border-slate-700 shadow-sm p-5 flex flex-col">
          <div className="flex items-center justify-between mb-3">
            <div>
              <h2 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                Customers by Segment
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Distribution of customers across RFM segments.
              </p>
            </div>
          </div>
          <div className="flex-1 h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={segmentDistribution}
                margin={{ top: 10, right: 24, left: 0, bottom: 8 }}
              >
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis
                  dataKey="name"
                  tick={{ fontSize: 12, fill: "#94a3b8" }}
                  axisLine={{ stroke: "#e5e7eb" }}
                />
                <YAxis
                  allowDecimals={false}
                  tick={{ fontSize: 12, fill: "#94a3b8" }}
                  axisLine={{ stroke: "#e5e7eb" }}
                />
                <Tooltip
                  formatter={(val) => [`${val} customers`, "Count"]}
                  labelStyle={{ fontSize: 12 }}
                  contentStyle={{
                    borderRadius: 12,
                    borderColor: "#e5e7eb",
                    fontSize: 12,
                  }}
                />
                <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                  {segmentDistribution.map((entry, index) => (
                    <Cell
                      key={`cell-${entry.name}`}
                      fill={SEGMENT_COLORS[index % SEGMENT_COLORS.length]}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Donut: segment share */}
        <div className="bg-white/90 dark:bg-slate-900/80 rounded-3xl border border-slate-100 dark:border-slate-700 shadow-sm p-5 flex flex-col h-[320px]">
          <div className="flex items-start justify-between mb-3">
            <div>
              <h2 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                Segment Share
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Percentage contribution of each segment.
              </p>
            </div>
            <div className="text-[11px] text-slate-500 dark:text-slate-400">
              Total{" "}
              <span className="font-semibold text-slate-900 dark:text-slate-100">
                {totalCustomers.toLocaleString()}
              </span>
            </div>
          </div>

          <div className="flex-1 flex items-center gap-3">
            {/* Chart */}
            <div className="w-1/2 h-full min-h-[220px] flex items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={segmentDistribution}
                    dataKey="value"
                    nameKey="name"
                    innerRadius={50}
                    outerRadius={70}
                    paddingAngle={3}
                    stroke="#ffffff"
                    strokeWidth={3}
                  >
                    {segmentDistribution.map((entry, index) => (
                      <Cell
                        key={entry.name}
                        fill={SEGMENT_COLORS[index % SEGMENT_COLORS.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={(value, _name, props) => {
                      const val = Number(value) || 0;
                      const percent =
                        totalCustomers > 0
                          ? ((val / totalCustomers) * 100).toFixed(0)
                          : 0;
                      return [`${percent}%`, props.payload.name];
                    }}
                    contentStyle={{
                      borderRadius: 12,
                      borderColor: "#e5e7eb",
                      fontSize: 12,
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* Legend */}
            <div className="w-1/2 flex flex-col gap-1.5 text-xs">
              {segmentDistribution.map((segment, index) => {
                const percent =
                  totalCustomers > 0
                    ? Math.round((segment.value / totalCustomers) * 100)
                    : 0;
                return (
                  <div
                    key={segment.name}
                    className="flex items-center justify-between rounded-xl px-2 py-1.5 hover:bg-slate-50 dark:hover:bg-slate-800 transition"
                  >
                    <div className="flex items-center gap-2">
                      <span
                        className="w-2 h-2 rounded-full"
                        style={{
                          backgroundColor:
                            SEGMENT_COLORS[index % SEGMENT_COLORS.length],
                        }}
                      />
                      <span className="font-medium text-slate-900 dark:text-slate-100">
                        {segment.name}
                      </span>
                    </div>
                    <span className="font-semibold text-slate-900 dark:text-slate-100">
                      {percent}%
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* Table */}
      {/* Table (paginated) */}
      <CustomersTable customers={paginatedCustomers} />

      {/* Pagination controls */}
      <div className="flex items-center justify-between mt-4 gap-3">
        <div className="flex items-center gap-2 text-xs text-slate-600 dark:text-slate-400">
          <span>Rows per page</span>
          <select
            value={pageSize}
            onChange={(e) => setPageSize(Number(e.target.value))}
            className="text-sm px-2 py-1 bg-white/90 dark:bg-slate-800 border rounded text-slate-700 dark:text-slate-100"
          >
            {pageSizes.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
          <span className="ml-2">
            {customers.length.toLocaleString()} total
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setPage(1)}
            disabled={page === 1}
            className="px-2 py-1 rounded bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-100 text-xs disabled:opacity-40"
          >
            « First
          </button>
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1}
            className="px-2 py-1 rounded bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-100 text-xs disabled:opacity-40"
          >
            ‹ Prev
          </button>

          <div className="text-xs px-3">
            Page{" "}
            <input
              type="number"
              min={1}
              max={totalPages}
              value={page}
              onChange={(e) => {
                const v = Number(e.target.value) || 1;
                setPage(Math.min(Math.max(1, v), totalPages));
              }}
              className="w-12 text-center bg-transparent outline-none text-slate-700 dark:text-slate-100"
            />{" "}
            of {totalPages}
          </div>

          <button
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
            className="px-2 py-1 rounded bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-100 text-xs disabled:opacity-40"
          >
            Next ›
          </button>
          <button
            onClick={() => setPage(totalPages)}
            disabled={page === totalPages}
            className="px-2 py-1 rounded bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-100 text-xs disabled:opacity-40"
          >
            Last »
          </button>
        </div>
      </div>
    </div>
  );
}

export default CustomerSegmentation;