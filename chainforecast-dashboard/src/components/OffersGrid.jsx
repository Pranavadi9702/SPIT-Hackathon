import { useState } from "react";

function OffersGrid({ offers }) {
  const [activeSegments, setActiveSegments] = useState({});

  const toggleSegment = (segment) => {
    setActiveSegments((prev) => ({
      ...prev,
      [segment]: !prev[segment],
    }));
  };

  return (
    <div className="bg-white/90 dark:bg-slate-900/80 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 p-4 lg:p-6">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
            Segment Offers
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Configure campaign ideas for each RFM segment
          </p>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {offers.map((item) => {
          const isActive = activeSegments[item.segment];

          return (
            <div
              key={item.segment}
              className="border border-slate-100 dark:border-slate-700 rounded-2xl p-4 flex flex-col gap-2 shadow-sm bg-white/90 dark:bg-slate-900/80"
            >
              <div className="flex items-center justify-between gap-2">
                <div>
                  <div className="text-xs font-semibold text-slate-900 dark:text-slate-100">
                    {item.segment}
                  </div>
                  <div className="text-[11px] text-slate-500 dark:text-slate-400">
                    {item.description}
                  </div>
                </div>

                {/* toggle switch */}
                <button
                  onClick={() => toggleSegment(item.segment)}
                  className={`relative inline-flex h-5 w-9 items-center rounded-full transition ${
                    isActive ? "bg-emerald-500" : "bg-slate-200 dark:bg-slate-700"
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white shadow transition ${
                      isActive ? "translate-x-4" : "translate-x-1"
                    }`}
                  />
                </button>
              </div>

              <div className="text-[11px] text-slate-700 dark:text-slate-200 bg-slate-50 dark:bg-slate-800 rounded-xl p-2">
                <span className="font-medium text-slate-900 dark:text-slate-100">
                  Sample Offer:{" "}
                </span>
                {item.offer}
              </div>

              <div
                className={`text-[10px] mt-auto ${
                  isActive
                    ? "text-emerald-600"
                    : "text-slate-500 dark:text-slate-400"
                }`}
              >
                Status:{" "}
                <span className="font-medium">
                  {isActive ? "Campaign active (UI only)" : "Inactive"}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default OffersGrid;
