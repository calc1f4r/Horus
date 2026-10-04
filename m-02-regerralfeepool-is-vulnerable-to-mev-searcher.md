---
# Core Classification
protocol: Mochi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42300
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-10-mochi
source_link: https://code4rena.com/reports/2021-10-mochi
github_link: https://github.com/code-423n4/2021-10-mochi-findings/issues/62

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
  - cross_chain
  - rwa
  - options_vault

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-02] `regerralFeePool` is vulnerable to MEV searcher

### Overview


The bug report is about a function called `claimRewardAsMochi` in the `ReferralFeePoolV0` contract. This function does not take into account the slippage, which means that users could potentially lose a lot of money when swapping assets. This is a high-risk issue because there are many MEV searchers on the Ethereum network. The bug was found by jonah1005 and cmichel and they recommend adding a new parameter called `minReceivedAmount` to mitigate this issue. The front-end should also calculate the minimum amount with the current price. This has been confirmed by ryuheimat from Mochi.

### Original Finding Content

_Submitted by jonah1005, also found by cmichel_

#### Impact
`claimRewardAsMochi` in the `ReferralFeePoolV0` ignores slippage. This is not a desirable design. There are a lot of MEV searchers in the current network. Swapping assets with no slippage control would get rekted. Please refer to <https://github.com/flashbots/pm>.

Given the current state of the Ethereum network, users would likely be sandwiched. I consider this is a high-risk issue.

#### Proof of Concept
[ReferralFeePoolV0.sol#L28-L48](https://github.com/code-423n4/2021-10-mochi/blob/main/projects/mochi-core/contracts/feePool/ReferralFeePoolV0.sol#L28-L48)
Please refer to  [Mushrooms Finance Theft of Yield Bug Fix Postmortem | by Immunefi | Immunefi | Medium](https://medium.com/immunefi/mushrooms-finance-theft-of-yield-bug-fix-postmortem-16bd6961388f) to see a possible attack pattern.

#### Recommended Mitigation Steps
I recommend adding `minReceivedAmount` as a parameter.

```solidity
function claimRewardAsMochi(uint256 _minReceivedAmount) external {
    // original logic here
    require(engine.mochi().balanceOf(address(this)) > _minReceivedAmount, "!min");
    engine.mochi().transfer(
        msg.sender,
        engine.mochi().balanceOf(address(this))
    );
}
```

Also, the front-end should calculate the min amount with the current price.

[ryuheimat (Mochi) confirmed](https://github.com/code-423n4/2021-10-mochi-findings/issues/62)



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mochi |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-mochi
- **GitHub**: https://github.com/code-423n4/2021-10-mochi-findings/issues/62
- **Contest**: https://code4rena.com/reports/2021-10-mochi

### Keywords for Search

`vulnerability`

