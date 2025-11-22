import { useEffect, useState } from "react";
import CustomersTable from "../components/CustomersTable";
import { customers as mockCustomers } from "../data/mockData";
import { fetchSegmentsSummary } from "../api/backend";

function CustomerSegmentation() {
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

  return (
    <div className="space-y-3">
      {loading && (
        <p className="text-xs text-slate-500">
          Loading customers from backend...
        </p>
      )}
      {error && (
        <p className="text-xs text-red-500">Backend error: {error}</p>
      )}
      <CustomersTable customers={customers} />
    </div>
  );
}

export default CustomerSegmentation;
