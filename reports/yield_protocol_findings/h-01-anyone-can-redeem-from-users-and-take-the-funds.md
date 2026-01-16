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
solodit_id: 53319
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] Anyone can redeem from users and take the funds

### Overview


A bug has been found in the `redeem()` function of the `OmoRouter.sol` contract. This function is used by users to redeem shares for assets. The issue is that the `owner` needs to set approval for the router address to transfer the shares, but this can be exploited by attackers who can drain the allowance for the router address in any vault shares. This can lead to the loss of funds for users. To fix this, the `owner` should only be `msg.sender` to prevent this exploit.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

The `redeem()` function in `OmoRouter.sol` contract is triggered by the user to request redeem shares for the equivalent assets.
`owner` should set approval for the router address to transfer the shares

```solidity
File: OmoRouter.sol
     function redeem(uint256 vaultId,uint256 shares, address receiver,address owner)
     /*code*/
         // Transfer shares from owner to router first
         IOmoVault(vault).transferFrom(owner, address(this), shares);

```

An attacker can drain any allowance for the router address in any vault shares (in case chains have the possibility of front-run, MEV bots can just front-run users `redeem()` transactions) and wait for an agent to do the rest (send the funds).

## Recommendations

The owner should only be `msg.sender`

```diff
File: OmoRouter.sol
-     function redeem(uint256 vaultId,uint256 shares, address receiver,address owner)
+     function redeem(uint256 vaultId,uint256 shares, address receiver)
     /*code*/
         // Transfer shares from owner to router first
-         IOmoVault(vault).transferFrom(msg.sender, address(this), shares);
+         IOmoVault(vault).transferFrom(owner, address(this), shares);

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

