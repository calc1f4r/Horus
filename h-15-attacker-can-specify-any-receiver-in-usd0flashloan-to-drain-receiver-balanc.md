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
solodit_id: 27505
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-tapioca
source_link: https://code4rena.com/reports/2023-07-tapioca
github_link: https://github.com/code-423n4/2023-07-tapioca-findings/issues/1223

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
finders_count: 2
finders:
  - mojito\_auditor
  - n1punp
---

## Vulnerability Title

[H-15] Attacker can specify any `receiver` in `USD0.flashLoan()` to drain `receiver` balance

### Overview


This bug report is about a feature in USD0's `flashLoan()` function, which allows the caller to specify the `receiver` address. USD0 is then minted to this address and burnt from this address plus a fee after the callback. The issue is that since there is a fee in each flash loan, an attacker can abuse this to drain the balance of the `receiver` because the `receiver` can be specified by the caller without validation.

The proof of concept demonstrated that the allowance checked that `receiver` approved to `address(this)` but not check if `receiver` approved to `msg.sender`. The recommended mitigation step is to consider changing the "allowance check" to be the allowance that the receiver gave to the caller instead of `address(this)`. This was confirmed by 0xRektora (Tapioca).

### Original Finding Content


The flash loan feature in USD0's `flashLoan()` function allows the caller to specify the `receiver` address. USD0 is then minted to this address and burnt from this address plus a fee after the callback. Since there is a fee in each flash loan, an attacker can abuse this to drain the balance of the `receiver` because the `receiver` can be specified by the caller without validation.

### Proof of Concept

The allowance checked that `receiver` approved to `address(this)` but not check if `receiver` approved to `msg.sender`

```solidity
uint256 _allowance = allowance(address(receiver), address(this));
require(_allowance >= (amount + fee), "USDO: repay not approved");
// @audit can specify receiver, drain receiver's balance
_approve(address(receiver), address(this), _allowance - (amount + fee));
_burn(address(receiver), amount + fee);
return true;
```

### Recommended Mitigation Steps

Consider changing the "allowance check" to be the allowance that the receiver gave to the caller instead of `address(this)`.

**[0xRektora (Tapioca) confirmed](https://github.com/code-423n4/2023-07-tapioca-findings/issues/1223#issuecomment-1702986076)**

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
| Finders | mojito\_auditor, n1punp |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-tapioca
- **GitHub**: https://github.com/code-423n4/2023-07-tapioca-findings/issues/1223
- **Contest**: https://code4rena.com/reports/2023-07-tapioca

### Keywords for Search

`vulnerability`

