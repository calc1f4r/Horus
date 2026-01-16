---
# Core Classification
protocol: yAxis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42288
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-09-yaxis
source_link: https://code4rena.com/reports/2021-09-yaxis
github_link: https://github.com/code-423n4/2021-09-yaxis-findings/issues/130

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-08] `Controller.inCaseStrategyGetStuck` does not update balance

### Overview


The report identifies a bug in the `Controller.inCaseStrategyGetStuck` function that can cause the `_vaultDetails[_vault].balances[_strategy]` variable to show an incorrect balance for a strategy. This can lead to issues in the `getBestStrategyWithdraw` function and cause the `Controller.withdraw` function to attempt to withdraw more than the actual balance. The recommended solution is to add a call to the `updateBalance` function in the `inCaseStrategyGetStuck` function. The team has acknowledged the issue and suggested adding checks to prevent admin rugging. However, the function is necessary for the strategist and the risk is mitigated as the strategies and controller should not have any token balance. The team plans to make this a governance-only feature to prevent any potential issues.

### Original Finding Content

_Submitted by cmichel_

The `Controller.inCaseStrategyGetStuck` withdraws from a strategy but does not call `updateBalance(_vault, _strategy)` afterwards.

#### Impact
The `_vaultDetails[_vault].balances[_strategy]` variable does not correctly track the actual strategy balance anymore.
I'm not sure what exactly this field is used for besides getting the withdraw amounts per strategy in `getBestStrategyWithdraw`.
As the strategy contains a lower amount than stored in the field, `Controller.withdraw` will attempt to withdraw too much.

#### Recommended Mitigation Steps
Call `updateBalance(_vault, _strategy)` in `inCaseStrategyGetStuck`.

**[Haz077 (yAxis) acknowledged](https://github.com/code-423n4/2021-09-yaxis-findings/issues/130)**

**[GalloDaSballo (judge) commented](https://github.com/code-423n4/2021-09-yaxis-findings/issues/130#issuecomment-943400238):**
 > Agree with finding, I also believe `inCaseStrategyGetStuck` and `inCaseTokenGetStuck` are vectors for admin rugging, may want to add checks to ensure only non strategy token can be withdrawn from the vaults and strats

**BobbyYaxis (yAxis) noted:**
> It's a needed function for the strategist. The risk of these functions are mitigated as the strategies and controller should never have a balance of any tokens regardless. So there should be nothing/meaningful for the strategist to ever "rug" in that sense. But we can make this a governance-only feature, rather than strategist.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | yAxis |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-yaxis
- **GitHub**: https://github.com/code-423n4/2021-09-yaxis-findings/issues/130
- **Contest**: https://code4rena.com/reports/2021-09-yaxis

### Keywords for Search

`vulnerability`

