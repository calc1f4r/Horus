---
# Core Classification
protocol: Moonbound
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62422
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-05-26-Moonbound.md
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
finders_count: 1
finders:
  - Hexens
---

## Vulnerability Title

[MNBD1-4] Tokens cannot graduate if an attacker transfers KAS to the BondingCurvePool contract

### Overview


This bug report is about a function called `graduateToken()` in the `BondingCurvePool.sol` contract. This function creates a new `ZealousSwapPair` between two tokens, MoonBound and KAS. The problem is that an attacker can manipulate the amount of KAS collected during the bonding curve phase, causing the function to fail. This can be exploited using a self-destruct technique. The suggested solution is to cap the amount of tokens used for liquidity if it exceeds the reserved amount. This bug has been fixed.

### Original Finding Content

**Severity:** Medium

**Path:** contracts/BondingCurvePool.sol#L247-L260 

**Description:** The `BondingCurvePool::graduateToken()` function is responsible for creating a new `ZealousSwapPair` between the MoonBound token and KAS. It does this by using the KAS collected during the bonding curve phase and a reserve of MoonBound tokens (25% of `maxSupply`):
```
function graduateToken() internal {
    ...
    // Add liquidity to DEX
    uint256 currentPrice = getPriceAtTokens(totalTokensSold);
    uint256 kasCollected = address(this).balance;

    uint256 tokenForLiquidity = (kasCollected * SCALING_FACTOR) / currentPrice;
    ...
}
```
The function calculates `kasCollected` using `address(this).balance`, and determines the number of MoonBound tokens needed for liquidity by dividing `kasCollected` by `currentPrice`.

Under normal conditions, `tokenForLiquidity` should always be less than the reserved token amount, because:

- When all curve tokens (75% of maxSupply) are sold:

    - `currentPrice` equals `graduationPriceKAS`

    - `kasCollected` is expected to be less than
```(curveTokens / 3) * graduationPriceKAS
= reservedTokens * graduationPriceKAS
```
(due to the deduction of `graduationFeeKAS`)

The issue arises when an attacker can artificially inflate `kasCollected` by forcefully transferring extra KAS to the contract. This causes `tokenForLiquidity` to exceed `reservedTokens`, which leads to a failure in the call to `IZealousSwapRouter02(zealousSwapRouter).addLiquidityKAS()` because of not enough token to transfer.

This can be exploited via a self-destruct technique, allowing the attacker to send `graduationFeeKAS + ε` KAS to the `BondingCurvePool` even though the contract lacks a `receive()` function.

**Remediation:**  If `tokenForLiquidity` exceeds `reservedTokens`, cap `tokenForLiquidity` to `reservedTokens`.
```
   uint256 tokenForLiquidity = (kasCollected * SCALING_FACTOR) / currentPrice;
++ if (tokenForLiquidity > reservedTokens) {
++    tokenForLiquidity = reservedTokens;
++ }
```

**Status:**  Fixed


- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Moonbound |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-05-26-Moonbound.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

