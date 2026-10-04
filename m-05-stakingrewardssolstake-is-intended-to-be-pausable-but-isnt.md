---
# Core Classification
protocol: Y2k Finance
chain: everychain
category: logic
vulnerability_type: pause

# Attack Vector Details
attack_type: pause
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5786
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-09-y2k-finance-contest
source_link: https://code4rena.com/reports/2022-09-y2k-finance
github_link: https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/38

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - pause
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - services
  - liquidity_manager
  - insurance

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

[M-05] StakingRewards.sol#stake is intended to be pausable but isn't

### Overview


The bug report is about a vulnerability in StakingRewards.sol, a smart contract code, which prevents the intended pausing of staking. The code in question is found at the given link. The impact of this vulnerability is that staking cannot be paused as intended. The proof of concept for this vulnerability is that StakingRewards.sol inherits pausable and implements the whenNotPaused modifier on stake, but does not implement any method to actually pause or unpause the contract. This renders the pausing system useless and staking cannot be paused as intended. To fix this vulnerability, it is recommended that the owner creates simple external pause and unpause functions that can be called by the owner.

### Original Finding Content


Staking is unable to be paused as intended.

### Proof of Concept

StakingRewards.sol inherits pausable and implements the whenNotPaused modifier on stake, but doesn't implement any method to actually pause or unpause the contract. Pausable.sol only implements internal functions, which requires external or public functions to be implemented to wrap them. Since nothing like this has been implemented, the entire pausing system is rendered useless and staking cannot be paused as is intended.

### Recommended Mitigation Steps

Create simple external pause and unpause functions that can be called by owner.

**[MiguelBits (Y2K Finance) disputed](https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/38)** 

**[HickupHH3 (judge) commented](https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/38#issuecomment-1280395938):**
 > Great catch!
> 
> While the contract is taken from Synthetix's StakingRewards; note that they use a [different version of Pausable](https://github.com/Synthetixio/synthetix/blob/develop/contracts/Pausable.sol) that comes with a `setPaused()` function. This is notably absent from OZ's implementation; one has to have the pause and unpause function explicitly created.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Y2k Finance |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-y2k-finance
- **GitHub**: https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/38
- **Contest**: https://code4rena.com/contests/2022-09-y2k-finance-contest

### Keywords for Search

`Pause, Business Logic`

