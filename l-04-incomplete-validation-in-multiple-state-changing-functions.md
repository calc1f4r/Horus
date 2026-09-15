---
# Core Classification
protocol: Csx
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44018
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/CSX-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[L-04] Incomplete Validation In Multiple State Changing Functions

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Description

1. Missing zero-address checks

It has been detected that almost all functions of the smart contracts are missing address validation. Every input address should be checked not to be zero, especially the ones that could lead to rendering the contract unusable, lock tokens, etc. This is considered a best practice.

2. No upeer-limit on `changeBaseFee()` and `baseFee` in constructor.

3. Add validation for 3 false input parameters in the `distribute()` function, in order to prevent emitting the Distribute event unnecessarily.

## Location of Affected Code

File: [TradeFactory/TradeFactoryBase.sol](https://github.com/csx-protocol/csx-contracts/blob/bc51a67ccff86f2c691375f3cc92ee8c0a9fc369/contracts/TradeFactory/TradeFactoryBase.sol)

```solidity
constructor(address _keepers, address _users, address _tradeFactoryBaseStorage, uint256 _baseFee) {
  keepersContract = IKeepers(_keepers);
  usersContract = IUsers(_users);
  tradeFactoryBaseStorage = ITradeFactoryBaseStorage(_tradeFactoryBaseStorage);
  baseFee = _baseFee;
}

function changeBaseFee(uint256 _baseFee) external isCouncil {
  baseFee = _baseFee;
}
```

File: [StakedCSX.sol#L119](https://github.com/csx-protocol/csx-contracts/blob/bc51a67ccff86f2c691375f3cc92ee8c0a9fc369/contracts/CSX/StakedCSX.sol#L119)

```solidity
function distribute(bool dWeth, bool dUsdc, bool dUsdt) external {
```

## Recommendation

Consider incorporating zero-address checks into the majority of state-changing functions, introducing an upper limit for the `changeBaseFee()` function and `baseFee` setting in the constructor, and implementing appropriate input validation within the `distribute()` function.

## Team Response

Acknowledged and fixed as proposed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Csx |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/CSX-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

