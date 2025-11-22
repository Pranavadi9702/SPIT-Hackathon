require("@nomiclabs/hardhat-ethers");
const dotenv = require("dotenv");

// silence dotenv logs
dotenv.config({ quiet: true });

const { GANACHE_PRIVATE_KEY, GANACHE_RPC_URL } = process.env;

/**
 * @type import('hardhat/config').HardhatUserConfig
 */
module.exports = {
  solidity: "0.8.20",
  defaultNetwork: "ganache",
  networks: {
    // Local Hardhat network (optional, still available)
    hardhat: {},

    // Ganache network (for your project requirement)
    ganache: {
      url: GANACHE_RPC_URL || "http://127.0.0.1:7545",
      // use the private key from Ganache (without quotes inside .env)
      accounts: GANACHE_PRIVATE_KEY ? [GANACHE_PRIVATE_KEY] : [],
    },
  },
};
