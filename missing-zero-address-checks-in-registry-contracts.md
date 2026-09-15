---
# Core Classification
protocol: Brahma
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18826
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-15-Brahma.md
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
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

Missing zero-address checks in Registry contracts

### Overview

See description below for full details.

### Original Finding Content

The AddressProviderService inherited by the registry contracts copies the registry values internally in the constructor.
```solidity
    constructor(address _addressProvider) {
        if (_addressProvider == address(0)) revert InvalidAddressProvider();
            addressProvider = AddressProvider(_addressProvider); strategyRegistry = addressProvider.strategyRegistry(); subscriptionRegistry = addressProvider.subscriptionRegistry(); subAccountRegistry = addressProvider.subAccountRegistry(); walletAdapterRegistry = addressProvider.walletAdapterRegistry(); walletRegistry = addressProvider.walletRegistry();
    }
```


If one of the registries is not initialized, the constructor will exit gracefully. It is worth adding this validation which will only occur per construction and not cost much gas.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Brahma |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-15-Brahma.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

