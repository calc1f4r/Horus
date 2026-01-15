---
# Core Classification
protocol: Zaros
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37978
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clyg8slke0001bvhpwszwjr7z
source_link: none
github_link: https://github.com/Cyfrin/2024-07-zaros

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
finders_count: 14
finders:
  - samuraii77
  - 0xShoonya
  - Aamirusmani1552
  - Draiakoo
  - S3v3ru5
---

## Vulnerability Title

Liquidation of accounts collateral not posible because some chainlink price feed doesn't exist or are marked as medium risk by chainlink

### Overview

See description below for full details.

### Original Finding Content

## Liquidation of accounts collateral not posible because some chainlink price feed doesn't exist or are marked as medium risk by chainlink

## Summary

Some price feeds doesn't exist or are marked as "medium risk" by chainlink.

## Vulnerability Details

Chainlink price feed for `WeETH / USD` and `WstETH / USD`  doesn't exist in arbitrum so is not possible to liquidate an account with those collaterals. Also `WETH / USD` price feed doesn't exist in arbitrum but exists ETH/USD, however current implementation doens't allow composition of price feeds. `WBTC / USD` and ` BNB/USD` are marked as medium risk by chainlink so the liquidation is possible but with some degree of risk.

### Collateral Chainlink Price Feed Analysis

| Feed         | Chainlink feed exits | Observation                          | Details                                                                             |
| ------------ | -------------------- | ------------------------------------ | ----------------------------------------------------------------------------------- |
| USDC / USD   | Y                    | green - low risk                     | [Feed link](https://arbiscan.io/address/0x50834F3163758fcC1Df9973b6e91f0F0F0434aD3) |
| WBTC / USD   | Y                    | yellow - medium risk                 | [Feed Link](https://arbiscan.io/address/0xd0C7101eACbB49F3deCcCc166d238410D6D46d57) |
| WeETH / USD  | N                    | -                                    | -                                                                                   |
| WETH / USD   | N                    | Exist ETH/USD not the same but close | [Feed Link](https://arbiscan.io/address/0x639Fe6ab55C921f74e7fac1ee960C0B6293ba612) |
| WstETH / USD | N                    | -                                    | -                                                                                   |
| USDZ  / USD  | N                    | Is the protocol token so no problem  | -                                                                                   |

### Markets Chainlink Price Feed Analysis

| Feed      | Chainlink feed exits | Observation          | Details                                                                             |
| --------- | -------------------- | -------------------- | ----------------------------------------------------------------------------------- |
| ARB/USD   | Y                    | green - low risk     | [Feed Link](https://arbiscan.io/address/0xb2A824043730FE05F3DA2efaFa1CBbe83fa548D6) |
| BNB/USD   | Y                    | yellow - medium risk | [Feed Link](https://arbiscan.io/address/0x6970460aabF80C5BE983C6b74e5D06dEDCA95D4A) |
| BTC/USD   | Y                    | green -low risk      | [Feed Link](https://arbiscan.io/address/0x6ce185860a4963106506C203335A2910413708e9) |
| DOGE/USD  | Y                    | green - low risk     | [Feed Link](https://arbiscan.io/address/0x9A7FB1b3950837a8D9b40517626E11D4127C098C) |
| ETH/USD   | Y                    | green - low risk     | [Feed Link](https://arbiscan.io/address/0x639Fe6ab55C921f74e7fac1ee960C0B6293ba612) |
| FTM/USD   | Y                    | green - low risk     | [Feed Link](https://arbiscan.io/address/0xFeaC1A3936514746e70170c0f539e70b23d36F19) |
| LINK/USD  | Y                    | green - low risk     | [Feed Link](https://arbiscan.io/address/0x86E53CF1B870786351Da77A57575e79CB55812CB) |
| LTC/USD   | Y                    | gren - low risk      | [Feed link](https://arbiscan.io/address/0x5698690a7B7B84F6aa985ef7690A8A7288FBc9c8) |
| MATIC/USD | Y                    | green - low risk     | [Feed Link](https://arbiscan.io/address/0x52099D4523531f678Dfc568a7B1e5038aadcE1d6) |
| SOL/USD   | Y                    | green - low risk     | [Feed link](https://arbiscan.io/address/0x24ceA4b8ce57cdA5058b924B9B9987992450590c) |

## Impact

* Liquidation regarding Accounts: Can't liquidate if there is no Chainlink price feed for a collateral, for example WeETH/USD. Also WBTC/USD is marked as medium risk by chainlink.
* Liquidation regarding Markets: Liquidation is possible but the price feed BNB/USD is marked as "Medium Risk" by chainlink.

## Tools Used

* VS Code
* [Chainlink trusted price feed site](https://docs.chain.link/data-feeds/price-feeds/addresses?network=arbitrum\&page=1)
* [Selecting quality of feed](https://docs.chain.link/data-feeds/selecting-data-feeds)



## Recommendations

Protocol Will need to deploy and maintain custom price feeds that are missing or not trusted.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Zaros |
| Report Date | N/A |
| Finders | samuraii77, 0xShoonya, Aamirusmani1552, Draiakoo, S3v3ru5, Auditism, Spearmint, krisp, 0xAbhayy, Slavcheww, ilchovski, nfmelendez, 0xaman |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-07-zaros
- **Contest**: https://codehawks.cyfrin.io/c/clyg8slke0001bvhpwszwjr7z

### Keywords for Search

`vulnerability`

