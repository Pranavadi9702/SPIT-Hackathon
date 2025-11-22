import { useMemo, useState } from "react";
import CustomerDetailsModal from "./CustomerDetailsModal";

const segments = ["All", "Champions", "Loyal Customers", "At-Risk", "New Customers"];

function CustomersTable({ customers }) {
  const [segmentFilter, setSegmentFilter] = useState("All");
  const [search, setSearch] = useState("");
  const [selectedCustomer, setSelectedCustomer] = useState(null);

  const filteredCustomers = useMemo(() => {
    return customers.filter((c) => {
      const matchesSegment =
        segmentFilter === "All" ? true : c.segment === segmentFilter;
      const query = search.trim().toLowerCase();
      const matchesSearch =
        !query ||
        c.name.toLowerCase().includes(query) ||
        c.id.toLowerCase().includes(query);
      return matchesSegment && matchesSearch;
    });
  }, [segmentFilter, search, customers]);

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-4 lg:p-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
        <div>
          <h2 className="text-sm font-semibold text-slate-900">
            Customer Segmentation
          </h2>
          <p className="text-xs text-slate-500">
            RFM-based segments with behavioral metrics
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-2">
          <select
            value={segmentFilter}
            onChange={(e) => setSegmentFilter(e.target.value)}
            className="text-xs border border-slate-200 rounded-xl px-2 py-1.5 bg-slate-50"
          >
            {segments.map((segment) => (
              <option key={segment} value={segment}>
                {segment}
              </option>
            ))}
          </select>

          <input
            type="text"
            placeholder="Search by name or ID"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="text-xs border border-slate-200 rounded-xl px-3 py-1.5 bg-slate-50"
          />
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full text-xs">
          <thead>
            <tr className="text-left text-slate-500 border-b border-slate-100">
              <th className="py-2 pr-4">Customer ID</th>
              <th className="py-2 pr-4">Name</th>
              <th className="py-2 pr-4">Segment</th>
              <th className="py-2 pr-4">Recency (days)</th>
              <th className="py-2 pr-4">Frequency</th>
              <th className="py-2 pr-4">Monetary (₹)</th>
            </tr>
          </thead>
          <tbody>
            {filteredCustomers.map((c) => (
              <tr
                key={c.id}
                onClick={() => setSelectedCustomer(c)}
                className="border-b border-slate-50 hover:bg-slate-50 cursor-pointer"
              >
                <td className="py-2 pr-4">{c.id}</td>
                <td className="py-2 pr-4">{c.name}</td>
                <td className="py-2 pr-4">{c.segment}</td>
                <td className="py-2 pr-4">{c.recency}</td>
                <td className="py-2 pr-4">{c.frequency}</td>
                <td className="py-2 pr-4">
                  ₹{c.monetary.toLocaleString()}
                </td>
              </tr>
            ))}
            {filteredCustomers.length === 0 && (
              <tr>
                <td colSpan={6} className="py-4 text-center text-slate-400">
                  No customers found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {selectedCustomer && (
        <CustomerDetailsModal
          customer={selectedCustomer}
          onClose={() => setSelectedCustomer(null)}
        />
      )}
    </div>
  );
}

export default CustomersTable;
