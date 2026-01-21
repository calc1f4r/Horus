---
# Core Classification
protocol: Thala Bazaar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47420
audit_firm: OtterSec
contest_link: https://github.com/bazaar-Labs/Bazaar-contracts
source_link: https://github.com/bazaar-Labs/Bazaar-contracts
github_link: https://github.com/bazaar-Labs/Bazaar-contracts

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
finders_count: 3
finders:
  - Robert Chen
  - Matteo Oliva
  - Nicholas R.Putra
---

## Vulnerability Title

LBP Fee Drainage

### Overview


The exitLBP function in the BazaarLBP contract does not reset the _swapFeeAmounts array after a successful exit. This array keeps track of the total swap fees accrued for each token in the LBP. If an LBP owner exits the pool using exitLBP, the liquidity will be withdrawn and the underlying assets will be distributed along with fees as intended. However, the _swapFeeAmounts array in BazaarLBP remains unchanged with the accumulated fees. As a result, it will be possible to transfer the LBP token (BPT) to the factory contract address after the LBP owner exits. This means that the recipient can redeem the swap fees multiple times, resulting in the loss of fees collected by the protocol. To fix this issue, the exitLBP function should be modified to reset the _swapFeeAmounts array within BazaarLBP after a successful exit. This bug has been resolved in issue #56.

### Original Finding Content

## ExitLBP Functionality Overview

The `exitLBP` function does not reset the `_swapFeeAmounts` arrays stored within `BazaarLBP` after a successful exit. This array keeps track of the total swap fees accrued for each token within the LBP. If an LBP owner exits the pool via `exitLBP`, the liquidity will be withdrawn, and the underlying assets will be distributed along with fees as intended. However, the `_swapFeeAmounts` array in `BazaarLBP` remains unchanged with the accumulated fees. As a result, it will be possible to transfer the LBP token (BPT) to the factory contract address after the LBP owner exits.

## Code Example

```solidity
// BazaarLBPFactory.sol solidity
function exitLBP(BazaarLBP lbp, address recipient, uint256[] memory minAmountsOut) external onlyLBPOwner(lbp) {
    // Exit from the pool. Receipt is this proxy so that we can extract fees.
    bytes memory userData = abi.encode(1, bptBal); // EXACT_BPT_IN_FOR_TOKENS_OUT ExitKind
    vault.exitPool(lbp.getPoolId(), address(this), payable(address(this)),
        IVault.ExitPoolRequest(assets, minAmountsOut, userData, false));
}
```

Thus, if `exitLBP` is called again with the transferred BPTs, it would attempt to exit again. Since the `_swapFeeAmounts` arrays still hold the previously accumulated fees, these fees would be distributed again, even though there is no actual liquidity withdrawal happening. This essentially allows the recipient to redeem the swap fees multiple times, resulting in the loss of swap fees collected by the protocol.

## Remediation

Modify `exitLBP` to reset the `_swapFeeAmounts` array within `BazaarLBP` after a successful exit.

## Patch

Resolved in #56.

© 2024 Otter Audits LLC. All Rights Reserved. 5/14

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Thala Bazaar |
| Report Date | N/A |
| Finders | Robert Chen, Matteo Oliva, Nicholas R.Putra |

### Source Links

- **Source**: https://github.com/bazaar-Labs/Bazaar-contracts
- **GitHub**: https://github.com/bazaar-Labs/Bazaar-contracts
- **Contest**: https://github.com/bazaar-Labs/Bazaar-contracts

### Keywords for Search

`vulnerability`

