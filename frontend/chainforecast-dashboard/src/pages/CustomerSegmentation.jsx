import CustomersTable from "../components/CustomersTable";
import { customers } from "../data/mockData";

function CustomerSegmentation() {
  return (
    <div className="space-y-6">
      <CustomersTable customers={customers} />
    </div>
  );
}

export default CustomerSegmentation;
