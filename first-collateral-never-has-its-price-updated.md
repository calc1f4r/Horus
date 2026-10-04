---
# Core Classification
protocol: Ethereum Reserve Dollar (ERD)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60117
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
source_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
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
finders_count: 3
finders:
  - Ibrahim Abouzied
  - Rabib Islam
  - Hytham Farah
---

## Vulnerability Title

First Collateral Never Has Its Price Updated

### Overview


The bug report is about a problem in the code for a program called CollateralManager. The client has noticed that when the program updates the price of a type of currency called ETH, it doesn't always update correctly. This is because the program starts counting from the second type of currency instead of the first. If the first type of currency is not ETH, its price will never be updated. The recommendation is to fix the code so that it updates the price of all currencies, and to make sure that the first currency is always ETH.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> ETH is the first supported collateral, and the price of ETH will be updated first before calling priceUpdated().

**File(s) affected:**`CollateralManager.sol`

**Description:**`CollateralManager.priceUpdate()` iterates through the supported collaterals and fetches an updated price from their oracles. However, the for loop starts iterating from index `1`. Nothing in `addCollateral()` prevents any particular collateral type from occupying index `0`. Such a collateral would never have its price updated.

**Recommendation:** Update `priceUpdate()` to iterate through all collaterals. If the first entry is intended to be WETH, enforce this during initialization or in `addCollateral()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ethereum Reserve Dollar (ERD) |
| Report Date | N/A |
| Finders | Ibrahim Abouzied, Rabib Islam, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html

### Keywords for Search

`vulnerability`

