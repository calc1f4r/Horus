---
# Core Classification
protocol: Accountable
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62987
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
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

protocol_categories:
  - options_vault
  - liquidity_manager
  - insurance
  - uncollateralized_lending

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Immeas
  - Chinmay
  - Alexzoid
---

## Vulnerability Title

Missing controller validation in `AccountableAsyncRedeemVault::requestRedeem` allows zero address state

### Overview

See description below for full details.

### Original Finding Content

**Description:** The `requestRedeem()` function fails to call `_checkController(controller)` validation, allowing the zero address to accumulate vault state.

**Impact:** `zeroControllerEmptyState` violation.

**Proof of Concept:** ❌ Violated: https://prover.certora.com/output/52567/acc42433123e4b289c0f84e69fa52a44/?anonymousKey=e60b3d66b5574868073bfde4218b385aa2fe5f2a

```solidity
// Zero address must have empty state for all vault fields
invariant zeroControllerEmptyState(env e)
    ghostVaultStatesMaxMint256[0] == 0 &&
    ghostVaultStatesMaxWithdraw256[0] == 0 &&
    ghostVaultStatesDepositAssets256[0] == 0 &&
    ghostVaultStatesRedeemShares256[0] == 0 &&
    ghostVaultStatesDepositPrice256[0] == 0 &&
    ghostVaultStatesMintPrice256[0] == 0 &&
    ghostVaultStatesRedeemPrice256[0] == 0 &&
    ghostVaultStatesWithdrawPrice256[0] == 0 &&
    ghostVaultStatesPendingDepositRequest256[0] == 0 &&
    ghostVaultStatesPendingRedeemRequest256[0] == 0 &&
    ghostVaultStatesClaimableCancelDepositRequest256[0] == 0 &&
    ghostVaultStatesClaimableCancelRedeemRequest256[0] == 0 &&
    !ghostVaultStatesPendingCancelDepositRequest[0] &&
    !ghostVaultStatesPendingCancelRedeemRequest[0] &&
    ghostRequestIds128[0] == 0
filtered { f -> !EXCLUDED_FUNCTION(f) } { preserved with (env eFunc) { SETUP(e, eFunc); } }
```

✅ Verified after the fix: https://prover.certora.com/output/52567/f385fd34e82c4635bd410279e4da2c97/?anonymousKey=82309551a07845692bfabb2164179224523f87ba

**Recommended Mitigation:**
```diff
diff --git a/credit-vaults-internal/src/vault/AccountableAsyncRedeemVault.sol b/credit-vaults-internal/src/vault/AccountableAsyncRedeemVault.sol
index 4cd0a3e..a64f47c 100644
--- a/credit-vaults-internal/src/vault/AccountableAsyncRedeemVault.sol
+++ b/credit-vaults-internal/src/vault/AccountableAsyncRedeemVault.sol
@@ -113,6 +113,9 @@ contract AccountableAsyncRedeemVault is IAccountableAsyncRedeemVault, Accountabl
         onlyAuth
         returns (uint256 requestId)
     {
+        // @certora FIX for zeroControllerEmptyState
+        _checkController(controller);
+
         _checkOperator(owner);
         _checkShares(owner, shares);
```

**Accountable:** Fixed in commit [`e90d3de`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/e90d3de5c133c73f0e783d552bb4e256400a547c)

**Cyfrin:** Verified. `checkController` added as a modifier to the function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Accountable |
| Report Date | N/A |
| Finders | Immeas, Chinmay, Alexzoid |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

