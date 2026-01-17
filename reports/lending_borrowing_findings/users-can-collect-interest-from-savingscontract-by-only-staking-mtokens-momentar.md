---
# Core Classification
protocol: mStable 1.1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13628
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/07/mstable-1.1/
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
  - liquid_staking
  - cdp
  - yield
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

Users can collect interest from SavingsContract by only staking mTokens momentarily ✓ Addressed

### Overview


A bug was reported in the SAVE contract which allows users to deposit mAssets in return for lending yield and swap fees. The bug allowed users to collect interest more than once in a 30 minute period, inflating the supply by more than 0.1%. The 30 minute window was enforced by a check in the SavingsManager.sol code. To fix this issue, the 30 minute window was removed so that every deposit also updates the exchange rate between credits and tokens. A fix is currently being worked on as part of the bug bounty program.

### Original Finding Content

#### Resolution



The blocker on collecting interest more than once in 30 minute period. A new APY bounds check has been added to verify that supply isn’t inflated by more than 0.1% within a 30 minutes window.


#### Description


The SAVE contract allows users to deposit mAssets in return for lending yield and swap fees. When depositing mAsset, users receive a “credit” tokens at the momentary credit/mAsset exchange rate which is updated at every deposit. However, the smart contract enforces a minimum timeframe of 30 minutes in which the interest rate will not be updated. A user who deposits shortly before the end of the timeframe will receive credits at the stale interest rate and can immediately trigger and update of the rate and withdraw at the updated (more favorable) rate after the 30 minutes window. As a result, it would be possible for users to benefit from interest payouts by only staking mAssets momentarily and using them for other purposes the rest of the time.


#### Examples


**code/contracts/savings/SavingsManager.sol:L141-L143**



```
// 1. Only collect interest if it has been 30 mins
uint256 timeSinceLastCollection = now.sub(previousCollection);
if(timeSinceLastCollection > THIRTY\_MINUTES) {

```

#### Recommendation


Remove the 30 minutes window such that every deposit also updates the exchange rate between credits and tokens. Note that this issue was reported independently during the bug bounty program and a fix is currently being worked on.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | mStable 1.1 |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/07/mstable-1.1/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

