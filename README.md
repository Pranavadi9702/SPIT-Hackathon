# 📊 **ChainForecast Dashboard**

### **AI + Blockchain Powered Retail Intelligence Platform**

---

# 🚀 **Overview**

**ChainForecast Dashboard** is an end-to-end **retail analytics platform** that combines:

* 🧠 **LSTM-powered sales forecasting (96% accuracy)**
* 👥 **RFM + KMeans customer segmentation**
* 📈 **Automated EDA, anomaly detection & peak analysis**
* 🔗 **Blockchain forecast logging (Solidity + Hardhat)**
* 🖥 **Interactive React dashboard (Tailwind + Recharts)**
* 🔐 **JWT + Firebase secured authentication**
* 🧩 **Flask ML backend with deterministic ML pipeline**

This platform delivers **real-time, actionable retail insights** for businesses.

---

# 🧠 **Machine Learning & Analytics Pipeline**

## 🔮 **LSTM Sales Forecasting**

* Weekly aggregated forecasting
* Predicts **next 4 weeks**
* Deterministic: seeds + reproducible
* Captures trends, seasonality & price elasticity
* Model accuracy exported as CSV

### ✔ **Model Accuracy**

**96.21% (100 − MAPE)**
Evaluated on real historical data (last 4 weeks).

---

## 👥 **Customer Segmentation (RFM + KMeans)**

The system computes RFM (Recency, Frequency, Monetary) scores and maps customers to:

* **Champions**
* **Loyal Customers**
* **Potential Loyalists**
* **At Risk**
* **Lost Customers**

Includes:

* KMeans clustering
* ARPU computation
* Customer-level segmentation table
* Segment-wise forecasting readiness

---

## 📊 **Automated Analytics**

Pipeline generates:

* Daily, weekly & monthly sales
* Category & country share
* Top customers & top products
* Peak detection + anomaly identification
* Rolling averages
* 4-week forecast breakdown
* Visual artifacts (CSV, plots)

---

# 🔗 **Blockchain Integration**

## **Smart Contract — `ForecastLogger.sol`**

Stores:

* Forecast output
* Accuracy
* Timestamp
* Model version hash

## **Hardhat Features**

* Local blockchain testing
* Deployment scripts
* ABI auto-extraction
* Ethers.js frontend integration

Ensures **tamper-proof forecast integrity & traceability**.

---

# 🔐 **Authentication & Security**

The platform uses a **hybrid secure auth system**:

### 🔹 **Firebase Authentication**

* Email + password login
* Firestore user documents

### 🔹 **JWT Token System**

* Passwords are **encrypted & stored safely**
* Backend issues **JWT tokens (HS256)**
* React validates tokens before loading pages
* All dashboard routes are **protected**

Ensures only verified users can access the dashboard.

---

# 🖥 **Frontend Dashboard (React + Tailwind)**

* 🌙 Full Dark Mode UI
* 🚀 Vite ultra-fast build
* 📊 Recharts for visual analytics
* 🔒 Protected routes using JWT
* 🎛 Responsive & modern UI components

---

# 📸 **Screenshots**


### 📌 **Overview Dashboard**

<img width="1900" height="919" alt="image" src="https://github.com/user-attachments/assets/2ed99dba-2252-4ea2-878f-2cca311c8c36" />


### 📌 **Sales Forecast Page**

<img width="1909" height="919" alt="image" src="https://github.com/user-attachments/assets/f1ded8d8-e33b-4ebf-8a86-22081684f281" />


### 📌 **Customer Segmentation Dashboard**

<img width="1896" height="916" alt="image" src="https://github.com/user-attachments/assets/1fc781b7-d7ab-43a6-9882-8e6ea3330d8d" />


### 📌 **Customer Table (Paginated + Searchable)**

<img width="1604" height="636" alt="image" src="https://github.com/user-attachments/assets/4d96b806-6158-4e2b-a48f-3c889adf7670" />


### 📌 **Offers Page**

<img width="1898" height="920" alt="image" src="https://github.com/user-attachments/assets/caf3c47a-2790-4ac8-a22b-d130c93adb74" />


### 📌 **Settings / Profile Page**

<img width="1900" height="921" alt="image" src="https://github.com/user-attachments/assets/69bcb43c-31b9-40ee-8b29-24f74e833c0d" />


---

# 🏗 **Project Structure**

```
SPIT-Hackathon-integrated/
│
├── backend/
│   ├── backend.py               # Flask API + ML pipeline
│   ├── artifacts/               # Data outputs + plots
│   ├── models/                  # LSTM + RFM + KMeans models
│   └── data/                    # Retail dataset
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── api/
│   │   ├── firebase.js
│   │   └── App.jsx
│   ├── public/
│   └── tailwind.config.js
│
├── blockchain/
│   ├── contracts/               # Solidity smart contract
│   │   └── ForecastLogger.sol
│   ├── scripts/                 # Deployment scripts
│   │   └── deploy.js
│   └── hardhat.config.js
│
└── assets/
    └── screenshots/
        ├── overview.png
        ├── forecast.png
        ├── segmentation.png
        ├── table.png
        ├── offers.png
        └── settings.png
```

---

# ⚙️ **Installation & Setup**

## 1️⃣ Backend Setup (Flask + ML)

```
cd backend
pip install -r requirements.txt
python backend.py
```

Backend runs at:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 2️⃣ Frontend Setup (React + Vite)

```
cd frontend
npm install
npm run dev
```

Frontend runs at:
👉 **[http://127.0.0.1:5173](http://127.0.0.1:5173)**

---

## 3️⃣ Blockchain Setup (Hardhat + Ethers.js)

```
cd blockchain
npm install
npx hardhat node
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
```

---

# 🔌 **API Endpoints**

### ▶ Run ML Pipeline

```
POST /api/run-pipeline
```

### ▶ Forecast Summary

```
GET /api/forecast-summary
```

### ▶ Customer Segments

```
GET /api/segments-summary
```

---

# 🌟 **Business Impact**

| Feature                 | Impact                                  |
| ----------------------- | --------------------------------------- |
| **96% model accuracy**  | Highly reliable forecasting decisions   |
| **RFM segmentation**    | Targeted marketing = increased revenue  |
| **Blockchain logging**  | Trustworthy, tamper-proof predictions   |
| **Automated EDA**       | Cuts analysis time from hours → seconds |
| **Real-time dashboard** | Instant decision-making                 |

---

# 🎯 **Future Enhancements**

* Multivariate forecasting
* AutoML hyperparameter tuning
* LSTM + Prophet hybrid model
* Multi-store comparison dashboard
* Streaming data ingestion
* Distributed model training
  
 ---
