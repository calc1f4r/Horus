---
# Core Classification
protocol: Moonwell  // SCA (Reserve + ERC20HoldingDeposit)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50100
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/moonwell/moonwell---sca-reserve--erc20holdingdeposit-6e898a
source_link: https://www.halborn.com/audits/moonwell/moonwell---sca-reserve--erc20holdingdeposit-6e898a
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

Missing oracle data staleness check

### Overview

See description below for full details.

### Original Finding Content

##### Description

In the `ReserveAutomation` contract, the `getPriceAndDecimals()` function checks that the returned price is positive and that the round is valid, using `answeredInRound >= roundId` and `updatedAt != 0`, but it does not check that the price data is recent. In some applications, using stale oracle data is a risk.

  

```
    /// @notice helper function to retrieve price from chainlink
    /// @param oracleAddress The address of the chainlink oracle
    /// returns the price and then the decimals of the given asset
    /// reverts if price is 0 or if the oracle data is invalid
    function getPriceAndDecimals(
        address oracleAddress
    ) public view returns (int256, uint8) {
        (
            uint80 roundId,
            int256 price,
            ,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = AggregatorV3Interface(oracleAddress).latestRoundData();
        bool valid = price > 0 && answeredInRound >= roundId && updatedAt != 0;
        require(valid, "ReserveAutomationModule: Oracle data is invalid");
        uint8 oracleDecimals = AggregatorV3Interface(oracleAddress).decimals();

        return (price, oracleDecimals); /// price always gt 0 at this point
    }
```

  

The `getPriceAndDecimals()` function does not adequately handle cases where the oracle returns the latest timestamp (`updatedAt`) outside the defined heartbeat interval for the requested asset.

Specifically, when using the `AggregatorV3Interface` from Chainlink, it is essential to validate the `updatedAt` timestamp returned by the `latestRoundData` function to ensure it is within acceptable ranges.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:L/A:N/D:L/Y:N/R:N/S:C (3.9)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:L/A:N/D:L/Y:N/R:N/S:C)

##### Recommendation

Implement validation checks for the returned oracle data when using the `AggregatorV3Interface`. Ensure that the latest returned timestamp is within the defined heartbeat interval for the requested asset.

##### Remediation Comment

**RISK ACCEPTED:** The **Moonwell team** has accepted the risk related to this finding.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Moonwell  // SCA (Reserve + ERC20HoldingDeposit) |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/moonwell/moonwell---sca-reserve--erc20holdingdeposit-6e898a
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/moonwell/moonwell---sca-reserve--erc20holdingdeposit-6e898a

### Keywords for Search

`vulnerability`

