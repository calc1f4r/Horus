---
# Core Classification
protocol: Olympus DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3206
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-08-olympus-dao-contest
source_link: https://code4rena.com/reports/2022-08-olympus
github_link: https://github.com/code-423n4/2022-08-olympus-findings/issues/117

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
  - liquid_staking
  - yield
  - cross_chain
  - leveraged_farming
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - brgltd
  - djxploit
---

## Vulnerability Title

[M-02] Solmate `safetransfer` and `safetransferfrom` does not check the codesize of the token address, which may lead to fund loss

### Overview


This bug report is about a vulnerability in the code of the project 2022-08-olympus. The vulnerability is in the getloan() and replayloan() functions of the TRSRY.sol file, located at lines 110 and 99 respectively. The issue is that the safetransfer and safetransferfrom functions do not check the existence of code at the token address. This could lead to miscalculation of funds and possibly loss of funds, as the protocol will think that funds have been transferred and successful, when in reality they have not. The proof of concept is the code at the two lines mentioned above. The vulnerability was found through manual code review. The recommended mitigation step is to use openzeppelin's safeERC20 or to implement a code existence check.

### Original Finding Content

_Submitted by djxploit, also found by brgltd_

In `getloan()` and `replayloan()`, the `safetransfer` and `safetransferfrom` doesn't check the existence of code at the token address. This is a known issue while using solmate's libraries.<br>
Hence this may lead to miscalculation of funds and may lead to loss of funds , because if `safetransfer()` and `safetransferfrom()` are called on a token address that doesn't have contract in it, it will always return success, bypassing the return value check. Due to this protocol will think that funds has been transferred and successful , and records will be accordingly calculated, but in reality funds were never transferred.<br>
So this will lead to miscalculation and possibly loss of funds

### Proof of Concept

<https://github.com/code-423n4/2022-08-olympus/blob/main/src/modules/TRSRY.sol#L110><br>
<https://github.com/code-423n4/2022-08-olympus/blob/main/src/modules/TRSRY.sol#L99>

### Recommended Mitigation Steps

Use openzeppelin's safeERC20 or implement a code existence check.

**[ind-igo (Olympus) confirmed and commented](https://github.com/code-423n4/2022-08-olympus-findings/issues/117#issuecomment-1240019949):**
 > Confirmed. Will implement this. Thank you.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Olympus DAO |
| Report Date | N/A |
| Finders | brgltd, djxploit |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-olympus
- **GitHub**: https://github.com/code-423n4/2022-08-olympus-findings/issues/117
- **Contest**: https://code4rena.com/contests/2022-08-olympus-dao-contest

### Keywords for Search

`vulnerability`

