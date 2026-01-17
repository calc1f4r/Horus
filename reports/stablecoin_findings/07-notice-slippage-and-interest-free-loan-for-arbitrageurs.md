---
# Core Classification
protocol: Tribe
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24493
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-09-tribe
source_link: https://code4rena.com/reports/2022-09-tribe
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
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[07] Notice - Slippage and Interest Free Loan for Arbitrageurs

### Overview

See description below for full details.

### Original Finding Content


Because `redeem` doesn't burn FEI, any caller can `mint` and `redeem` multiple times in the same tx with the goal of arbing out the FEI - DAI pair.

[SimpleFeiDaiPSM.sol#L105-L106](https://github.com/code-423n4/2022-09-tribe/blob/769b0586b4975270b669d7d1581aa5672d6999d5/contracts/peg/SimpleFeiDaiPSM.sol#L105-L106)

```solidity
    function burnFeiHeld() external {

```

While FEI being tradeable for DAI is enforcing a 1-1 trade (FEI price goes up due to arbing, up to 100% + FEE), allowing the opposite swap is a easy target for arbitrageurs.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tribe |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-tribe
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-09-tribe

### Keywords for Search

`vulnerability`

