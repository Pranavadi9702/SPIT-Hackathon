// src/components/SegmentsChart.jsx
import { useNavigate } from "react-router-dom";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Label,
} from "recharts";

const COLORS = ["#4f46e5", "#22c55e", "#0ea5e9", "#f97316", "#9ca3af"];

function SegmentsChart({ data, totalCustomers = 8452 }) {
  const navigate = useNavigate();
  const totalValue = data.reduce((sum, d) => sum + d.value, 0);

  const segments = data.map((d, index) => {
    const percent = (d.value / totalValue) * 100;
    return {
      ...d,
      percent,
      color: COLORS[index % COLORS.length],
    };
  });

  return (
    <div className="bg-white/90 dark:bg-slate-900/80 rounded-3xl border border-slate-100 dark:border-slate-700 shadow-sm h-full flex flex-col">
      {/* Header */}
      <div className="px-6 pt-5 pb-3 flex items-start justify-between">
        <div>
          <h2 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
            Customer Segments
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            RFM distribution
          </p>
        </div>
        <div className="text-right text-[11px] text-slate-500 dark:text-slate-400">
          <div>Monthly</div>
          <div className="mt-0.5">
            Total{" "}
            <span className="font-semibold text-slate-900 dark:text-slate-100">
              {totalCustomers.toLocaleString()}
            </span>
          </div>
        </div>
      </div>

      {/* Middle: donut + legend */}
      <div className="flex-1 px-4 pb-3 flex items-center gap-4">
        {/* Donut chart */}
        <div className="w-1/2">
          <div className="w-full h-56">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={segments}
                  dataKey="value"
                  nameKey="name"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={3}
                  strokeWidth={0}
                >
                  {segments.map((entry) => (
                    <Cell key={entry.name} fill={entry.color} />
                  ))}
                  <Label
                    position="center"
                    content={(props) => {
                      const { cx, cy } = props.viewBox;
                      return (
                        <g>
                          <text
                            x={cx}
                            y={cy - 4}
                            textAnchor="middle"
                            className="fill-slate-900 dark:fill-slate-100 text-xs font-semibold"
                          >
                            RFM
                          </text>
                          <text
                            x={cx}
                            y={cy + 11}
                            textAnchor="middle"
                            className="fill-slate-400 dark:fill-slate-500 text-[10px]"
                          >
                            segments
                          </text>
                        </g>
                      );
                    }}
                  />
                </Pie>
                <Tooltip
                  formatter={(_value, _name, props) => [
                    `${props.payload.percent.toFixed(0)}%`,
                    props.payload.name,
                  ]}
                  contentStyle={{
                    borderRadius: 12,
                    borderColor: "#e5e7eb",
                    fontSize: 12,
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Legend */}
        <div className="w-1/2 flex flex-col gap-1.5">
          {segments.map((segment) => (
            <div
              key={segment.name}
              className="flex justify-between text-xs rounded-xl px-2 py-1.5 hover:bg-slate-50 dark:hover:bg-slate-800 transition"
            >
              <div className="flex items-center gap-2">
                <span
                  className="w-2 h-2 rounded-full"
                  style={{ backgroundColor: segment.color }}
                />
                <div className="flex flex-col">
                  <span className="font-medium text-slate-900 dark:text-slate-100">
                    {segment.name}
                  </span>
                  <span className="text-[11px] text-slate-500 dark:text-slate-400">
                    {segment.percent.toFixed(0)}% of base
                  </span>
                </div>
              </div>
              <span className="font-semibold text-slate-900 dark:text-slate-100">
                {segment.percent.toFixed(0)}%
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Footer buttons */}
      <div className="px-6 pb-4 flex items-center gap-3">
        <button
          onClick={() => navigate("/customer-segmentation")}
          className="rounded-full bg-indigo-500 px-4 py-1.5 text-xs font-medium text-white shadow-sm hover:bg-indigo-600 dark:hover:bg-indigo-400 transition"
        >
          View Details
        </button>
        <button className="rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-4 py-1.5 text-xs font-medium text-slate-700 dark:text-slate-100 shadow-sm">
          Export
        </button>
      </div>
    </div>
  );
}

export default SegmentsChart;
