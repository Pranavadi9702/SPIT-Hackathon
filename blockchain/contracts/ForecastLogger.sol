// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title ForecastLogger
/// @notice Stores the final forecasted sales value immutably on-chain
contract ForecastLogger {
    uint256 public latestForecast;
    string public latestModelVersion;
    uint256 public lastUpdatedAt;

    event ForecastSaved(
        uint256 value,
        string modelVersion,
        uint256 timestamp
    );

    constructor() {}

    /// @notice Save a new forecast to the blockchain
    /// @param _value final forecasted sales value (e.g. total next 4 weeks)
    /// @param _modelVersion simple string like "v1.0"
    function saveForecast(uint256 _value, string calldata _modelVersion) external {
        latestForecast = _value;
        latestModelVersion = _modelVersion;
        lastUpdatedAt = block.timestamp;

        emit ForecastSaved(_value, _modelVersion, block.timestamp);
    }
}
