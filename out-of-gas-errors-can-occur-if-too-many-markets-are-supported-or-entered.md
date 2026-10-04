---
# Core Classification
protocol: Elara Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59157
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/elara-finance/ceaf2e43-2883-4f4f-bd80-20dc354abb46/index.html
source_link: https://certificate.quantstamp.com/full/elara-finance/ceaf2e43-2883-4f4f-bd80-20dc354abb46/index.html
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
  - Gereon Mendler
  - Julio Aguilar
  - Valerian Callens
---

## Vulnerability Title

Out-of-Gas Errors Can Occur if Too Many Markets Are Supported or Entered

### Overview


This bug report discusses potential issues with the Compound code related to Out-of-Gas errors. The client has decided to keep the original code despite the concerns raised in the audit report. The report mentions that the `allMarkets` list in `ComptrollerV3Storage` could cause problems if too many markets are supported, making it impossible to add new ones and causing the `claimComp()` function to fail. Additionally, the `maxAssets` value is not being used in the code, which could lead to issues with operations such as liquidations. The recommendation is to perform gas simulations to determine the maximum number of markets that should be supported and to enforce checks based on the `maxAssets` value.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> We understand and appreciate the concern raised in the audit report regarding potential Out-of-Gas errors. However, we have decided to retain the original Compound code for the following reasons:
> 
> 
> 1.   Historical Performance: Compound has not experienced such Out-of-Gas errors in practice.
> 2.   Stress Testing: We have conducted extensive stress tests on other blockchains, including interactions with over 200,000 wallet addresses, without encountering this issue.
> 3.   Practical Limitations: In our actual operations, we will strictly control the number of listed assets, limiting the maximum to 4. This significantly reduces the risk of reaching gas limits.

**File(s) affected:**`Comptroller.sol`

**Description:** The list `allMarkets` in `ComptrollerV3Storage` records all CTokens supported by the system. This list is iterated when a user wants to claim `COMP` from all its entered markets via the function `Comptroller.claimComp()`, and when a new market is added in `Comptroller._addMarketInternal()`. If too many markets are supported, it will not be possible to add a new one, and the function `claimComp()` will also start reverting because the amount of gas used is too high.

Also, the `maxAssets` value is defined in `ComptrollerV1Storage` to cap the maximum number of markets a specific address can enter as a borrower. However, this maximum cap is not used in the code. As a result, if a lot of markets are supported and the user enters all of them, it could avoid the execution of some operations such as liquidations if they consume too much gas when browsing the list of assets he borrowed (`ComptrollerV1Storage.accountAssets`).

**Recommendation:** While this could become a problem when too many markets are supported, we recommend identifying worst-case scenarios by performing gas simulations to identify what is the maximum amount of markets that should be supported by the system (`maxSup`). Same recommendation for the number of markets a user can enter (`maxEnt`). If `maxEnt < maxSup`, consider enforcing checks based on the value of `maxAssets`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Elara Finance |
| Report Date | N/A |
| Finders | Gereon Mendler, Julio Aguilar, Valerian Callens |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/elara-finance/ceaf2e43-2883-4f4f-bd80-20dc354abb46/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/elara-finance/ceaf2e43-2883-4f4f-bd80-20dc354abb46/index.html

### Keywords for Search

`vulnerability`

