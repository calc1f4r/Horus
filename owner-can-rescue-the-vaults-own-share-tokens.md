---
# Core Classification
protocol: Sherpa
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63836
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Immeas
  - MrPotatoMagic
---

## Vulnerability Title

Owner can rescue the vault’s own share tokens

### Overview


The bug report is about a function called `SherpaVault::rescueTokens` which is supposed to prevent the rescue of a specific token, called the wrapper token, in order to protect user funds. However, the function currently allows the rescue of the vault's own share token, which can be exploited by the owner or a compromised owner key to withdraw user deposits. The recommended solution is to disallow the rescue of the vault's own share token. This bug has been fixed in a recent commit.

### Original Finding Content

**Description:** [`SherpaVault::rescueTokens`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/blob/50eb8ad6ee048a767f7ed2265404c59592c098b7/contracts/SherpaVault.sol#L730-L740) forbids rescuing the wrapper token:
```solidity
// CRITICAL: Cannot rescue the wrapper token (user funds)
// This protects deposited SherpaUSD from being withdrawn by owner
if (token == stableWrapper) revert CannotRescueWrapperToken();
```

But it allows rescuing the vault’s own share token (`token == address(vault)`). Since[ newly minted shares](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/blob/50eb8ad6ee048a767f7ed2265404c59592c098b7/contracts/SherpaVault.sol#L543-L544) for pending deposits are held in vault custody at `address(this)` and user redemptions transfer from this balance:
```solidity
accountingSupply += mintShares;
_mint(address(this), mintShares);
```

The owner can transfer out custody shares via `rescueTokens`, reducing the vault-held pool that backs users’ pending/redemption balances.

**Impact:** An owner (or compromised owner key) can move vault-custodied shares away from `address(this)`, which they then can withdraw for the underlying deposit.

**Recommended Mitigation:** Disallow rescuing the vault’s own share token:

```diff
- if (token == stableWrapper) revert CannotRescueWrapperToken();
+ if (token == stableWrapper || token == address(this)) revert CannotRescueWrapperToken();
```

**Sherpa:** Fixed in commit [`1a634e0`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/commit/1a634e0331968ea5a73f38a62ef824da9376ab52)

**Cyfrin:** Verified. The vault token is now also prevented from being rescued.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Sherpa |
| Report Date | N/A |
| Finders | Immeas, MrPotatoMagic |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

