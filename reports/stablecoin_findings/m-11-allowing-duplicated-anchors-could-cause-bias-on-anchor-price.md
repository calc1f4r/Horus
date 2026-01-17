---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3937
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-04-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-04-vader
github_link: https://github.com/code-423n4/2021-04-vader-findings/issues/314

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
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-11] Allowing duplicated anchors could cause bias on anchor price.

### Overview


This bug report concerns a vulnerability in the Router.sol file of the vader-protocol code. The vulnerability allows anyone to interrupt the setup of the five anchors and allows duplicate anchors to be added. This could bias the result of the getAnchorPrice function. The bug report contains a link to a Proof of Concept (PoC) to demonstrate the vulnerability. The PoC can be run using the command 'npx hardhat test 200_listAnchor.js'. The bug report also provides two recommended mitigation steps to help fix the vulnerability. These steps involve adding a require statement to only allow the listAnchor function to be called from the deployer, and also checking if an anchor has already been added.

### Original Finding Content


In `Router.sol`, the setup of the five anchors can be interrupted by anyone adding a new anchor due to the lack of access control of the `listAnchor` function. Also, duplicate anchors are allowed. If the same anchor is added three times, then this anchor biases the result of `getAnchorPrice`.

Referenced code:
[Router.sol#L245-L252](https://github.com/code-423n4/2021-04-vader/blob/main/vader-protocol/contracts/Router.sol#L245-L252)

PoC: [Link to PoC](https://drive.google.com/drive/folders/1W3jhlWIIh7FxTLZET3z49yA0DBvlbcPg?usp=sharing)
See the file `200_listAnchor.js` for a PoC of this attack. To run it, use `npx hardhat test 200_listAnchor.js`.

Recommend only allowing `listAnchor` to be called from the deployer by adding a `require` statement. Also, check if an anchor is added before by `require(_isCurated == false)`.

**[strictly-scarce (vader) acknowledged](https://github.com/code-423n4/2021-04-vader-findings/issues/314#issuecomment-830633778):**
 > Deployer will list the anchors, seems highly unlikely they will get griefed in practice. Severity: 1



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-04-vader
- **GitHub**: https://github.com/code-423n4/2021-04-vader-findings/issues/314
- **Contest**: https://code4rena.com/contests/2021-04-vader-protocol-contest

### Keywords for Search

`vulnerability`

