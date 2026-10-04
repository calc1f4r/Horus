---
# Core Classification
protocol: TokenOps 3 - Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61761
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/token-ops-3-staking/8ab84b1e-f47d-4da9-996f-5781e9f21428/index.html
source_link: https://certificate.quantstamp.com/full/token-ops-3-staking/8ab84b1e-f47d-4da9-996f-5781e9f21428/index.html
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - István Böhm
  - Julio Aguilar
  - Cameron Biniamow
---

## Vulnerability Title

DoS While Calculating Rewards

### Overview


The client has updated their code to fix a bug where users could experience a denial of service and be unable to interact with their stake if they have not staked, withdrawn, or claimed rewards after a certain number of staker condition updates. This was caused by the function used to calculate rewards running out of gas. The client has reduced the initial value of `maxStakingConditions` and added a global cap to prevent this issue. However, if the owner sets this cap too high, transactions involving reward calculation could still become too gas-intensive and prevent users from executing certain functions. It is recommended that the code be evaluated to ensure reliable performance within gas constraints, or a function be added to allow stakers to manually calculate rewards and control gas usage. 

### Original Finding Content

**Update**
Fixed in `da37d6c3f5e989aa16c6cccfbfc8d38ebddfa34f`. The client reduced the initial value of `maxStakingConditions` to 20 and introduced a global cap `MAX_STAKING_CONDITIONS_LIMIT` set to 512. While users still need to loop through all conditions since their last update to calculate rewards, these values were chosen based on thorough gas usage testing to ensure that even large iterations do not present practical issues.

**File(s) affected:**`contracts/Staking.sol`

**Description:** Staker rewards are calculated by iterating over all staker conditions since the staker's last update. If a staker has not staked, withdrawn, or claimed rewards after a sufficiently high number of staker condition updates, the function `_claimRewards()` could run out of gas and fail. Thus, the staker could experience a denial of service and be prevented from interacting with their stake altogether.

While `maxStakingConditions` (default `30`) provides a cap, if the `owner` sets this cap sufficiently high using the `setMaxStakingConditions()` function, transactions involving reward calculation (`stake()`, `withdraw()`, `claim()`) could become too gas-intensive, potentially exceeding block gas limits and preventing the users from executing the affected functions.

**Recommendation:** Consider adding a function to the `Staking` contract that allows stakers to manually calculate rewards for a specified number of condition updates, giving them control over gas usage. Alternatively, thoroughly evaluate the gas costs of the `_calculateRewards()` function, especially given the default of `30` iterations, and assess whether setting a hard limit on the number of staking conditions would help ensure reliable performance within gas constraints.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | TokenOps 3 - Staking |
| Report Date | N/A |
| Finders | István Böhm, Julio Aguilar, Cameron Biniamow |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/token-ops-3-staking/8ab84b1e-f47d-4da9-996f-5781e9f21428/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/token-ops-3-staking/8ab84b1e-f47d-4da9-996f-5781e9f21428/index.html

### Keywords for Search

`vulnerability`

