import StatsCard from "../components/StatsCard";
import ForecastChart from "../components/ForecastChart";
import SegmentsChart from "../components/SegmentsChart";
import {
  statsCards,
  weeklySalesData,
  customerSegmentsData,
} from "../data/mockData";

function Overview() {
  return (
    <div className="space-y-6">
      {/* Top header row */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Overview</h1>
          <p className="text-sm text-slate-500 mt-1">
            Interactive sales insights — range: <span className="font-medium">4w</span>
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

          <button className="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 shadow-sm">
            Last 4 weeks
          </button>

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
        <div className="lg:col-span-2">
          {/* height similar to reference so it fits on screen */}
          <div className="h-[360px]">
            <ForecastChart data={weeklySalesData} />
          </div>
        </div>
        <div>
          <div className="h-[360px]">
            <SegmentsChart data={customerSegmentsData} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Overview;
