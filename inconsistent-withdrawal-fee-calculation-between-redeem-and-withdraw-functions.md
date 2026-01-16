---
# Core Classification
protocol: Usual
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46639
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/98727af1-95b1-4446-b39f-465d8ac83f01
source_link: https://cdn.cantina.xyz/reports/cantina_usual_phase2_october2024.pdf
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
finders_count: 3
finders:
  - Chinmay Farkya
  - deadrosesxyz
  - phaze
---

## Vulnerability Title

Inconsistent withdrawal fee calculation between redeem and withdraw functions 

### Overview


The UsualX contract has a bug that allows users to withdraw more assets than intended, resulting in a lower withdrawal fee. This is due to a discrepancy in the calculation of the withdrawal fee between the redeem() and withdraw() functions. The correct formula should be shares = convertToShares(assets / (1 - feeRate)), but the previewRedeem() and previewWithdraw() functions use different approaches. This bug can be exploited by users to pay less in withdrawal fees, potentially causing a loss of revenue for the protocol. The likelihood of this issue occurring is high and it affects both sophisticated users and regular users. A proof of concept has been provided to demonstrate the bug. The recommendation is to update the previewWithdraw() function to calculate the fee consistently with the redeem() function. This bug has been fixed in the latest commit.

### Original Finding Content

## UsualX Contract Withdrawal Fee Inconsistency

## Context
`UsualX.sol#L536-L545`

## Description
The UsualX contract implements withdrawal fees inconsistently between the `redeem()` and `withdraw()` functions. This discrepancy allows users to extract more assets than intended when using the `withdraw()` function repeatedly, effectively reducing the withdrawal fee.

The `previewRedeem()` and `previewWithdraw()` functions, which are used by `redeem()` and `withdraw()` respectively, calculate the withdrawal fee using different approaches:
1. `previewRedeem()` calculates assets as:
   ```
   assets = convertToAssets(shares) * (1 - feeRate)
   ```
   
2. `previewWithdraw()` calculates shares as:
   ```
   shares = convertToShares(assets * (1 + feeRate))
   ```

However, the correct approach should be:
```
shares = convertToShares(assets / (1 - feeRate))
```

This inconsistency leads to:
- `redeem()` correctly deducting a 5% fee (for a 5% fee rate).
- `withdraw()` allowing users to initially withdraw 95% of assets but leaving a small amount of shares that can be further withdrawn.

By repeatedly calling `withdraw()`, users can extract more assets than intended, resulting in an effective fee of approximately 4.762% instead of the intended 5%. The corrected formula's derivation can be seen as follows:
```
assets = convertToAssets(shares) · 0.95
=⇒ assets / 0.95 = convertToAssets(shares)
=⇒ convertToShares(assets / 0.95) = shares
=⇒ convertToShares((assets + assets · 0.05) / 0.95) = shares
=⇒ convertToShares((assets + assets · 0.05) / (1 - 0.05)) = shares
```

## Impact
The impact is moderate. Users can exploit this discrepancy to pay less in withdrawal fees than intended, potentially leading to a loss of revenue for the protocol or other stakeholders who were meant to benefit from these fees.

## Likelihood
The likelihood of this issue occurring is high. While deliberate exploitation by sophisticated users or automated systems is possible, especially for large withdrawals, this discrepancy will also affect regular users unknowingly. Any user who chooses to withdraw using the `withdraw()` function instead of `redeem()` will inadvertently benefit from the lower effective fee rate, regardless of their awareness of the underlying issue.

## Proof of Concept
```solidity
function test_poc_withdraw_redeem_fee_equivalence() public {
    uint256 fee = 5_00; // 5%
    vm.prank(admin);
    registryAccess.grantRole(WITHDRAW_FEE_UPDATER_ROLE, address(this));
    usualX.updateWithdrawFee(fee);
    uint256 depositAmount = 100e18;
    vm.startPrank(alice);
    ERC20Mock(usual).mint(alice, depositAmount);
    ERC20Mock(usual).approve(address(usualX), depositAmount);
    usualX.deposit(depositAmount, alice);
    uint256 snap = vm.snapshot();

    // Scenario 1: Alice redeems all her shares using `redeem()`
    uint256 redeemShares = usualX.maxRedeem(alice);
    uint256 redeemAssets = usualX.redeem(redeemShares, alice, alice);
    assertEq(usualX.balanceOf(alice), 0);
    assertEq(ERC20(usual).balanceOf(alice), 95e18); // 5% fee

    // Scenario 2: Alice redeems all her shares using `withdraw()`
    vm.revertTo(snap);
    uint256 withdrawAssets = usualX.maxWithdraw(alice);
    uint256 withdrawShares = usualX.withdraw(withdrawAssets, alice, alice);
    assertEq(ERC20(usual).balanceOf(alice), 95e18); // 5% fee
    assertGt(usualX.balanceOf(alice), 0);

    // Alice can further withdraw assets beyond her limit
    for (uint256 i; i < 100; i++) {
        withdrawAssets = usualX.maxWithdraw(alice);
        withdrawShares = usualX.withdraw(withdrawAssets, alice, alice);
    }
    assertApproxEqRel(ERC20(usual).balanceOf(alice), 95.238e18, 0.0001e18); // ~4.762% effective fee
}
```

## Recommendation
Update the `previewWithdraw()` function to correctly calculate the number of shares required for a given asset amount:
```solidity
function previewWithdraw(uint256 assets) public view override returns (uint256 shares) {
    UsualXStorageV0 storage $ = _usualXStorageV0();
    
    // Calculate the total assets needed, including the fee
    // uint256 fee = Math.mulDiv(assets, $.withdrawFeeBps, BASIS_POINT_BASE, Math.Rounding.Floor);
    
    // Calculate the fee based on the equivalent assets of these shares
    uint256 fee = Math.mulDiv(assets, $.withdrawFeeBps, BASIS_POINT_BASE - $.withdrawFeeBps, Math.Rounding.Ceil);
    
    // Calculate total assets needed, including fee
    uint256 assetsWithFee = assets + fee;
    
    // Calculate total shares needed, including fee
    shares = convertToShares(assetsWithFee);
}
```

This change ensures that the withdrawal fee is calculated consistently across both `redeem()` and `withdraw()` functions, preventing users from exploiting the discrepancy to pay lower fees.

## Usual
Fixed in commit `4f62ce6d`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Usual |
| Report Date | N/A |
| Finders | Chinmay Farkya, deadrosesxyz, phaze |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_usual_phase2_october2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/98727af1-95b1-4446-b39f-465d8ac83f01

### Keywords for Search

`vulnerability`

