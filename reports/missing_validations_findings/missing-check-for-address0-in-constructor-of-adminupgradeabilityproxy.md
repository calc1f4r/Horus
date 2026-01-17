---
# Core Classification
protocol: AZTEC
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16735
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/aztec.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/aztec.pdf
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
finders_count: 6
finders:
  - James Miller
  - Ben Perez
  - Paul Kehrer
  - Alan Cao
  - Will Song
---

## Vulnerability Title

Missing check for address(0) in constructor of AdminUpgradeabilityProxy

### Overview


This bug report is about a vulnerability found in the BaseAdminUpgradeabilityProxy and AdminUpgradeabilityProxy contracts. The changeAdmin function in BaseAdminUpgradeabilityProxy performs a zero-address check before calling _setAdmin(), however, the constructor of AdminUpgradeabilityProxy calls _setAdmin() without performing a zero-address check. If the constructor for AdminUpgradeabilityProxy is called with _admin set to zero, then the contract will be un-administrable. 

The exploit scenario is that the AZTEC deployment system has an implementation error and mistakenly sets the admin address of AdminUpgradeabilityProxy to zero. A malicious internal user at AZTEC sabotages the setup procedure and uses their administrative privileges to set the admin address in AdminUpgradeabilityProxy to zero.

The recommendation to prevent this vulnerability is to always perform zero-address checks when setting up permissions. In the long term, review invariants within all components of the system and ensure these properties hold. Consider testing these properties using a property-testing tool such as Echidna.

### Original Finding Content

## Type: Cryptography  
## Target: Swap.sol  

## Difficulty: Low  

## Description  
In `BaseAdminUpgradeabilityProxy`, the `changeAdmin` function performs a zero-address check before calling `_setAdmin()`.  

![Figure 9.1: changeAdmin function in BaseAdminUpgradeabilityProxy](link_to_figure_9.1)  

However, the constructor of `AdminUpgradeabilityProxy` calls `_setAdmin()` without performing a zero-address check.  

![Figure 9.2: The constructor for AdminUpgradeabilityProxy](link_to_figure_9.2)  

If the constructor for `AdminUpgradeabilityProxy` is called with `_admin` set to zero, then the contract will be un-administrable.  

## Exploit Scenario  
The AZTEC deployment system has an implementation error and mistakenly sets the admin address of `AdminUpgradeabilityProxy` to zero. A malicious internal user at AZTEC sabotages the setup procedure and uses their administrative privileges to set the admin address in `AdminUpgradeabilityProxy` to zero.  

## Recommendation  
- **Short term**: Always perform zero-address checks when setting up permissions.  
- **Long term**: Review invariants within all components of the system and ensure these properties hold. Consider testing these properties using a property-testing tool such as Echidna.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | AZTEC |
| Report Date | N/A |
| Finders | James Miller, Ben Perez, Paul Kehrer, Alan Cao, Will Song, David Pokora |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/aztec.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/aztec.pdf

### Keywords for Search

`vulnerability`

