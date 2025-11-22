function getSuggestedOffer(segment) {
  switch (segment) {
    case "Champions":
      return "Offer exclusive VIP rewards, early access, and higher-tier loyalty perks.";
    case "Loyal Customers":
      return "Encourage bundling and subscriptions with tiered discounts.";
    case "At-Risk":
      return "Send time-bound winback offers and reminders with strong incentives.";
    case "New Customers":
      return "Give a second-purchase coupon and referral rewards.";
    default:
      return "Provide a personalized recommendation based on their browsing and purchase history.";
  }
}

function CustomerDetailsModal({ customer, onClose }) {
  if (!customer) return null;

  const rfmScore = `${Math.max(
    1,
    5 - Math.floor(customer.recency / 15)
  )}${Math.min(5, Math.ceil(customer.frequency / 5))}${Math.min(
    5,
    Math.ceil(customer.monetary / 10000)
  )}`;

  return (
    <div className="fixed inset-0 z-40 flex items-center justify-end bg-black/40">
      <div className="w-full max-w-md h-full bg-white dark:bg-slate-950 shadow-xl border-l border-slate-200 dark:border-slate-800 p-6 flex flex-col">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
            Customer Details
          </h2>
          <button
            onClick={onClose}
            className="text-sm text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100"
          >
            Close
          </button>
        </div>

        <div className="space-y-4 flex-1 overflow-y-auto">
          <div>
            <div className="text-xs text-slate-500 dark:text-slate-400 uppercase">
              Customer
            </div>
            <div className="text-base font-semibold text-slate-900 dark:text-slate-100">
              {customer.name}
            </div>
            <div className="text-xs text-slate-500 dark:text-slate-400">
              {customer.id}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div className="bg-slate-50 dark:bg-slate-900/80 rounded-xl p-3 border border-slate-100 dark:border-slate-700">
              <div className="text-slate-500 dark:text-slate-400">Segment</div>
              <div className="font-semibold text-slate-900 dark:text-slate-100">
                {customer.segment}
              </div>
            </div>
            <div className="bg-slate-50 dark:bg-slate-900/80 rounded-xl p-3 border border-slate-100 dark:border-slate-700">
              <div className="text-slate-500 dark:text-slate-400">
                RFM Score
              </div>
              <div className="font-semibold text-slate-900 dark:text-slate-100">
                {rfmScore}
              </div>
            </div>
            <div className="bg-slate-50 dark:bg-slate-900/80 rounded-xl p-3 border border-slate-100 dark:border-slate-700">
              <div className="text-slate-500 dark:text-slate-400">
                Recency
              </div>
              <div className="font-semibold text-slate-900 dark:text-slate-100">
                {customer.recency} days
              </div>
            </div>
            <div className="bg-slate-50 dark:bg-slate-900/80 rounded-xl p-3 border border-slate-100 dark:border-slate-700">
              <div className="text-slate-500 dark:text-slate-400">
                Frequency
              </div>
              <div className="font-semibold text-slate-900 dark:text-slate-100">
                {customer.frequency} orders
              </div>
            </div>
            <div className="bg-slate-50 dark:bg-slate-900/80 rounded-xl p-3 col-span-2 border border-slate-100 dark:border-slate-700">
              <div className="text-slate-500 dark:text-slate-400">
                Monetary Value
              </div>
              <div className="font-semibold text-slate-900 dark:text-slate-100">
                ₹{customer.monetary.toLocaleString()}
              </div>
            </div>
          </div>

          <div className="bg-emerald-50 dark:bg-emerald-500/10 border border-emerald-100 dark:border-emerald-500/40 rounded-xl p-3 text-xs">
            <div className="text-emerald-700 dark:text-emerald-300 font-semibold mb-1">
              Suggested Offer
            </div>
            <p className="text-emerald-800 dark:text-emerald-200">
              {getSuggestedOffer(customer.segment)}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CustomerDetailsModal;