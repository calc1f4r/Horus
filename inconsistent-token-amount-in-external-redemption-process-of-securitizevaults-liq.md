---
# Core Classification
protocol: Securitize Redeem Swap Vault Na
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64247
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
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
  - Hans
---

## Vulnerability Title

Inconsistent token amount in external redemption process of SecuritizeVault's liquidate function

### Overview


The report describes a bug in the liquidation process of SecuritizeVault, where there is a mismatch between the calculated amount and the actual amount of stable coins received from the redemption contract. This can result in users receiving less stable coins than expected or the transaction failing due to insufficient balance. The recommended solution is to track the actual received amount and transfer it to the user. The bug has been fixed by Securitize and verified by Cyfrin.

### Original Finding Content

**Description:** In SecuritizeVault's liquidation process with external redemption, there's likely a mismatch between the actual received stable coins from the redemption contract and the amount calculated to send to the liquidator. The vault calculates the output amount using `navProvider.rate()` after the external redemption, but this calculated amount may differ from the actual stable coins received due to rounding discrepancies and rate variations during the redemption process.
```solidity
SecuritizeVault.sol
261:         if (address(0) != address(redemption)) {
262:             IERC20(asset()).approve(address(redemption), assets);
263:             redemption.redeem(assets);//@audit-info this sends underlying token to the redemption, receives stablecoin into this contract
264:             uint256 rate = navProvider.rate();
265:             uint256 decimalsFactor = 10 ** decimals();
266:             // after external redemption, vault gets liquidity to supply msg.sender (assets * nav)
267:             // liquidationToken === stableCoin
268:             liquidationToken.safeTransfer(msg.sender, assets.mulDiv(rate, decimalsFactor, Math.Rounding.Floor));//@audit-issue possible inconsistency in the amoutns. consider sending the balance delta instead
269:         }

```
**Impact:** Users either receive less stable coins than they should (value loss) or the transaction reverts due to insufficient balance when the calculated amount exceeds received tokens, making the liquidation functionality unreliable.

**Recommended Mitigation:** Track actual received stable coins from redemption contract and transfer them.
```solidity
    if (address(0) != address(redemption)) {
        IERC20 liquidityToken = IERC20(redemption.liquidity());
        uint256 balanceBefore = liquidityToken.balanceOf(address(this));
        redemption.redeem(assets);
        uint256 receivedAmount = liquidityToken.balanceOf(address(this)) - balanceBefore;
        liquidityToken.transfer(msg.sender, receivedAmount);
    }
```

**Securitize:** Fixed in commit [ef761a](https://bitbucket.org/securitize_dev/bc-securitize-vault-sc/commits/ef761a654b4015478c82cecd33cc54f7a97d37bb).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Redeem Swap Vault Na |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

