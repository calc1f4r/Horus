---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17890
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

Lack of return value check in CurveAMO_V3 may result in failed collateral retrieval

### Overview


The bug report is about a data validation issue with the CurveAMO_V3 contract. This contract does not check the return value of a call to transfer tokens from the collateral_token contract to the pool address. This means that such transfers could fail without being detected. The issue is also present in the CurveAMO_V3.withdrawCRVRewards function.

The exploit scenario is that Alice, the owner of a contract, calls the giveCollatBack function to retrieve USDC profits. If the target token implementation returns false instead of reverting, such as BAT, the transfer call fails but the transaction still succeeds.

To fix this issue, the short term solution is to either wrap the transfer call in a require statement or use a safeTransfer function. This will guarantee that if a transfer fails, the transaction will fail as well. For the long term, it is recommended to integrate Slither into the continuous integration pipeline to catch missing return value checks.

### Original Finding Content

## Data Validation

**Target:** import.sol

**Difficulty:** High

## Description

The `CurveAMO_V3` contract does not check the return value of a call to transfer tokens from the `collateral_token` contract to the pool address. Without this check, such transfers could fail.

```solidity
// Give USDC profits back
function giveCollatBack(uint256 amount) external onlyByOwnerOrGovernance {
    collateral_token.transfer(address(pool), amount);
    returned_collat_historical = returned_collat_historical.add(amount);
}
```

*Figure 10.1: contracts/Curve/CurveAMO_V3.sol#L339-L343*

If the target token implementation returns `false` instead of reverting, the `giveCollatBack` function may not detect the failed transfer call. Instead, the `giveCollatBack` function may return `true` despite its failure to transfer tokens to the pool. This issue is also present in `CurveAMO_V3.withdrawCRVRewards`.

## Exploit Scenario

Alice, the owner of a contract, calls the `giveCollatBack` function to retrieve USDC profits. The contract interacts with a token that returns `false` instead of reverting, such as BAT. Because of a lack of funds, the token transfer call fails. When Alice invokes the contract, the tokens are not actually sent, but the transaction succeeds.

## Recommendations

**Short term:** Either wrap the transfer call in a `require` statement or use a `safeTransfer` function. Taking either step will ensure that if a transfer fails, the transaction will also fail.

**Long term:** Integrate Slither into the continuous integration pipeline to catch missing return value checks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels, Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf

### Keywords for Search

`vulnerability`

