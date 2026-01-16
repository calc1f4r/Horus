---
# Core Classification
protocol: Covalent
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42309
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-10-covalent
source_link: https://code4rena.com/reports/2021-10-covalent
github_link: https://github.com/code-423n4/2021-10-covalent-findings/issues/17

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
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-02] Incorrect `updateGlobalExchangeRate` implementation

### Overview


This bug report was submitted by user xYrYuYx and addresses an issue with the `UpdateGlobalExchangeRate` function. When the `totalGlobalShares` is zero, the implementation is incorrect and can lead to a loss of funds. The user provided a test case to demonstrate this issue and used Hardhat test as a tool. The recommended mitigation steps include rethinking the function when `totalGlobalShares` is zero and adding a validator instance to prevent this situation. The issue was acknowledged and marked as resolved, but the judge suggested separating the shares accounting from the activation of validator to prevent griefing. This bug is rated as a medium severity as it can lead to a loss of funds under specific conditions. 

### Original Finding Content

_Submitted by xYrYuYx_

#### Impact
`UpdateGlobalExchangeRate` has incorrect implementation when `totalGlobalShares` is zero.

If any user didn't start stake, `totalGlobalShares` is 0, and every stake it will increase.
but there is possibility that `totalGlobalShares` can be 0 amount later by unstake or disable validator.

#### Proof of Concept
This is my test case to proof this issue: [C4_issues.js L76](https://github.com/xYrYuYx/C4-2021-10-covalent/blob/main/test/c4-tests/C4_issues.js#L76)

In my test case, I disabled validator to make `totalGlobalShares` to zero.
And in this case, some reward amount will be forever locked in the contract.
After disable validator, I mined 10 blocks, and 4 more blocks mined due to other function calls,
So total 14 CQT is forever locked in the contract.

#### Tools Used
Hardhat test

#### Recommended Mitigation Steps
Please think again when `totalGlobalShares` is zero.

**[kitti-katy (Covalent) acknowledged](https://github.com/code-423n4/2021-10-covalent-findings/issues/17#issuecomment-948913401):**
 > That is right, and I think the best solution would be to add a validator instance who is the owner and stake some low amount of tokens in it. This way we can make sure there is no such situation when `totalGlobalShares ` becomes `0` and if everyone unstaked, the owner could take out reward tokens and then unstake / redeem rewards.
>
> Not sure. That could even be marked as "high risk". if the situation happens and not handled right away (taking out reward tokens), then there could be more significant financial loss.

**[kitti-katy (Covalent) commented](https://github.com/code-423n4/2021-10-covalent-findings/issues/17#issuecomment-950028436):**
 > marked resolved as it will be manually handled

**[GalloDaSballo (judge) commented](https://github.com/code-423n4/2021-10-covalent-findings/issues/17#issuecomment-962730124):**
 > The issue found by the warden is straightforward:
> Through mix of unstaking and the use of `disableValidator` the warden was able to lock funds, making them irredemeable
>
> It seems to me that this is caused by the fact that `unstake` as well as `disableValidator` will reduce the shares: https://github.com/code-423n4/2021-10-covalent/blob/a8368e7982d336a4b464a53cfe221b2395da801f/contracts/DelegatedStaking.sol#L348`
>
> I would recommend separating the shares accounting from the activation of validator, simply removing the subtraction  of global shares in `disableValidator` would allow them to claim those shares.
>
> The function `disableValidator` can be called by either the validator or the owner, while onlyOwner can add a new validator
>
> The owner has the ability to perform this type of griefing, as well as a group of validators if they so chose
>
> Due to the specifics of the grief I will rate it of Medium Severity, as per the docs:
> `
> 2 — Med: Assets not at direct risk, but the function of the protocol or its availability could be impacted, or leak value with a hypothetical attack path with stated assumptions, but external requirements.
> `
>
> In this case we have a way to leak value (lock funds) with specific condition (malicious owner or multiple griefing validators)



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Covalent |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-covalent
- **GitHub**: https://github.com/code-423n4/2021-10-covalent-findings/issues/17
- **Contest**: https://code4rena.com/reports/2021-10-covalent

### Keywords for Search

`vulnerability`

