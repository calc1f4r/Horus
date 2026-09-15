---
# Core Classification
protocol: Ondo Global Markets
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62336
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md
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
finders_count: 2
finders:
  - Immeas
  - Al-Qa'qa'
---

## Vulnerability Title

Compliance check discrepancy between `onUSDManager` and `onUSD` transfers

### Overview

See description below for full details.

### Original Finding Content

**Description:** When minting or redeeming `onUSD` via `onUSDManager`, the contract extends `BaseRWAManager`, which performs a compliance check using the `onUSD` token address (`address(onUSD)`) as the `rwaToken` identifier. This happens in [`BaseRWAManager::_processSubscription`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/xManager/rwaManagers/BaseRWAManager.sol#L171-L172):

```solidity
// Reverts if user address is not compliant
ondoCompliance.checkIsCompliant(rwaToken, _msgSender());
```

The same check occurs during redemptions via [`BaseRWAManager::_processRedemption`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/xManager/rwaManagers/BaseRWAManager.sol#L243-L244).

Separately, the `onUSD` token contract itself performs compliance checks inside [`onUSD::_beforeTokenTransfer`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/onUSD.sol#L168-L180), which is invoked during transfers, minting, and burning. This function calls the inherited [`OndoComplianceGMClientUpgradeable::_checkIsCompliant`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/gmTokenCompliance/OndoComplianceGMClientUpgradeable.sol#L86-L88), which delegates to [`OndoComplianceGMView::checkIsCompliant`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/gmTokenCompliance/OndoComplianceGMView.sol#L75-L81):

```solidity
function checkIsCompliant(address user) external override {
  compliance.checkIsCompliant(gmIdentifier, user);
}
```

Here, [`OndoComplianceGMViewgmIdentifier`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/gmTokenCompliance/OndoComplianceGMView.sol#L34-L36) is a hardcoded address derived from the string `"global_markets"` and used as the `rwaToken` identifier:

```solidity
address public gmIdentifier =
  address(uint160(uint256(keccak256(abi.encodePacked("global_markets")))));
```

As a result, minting and redeeming will trigger two compliance checks with different identifiers:

* `address(onUSD)` via the manager logic
* `gmIdentifier` via the token's `_beforeTokenTransfer`

**Impact:** Although `_beforeTokenTransfer` runs during minting and burning, meaning both compliance checks still occur, the use of two different `rwaToken` identifiers introduces an unnecessary inconsistency. If the two compliance lists are not aligned, minting or redeeming could revert unexpectedly, despite the user being compliant under one identifier.

**Recommended Mitigation:** There are two possible mitigation approaches, depending on which compliance identifier is intended as canonical for `onUSD`.

1) Update `OnUSD::_beforeTokenTransfer` to explicitly use `address(this)` as the `rwaToken` in all compliance checks. This aligns the transfer/mint/burn logic with the identifier used in the manager’s mint/redeem flow, ensuring consistency and eliminating the need to maintain two separate compliance lists.

   ```solidity
   if (from != msg.sender && to != msg.sender) {
     compliance.checkIsCompliant(address(this), msg.sender);
   }

   if (from != address(0)) {
     // If not minting
     compliance.checkIsCompliant(address(this), from);
   }

   if (to != address(0)) {
     // If not burning
     compliance.checkIsCompliant(address(this), to);
   }
   ```

2) If `gmIdentifier` is intended to serve as a shared compliance identity for global markets assets (including `onUSD`), consider using `gmIdentifier` in the `onUSDManager` mint/redeem flow as well. This would unify all compliance checks under a single identifier, reducing operational fragmentation.


**Ondo:** Acknowledged. The `OndoCompliance` check in the `USDonManager` only exists due to the `USDonManager` inheriting the `BaseRWAManager` - since the check already exists in `USDon` transfers themselves it would be completely redundant if used. Knowing this, we will leave the sanctions and blocklist unset for `USDon` in `OndoCompliance` so that the checks coming from the `USDonManager` are effectively bypassed, and we instead rely on checks stemming from `USDon` transfers themselves and keyed on the `gmIdentifier`.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Ondo Global Markets |
| Report Date | N/A |
| Finders | Immeas, Al-Qa'qa' |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

