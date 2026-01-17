---
# Core Classification
protocol: Anvil Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41260
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/anvil-audit
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
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Beneficiary Must Transfer Credit Before Receiving Collateral

### Overview


The bug report addresses an issue with redeeming uLoC tokens from the `LetterOfCredit` contract. Currently, when a beneficiary or authorized user redeems their tokens, they are required to send the credited amount back to the contract. This is unnecessary and can be burdensome, as it requires the user to have the credited token balance and approve the contract to spend it. This may not be feasible for some users and prevents them from redeeming their tokens. The report suggests removing this requirement to make the process simpler and more efficient. This issue has since been resolved in a recent update.

### Original Finding Content

When a beneficiary or authorized address [redeems](https://github.com/AmperaFoundation/sol-contracts/blob/4c4423791b3427153937881fc5287a81283ee141/contracts/LetterOfCredit.sol#L449) a uLoC, they need to send the credited amount to the `LetterOfCredit` contract as a consequence of sharing liquidation logic, for example, [here](https://github.com/AmperaFoundation/sol-contracts/blob/4c4423791b3427153937881fc5287a81283ee141/contracts/LetterOfCredit.sol#L1167-L1171). They are eventually [sent back](https://github.com/AmperaFoundation/sol-contracts/blob/4c4423791b3427153937881fc5287a81283ee141/contracts/LetterOfCredit.sol#L1267-L1274) the credited amount during the call.


This is cumbersome, and unnecessary to perform the redemption. The beneficiary/authorized user needs to have the credited token amount balance in their wallet, and also approve the `LetterOfCredit` to spend the credited amount, thereby wasting gas. The beneficiary may not have the means to obtain the balance required for this transfer and may be unable to redeem the tokens they are owed.


Consider removing the credited token transfers during redeem calls to avoid this unnecessary action.


***Update:** Resolved in [pull request \#152](https://github.com/AmperaFoundation/sol-contracts/pull/152).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Anvil Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/anvil-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

