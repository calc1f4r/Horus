---
# Core Classification
protocol: Telcoin Association
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52894
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/b80e13dc-e186-4baa-b911-1d92292c2566
source_link: https://cdn.cantina.xyz/reports/cantina_tao_march2025.pdf
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
finders_count: 2
finders:
  - Philogy
  - phaze
---

## Vulnerability Title

Missing validation of token address when setting TAN issuance plugin 

### Overview

See description below for full details.

### Original Finding Content

## TANIssuanceHistory Contract Issue Report

## Context
TANIssuanceHistory.sol#L140

## Description
In the `TANIssuanceHistory` contract, the `setTanIssuancePlugin()` function allows the owner to set a new issuance plugin. However, it does not verify that the new plugin's TEL token address matches the current TEL token address. This could lead to inconsistencies if a plugin with a different token address is set.

The current implementation only checks that the new plugin address is not the zero address and that it contains code, but does not validate the compatibility of the token addresses:

```solidity
function setTanIssuancePlugin(ISimplePlugin newPlugin) external onlyOwner {
    if (address(newPlugin) == address(0x0) || address(newPlugin).code.length == 0) {
        revert InvalidAddress(address(newPlugin));
    }
    tanIssuancePlugin = newPlugin;
}
```

## Recommendation
Add a validation check to ensure that the new plugin's TEL token address matches the current TEL token address:

```solidity
error IncompatiblePlugin();

function setTanIssuancePlugin(ISimplePlugin newPlugin) external onlyOwner {
    // Original checks
    if (address(newPlugin) == address(0x0) || address(newPlugin).code.length == 0) {
        revert InvalidAddress(address(newPlugin));
    }
    
    // Ensure the new plugin uses the same TEL token
    if (newPlugin.tel() != tel) {
        revert IncompatiblePlugin();
    }
    
    tanIssuancePlugin = newPlugin;
}
```

This additional check provides a defensive measure against configuration errors that could lead to operational issues and removes the need to check for the zero address or an address without code.

## Status
- **Telcoin:** Fixed in commit d970896.
- **Cantina Managed:** Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Telcoin Association |
| Report Date | N/A |
| Finders | Philogy, phaze |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_tao_march2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/b80e13dc-e186-4baa-b911-1d92292c2566

### Keywords for Search

`vulnerability`

