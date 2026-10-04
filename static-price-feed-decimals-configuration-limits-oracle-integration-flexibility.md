---
# Core Classification
protocol: Genius Contracts Re-Assessment
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51977
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/shuttle-labs/genius-contracts-re-assessment
source_link: https://www.halborn.com/audits/shuttle-labs/genius-contracts-re-assessment
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Static Price Feed Decimals Configuration Limits Oracle Integration Flexibility

### Overview

See description below for full details.

### Original Finding Content

##### Description

The **GeniusVaultCore** contract hardcodes price bounds with an assumed 8 decimals precision, even if it's the default behavior of Chainlink price feeds, it is not guaranteed that in the future price feeds use the same decimal configurations:

```
// Price bounds (8 decimals like Chainlink)
uint256 public constant PRICE_LOWER_BOUND = 98_000_000;// 0.98
uint256 public constant PRICE_UPPER_BOUND = 102_000_000;// 1.02
```

  

The price verification function uses these static bounds without accounting for the actual decimals returned by the price feed:

```
function _verifyStablecoinPrice() internal view returns (bool) {
    try stablecoinPriceFeed.latestRoundData() returns (
        uint80 roundId,
        int256 price,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    ) {
        uint256 priceUint = uint256(price);
        if (priceUint < PRICE_LOWER_BOUND || priceUint > PRICE_UPPER_BOUND) {
            revert GeniusErrors.PriceOutOfBounds(priceUint);
        }
```

  

**Impact:**

1. Integration breaks with price feeds using non-8 decimal configurations
2. Manual deployment adjustments needed for different oracle implementations
3. Reduced protocol flexibility when integrating with new price feeds

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U)

##### Recommendation

It is recommended to initialize price bounds dynamically based on the price feed's decimals configuration:

```
contract GeniusVaultCore {
    uint256 public immutable PRICE_LOWER_BOUND;
    uint256 public immutable PRICE_UPPER_BOUND;

    function _initialize(
        address _stablecoin,
        address _admin,
        address _multicall,
        uint256 _rebalanceThreshold,
        address _priceFeed
    ) internal onlyInitializing {
        uint8 decimals = AggregatorV3Interface(_priceFeed).decimals();
        uint256 base = 10 ** decimals;

        PRICE_LOWER_BOUND = (98 * base) / 100;// 0.98 with proper decimals
        PRICE_UPPER_BOUND = (102 * base) / 100;// 1.02 with proper decimals

    // Rest of initialization...
    }
}
```

##### Remediation

**SOLVED:** Price feeds can now be configured in `initialize()` function.

##### Remediation Hash

<https://github.com/Shuttle-Labs/genius-contracts/commit/074203878693be1bd82cef3117451bbf42e3e838>

##### References

[Shuttle-Labs/genius-contracts/src/GeniusVaultCore.sol#L40](https://github.com/Shuttle-Labs/genius-contracts/blob/main/src/GeniusVaultCore.sol#L40)

[Shuttle-Labs/genius-contracts/src/GeniusVaultCore.sol#L404](https://github.com/Shuttle-Labs/genius-contracts/blob/main/src/GeniusVaultCore.sol#L404)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Genius Contracts Re-Assessment |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/shuttle-labs/genius-contracts-re-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/shuttle-labs/genius-contracts-re-assessment

### Keywords for Search

`vulnerability`

