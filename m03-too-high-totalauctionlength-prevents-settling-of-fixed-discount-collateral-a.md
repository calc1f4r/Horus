---
# Core Classification
protocol: GEB Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11201
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/geb-protocol-audit/
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

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - launchpad
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M03] Too high totalAuctionLength prevents settling of fixed-discount collateral auctions

### Overview


This bug report is about the variable `totalAuctionLength` in the `FixedDiscountCollateralAuctionHouse` code. This variable is used to determine the deadline of an auction and was initially set to 10 years. However, this long time frame is not suitable for fixed-discount auctions, as they can be completed in one single transaction and thus don't need such a long deadline. The `settleAuction` function was also performing the same operations as the `buyCollateral` function. The Reflexer Labs team has since fixed this bug by removing the `totalAuctionLength` and `auctionDeadline` functionality for fixed-discount auctions in the commit `c582fb57c746e36ed6f43ca80a7816e751c0ae2d`.

### Original Finding Content

Within [`FixedDiscountCollateralAuctionHouse`](https://github.com/reflexer-labs/geb/blob/261407b6b332c2063e4256aa5f9b223d52dad7e1/src/CollateralAuctionHouse.sol#L352), the variable [`totalAuctionLength` is initialized with a value of 10 years](https://github.com/reflexer-labs/geb/blob/261407b6b332c2063e4256aa5f9b223d52dad7e1/src/CollateralAuctionHouse.sol#L408). This value is used at the start of an auction [to determine the auction’s deadline](https://github.com/reflexer-labs/geb/blob/261407b6b332c2063e4256aa5f9b223d52dad7e1/src/CollateralAuctionHouse.sol#L687).


We understand that `totalAuctionLength` does not have the same meaning in fixed-discount auctions as it has in the english auction, since a fixed-discount auction can be completed using flash loans in one single transaction, thereby speeding up the duration of the auction. Having a deadline far in the future [prevents a fixed-discount auction from settling](https://github.com/reflexer-labs/geb/blob/261407b6b332c2063e4256aa5f9b223d52dad7e1/src/CollateralAuctionHouse.sol#L853).


Moreover, the [`settleAuction`](https://github.com/reflexer-labs/geb/blob/261407b6b332c2063e4256aa5f9b223d52dad7e1/src/CollateralAuctionHouse.sol#L850) function is performing the same operations as [lines 839-843 of the `buyCollateral`](https://github.com/reflexer-labs/geb/blob/261407b6b332c2063e4256aa5f9b223d52dad7e1/src/CollateralAuctionHouse.sol#L839-L843) function.


If the `settleAuction` function is needed in any circumstance other than when all collateral has been sold, as in the `buyCollateral` function, consider giving a proper value to `totalAuctionLength`, so it can be called in a more reasonable timeframe. Note that the `settleAuction` function is declared as `external` and can be called by anyone when `now` is greater than the deadline.


***Update:** Fixed in [commit `c582fb57c746e36ed6f43ca80a7816e751c0ae2d`](https://github.com/reflexer-labs/geb/commit/c582fb57c746e36ed6f43ca80a7816e751c0ae2d). The Reflexer Labs team has removed functionality from the `settleAuction` function within `FixedDiscountCollateralAuction` and made `totalAuctionLength` and `auctionDeadline` obsolete for fixed discount auctions.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | GEB Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/geb-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

