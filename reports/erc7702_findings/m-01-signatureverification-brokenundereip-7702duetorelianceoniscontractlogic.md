---
# Core Classification
protocol: FactcheckDotFun
chain: everychain
category: uncategorized
vulnerability_type: eip-1271

# Attack Vector Details
attack_type: eip-1271
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57707
audit_firm: Kann
contest_link: none
source_link: https://github.com/Kann-Audits/Kann-Audits/blob/main/reports/md-format/private-audits-reports/FactcheckDotFun.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4.5

# Context Tags
tags:
  - eip-1271

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Kann
---

## Vulnerability Title

[M-01] SignatureVerification BrokenUnderEIP-7702DuetoRelianceonisContractLogic

### Overview


The FactCheckExchange.sol contract has a function called settleMatchedOrders() that is used to validate orders using signatures. This function checks if the address is a contract or an externally owned account (EOA) and uses different methods to verify the signature. However, with the upcoming Ethereum Pectra upgrade, this logic will break because of a new feature called EIP-7702. This feature allows EOAs to temporarily attach code during a transaction, making them appear as contracts at runtime. As a result, the function will mistakenly treat these EOAs as contracts and fail to validate the signature. This bug has been fixed by the team.

### Original Finding Content

## Severity

Medium

## Description

In the FactCheckExchange.sol contract,the settleMatchedOrders() function attempts to
validate orders using signatures by distinguishing EOAs from contracts. It uses the following logic:

-If the address has code (isContract returns true), it calls isValidSignature() via ERC-1271.
-If the address has no code, it assumes it’s an EOA and uses ECDSA.recover() to verify the signature.

This approach breaks under the upcoming Ethereum Pectra upgrade, which includes EIP-7702. EIP
7702 allows EOAs to temporarily attach code during a transaction, meaning any externally owned
account can now appear as a contract at runtime.
As aresult:
A 7702-enabled EOA with temporary code will cause the logic to treat it as a contract.
If the code does not implement ERC-1271,the isValidSignature() call will fail.
The logic does not fall back to ECDSA.recover(), causing legitimate EOA signatures to be rejected

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4.5/5 |
| Audit Firm | Kann |
| Protocol | FactcheckDotFun |
| Report Date | N/A |
| Finders | Kann |

### Source Links

- **Source**: https://github.com/Kann-Audits/Kann-Audits/blob/main/reports/md-format/private-audits-reports/FactcheckDotFun.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`EIP-1271`

