---
# Core Classification
protocol: Biconomy Nexus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43817
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
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
finders_count: 7
finders:
  - Blockdev
  - Devtooligan
  - Chinmay Farkya
  - Christoph Michel
  - Víctor Martínez
---

## Vulnerability Title

Setting the ERC-7484 registry may put modules in a insecure state

### Overview


This bug report discusses an issue with the ERC-7484 registry settings. When the registry is configured, certain modules may become inactive or disabled. This can happen if the settings are changed, such as updating the list of attester addresses or changing the threshold. The report recommends checking the registry for each module when updating the configuration settings. The report also mentions that this may involve tracking the list of fallback handlers. Both Biconomy and Spearbit have acknowledged the issue.

### Original Finding Content

## Severity: Medium Risk

## Context
(No context files were provided by the reviewer)

## Description
When the settings for the ERC-7484 registry are set, insecure modules may be left inactive or executor modules may become suddenly deactivated.

The `setRegistry` function is used to configure the registry. Configurable options include updating the set of attester addresses, changing the threshold, updating the address of the registry, or disabling it altogether by setting the registry to address zero.

```solidity
function _configureRegistry(IERC7484 newRegistry, address[] calldata attesters, uint8 threshold) internal {
    registry = newRegistry;
    if (address(newRegistry) != address(0)) {
        newRegistry.trustAttesters(threshold, attesters);
    }
    emit ERC7484RegistryConfigured(newRegistry);
}
```

Any one of these options may affect currently installed modules. For example, an executor may not meet the new threshold that was set and would instantly be disabled. Or worse, a validator may not have the required number of attestations and would continue to be active.

## Recommendation
When updating the configuration settings, if the registry address is not set to zero, then iterate through each module and perform the registry check.

```solidity
function _configureRegistry(IERC7484 newRegistry, address[] calldata attesters, uint8 threshold) internal {
    registry = newRegistry;
    if (address(newRegistry) != address(0)) {
        newRegistry.trustAttesters(threshold, attesters);
        AccountStorage storage ams = _getAccountStorage();

        // (iterate over validators calling _checkRegistry() for each
        // (repeat for executors)
        // (repeat for fallback handlers)

        _checkRegistry(ams.hook, 4);
    }
    // emit ERC7484RegistryConfigured(newRegistry); // Note this would also involve tracking the list of fallback handlers.
}
```

Biconomy: Acknowledged.  
Spearbit: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Biconomy Nexus |
| Report Date | N/A |
| Finders | Blockdev, Devtooligan, Chinmay Farkya, Christoph Michel, Víctor Martínez, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf

### Keywords for Search

`vulnerability`

