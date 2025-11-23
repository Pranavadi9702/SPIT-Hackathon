export const statsCards = [
  {
    id: 1,
    title: "Total Sales (Last 4 Weeks)",
    value: "₹12,45,000",
    change: "+8.2%",
    changeLabel: "vs last month",
    icon: "💰",
  },
  {
    id: 2,
    title: "Forecasted Sales (Next 4 Weeks)",
    value: "₹13,20,000",
    change: "+5.1%",
    changeLabel: "projected",
    icon: "📈",
  },
  {
    id: 3,
    title: "Total Customers",
    value: "8,452",
    change: "+3.4%",
    changeLabel: "vs last month",
    icon: "👥",
  },
  {
    id: 4,
    title: "Top Segment",
    value: "Champions",
    change: "+5%",
    changeLabel: "growth in last 30 days",
    icon: "🏆",
  },
];

export const weeklySalesData = [
  { week: "Week 1", actual: 280000, forecast: 300000 },
  { week: "Week 2", actual: 310000, forecast: 320000 },
  { week: "Week 3", actual: 320000, forecast: 340000 },
  { week: "Week 4", actual: 335000, forecast: 360000 },
];

export const customerSegmentsData = [
  { name: "Champions", value: 25 },
  { name: "Loyal Customers", value: 30 },
  { name: "At-Risk", value: 15 },
  { name: "New Customers", value: 20 },
  { name: "Others", value: 10 },
];

export const customers = [
  {
    id: "CUS-1001",
    name: "Aarav Sharma",
    segment: "Champions",
    recency: 3,
    frequency: 18,
    monetary: 52000,
  },
  {
    id: "CUS-1002",
    name: "Priya Verma",
    segment: "Loyal Customers",
    recency: 15,
    frequency: 12,
    monetary: 31500,
  },
  {
    id: "CUS-1003",
    name: "Rohan Mehta",
    segment: "At-Risk",
    recency: 45,
    frequency: 6,
    monetary: 20500,
  },
  {
    id: "CUS-1004",
    name: "Sneha Kulkarni",
    segment: "New Customers",
    recency: 5,
    frequency: 2,
    monetary: 4500,
  },
  {
    id: "CUS-1005",
    name: "Vikram Singh",
    segment: "Champions",
    recency: 2,
    frequency: 22,
    monetary: 68000,
  },
];

export const offersBySegment = [
  {
    segment: "Champions",
    description: "High-value, highly engaged customers.",
    offer: "Exclusive early access to new products + 15% off next order.",
  },
  {
    segment: "Loyal Customers",
    description: "Frequent buyers with consistent spend.",
    offer: "10% loyalty discount + bonus points on weekend purchases.",
  },
  {
    segment: "At-Risk",
    description: "Previously active but engagement declining.",
    offer: "Winback campaign: 20% off + free shipping if they purchase this week.",
  },
  {
    segment: "New Customers",
    description: "Recently acquired customers.",
    offer: "Welcome offer: 10% off second purchase + referral bonus.",
  },
];
