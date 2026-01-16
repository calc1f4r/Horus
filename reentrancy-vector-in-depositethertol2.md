---
# Core Classification
protocol: Taiko
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36009
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/taiko/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/taiko/review.pdf
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

protocol_categories:
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Reentrancy Vector In depositEtherToL2()

### Overview


The function depositEtherToL2() does not have the necessary protection against reentrancy, which means it is possible for the function to be called multiple times. This can potentially lead to unexpected behavior and security issues. The function also reads and writes to certain fields that could be exploited for reentrancy. Additionally, another function called within depositEtherToL2() could potentially bypass a security check, but it appears to be safe due to the lack of code in a related function. The testing team was unable to find any issues during their allotted time, but the potential impact is still considered medium severity. The recommendation is to add the necessary protection to depositEtherToL2() in the file TaikoL1.sol. This issue has been resolved in PR #15569. Another issue was also found where a specific function can only be called once, which has also been resolved.

### Original Finding Content

## Description

The function `depositEtherToL2()` does not have the `nonReentrant` modifier. It is therefore possible to reenter into `depositEtherToL2()`. Both `proposeBlock()` and `depositEtherToL2()` read and write to the fields `state.ethDeposits` and `state.slotA.numEthDeposits` and are potential reentrancy vectors. Additionally, `LibDepositing.depositEtherToL2()` makes a call to the bridge contract which would allow bypassing the `canDepositEthToL2()` check. However, the bridge contract implements a `receive()` function with no code, and so reentrancy is not possible. 

The testing team was unable to find, during the allocated time, an exploitable reentrancy vector to negatively impact the contract. Thus, the impact is rated as medium severity.

## Recommendations

Add the `nonReentrant` modifier to the function `depositEtherToL2()` in `TaikoL1.sol`.

## Resolution

The `nonReentrant` modifier has been added to `depositEtherToL2()` in PR #15569.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Taiko |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/taiko/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/taiko/review.pdf

### Keywords for Search

`vulnerability`

