---
# Core Classification
protocol: Ondo Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32012
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-ondo-finance
source_link: https://code4rena.com/reports/2024-03-ondo-finance
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

protocol_categories:
  - leveraged_farming
  - rwa
  - services
  - cdp
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-01] No oracle price staleness checks

### Overview

See description below for full details.

### Original Finding Content


Both `ousgInstantManager` and `rOUSG` uses an oracle to determine the price of `OUSG`.

[`rOUSG::getOUSGPrice`](https://github.com/code-423n4/2024-03-ondo-finance/blob/main/contracts/ousg/rOUSG.sol#L378-L380):

```solidity
File: contracts/ousg/rOUSG.sol

378:  function getOUSGPrice() public view returns (uint256 price) {
379:    (price, ) = oracle.getPriceData();
380:  }
```

Very similar in [`ousgInstantManager::getOUSGPrice`](https://github.com/code-423n4/2024-03-ondo-finance/blob/main/contracts/ousg/ousgInstantManager.sol#L479-L485) but with a "lowest" price check.

Here only the first parameter, `price` is used. However, the second parameter returned is the [`priceTimestamp`](https://github.com/code-423n4/2024-03-ondo-finance/blob/main/contracts/rwaOracles/RWAOracleExternalComparisonCheck.sol#L127), which is the timestamp at which the price was updated. If this is old it can lead to incorrect `OUSG` prices used for `rOUSG` or instant `minting`/`redeeming`.

### Recommendation

Consider adding a check to confirm the price used isn't stale.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ondo Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-ondo-finance
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-03-ondo-finance

### Keywords for Search

`vulnerability`

