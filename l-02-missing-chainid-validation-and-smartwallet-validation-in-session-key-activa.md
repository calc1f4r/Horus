---
# Core Classification
protocol: Etherspot Credibleaccountmodule
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61418
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Etherspot-CredibleAccountModule-Security-Review.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[L-02] Missing `chainID` Validation and `smartWallet` Validation in Session Key Activation

### Overview

See description below for full details.

### Original Finding Content


## Severity

Low Risk

## Description

The `enableSessionKey()` function processes `ResourceLock` data but fails to validate `chainId` & `smartWallet` fields:

- `chainId` – Not checked against the current blockchain, allowing cross-chain replay (though with limited impact).
- `smartWallet` – Completely ignored, defaulting to `msg.sender` for session binding (unlikely to be exploited in current design).

While these do not immediately threaten funds, they violate best practices for session management.

## Location of Affected Code

File: [src/modules/validators/CredibleAccountModule.sol#L122](https://github.com/etherspot/etherspot-modular-accounts/blob/d4774db9f544cc6f69000c55e97627f93fe7242b/src/modules/validators/CredibleAccountModule.sol#L122)

## Recommendation

Consider adding a `chainID` and `smartWallet` validation:

- `chainID`

```solidity
if (rl.chainId != 0 && rl.chainId != block.chainid) {
    revert();
}
```

- `smartWallet`

```solidity
address targetWallet = rl.smartWallet != address(0) ? rl.smartWallet : msg.sender;
```

## Team Response

Fixed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Etherspot Credibleaccountmodule |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Etherspot-CredibleAccountModule-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

