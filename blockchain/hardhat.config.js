require("@nomiclabs/hardhat-ethers");
const dotenv = require("dotenv");

// 👇 this kills those noisy [dotenv@17.2.3] logs
dotenv.config({ quiet: true });

const { GANACHE_PRIVATE_KEY, GANACHE_RPC_URL } = process.env;

module.exports = {
  solidity: "0.8.20",
  networks: {
    ganache: {
      url: GANACHE_RPC_URL || "http://127.0.0.1:7545",
      accounts: GANACHE_PRIVATE_KEY ? [GANACHE_PRIVATE_KEY] : [],
    },
  },
};
