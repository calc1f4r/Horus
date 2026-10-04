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
solodit_id: 42210
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-05-fairside
source_link: https://code4rena.com/reports/2021-05-fairside
github_link: https://github.com/code-423n4/2021-05-fairside-findings/issues/45

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

[M-12] `ERC20ConvictionScore.acquireConviction` implements wrong governance checks

### Overview


The report highlights two issues with the governance checks when acquiring them from an NFT. The first issue is that the balance check is missing in the `acquireConviction` function, which allows users to become governors without meeting the minimum balance requirement. The second issue is that the governance state of an NFT is blindly applied to new users, even if the governance parameters have changed. This allows users to circumvent any changes to the parameters by front-running NFT creation. The report recommends adding the missing balance check and removing the governance transfer from the NFT, and instead computing it based on the current governance parameters. The FairSide team has confirmed and resolved the first issue, and the fix has been implemented in their code.

### Original Finding Content


There are two issues with the governance checks when acquiring them from an NFT:

#### **(Issue 1) Missing balance check**
The governance checks in `_updateConvictionScore` are:
```solidity
!isGovernance[user]
&& userConvictionScore >= governanceThreshold
&& balanceOf(user) >= governanceMinimumBalance;
```
Whereas in `acquireConviction`, only `userConvictionScore >= governanceThreshold` is checked but not `&& balanceOf(user) >= governanceMinimumBalance`.

```solidity
else if (
    !isGovernance[msg.sender] && userNew >= governanceThreshold
) {
    isGovernance[msg.sender] = true;
}
```

#### **(Issue 2) the `wasGovernance` might be outdated**

The second issue is that at the time of NFT creation, the `governanceThreshold` or `governanceMinimumBalance` was different and would not qualify for a governor now.
The NFT's governance state is blindly appplied to the new user:

```solidity
if (wasGovernance && !isGovernance[msg.sender]) {
    isGovernance[msg.sender] = true;
}
```

This allows a user to circumvent any governance parameter changes by front-running the change with an NFT creation. It's easy to circumvent the balance check to become a governor by minting and redeeming your own NFT. One can also circumvent any governance parameter increases by front-running these actions with an NFT creation and then backrunning with a redemption.

Recommend adding the missing balance check-in `acquireConviction`, removing the `wasGovernance` governance transfer from the NFT, and recomputing it based solely on the current `governanceThreshold` / `governanceMinimumBalance` settings.

**[fairside-core (FairSide) confirmed](https://github.com/code-423n4/2021-05-fairside-findings/issues/45#issuecomment-851009327):**
 > The latter of the two issue "types" is actually desired behavior. If a user was historically a governance member, the NFT should boast the exact same rights, and new thresholds should not retroactively apply. The former, however, is a valid issue as it allows circumventing the balance check!

**[fairside-core (FairSide) resolved](https://github.com/code-423n4/2021-05-fairside-findings/issues/45#issuecomment-852116812):**
 > Fixed in [PR#12](https://github.com/fairside-core/2021-05-fairside/pull/12).



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
- **GitHub**: https://github.com/code-423n4/2021-05-fairside-findings/issues/45
- **Contest**: https://code4rena.com/reports/2021-05-fairside

### Keywords for Search

`vulnerability`

