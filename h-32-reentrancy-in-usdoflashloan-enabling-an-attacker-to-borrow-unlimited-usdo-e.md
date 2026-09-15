---
# Core Classification
protocol: Tapioca DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27522
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-tapioca
source_link: https://code4rena.com/reports/2023-07-tapioca
github_link: https://github.com/code-423n4/2023-07-tapioca-findings/issues/1043

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - GalloDaSballo
  - kodyvim
  - dirk\_y
  - RedOneN
  - zzzitron
---

## Vulnerability Title

[H-32] Reentrancy in `USDO.flashLoan()`, enabling an attacker to borrow unlimited USDO exceeding the max borrow limit

### Overview


This bug report describes an exploit that allows an attacker to borrow an unlimited amount of USDO due to a missing reentrancy protection modifier in the `USDO.flashLoan()` function. A proof of concept and malicious contract have been provided, and the recommended mitigation steps are to add a reentrancy protection modifier to `USDO.flashLoan()`. The severity of the bug was initially rated as Medium, but was increased to High by the Judge.

### Original Finding Content


Due to an reentrancy attack vector, an attacker can flashLoan an unlimited amount of USDO. For example the attacker can create a malicious contract as the `receiver`, to execute the attack via the `onFlashLoan` callback (line 94 USDO.sol).

The exploit works because `USDO.flashLoan()` is missing a reentrancy protection (modifier).

As a result an unlimited amount of USDO can be borrowed by an attacker via the flashLoan exploit described above.

### Proof of Concept

Here is a POC that shows an exploit:

<https://gist.github.com/zzzitron/a121bc1ba8cc947d927d4629a90f7991>

To run the exploit add this malicious contract into the contracts folder:

<https://gist.github.com/zzzitron/8de3be7ddf674cc19a6272b59cfccde1>


### Recommended Mitigation Steps

Consider adding some reentrancy protection modifier to `USDO.flashLoan()`.

**[0xRektora (Tapioca) confirmed, but disagreed with severity and commented](https://github.com/code-423n4/2023-07-tapioca-findings/issues/1043#issuecomment-1691816035):**
 > Should be `High` severity, could really harm the protocol.

**[LSDan (Judge) increased severity to High](https://github.com/code-423n4/2023-07-tapioca-findings/issues/1043#issuecomment-1723621757)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tapioca DAO |
| Report Date | N/A |
| Finders | GalloDaSballo, kodyvim, dirk\_y, RedOneN, zzzitron, ayeslick, unsafesol, andy |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-tapioca
- **GitHub**: https://github.com/code-423n4/2023-07-tapioca-findings/issues/1043
- **Contest**: https://code4rena.com/reports/2023-07-tapioca

### Keywords for Search

`vulnerability`

