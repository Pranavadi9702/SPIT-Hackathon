// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title ForecastLogger
/// @notice Stores the final forecasted sales value immutably on-chain
/// @dev Store forecast as an integer (e.g. total sales in smallest unit: paise)
contract ForecastLogger {
    /// @notice Latest forecasted sales value (e.g. next 4-week total)
    uint256 public latestForecast;

    /// @notice Simple string to track which model/version produced this forecast
    string public latestModelVersion;

    /// @notice Unix timestamp when the latest forecast was saved
    uint256 public lastUpdatedAt;

    /// @dev Emitted whenever a new forecast is saved
    event ForecastSaved(
        uint256 value,
        string modelVersion,
        uint256 timestamp
    );

    constructor() {}

    /// @notice Save a new forecast to the blockchain
    /// @param _value Final forecasted sales value (e.g. total next 4 weeks)
    /// @param _modelVersion Simple string like "lstm-v1.0" or "v2-2025-11-22"
    function saveForecast(uint256 _value, string calldata _modelVersion) external {
        latestForecast = _value;
        latestModelVersion = _modelVersion;
        lastUpdatedAt = block.timestamp;

        emit ForecastSaved(_value, _modelVersion, block.timestamp);
    }

    /// @notice Convenience getter returning all info in one call
    /// @return value Latest forecast value
    /// @return modelVersion Model version string
    /// @return timestamp Block timestamp when it was last updated
    function getLatestForecast()
        external
        view
        returns (uint256 value, string memory modelVersion, uint256 timestamp)
    {
        return (latestForecast, latestModelVersion, lastUpdatedAt);
    }
}
