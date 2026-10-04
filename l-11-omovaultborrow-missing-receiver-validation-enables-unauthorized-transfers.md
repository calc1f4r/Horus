---
# Core Classification
protocol: Omo_2025-01-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53359
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-11] `OmoVault.borrow` missing receiver validation enables unauthorized transfers

### Overview

See description below for full details.

### Original Finding Content

The `OmoVault.borrow()` function allows whitelisted agents to borrow assets from the vault to reinvest and generate yield, the function accepts a `receiver` parameter, which determines the address that will receive the borrowed assets, however, there is no validation to ensure that the `receiver` is a registered account, which allows borrowing assets for unauthoized accounts:

```solidity
    function borrow(
        uint256 assets,
        address receiver
    ) external nonReentrant onlyAgent {
        address msgSender = msg.sender;
        require(assets != 0, "ZERO_ASSETS");

        asset.safeTransfer(receiver, assets);

        emit Borrow(msgSender, receiver, assets);
    }
```

Update the `OmoVault.borrow()` function to check that the receiver is a registered account before transferring borrowed assets.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Omo_2025-01-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

