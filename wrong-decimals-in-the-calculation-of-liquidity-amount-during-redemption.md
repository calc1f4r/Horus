---
# Core Classification
protocol: Securitize Redemptions
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64224
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
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
  - Hans
---

## Vulnerability Title

Wrong decimals in the calculation of liquidity amount during redemption

### Overview


The contract `SecuritizeRedemption` contains a function called `redeem()` that allows investors to redeem their assets for a stable coin. However, there is a bug in the code where the amount of stable coin being transferred is incorrect. This can result in a significant financial loss for the protocol. The recommended solution is to change the calculation of the liquidity amount. The bug has been fixed by the company Securitize and verified by Cyfrin.

### Original Finding Content

**Description:** The contract `SecuritizeRedemption` provides a public function `redeem()` so that investors can redeem their asset (DS Token) for liquidity token. (Stable Coin)
The parameter `_amount` represents the amount of asset to be redeemed and it is in decimals of the asset token.
The function utilizes the rate provided by the `navProvider` and the rate is in decimals of the stable coin.
```solidity
SecuritizeRedemption.sol
77:     function redeem(uint256 _amount) whenNotPaused external override {
78:         uint256 rate = navProvider.rate();
79:         require(rate != 0, "Rate should be defined");
80:         require(asset.balanceOf(msg.sender) >= _amount, "Redeemer has not enough balance");
81:         require(address(liquidityProvider) != address(0), "Liquidity provider should be defined");
82:         require(liquidityProvider.availableLiquidity() >= _amount, "Not enough liquidity");
83:
84:         ERC20 stableCoin = ERC20(address(liquidityProvider.liquidityToken()));
85:         uint256 liquidity = _amount * rate / (10 ** stableCoin.decimals());
86:
87:         liquidityProvider.supplyTo(msg.sender, liquidity);
88:         asset.transferFrom(msg.sender, liquidityProvider.recipient(), _amount);
89:
90:         emit RedemptionCompleted(msg.sender, _amount, liquidity, rate);
91:     }
```
Looking at the L85 where the returning liquidity amount is calculated, we can see that the `liquidity` will be in the decimals of asset token  which can be different from the decimals of liquidity token (stable coin).
We can verify that the `liquidity` value here must be in the decimals of stable coin because `CollateralLiquidityProvider::supplyTo()` function transfers `liquidityToken` using the provided amount as is.
Assuming a realistic scenario, where the `liquidityToken=USDC` with 6 decimals and `asset` is a standard ERC20 with 18 decimals, this vulnerability will transfer 1e12 times of the actually required value to the redeemer.

**Impact:** We evaluate the impact to be CRITICAL because the vulnerability can cause a severe financial loss to the protocol in a realistic scenario.

**Recommended Mitigation:**
```diff
-         uint256 liquidity = _amount * rate / (10 ** stableCoin.decimals());
+         uint256 liquidity = _amount * rate / (10 ** asset.decimals());
```

**Securitize:** Fixed in commit [3977ca](https://bitbucket.org/securitize_dev/bc-redemption-sc/commits/3977ca8ffb259a01e8dab894745751cf2150abf4)

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Redemptions |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

