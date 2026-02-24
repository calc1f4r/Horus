---
# Core Classification
protocol: AragonBlack Fundraising
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13922
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2019/11/aragonblack-fundraising/
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
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Sergii Kravchenko
  - Martin Ortner
---

## Vulnerability Title

Bancor formula should not be updated during the batch ✓ Fixed

### Overview


This report is about a bug found in the BatchedBancorMarketMaker.sol contract. Shareholders were able to vote to change the bancor formula contract, which could make the price in the current batch unpredictable. To fix the issue, AragonBlack/[email protected]`a8c2e21` stored a reference to the formula with the meta batch. It is recommended that the bancor formula update should be executed in the next batch or with a timelock that is greater than batch duration.

### Original Finding Content

#### Resolution



Fixed with [AragonBlack/[email protected]`a8c2e21`](https://github.com/AragonBlack/fundraising/pull/155/commits/a8c2e21b52a90b0f167cfcd67ecd1c6b1c664416) by storing a ref to the Formula with the meta batch.


#### Description


Shareholders can vote to change the bancor formula contract. That can make a price in the current batch unpredictable.


**code/apps/batched-bancor-market-maker/contracts/BatchedBancorMarketMaker.sol:L212-L216**



```
function updateFormula(IBancorFormula \_formula) external auth(UPDATE\_FORMULA\_ROLE) {
    require(isContract(\_formula), ERROR\_CONTRACT\_IS\_EOA);

    \_updateFormula(\_formula);
}

```
#### Recommendation


Bancor formula update should be executed in the next batch or with a timelock that is greater than batch duration.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | AragonBlack Fundraising |
| Report Date | N/A |
| Finders | Sergii Kravchenko, Martin Ortner |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2019/11/aragonblack-fundraising/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

