---
# Core Classification
protocol: Pheasant Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60329
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html
source_link: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html
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

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Danny Aksenov
  - Faycal Lalidji
  - Ruben Koch
  - Valerian Callens
  - Guillermo Escobero
---

## Vulnerability Title

Reentrancy Lets Relayer Withdraw More than Expected by Bond Withdrawal

### Overview


The bug report addresses an issue in the `BondManager.sol` file, where a Relayer can withdraw a certain amount of tokens from their bond by calling the `executeWithdrawBond()` function. However, if the Relayer is a contract and the withdrawn token is a native token or a special ERC20 implementation, reentrancy can occur, resulting in incorrect accounting and potentially leaving only a portion of the tokens in the bond. The recommendation is to add a non-reentrant modifier to the function and follow the Check-Effects-Interacts pattern to prevent this issue.

### Original Finding Content

**Update**
Addressed in: `b0faa8d93c7a7d91961db24753a322a3a8117ca0`.

**File(s) affected:**`BondManager.sol`

**Description:** The Relayer can plan a request to withdraw a given amount `A` of tokens from its bond by calling the function `executeWithdrawBond()`. He will have to wait for a delay of `UPDATE_PERIOD` before being able to withdraw that amount by calling the function `finalizeWithdrawalBond()`. However, in the special case where the Relayer is a contract and the withdrawn token is a native token or some special ERC20 implementation, reentrancy is possible and the Relayer can withdraw a maximum of `totalLockedAmount - totalLockedAmount % A` because each withdrawal must be of exactly A tokens. It would result in a broken internal accounting and in the worst case, only `totalLockedAmount % A` remaining in the bond manager.

**Recommendation:** Add a non-reentrant modifier to the function and follow the Check-Effects-Interacts pattern.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Pheasant Network |
| Report Date | N/A |
| Finders | Danny Aksenov, Faycal Lalidji, Ruben Koch, Valerian Callens, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html

### Keywords for Search

`vulnerability`

