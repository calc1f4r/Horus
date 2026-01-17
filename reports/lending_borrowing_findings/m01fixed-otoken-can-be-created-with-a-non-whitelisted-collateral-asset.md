---
# Core Classification
protocol: Opyn Gamma Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11227
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/opyn-gamma-protocol-audit/
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
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M01][Fixed] oToken can be created with a non-whitelisted collateral asset

### Overview


This bug report is related to a product consisting of a set of assets and an option type. The product needs to be whitelisted by an admin using the `Whitelist` contract's `whitelistProduct` function. After that, a user can call the `OtokenFactory`'s `createOtoken` function with the same assets and option type. However, the collateral itself may not be approved. This is because the `whitelistProduct` function does not check if the collateral is allowed in the platform or not. As a result, the transaction will revert when the user wants to deposit some collateral in their vault. 

The solution to this bug is to validate if the assets involved in a product have been already whitelisted before allowing the creation of oTokens. This bug has been fixed in Pull Request #290 where the collateral asset is required to be whitelisted during the process of whitelisting the product.

### Original Finding Content

A product consists of a set of assets and an option type. Each product has to be whitelisted by the admin using the [`whitelistProduct` function](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Whitelist.sol#L131) from the `Whitelist` contract.


Then, a user can call the [`createOtoken` function](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/OtokenFactory.sol#L55) from the `OtokenFactory` with the same assets and option type, and because the product is whitelisted, the [requirement on line 70](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/OtokenFactory.sol#L70-L78) will succeed.


However, although the product has been whitelisted, the collateral itself may not be approved. This is because the `whitelistProduct` function does not check against the [`isWhitelistedCollateral` function](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Whitelist.sol#L100) if that collateral is allowed in the platform or not. Therefore, the first engagement with the collateral will appear on [line 613](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Controller.sol#L613) from `Controller.sol`, where the transaction will revert when the user wants to deposit some collateral in their vault.


Consider validating if the assets involved in a product have been already whitelisted before allowing the creation of oTokens.


**Update:** *Fixed in [PR#290](https://github.com/opynfinance/GammaProtocol/pull/290) where the collateral asset is required to be whitelisted during the process of whitelisting the product.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Opyn Gamma Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/opyn-gamma-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

