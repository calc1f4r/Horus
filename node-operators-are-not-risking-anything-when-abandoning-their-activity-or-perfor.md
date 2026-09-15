---
# Core Classification
protocol: Geodefi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20758
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/11/geodefi/
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
  - Sergii Kravchenko
  -  Christian Goll
  -  Chingiz Mardanov

---

## Vulnerability Title

Node operators are not risking anything when abandoning their activity or performing malicious actions

### Overview


This bug report is about the staking process for node operators. When initiating a validator, they need to provide 1 ETH as a deposit. Oracle then needs to ensure that the validator is created correctly and deposit the remaining 31 ETH on chain, while reimbursing the node operator the initial deposit. The problem is that the node operators have no skin in the game to continue managing the validators, as the funds do not originally belong to them. This could lead to node operators stopping operation or trying to get slashed on purpose to capitalize while shorting the assets elsewhere.

To address this issue, the Senate needs to be extra careful when approving operator onboarding proposals or potentially only reimburse the node operators the initial deposit after the funds were withdrawn from the MiniGovernance.

### Original Finding Content

#### Description


During the staking process, the node operators need to provide 1 ETH as a deposit for every validator that they would like to initiate. After that is done, Oracle needs to ensure that validator creation has been done correctly and then deposit the remaining 31 ETH on chain as well as reimburse 1 ETH back to the node operator. The node operator can then proceed to withdraw the funds that were used as initial deposits. As the result, node operators operate nodes that have 32 ETH each and none of which originally belonged to the operator. They essentially have no skin in the game to continue managing the validators besides a potential share in staking rewards. Instead, node operators could stop operation, or try to get slashed on purpose to create turmoil around derivatives on the market and try to capitalize while shorting the assets elsewhere.


#### Recommendation


Senate will need to be extra careful when approving operator onboarding proposals or potentially only reimburse the node operators the initial deposit after the funds were withdrawn from the MiniGovernance.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Geodefi |
| Report Date | N/A |
| Finders | Sergii Kravchenko,  Christian Goll,  Chingiz Mardanov
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/11/geodefi/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

