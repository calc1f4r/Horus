---
# Core Classification
protocol: FairSide
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42209
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-05-fairside
source_link: https://code4rena.com/reports/2021-05-fairside
github_link: https://github.com/code-423n4/2021-05-fairside-findings/issues/75

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
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-11] The variable `fShareRatio` is vulnerable to manipulation by flash minting and burning

### Overview


The bug report highlights a vulnerability in the function `purchaseMembership` of the `FSDNetwork` contract. The variable `fShareRatio` can be manipulated by flash minting and burning, which can affect important checks such as the pool's capital and staking rewards. This manipulation is possible because the `fShareRatio` is calculated using `fsd.getReserveBalance()`, which can be increased significantly through flash loans. This could result in users being able to purchase memberships even if the `fShareRatio` is less than 100% or earning more staking rewards than intended. The report recommends implementing a wait time to prevent flash minting and burning. The team has confirmed and resolved the issue by fixing it in a pull request. A judge has labeled this as low risk due to the 3.5% tribute fee making it unlikely for flash minting to be profitable. 

### Original Finding Content


The variable `fShareRatio` in the function `purchaseMembership` of contract `FSDNetwork` is vulnerable to manipulation by flash minting and burning, which could affect several critical logics, such as the check of enough capital in the pool (line 139-142) and the staking rewards (line 179-182).

The `fShareRatio` is calculated (line 136) by:

```solidity
(fsd.getReserveBalance() - totalOpenRequests).mul(1 ether) / fShare;
```

Where `fsd.getReserveBalance()` can be significantly increased by a user minting a large amount of FSD tokens with flash loans. In that case, the increased `fShareRatio` could affect the function `purchaseMembership` results. For Example, the user could purchase the membership even if the `fShareRatio` is < 100% previously, or the user could earn more staking rewards than before to reduce the membership fees. Although performing flash minting and burning might not be profitable overall since a 3.5% tribute fee is required when burning FSD tokens, it is still important to be aware of the possible manipulation of `fShareRatio`.

Recommend forcing users to wait for (at least) a block to prevent flash minting and burning.

**[fairside-core (FairSide) confirmed](https://github.com/code-423n4/2021-05-fairside-findings/issues/75#issuecomment-850994783):**
 > I believe this to be a minor (1) or none (0) severity issue given that the manipulation of `fShareRatio` is unsustainable due to the fee, and the Example given is actually not possible. Suppose I affect `fShareRatio` to go above 100% to purchase a membership. In that case, I will be unable to burn the necessary FSD to go below 100% again as burning is disabled when the ratio is or would go to below 100%.

**[fairside-core (FairSide) resolved](https://github.com/code-423n4/2021-05-fairside-findings/issues/75#issuecomment-851032182):**
 > Fixed in [PR#2](https://github.com/fairside-core/2021-05-fairside/pull/2).

**[cemozerr (Judge) commented](https://github.com/code-423n4/2021-05-fairside-findings/issues/75#issuecomment-857099487):**
 > Labeling this as low risk as a 3.5% tribute fee makes it very unlikely that these flash minting will be profitable.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | FairSide |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-fairside
- **GitHub**: https://github.com/code-423n4/2021-05-fairside-findings/issues/75
- **Contest**: https://code4rena.com/reports/2021-05-fairside

### Keywords for Search

`vulnerability`

