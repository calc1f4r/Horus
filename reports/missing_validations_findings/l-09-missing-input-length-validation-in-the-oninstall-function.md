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
solodit_id: 61425
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

[L-09] Missing Input Length Validation in the `onInstall()` Function

### Overview

See description below for full details.

### Original Finding Content


## Severity

Low Risk

## Description

The `onInstall()` function directly slices the last 20 bytes of `_data` to derive the owner's address.

```solidity
address owner = address(bytes20(_data[_data.length - 20:]));
```

However, it does not validate whether `_data.length >= 20` before slicing. If the `_data` provided is less than 20 bytes long, this will result in an out-of-bounds read.

## Location of Affected Code

File: [src/modules/validators/CredibleAccountModule.sol#L287](https://github.com/etherspot/etherspot-modular-accounts/blob/d4774db9f544cc6f69000c55e97627f93fe7242b/src/modules/validators/CredibleAccountModule.sol#L287)

```solidity
function onInstall(bytes calldata _data) external override {
    address owner = address(bytes20(_data[_data.length - 20:]));
    if (validatorStorage[msg.sender].enabled) {
        revert RLV_AlreadyInstalled(msg.sender, validatorStorage[msg.sender].owner);
    }
    validatorStorage[msg.sender].owner = owner;
    validatorStorage[msg.sender].enabled = true;
    emit RLV_ValidatorEnabled(msg.sender, owner);
}
```

## Recommendation

Consider adding the missing input data length check:

```solidity
if (_data.length < 20) {
    revert();
}
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

