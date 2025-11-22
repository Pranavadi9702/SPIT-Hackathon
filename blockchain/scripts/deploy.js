const hre = require("hardhat");

async function main() {
  // ethers plugin adds hre.ethers
  const ForecastLogger = await hre.ethers.getContractFactory("ForecastLogger");
  const forecastLogger = await ForecastLogger.deploy();

  await forecastLogger.deployed();

  console.log("🚀 ForecastLogger deployed to:", forecastLogger.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
