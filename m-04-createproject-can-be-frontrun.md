---
# Core Classification
protocol: Joyn
chain: everychain
category: economic
vulnerability_type: front-running

# Attack Vector Details
attack_type: front-running
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1764
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-joyn-contest
source_link: https://code4rena.com/reports/2022-03-joyn
github_link: https://github.com/code-423n4/2022-03-joyn-findings/issues/26

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:
  - front-running

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - kirk-baird
  - wuwe1
  - defsec
---

## Vulnerability Title

[M-04] createProject can be frontrun

### Overview


This bug report is about a vulnerability in the CoreFactory Solidity contract, which can be found on GitHub at the link provided. The vulnerability could allow a malicious user to become the owner of a collection and withdraw paymentToken, as the collections.isForSale can be changed by the frontrunner. The malicious user could do this by calling the createProject function. 

To mitigate this vulnerability, two solutions are proposed. The first is to consider using a white list on project creation. The second is to ask the user to sign their address and check the signature against the msg.sender. This solution can be found on the OpenZeppelin Contracts GitHub page.

### Original Finding Content

_Submitted by wuwe1, also found by defsec, and kirk-baird_

This is dangerous in scam senario because the malicious user can frontrun and become the owner of the collection. As owner, one can withdraw `paymentToken`. (note that \_collections.isForSale can be change by frontrunner)

### Proof of Concept

1.  Anyone can call `createProject`.

<https://github.com/code-423n4/2022-03-joyn/blob/main/core-contracts/contracts/CoreFactory.sol#L70-L77>

```solidity
  function createProject(
    string memory _projectId,
    Collection[] memory _collections
  ) external onlyAvailableProject(_projectId) {
    require(
      _collections.length > 0,
      'CoreFactory: should have more at least one collection'
    );
```

### Recommended Mitigation Steps

Two ways to mitigate.

1.  Consider use white list on project creation.
2.  Ask user to sign their address and check the signature against `msg.sender`.  <https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/ECDSA.sol#L102>


**[sofianeOuafir (Joyn) confirmed and commented](https://github.com/code-423n4/2022-03-joyn-findings/issues/26#issuecomment-1099700412):**
 > This is an issue and we intend to fix it!

**[deluca-mike (judge) commented](https://github.com/code-423n4/2022-03-joyn-findings/issues/26#issuecomment-1105980217):**
 > The solutions listed in #34 and #35 are better.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Joyn |
| Report Date | N/A |
| Finders | kirk-baird, wuwe1, defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-joyn
- **GitHub**: https://github.com/code-423n4/2022-03-joyn-findings/issues/26
- **Contest**: https://code4rena.com/contests/2022-03-joyn-contest

### Keywords for Search

`Front-Running`

