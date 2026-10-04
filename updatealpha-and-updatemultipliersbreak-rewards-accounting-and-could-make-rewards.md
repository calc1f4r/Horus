---
# Core Classification
protocol: Venus Prime Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32969
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/venus-prime-audit
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

updateAlpha and updateMultipliersBreak Rewards Accounting and Could Make Rewards Pool Insolvent

### Overview


This bug report discusses an issue with the calculation and distribution of rewards in the Venus Protocol. The bug occurs when updating the total interest for each market, as this is not done before collecting interest from individual users. This means that the score used to calculate interest may be different from the score used to distribute rewards, leading to incorrect reward allocations. This can result in some users receiving more rewards than they should, while others receive none at all. The Venus team has addressed this issue in a recent update.

### Original Finding Content

Every time interest is accrued, the total rewards are [divided by the total sum of the user's scores](https://github.com/VenusProtocol/venus-protocol/blob/f31a0543da039dab69112c6be3e36ea54959503b/contracts/Tokens/Prime/Prime.sol#L456) to get the rewards entitled per score. This assumes that the total score for each user is the same when interest is collected as when it is calculated. This invariant is usually maintained as `executeBoost` collects the interest from users before any actions that change their XVS or VToken balances (which play a role in score calculation). 


However, `updateAlpha` and `updateMultipliers` [update](https://github.com/VenusProtocol/venus-protocol/blob/f31a0543da039dab69112c6be3e36ea54959503b/contracts/Tokens/Prime/Prime.sol#L119) the total interest for every market but do not first collect the interest for every individual user. This means that when users collect interest after the alpha or multiplier update, the new score is multiplied by the interest accrued since the last time `executeBoost` was called. However, that score is different from the score used to calculate the interest at the time. Additionally, the `sumOfScores` now does not equal the `sumOfScores` during interest calculation. 


If the update increases the sum total of the user's scores, there would not be enough funds in the reserve to pay out all the accounted-for reward amounts. This would mean that users who collect interest early on will get a larger reward than they should, while later claimants will have zero rewards as the reward pool will become insolvent. 





***Update:** Resolved in [pull request #196](https://github.com/VenusProtocol/venus-protocol/pull/196)* at commit [f5e3221](https://github.com/VenusProtocol/venus-protocol/commit/f5e32216191f7959a51d30687df5610af543eca5).*The Venus team stated:*



> *With this change, we'll always accrue interest before updating the user score, so the rewards will be allocated using the right score*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Venus Prime Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/venus-prime-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

