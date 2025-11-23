// /* eslint-disable no-unused-vars */
// // import { useEffect, useState } from "react";
// // import StatsCard from "../components/StatsCard";
// // import ForecastChart from "../components/ForecastChart";
// // import SegmentsChart from "../components/SegmentsChart";
// // import {
// //   statsCards as defaultStatsCards,
// //   weeklySalesData as defaultWeeklySalesData,
// //   customerSegmentsData as defaultCustomerSegmentsData,
// // } from "../data/mockData";

// // // Change this if your backend runs on a different host/port
// // const API_BASE_URL = "http://127.0.0.1:5000";

// // function Overview() {
// //   // Start with placeholders for values + percentages (fully runtime later)
// //   const [stats, setStats] = useState(
// //     defaultStatsCards.map((card) => ({
// //       ...card,
// //       value: "----",
// //       change: "---",
// //       changeLabel: card.changeLabel ?? "", // keep labels if defined
// //     }))
// //   );

// //   // Charts can start with mock data so layout is not empty
// //   const [weeklyData, setWeeklyData] = useState(defaultWeeklySalesData);
// //   // const [segmentData, setSegmentData] = useState(defaultCustomerSegmentsData);

// //   const [loading, setLoading] = useState(true);
// //   const [uploading, setUploading] = useState(false);

// //   const [segmentData, setSegmentData] = useState(defaultCustomerSegmentsData);
// //   const [refreshTrigger, setRefreshTrigger] = useState(0);


// //   useEffect(() => {
// //     async function fetchDashboardData() {
// //       try {
// //         // 1) Forecast summary for KPIs + line chart
// //         const resForecast = await fetch(`${API_BASE_URL}/api/forecast-summary`);
// //         const dataForecast = await resForecast.json();

// //         if (dataForecast.status === "success") {
// //           const apiWeekly = Array.isArray(dataForecast.weeklySalesData)
// //             ? dataForecast.weeklySalesData
// //             : [];

// //           // -------- Line chart data --------
// //           setWeeklyData(apiWeekly.length ? apiWeekly : defaultWeeklySalesData);

// //           // -------- KPI #1: Total Sales (Last 4 Weeks) --------
// //           // Use model-calculated value from backend if available
// //           let totalSalesFormatted = "₹0";
// //           let totalSalesChangeText = "---";
          
// //           if (dataForecast.metrics && dataForecast.metrics.last_4_weeks_total) {
// //             const salesNum = parseFloat(dataForecast.metrics.last_4_weeks_total);
// //             if (!isNaN(salesNum)) {
// //               totalSalesFormatted = `₹${Math.round(salesNum).toLocaleString("en-IN")}`;
// //             }
// //           }
          
// //           if (dataForecast.metrics && dataForecast.metrics.sales_change_pct !== null && dataForecast.metrics.sales_change_pct !== undefined) {
// //             const change = parseFloat(dataForecast.metrics.sales_change_pct);
// //             if (!isNaN(change)) {
// //               const sign = change > 0 ? "+" : change < 0 ? "" : "";
// //               totalSalesChangeText = `${sign}${change.toFixed(2)}%`;
// //             }
// //           }

// //           // -------- KPI #2: Forecasted Sales (Next 4 Weeks) --------
// //           const forecastFormatted =
// //             dataForecast.total_forecast_formatted || "₹0";

// //           let forecastChangeText = "---";
// //           // Use backend-calculated forecast change percentage from metrics
// //           if (dataForecast.metrics && dataForecast.metrics.forecast_change_pct !== null && dataForecast.metrics.forecast_change_pct !== undefined) {
// //             const change = parseFloat(dataForecast.metrics.forecast_change_pct);
// //             if (!isNaN(change)) {
// //               const sign = change > 0 ? "+" : change < 0 ? "" : "";
// //               forecastChangeText = `${sign}${change.toFixed(2)}%`;
// //             }
// //           }

// //           // -------- Update KPI cards #1 and #2 (fully runtime) --------
// //           setStats((prev) =>
// //             prev.map((card) => {
// //               if (card.id === 1) {
// //                 return {
// //                   ...card,
// //                   value: totalSalesFormatted,
// //                   change: totalSalesChangeText,
// //                   changeLabel: "vs previous 4 weeks",
// //                 };
// //               }
// //               if (card.id === 2) {
// //                 return {
// //                   ...card,
// //                   value: forecastFormatted,
// //                   change: forecastChangeText,
// //                   changeLabel: "vs last 4 weeks",
// //                 };
// //               }
// //               return card;
// //             })
// //           );
// //         }

// //         // 2) Segments summary for pie chart + Total Customers + Top Segment
// //         const resSegments = await fetch(
// //           `${API_BASE_URL}/api/segments-summary`
// //         );
// //         const dataSegments = await resSegments.json();

// //         if (
// //           dataSegments.status === "success" &&
// //           Array.isArray(dataSegments.segments)
// //         ) {
// //           // -------- Pie chart data --------
// //           const segData = dataSegments.segments.map((s) => ({
// //             name: s.name,
// //             value: s.value,
// //           }));
// //           setSegmentData(segData.length ? segData : defaultCustomerSegmentsData);

// //           // -------- Base metrics from backend --------
// //           const totalCustomers =
// //             Array.isArray(dataSegments.customers) &&
// //             dataSegments.customers.length > 0
// //               ? dataSegments.customers.length
// //               : null;

// //           let topSegmentName = null;
// //           let topSegmentCount = null;

// //           if (segData.length > 0) {
// //             const topSeg = segData.reduce((a, b) =>
// //               b.value > a.value ? b : a
// //             );
// //             topSegmentName = topSeg.name;
// //             topSegmentCount = topSeg.value;
// //           }

// //           // High-value segments for KPI #3 change (Champions, Loyal, Potential)
// //           let pctHighValue = null;
// //           if (totalCustomers && totalCustomers > 0) {
// //             const highValueNames = [
// //               "Champions",
// //               "Loyal Customers",
// //               "Potential Loyalists",
// //             ];
// //             const highValueCount = segData
// //               .filter((s) => highValueNames.includes(s.name))
// //               .reduce((sum, s) => sum + (s.value || 0), 0);
// //             pctHighValue = (highValueCount / totalCustomers) * 100;
// //           }

// //           // Top segment share for KPI #4 change
// //           let pctTopSegment = null;
// //           if (
// //             totalCustomers &&
// //             totalCustomers > 0 &&
// //             topSegmentCount != null
// //           ) {
// //             pctTopSegment = (topSegmentCount / totalCustomers) * 100;
// //           }

// //           // -------- Update KPI #3 and #4 (fully runtime) --------
// //           setStats((prev) =>
// //             prev.map((card) => {
// //               // Total Customers card (id 3)
// //               if (card.id === 3 && totalCustomers != null) {
// //                 const formattedTotal = totalCustomers.toLocaleString("en-IN");
// //                 return {
// //                   ...card,
// //                   value: formattedTotal,
// //                   change:
// //                     pctHighValue != null
// //                       ? `${pctHighValue.toFixed(1)}%`
// //                       : "---",
// //                   changeLabel: "in high-value segments",
// //                 };
// //               }

// //               // Top Segment card (id 4)
// //               if (card.id === 4 && topSegmentName) {
// //                 return {
// //                   ...card,
// //                   value: topSegmentName,
// //                   change:
// //                     pctTopSegment != null
// //                       ? `${pctTopSegment.toFixed(1)}%`
// //                       : "---",
// //                   changeLabel: "of total customers",
// //                 };
// //               }

// //               return card;
// //             })
// //           );
// //         }
// //       } catch (error) {
// //         console.error("Error fetching dashboard data:", error);
// //         // Fallback to mock data if backend fails completely
// //         setWeeklyData(defaultWeeklySalesData);
// //         setSegmentData(defaultCustomerSegmentsData);
// //         setStats(defaultStatsCards);
// //       } finally {
// //         setLoading(false);
// //       }
// //     }

// //     fetchDashboardData();

// //     // Auto-refresh every 10 seconds to catch updated data from backend pipeline
// //     const interval = setInterval(() => {
// //       fetchDashboardData();
// //     }, 60000);

// //     return () => clearInterval(interval);
// //   }, [refreshTrigger]);

// //   // Handle CSV file upload
// //   const handleCSVUpload = async (event) => {
// //     const file = event.target.files?.[0];
// //     if (!file) return;

// //     setUploading(true);
// //     setLoading(true);

// //     try {
// //       const formData = new FormData();
// //       formData.append("file", file);

// //       const uploadRes = await fetch(`${API_BASE_URL}/api/upload-csv`, {
// //         method: "POST",
// //         body: formData,
// //       });

// //       if (uploadRes.ok) {
// //         console.log("CSV uploaded successfully, model is processing...");
        
// //         // Wait for backend to process, then fetch updated data every 5 seconds
// //         let attempts = 0;
// //         const checkCompletion = setInterval(async () => {
// //           attempts++;
// //           try {
// //             const res = await fetch(`${API_BASE_URL}/api/forecast-summary`);
// //             const data = await res.json();
// //             if (data.status === "success" && data.metrics) {
// //               clearInterval(checkCompletion);
// //               setRefreshTrigger(prev => prev + 1);
// //               setUploading(false);
// //               alert("New dataset processed successfully! Dashboard updated.");
// //             }
// //           // eslint-disable-next-line no-unused-vars
// //           } catch (err) {
// //             console.log("Waiting for model processing...");
// //           }
          
// //           if (attempts > 30) {
// //             // Stop after 2.5 minutes
// //             clearInterval(checkCompletion);
// //             setUploading(false);
// //             setLoading(false);
// //           }
// //         }, 5000);
// //       } else {
// //         alert("Failed to upload CSV. Please try again.");
// //         setUploading(false);
// //         setLoading(false);
// //       }
// //     } catch (error) {
// //       console.error("Error uploading CSV:", error);
// //       alert("Error uploading CSV: " + error.message);
// //       setUploading(false);
// //       setLoading(false);
// //     }
// //   };

// //   // Handle CSV export
// //   const handleCSVExport = async () => {
// //     try {
// //       const res = await fetch(`${API_BASE_URL}/api/export-csv`);
// //       if (!res.ok) throw new Error("Export failed");

// //       const blob = await res.blob();
// //       const url = window.URL.createObjectURL(blob);
// //       const a = document.createElement("a");
// //       a.href = url;
// //       a.download = `forecast_report_${new Date().toISOString().split('T')[0]}.csv`;
// //       a.click();
// //       window.URL.revokeObjectURL(url);
// //     } catch (error) {
// //       console.error("Error exporting CSV:", error);
// //       alert("Error exporting CSV: " + error.message);
// //     }
// //   };

// //   return (
// //     <div className="relative space-y-6">
// //       {/* LOADING OVERLAY */}
// //       {loading && (
// //         <div className="absolute inset-0 z-50 flex items-center justify-center bg-white/70 backdrop-blur-sm">
// //           <div className="flex flex-col items-center gap-3">
// //             <div className="h-8 w-8 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
// //             <p className="text-sm font-medium text-slate-700">
// //               Running forecast pipeline...
// //             </p>
// //             <p className="text-xs text-slate-500">
// //               Fetching LSTM forecasts and customer segments
// //             </p>
// //           </div>
// //         </div>
// //       )}

// //       {/* Top header row */}
// //       <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
// //         <div>
// //           <h1 className="text-2xl font-semibold text-slate-900">Overview</h1>
// //           <p className="mt-1 text-sm text-slate-500">
// //             LSTM-powered demand forecasting, RFM segmentation, and campaign
// //             insights for your retail data.
// //           </p>
// //         </div>

// //         <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500">
// //           <div className="flex items-center gap-1 rounded-full border border-slate-200 bg-white px-2.5 py-1 shadow-sm">
// //             <span className="h-2 w-2 rounded-full bg-emerald-500" />
// //             Model: LSTM (weekly)
// //           </div>
// //           <div className="flex items-center gap-1 rounded-full border border-slate-200 bg-white px-2.5 py-1 shadow-sm">
// //             <span className="h-2 w-2 rounded-full bg-indigo-500" />
// //             RFM + KMeans segmentation
// //           </div>
// //         </div>
// //       </div>

// //       {/* Filter / toolbar row */}
// //       <div className="flex flex-col gap-3 rounded-3xl border border-slate-100 bg-white/70 p-4 shadow-sm backdrop-blur md:flex-row md:items-center md:justify-between">
// //         <div className="flex items-center gap-3">
// //           <div className="flex h-9 items-center gap-2 rounded-full border border-slate-200 bg-slate-50/70 px-3">
// //             <span className="text-xs font-medium text-slate-500">Store</span>
// //             <select className="bg-transparent text-xs font-medium text-slate-900 outline-none">
// //               <option>Main Store</option>
// //               <option>All Channels</option>
// //             </select>
// //           </div>

// //           <div className="flex h-9 items-center gap-2 rounded-full border border-slate-200 bg-slate-50/70 px-3">
// //             <span className="text-xs font-medium text-slate-500">Horizon</span>
// //             <select className="bg-transparent text-xs font-medium text-slate-900 outline-none">
// //               <option>Next 4 weeks</option>
// //               <option>Next 8 weeks</option>
// //               <option>Next 12 weeks</option>
// //             </select>
// //           </div>
// //         </div>

// //         <div className="flex flex-wrap items-center gap-2">
// //           <div className="flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50/70 px-3 py-1">
// //             <input
// //               type="text"
// //               placeholder="Filter segments..."
// //               className="flex-1 outline-none text-xs text-slate-600 placeholder:text-slate-400 bg-transparent"
// //             />
// //             <span className="text-slate-400 text-lg">🔍</span>
// //           </div>

// //           <button className="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 shadow-sm">
// //             Last 4 weeks
// //           </button>

// //           <button 
// //             onClick={() => setRefreshTrigger(prev => prev + 1)}
// //             className="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 shadow-sm hover:bg-slate-50 transition"
// //             title="Refresh data from backend"
// //           >
// //             Refresh
// //           </button>

// //           <button 
// //             onClick={handleCSVExport}
// //             className="rounded-full bg-indigo-500 px-3.5 py-1.5 text-xs font-medium text-white shadow-sm hover:bg-indigo-600 transition"
// //             title="Download current forecast report"
// //           >
// //             Export CSV
// //           </button>

// //           <label className="rounded-full bg-emerald-500 px-3.5 py-1.5 text-xs font-medium text-white shadow-sm hover:bg-emerald-600 transition cursor-pointer">
// //             Upload CSV
// //             <input
// //               type="file"
// //               accept=".csv"
// //               onChange={handleCSVUpload}
// //               disabled={uploading}
// //               className="hidden"
// //             />
// //           </label>
// //         </div>
// //       </div>

// //       {/* Stats cards row */}
// //       <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
// //         {stats.map((card) => (
// //           <StatsCard key={card.id} {...card} />
// //         ))}
// //       </div>

// //       {/* Charts row */}
// //       <div className="grid gap-4 lg:grid-cols-3">
// //         <div className="lg:col-span-2">
// //           {/* height similar to reference so it fits on screen */}
// //           <div className="h-[360px]">
// //             <ForecastChart data={weeklyData} />
// //           </div>
// //         </div>
// //         <div>
// //           <div className="h-[360px]">
// //             <SegmentsChart data={segmentData} />
// //           </div>
// //         </div>
// //       </div>
// //     </div>
// //   );
// // }

// // export default Overview;




// import { useEffect, useState } from "react";
// import StatsCard from "../components/StatsCard";
// import ForecastChart from "../components/ForecastChart";
// import SegmentsChart from "../components/SegmentsChart";
// import {
//   statsCards as defaultStatsCards,
//   weeklySalesData as defaultWeeklySalesData,
//   customerSegmentsData as defaultCustomerSegmentsData,
// } from "../data/mockData";

// // Change this if your backend runs on a different host/port
// const API_BASE_URL = "http://127.0.0.1:5000";

// function Overview() {
//   // Start with placeholders for values + percentages (fully runtime later)
//   const [stats, setStats] = useState(
//     defaultStatsCards.map((card) => ({
//       ...card,
//       value: "----",
//       change: "---",
//       changeLabel: card.changeLabel ?? "", // keep labels if defined
//     }))
//   );

//   // Charts can start with mock data so layout is not empty
//   const [weeklyData, setWeeklyData] = useState(defaultWeeklySalesData);
//   const [segmentData, setSegmentData] = useState(defaultCustomerSegmentsData);

//   const [loading, setLoading] = useState(true);
//   const [uploading, setUploading] = useState(false);

//   // Used to manually trigger refresh from the button / CSV upload
//   const [refreshTrigger, setRefreshTrigger] = useState(0);

//   // Store backend rate-limit info (from /api/forecast-summary)
//   const [rateLimitInfo, setRateLimitInfo] = useState({
//     active: false,
//     cooldownSeconds: 0,
//   });

//   useEffect(() => {
//     async function fetchDashboardData() {
//       // Show loading overlay for each fetch (initial + manual refresh)
//       setLoading(true);

//       try {
//         // 1) Forecast summary for KPIs + line chart
//         const resForecast = await fetch(`${API_BASE_URL}/api/forecast-summary`);
//         const dataForecast = await resForecast.json();

//         if (dataForecast.status === "success") {
//           const apiWeekly = Array.isArray(dataForecast.weeklySalesData)
//             ? dataForecast.weeklySalesData
//             : [];

//           // Update rate-limit info from backend (so you can see cooldown)
//           if (dataForecast.rateLimit) {
//             setRateLimitInfo({
//               active: !!dataForecast.rateLimit.active,
//               cooldownSeconds: dataForecast.rateLimit.cooldownSeconds ?? 0,
//             });
//           } else {
//             setRateLimitInfo({
//               active: false,
//               cooldownSeconds: 0,
//             });
//           }

//           // -------- Line chart data --------
//           setWeeklyData(apiWeekly.length ? apiWeekly : defaultWeeklySalesData);

//           // -------- KPI #1: Total Sales (Last 4 Weeks) --------
//           // Use model-calculated value from backend if available
//           let totalSalesFormatted = "₹0";
//           let totalSalesChangeText = "---";

//           if (
//             dataForecast.metrics &&
//             dataForecast.metrics.last_4_weeks_total
//           ) {
//             const salesNum = parseFloat(
//               dataForecast.metrics.last_4_weeks_total
//             );
//             if (!isNaN(salesNum)) {
//               totalSalesFormatted = `₹${Math.round(
//                 salesNum
//               ).toLocaleString("en-IN")}`;
//             }
//           }

//           if (
//             dataForecast.metrics &&
//             dataForecast.metrics.sales_change_pct !== null &&
//             dataForecast.metrics.sales_change_pct !== undefined
//           ) {
//             const change = parseFloat(
//               dataForecast.metrics.sales_change_pct
//             );
//             if (!isNaN(change)) {
//               const sign = change > 0 ? "+" : change < 0 ? "" : "";
//               totalSalesChangeText = `${sign}${change.toFixed(2)}%`;
//             }
//           }

//           // -------- KPI #2: Forecasted Sales (Next 4 Weeks) --------
//           const forecastFormatted =
//             dataForecast.total_forecast_formatted || "₹0";

//           let forecastChangeText = "---";
//           // Use backend-calculated forecast change percentage from metrics
//           if (
//             dataForecast.metrics &&
//             dataForecast.metrics.forecast_change_pct !== null &&
//             dataForecast.metrics.forecast_change_pct !== undefined
//           ) {
//             const change = parseFloat(
//               dataForecast.metrics.forecast_change_pct
//             );
//             if (!isNaN(change)) {
//               const sign = change > 0 ? "+" : change < 0 ? "" : "";
//               forecastChangeText = `${sign}${change.toFixed(2)}%`;
//             }
//           }

//           // -------- Update KPI cards #1 and #2 (fully runtime) --------
//           setStats((prev) =>
//             prev.map((card) => {
//               if (card.id === 1) {
//                 return {
//                   ...card,
//                   value: totalSalesFormatted,
//                   change: totalSalesChangeText,
//                   changeLabel: "vs previous 4 weeks",
//                 };
//               }
//               if (card.id === 2) {
//                 return {
//                   ...card,
//                   value: forecastFormatted,
//                   change: forecastChangeText,
//                   changeLabel: "vs last 4 weeks",
//                 };
//               }
//               return card;
//             })
//           );
//         }

//         // 2) Segments summary for pie chart + Total Customers + Top Segment
//         const resSegments = await fetch(
//           `${API_BASE_URL}/api/segments-summary`
//         );
//         const dataSegments = await resSegments.json();

//         if (
//           dataSegments.status === "success" &&
//           Array.isArray(dataSegments.segments)
//         ) {
//           // -------- Pie chart data --------
//           const segData = dataSegments.segments.map((s) => ({
//             name: s.name,
//             value: s.value,
//           }));
//           setSegmentData(
//             segData.length ? segData : defaultCustomerSegmentsData
//           );

//           // -------- Base metrics from backend --------
//           const totalCustomers =
//             Array.isArray(dataSegments.customers) &&
//             dataSegments.customers.length > 0
//               ? dataSegments.customers.length
//               : null;

//           let topSegmentName = null;
//           let topSegmentCount = null;

//           if (segData.length > 0) {
//             const topSeg = segData.reduce((a, b) =>
//               b.value > a.value ? b : a
//             );
//             topSegmentName = topSeg.name;
//             topSegmentCount = topSeg.value;
//           }

//           // High-value segments for KPI #3 change (Champions, Loyal, Potential)
//           let pctHighValue = null;
//           if (totalCustomers && totalCustomers > 0) {
//             const highValueNames = [
//               "Champions",
//               "Loyal Customers",
//               "Potential Loyalists",
//             ];
//             const highValueCount = segData
//               .filter((s) => highValueNames.includes(s.name))
//               .reduce((sum, s) => sum + (s.value || 0), 0);
//             pctHighValue = (highValueCount / totalCustomers) * 100;
//           }

//           // Top segment share for KPI #4 change
//           let pctTopSegment = null;
//           if (
//             totalCustomers &&
//             totalCustomers > 0 &&
//             topSegmentCount != null
//           ) {
//             pctTopSegment = (topSegmentCount / totalCustomers) * 100;
//           }

//           // -------- Update KPI #3 and #4 (fully runtime) --------
//           setStats((prev) =>
//             prev.map((card) => {
//               // Total Customers card (id 3)
//               if (card.id === 3 && totalCustomers != null) {
//                 const formattedTotal =
//                   totalCustomers.toLocaleString("en-IN");
//                 return {
//                   ...card,
//                   value: formattedTotal,
//                   change:
//                     pctHighValue != null
//                       ? `${pctHighValue.toFixed(1)}%`
//                       : "---",
//                   changeLabel: "in high-value segments",
//                 };
//               }

//               // Top Segment card (id 4)
//               if (card.id === 4 && topSegmentName) {
//                 return {
//                   ...card,
//                   value: topSegmentName,
//                   change:
//                     pctTopSegment != null
//                       ? `${pctTopSegment.toFixed(1)}%`
//                       : "---",
//                   changeLabel: "of total customers",
//                 };
//               }

//               return card;
//             })
//           );
//         }
//       } catch (error) {
//         console.error("Error fetching dashboard data:", error);
//         // Fallback to mock data if backend fails completely
//         setWeeklyData(defaultWeeklySalesData);
//         setSegmentData(defaultCustomerSegmentsData);
//         setStats(defaultStatsCards);
//         setRateLimitInfo({
//           active: false,
//           cooldownSeconds: 0,
//         });
//       } finally {
//         setLoading(false);
//       }
//     }

//     // 🔹 NO AUTO-REFRESH INTERVAL ANYMORE
//     // This will run:
//     // - once on initial mount (refreshTrigger = 0)
//     // - again whenever you click Refresh (refreshTrigger++) 
//     // - again after a successful CSV upload (where we also refreshTrigger++)
//     fetchDashboardData();
//   }, [refreshTrigger]);

//   // Handle CSV file upload
//   const handleCSVUpload = async (event) => {
//     const file = event.target.files?.[0];
//     if (!file) return;

//     setUploading(true);
//     setLoading(true);

//     try {
//       const formData = new FormData();
//       formData.append("file", file);

//       const uploadRes = await fetch(`${API_BASE_URL}/api/upload-csv`, {
//         method: "POST",
//         body: formData,
//       });

//       if (uploadRes.ok) {
//         console.log("CSV uploaded successfully, model is processing...");

//         // Wait for backend to process, then fetch updated data every 5 seconds
//         let attempts = 0;
//         const checkCompletion = setInterval(async () => {
//           attempts++;
//           try {
//             const res = await fetch(
//               `${API_BASE_URL}/api/forecast-summary`
//             );
//             const data = await res.json();
//             if (data.status === "success" && data.metrics) {
//               clearInterval(checkCompletion);
//               // Trigger a ONE-TIME refresh of the whole dashboard
//               setRefreshTrigger((prev) => prev + 1);
//               setUploading(false);
//               setLoading(false);
//               alert(
//                 "New dataset processed successfully! Dashboard updated."
//               );
//             }
//           } catch (err) {
//             console.log("Waiting for model processing...");
//           }

//           if (attempts > 30) {
//             // Stop after 2.5 minutes
//             clearInterval(checkCompletion);
//             setUploading(false);
//             setLoading(false);
//           }
//         }, 5000);
//       } else {
//         alert("Failed to upload CSV. Please try again.");
//         setUploading(false);
//         setLoading(false);
//       }
//     } catch (error) {
//       console.error("Error uploading CSV:", error);
//       alert("Error uploading CSV: " + error.message);
//       setUploading(false);
//       setLoading(false);
//     }
//   };

//   // Handle CSV export
//   const handleCSVExport = async () => {
//     try {
//       const res = await fetch(`${API_BASE_URL}/api/export-csv`);
//       if (!res.ok) throw new Error("Export failed");

//       const blob = await res.blob();
//       const url = window.URL.createObjectURL(blob);
//       const a = document.createElement("a");
//       a.href = url;
//       a.download = `forecast_report_${
//         new Date().toISOString().split("T")[0]
//       }.csv`;
//       a.click();
//       window.URL.revokeObjectURL(url);
//     } catch (error) {
//       console.error("Error exporting CSV:", error);
//       alert("Error exporting CSV: " + error.message);
//     }
//   };

//   return (
//     <div className="relative space-y-6">
//       {/* LOADING OVERLAY */}
//       {loading && (
//         <div className="absolute inset-0 z-50 flex items-center justify-center bg-white/70 backdrop-blur-sm">
//           <div className="flex flex-col items-center gap-3">
//             <div className="h-8 w-8 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
//             <p className="text-sm font-medium text-slate-700">
//               Running forecast pipeline...
//             </p>
//             <p className="text-xs text-slate-500">
//               Fetching LSTM forecasts and customer segments
//             </p>
//           </div>
//         </div>
//       )}

//       {/* Top header row */}
//       <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
//         <div>
//           <h1 className="text-2xl font-semibold text-slate-900">
//             Overview
//           </h1>
//           <p className="mt-1 text-sm text-slate-500">
//             LSTM-powered demand forecasting, RFM segmentation, and
//             campaign insights for your retail data.
//           </p>
//           {rateLimitInfo.active && (
//             <p className="mt-2 text-xs text-amber-600">
//               On-chain logging cooldown active (~
//               {rateLimitInfo.cooldownSeconds}s remaining). Forecast
//               data will still load; new logs will resume after the
//               cooldown.
//             </p>
//           )}
//         </div>

//         <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500">
//           <div className="flex items-center gap-1 rounded-full border border-slate-200 bg-white px-2.5 py-1 shadow-sm">
//             <span className="h-2 w-2 rounded-full bg-emerald-500" />
//             Model: LSTM (weekly)
//           </div>
//           <div className="flex items-center gap-1 rounded-full border border-slate-200 bg-white px-2.5 py-1 shadow-sm">
//             <span className="h-2 w-2 rounded-full bg-indigo-500" />
//             RFM + KMeans segmentation
//           </div>
//         </div>
//       </div>

//       {/* Filter / toolbar row */}
//       <div className="flex flex-col gap-3 rounded-3xl border border-slate-100 bg-white/70 p-4 shadow-sm backdrop-blur md:flex-row md:items-center md:justify-between">
//         <div className="flex items-center gap-3">
//           <div className="flex h-9 items-center gap-2 rounded-full border border-slate-200 bg-slate-50/70 px-3">
//             <span className="text-xs font-medium text-slate-500">
//               Store
//             </span>
//             <select className="bg-transparent text-xs font-medium text-slate-900 outline-none">
//               <option>Main Store</option>
//               <option>All Channels</option>
//             </select>
//           </div>

//           <div className="flex h-9 items-center gap-2 rounded-full border border-slate-200 bg-slate-50/70 px-3">
//             <span className="text-xs font-medium text-slate-500">
//               Horizon
//             </span>
//             <select className="bg-transparent text-xs font-medium text-slate-900 outline-none">
//               <option>Next 4 weeks</option>
//               <option>Next 8 weeks</option>
//               <option>Next 12 weeks</option>
//             </select>
//           </div>
//         </div>

//         <div className="flex flex-wrap items-center gap-2">
//           <div className="flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50/70 px-3 py-1">
//             <input
//               type="text"
//               placeholder="Filter segments..."
//               className="flex-1 outline-none text-xs text-slate-600 placeholder:text-slate-400 bg-transparent"
//             />
//             <span className="text-slate-400 text-lg">🔍</span>
//           </div>

//           <button className="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 shadow-sm">
//             Last 4 weeks
//           </button>

//           <button
//             onClick={() => setRefreshTrigger((prev) => prev + 1)}
//             disabled={loading}
//             className={`rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 shadow-sm transition ${
//               loading
//                 ? "opacity-60 cursor-not-allowed"
//                 : "hover:bg-slate-50"
//             }`}
//             title="Refresh data from backend"
//           >
//             Refresh
//           </button>

//           <button
//             onClick={handleCSVExport}
//             className="rounded-full bg-indigo-500 px-3.5 py-1.5 text-xs font-medium text-white shadow-sm hover:bg-indigo-600 transition"
//             title="Download current forecast report"
//           >
//             Export CSV
//           </button>

//           <label className="rounded-full bg-emerald-500 px-3.5 py-1.5 text-xs font-medium text-white shadow-sm hover:bg-emerald-600 transition cursor-pointer">
//             Upload CSV
//             <input
//               type="file"
//               accept=".csv"
//               onChange={handleCSVUpload}
//               disabled={uploading}
//               className="hidden"
//             />
//           </label>
//         </div>
//       </div>

//       {/* Stats cards row */}
//       <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
//         {stats.map((card) => (
//           <StatsCard key={card.id} {...card} />
//         ))}
//       </div>

//       {/* Charts row */}
//       <div className="grid gap-4 lg:grid-cols-3">
//         <div className="lg:col-span-2">
//           {/* height similar to reference so it fits on screen */}
//           <div className="h-[360px]">
//             <ForecastChart data={weeklyData} />
//           </div>
//         </div>
//         <div>
//           <div className="h-[360px]">
//             <SegmentsChart data={segmentData} />
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default Overview;



