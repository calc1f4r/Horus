---
# Core Classification
protocol: Fei Tribechief
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32157
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/07/fei-tribechief/
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
  - dexes
  - cdp
  - services
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 3
finders:
  -  David Oz Kashi
                        
  - Sergii Kravchenko
  -  Martin Ortner
---

## Vulnerability Title

TribalChief - A wrong user.rewardDebt  value is calculated during the withdrawFromDeposit function call

### Overview


The report describes a bug in the TribalChief contract where the reward debt is not being updated correctly when a single deposit is withdrawn. This results in a lower reward debt and a larger reward for the user. The recommendation is to use the virtualAmountDelta instead of the user's virtualAmount to fix the bug. This bug can potentially allow a user to steal all the Tribe tokens from the contract by making multiple deposit-withdraw actions.

### Original Finding Content

#### Description


When withdrawing a single deposit, the reward debt is updated:


**contracts/staking/TribalChief.sol:L468-L474**



```
uint128 virtualAmountDelta = uint128( ( amount * poolDeposit.multiplier ) / SCALE_FACTOR );

// Effects
poolDeposit.amount -= amount;
user.rewardDebt = user.rewardDebt - toSigned128(user.virtualAmount * pool.accTribePerShare) / toSigned128(ACC_TRIBE_PRECISION);
user.virtualAmount -= virtualAmountDelta;
pool.virtualTotalSupply -= virtualAmountDelta;

```
Instead of the `user.virtualAmount` in reward debt calculation, the `virtualAmountDelta`  should be used.
Because of that bug, the reward debt is much lower than it would be, which means that the reward itself will be much larger during the harvest.
By making multiple deposit-withdraw actions, any user can steal all the Tribe tokens from the contract.


#### Recommendation


Use the `virtualAmountDelta` instead of the `user.virtualAmount`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Fei Tribechief |
| Report Date | N/A |
| Finders |  David Oz Kashi
                        , Sergii Kravchenko,  Martin Ortner |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/07/fei-tribechief/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

