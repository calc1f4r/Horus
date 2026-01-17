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
solodit_id: 53358
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

[L-10] Missing registered agent validation in `OmoVault.borrow()` function

### Overview

See description below for full details.

### Original Finding Content

The `OmoVault.borrow()` function is designed to allow whitelisted agents to borrow assets from the vault for reinvestment and yield generation, it accepts a `receiver` parameter, which determines the account that will receive the borrowed assets.

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

While the function ensures that the caller is a whitelisted agent; **it does not verify whether the agent is registered as an authorized agent for the `receiver` account**, so any agent could borrow on behalf of another `DynamicAccount` even if they are not a registered agent for that account.

Since the protocol relies on `DynamicAccount` wallets, where agents manage assets on behalf of users, failing to enforce this validation could allow unauthorized agents to execute financial operations on accounts they do not control.

Recommendations:

Implement a check in the `OmoVault.borrow()` function to ensure that the borrowing agent is a registered agent for the specified receiver.

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

