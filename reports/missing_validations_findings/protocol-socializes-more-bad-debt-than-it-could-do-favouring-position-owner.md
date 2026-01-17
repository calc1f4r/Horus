---
# Core Classification
protocol: Euler
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54143
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55
source_link: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
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
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - T1MOH
---

## Vulnerability Title

Protocol socializes more bad debt than it could do favouring position owner 

### Overview

See description below for full details.

### Original Finding Content

## Liquidation Module Overview

## Context
`Liquidation.sol#L215-L216`

## Description
The Liquidation module socializes bad debt when an account does not have any liquidatable collateral. It decreases the `totalBorrows` by the remaining account's debt. By design, all the depositors share this loss because `totalBorrows` and, hence, `totalAssets` are decreased.

### Function
```solidity
function executeLiquidation(VaultCache memory vaultCache, LiquidationCache memory liqCache, uint256 minYieldBalance) private {
    // ...
    // Handle debt socialization
    if (
        vaultCache.configFlags.isNotSet(CFG_DONT_SOCIALIZE_DEBT) && 
        liqCache.liability > liqCache.repay &&
        checkNoCollateral(liqCache.violator, liqCache.collaterals) // <<<
    ) {
        Assets owedRemaining = liqCache.liability.subUnchecked(liqCache.repay);
        decreaseBorrow(vaultCache, liqCache.violator, owedRemaining); // <<<

        // decreaseBorrow emits Repay without any assets entering the vault. Emit Withdraw from and to zero
        // address, to cover the missing amount for offchain trackers.
        emit Withdraw(liqCache.liquidator, address(0), address(0), owedRemaining.toUint(), 0);
        emit DebtSocialized(liqCache.violator, owedRemaining.toUint());
    }
    // ...
}
```

However, it does not take into consideration the liquidatee's balance during liquidation. This is an issue because the protocol assumes it is `0` and does not reduce it. Suppose the following scenario:

1. User has: 
   - collateral = 100
   - LTV = 0.8
   - borrowed = 120
   - shares = 40. For simplicity, assume shares == assets.
   
2. Position is liquidatable because \(100 \times 0.8 < 120\), therefore the user cannot move his shares - at the end of every transfer, a status check is executed.

3. Liquidation is executed. 
   - discountFactor = \(\frac{100 \times 0.8}{120} = 0.66\), 
   - so the liquidator receives 100 collateral and repays debt = \(100 \times 0.66 = 66\).

4. As a result, debt \(= 120 - 66 = 54\) will be socialized.

5. The issue is that it must first reduce bad debt by the user’s balance shares = 40, and socialize only \(54 - 40 = 14\) debt between depositors.

## Recommendation
Convert the user's balance of Controller shares to assets and deduct it from bad debt at the end of liquidation, and socialize bad debt only if it remains after such a deduction.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Euler |
| Report Date | N/A |
| Finders | T1MOH |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55

### Keywords for Search

`vulnerability`

