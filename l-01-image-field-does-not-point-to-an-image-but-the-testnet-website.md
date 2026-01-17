---
# Core Classification
protocol: Open Dollar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29364
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-opendollar
source_link: https://code4rena.com/reports/2023-10-opendollar
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

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-01] Image field does not point to an image but the testnet website

### Overview

See description below for full details.

### Original Finding Content


There is 1 instance of this issue:

In the below string variable contractMetaData, we can observe the image field points as such `"image": "https://app.opendollar.com/collectionImage.png"`. If we follow the link it leads us to the testnet website and not an image.
```solidity
File: Vault721.sol
22:   string public contractMetaData =
23:     '{"name": "Open Dollar Vaults","description": "Tradable Vaults for the Open Dollar stablecoin protocol. Caution! Trading this NFT means trading the ownership of your Vault in the Open Dollar protocol and all of the assets/collateral inside each Vault.","image": "https://app.opendollar.com/collectionImage.png","external_link": "https://opendollar.com"}';
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Open Dollar |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-opendollar
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2023-10-opendollar

### Keywords for Search

`vulnerability`

