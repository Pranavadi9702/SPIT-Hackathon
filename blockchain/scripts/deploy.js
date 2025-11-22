const hre = require("hardhat");

async function main() {
  // Get the deployer account (from GANACHE_PRIVATE_KEY)
  const [deployer] = await hre.ethers.getSigners();

  console.log("🚀 Deploying ForecastLogger with account:", deployer.address);
  console.log("💰 Deployer balance:", (await deployer.getBalance()).toString());

  // Get contract factory and deploy
  const ForecastLogger = await hre.ethers.getContractFactory("ForecastLogger");
  const forecastLogger = await ForecastLogger.deploy();

  // Wait until deployment is mined
  await forecastLogger.deployed();

  console.log("✅ ForecastLogger deployed to:", forecastLogger.address);
}

// Hardhat pattern
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Deployment failed:", error);
    process.exit(1);
  });
