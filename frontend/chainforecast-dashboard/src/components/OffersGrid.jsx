import { useState } from "react";

// Example asset path you provided earlier (kept per dev note, not used in UI)
const sampleHero = "/mnt/data/ce4df813-0119-4bd5-9723-f956eb25b1f0.png";

function OffersGrid({ offers }) {
  const [activeSegments, setActiveSegments] = useState({});
  const [showToast, setShowToast] = useState(false);
  const [toastTimeoutId, setToastTimeoutId] = useState(null);

  // Stub: replace with your real API call to send SMS
  const sendSMS = async (segment) => {
    // Example: call your backend endpoint here
    // await fetch(`/api/offers/${segment}/send-sms`, { method: "POST" });
    console.log(`(stub) Sending SMS for segment: ${segment}`);
  };

  const toggleSegment = (segment) => {
    setActiveSegments((prev) => {
      const nextValue = !prev[segment];

      // If toggling ON, trigger SMS and show toast
      if (nextValue) {
        // Call sendSMS (async but we don't block UI)
        sendSMS(segment).catch((e) => console.error("SMS send failed", e));

        // show toast
        setShowToast(true);

        // clear previous timeout if any
        if (toastTimeoutId) {
          clearTimeout(toastTimeoutId);
        }
        // auto-hide after 4s
        const id = setTimeout(() => setShowToast(false), 4000);
        setToastTimeoutId(id);
      }

      return {
        ...prev,
        [segment]: nextValue,
      };
    });
  };

  return (
    <>
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
            const isActive = !!activeSegments[item.segment];

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
                    {isActive ? "Campaign Active" : "Inactive"}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Toast popup */}
      {showToast && (
        <div className="fixed left-1/2 bottom-8 transform -translate-x-1/2 z-50">
          <div className="max-w-xl px-4 py-3 rounded-lg bg-slate-900 text-slate-100 shadow-lg border border-slate-700">
            A SMS has been sent to all the customers on their respective phone numbers.
          </div>
        </div>
      )}
    </>
  );
}

export default OffersGrid;
