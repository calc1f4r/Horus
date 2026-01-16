---
# Core Classification
protocol: Inverse Finance
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5737
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-inverse-finance-contest
source_link: https://code4rena.com/reports/2022-10-inverse
github_link: https://github.com/code-423n4/2022-10-inverse-findings/issues/301

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - validation
  - admin

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 16
finders:
  - d3e4
  - pashov
  - codexploder
  - simon135
  - 0xbepresent
---

## Vulnerability Title

[M-08] Protocol withdrawals of collateral can be unexpectedly locked if governance sets the collateralFactorBps to 0

### Overview


This bug report is about the FiRM `Marketplace` contract which contains multiple governance functions for setting important values for a given debt market. In particular, `Market.setCollateralFactorBps()` sets the ratio for how much collateral is required for loans vs the debt taken on by the user. The function `Market.getWithdrawalLimitInternal()` calculates how much collateral a user can withdraw from the protocol, but it contains a check that would cause the user to not be able to withdraw any tokens, so long as they had any non-0 amount of debt and the `collateralFactorBps` was 0.

The severity of this vulnerability is high as it would disproportionately affect users whose debt values were low compared to their deposited collateral. It could also cause at least 64 hours of lock as the time required to process governance items in its workflow is 24 hours before the proposal is put up for an on-chain vote and then a 40 hour holding period.

The bug can be mitigated by considering a minimum value for the collateral factor, to go along with the maximum value check already present in the setter function. This will still reduce the quantity of collateral that can be withdrawn by users, but it would allow for some withdraws to occur. Alternatively, an explicit withdrawal lock could be implemented, making the semantic clear. Manual review is the recommended tooling for this bug.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-10-inverse/blob/3e81f0f5908ea99b36e6ab72f13488bbfe622183/src/Market.sol#L359
https://github.com/code-423n4/2022-10-inverse/blob/3e81f0f5908ea99b36e6ab72f13488bbfe622183/src/Market.sol#L376


## Vulnerability details

#### Description

The FiRM `Marketplace` contract contains multiple governance functions for setting important values for a given debt market. Many of these are numeric values that affect ratios/levels for debt positions, fees, incentives, etc.

In particular, `Market.setCollateralFactorBps()` sets the ratio for how much collateral is required for loans vs the debt taken on by the user. The lower the value, the less debt a user can take on. See `Market.getCreditLimitInternal()` for that implementation.

The function `Market.getWithdrawalLimitInternal()` calculates how much collateral a user can withdraw from the protocol, factoring in their current level of debt. It contains the following check:

`if(collateralFactorBps == 0) return 0;`

This would cause the user to not be able to withdraw any tokens, so long as they had any non-0 amount of debt and the `collateralFactorBps` was 0.

#### Severity Rationalization

It is the warden's estimation that all semantics for locking functionality of the protocol should be explicit rather than implicit. While it is very unlikely that governance would intentionally set this value to 0, if it were to do so it would disproportionately affect users whose debt values were low compared to their deposited collateral.

It is also obvious that the same function that set the value to 0 could be used to revert the change. However, this would take time. Inverse Finance has mandatory minimums for the time required to process governance items in its workflow (https://docs.inverse.finance/inverse-finance/governance/creating-a-proposal)

> The community has a social agreement to post all proposals on the forum and as a draft in GovMills at least 24 hours before the proposal is put up for an on-chain vote, and also to host a community call focusing on the proposal before the voting period.

> Once a proposal has passed, it must be queued on-chain. This action can be triggered by anyone who is willing to pay the gas fee (usually done by a DAO member). The proposal then enters a holding period of 40 hours to allow users time to prepare for the consequences of the execution of the proposal.

As such, were the situation to occur it would cause at least 64 hours of lock.

Since the contract itself only overtly contains locking for new borrowing, this implicit lock on withdraws seems like an unnecessary risk.

#### Mitigation

Consider a minimum for this value, to go along with the maximum value check already present in the setter function. While this will still reduce the quantity of collateral that can be withdrawn by users, it would allow for some withdraws to occur.

An explicit withdrawal lock could be implemented, making the semantic clear. This function could have modified access controls to enable faster reactions vs governance alone.

Alternatively, if there was an intention for this value to accept `0`, consider an 'escape hatch' function that could be enacted by users when a 'defaulted' state is set on the Market.


#### Tooling
Manual review

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Inverse Finance |
| Report Date | N/A |
| Finders | d3e4, pashov, codexploder, simon135, 0xbepresent, RaoulSchaffranek, Jujic, cryptonue, Lambda, pedroais, trustindistrust, c7e7eff, peanuts, jwood, catchup, eierina |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-inverse
- **GitHub**: https://github.com/code-423n4/2022-10-inverse-findings/issues/301
- **Contest**: https://code4rena.com/contests/2022-10-inverse-finance-contest

### Keywords for Search

`Validation, Admin`

