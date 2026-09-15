---
# Core Classification
protocol: Simple Token Sale Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11959
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/simple-token-sale-audit-30e5f2365463/
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
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Missing validation of the TOKEN_SALE constant

### Overview

See description below for full details.

### Original Finding Content

In the [`TokenSale`](https://github.com/OpenSTFoundation/SimpleTokenSale/blob/1a1e863441ba0149d7585203f5dbc6e800af00cf/contracts/TokenSale.sol#L128) contract, there is validation for most of the configuration constants which is a very good practice. The validation skips checking the correctness of`TOKENS_SALE` parameter which can allow creation of a contract that is unable to sell any tokens at all.


We recommend adding the missing validation to the `TokenSale` constructor.


**Update**: *The Simple Token team indicated that, `TOKENS_SALE` is effectively validated by (1) the constructor confirming that all of the token values add up to `TOKENS_MAX` and (2) `TokenSale.initialize` confirming that the balance of `TokenSale` is equal to `TOKENS_SALE`. It is true that if `TOKEN_SALE` were set to `0`in `TokenSaleConfig` (and other values adjusted) and if we either transfer `0 ST`to `TokenSale` or do not transfer anything at all, those validations would pass. However, the team thinks they must surely be allowed to assume that their config contract is correct.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Simple Token Sale Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/simple-token-sale-audit-30e5f2365463/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

