---
# Core Classification
protocol: Arkis DeFi Prime Brokerage Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43789
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-12-arkis-defi-prime-brokerage-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-12-arkis-defi-prime-brokerage-securityreview.pdf
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
finders_count: 2
finders:
  - Damilola Edwards
  - Benjamin Samuels
---

## Vulnerability Title

BeaconDS can create broken margin accounts via an undeployed Account implementation

### Overview


The report describes a bug in the AccountFactory contract, which uses the BeaconDS contract to set and retrieve the Account implementation. However, the BeaconDS contract does not check for the existence of the contract when setting the implementation. This can lead to an exploit where the Account contract is updated to a new implementation, but the deployment fails and goes unnoticed. As a result, newly created accounts will be represented by a contract that calls into an address with no contract deployed, allowing all calls to succeed. The report recommends short-term and long-term solutions to address this issue. 

### Original Finding Content

## Diﬃculty: N/A

## Type: Undeﬁned Behavior

### Description
The AccountFactory contract uses the BeaconDS contract for setting/retrieving the Account implementation; however, BeaconDS does not perform contract existence checks when the Account implementation is set, as shown in Figure 5.1.

```solidity
function setImplementation(address newImplementation) external override onlyOwner {
    if (newImplementation == address(0)) revert ImplementationAddressIsZero();
    if (_implementation() == newImplementation) revert AlreadyUpToDate();
    assembly {
        sstore(IMPLEMENTATION_SLOT, newImplementation)
    }
}
```
*Figure 5.1: The setImplementation function does not check whether a contract is deployed to newImplementation. (contracts/base/proxy/BeaconDS.sol#13–20)*

### Exploit Scenario
There are plans to update the Account contract to a CREATE2-based implementation whose address can be calculated ahead of time. The transaction to deploy the Account contract fails, and the failure is not noticed. When `AccountFactory.setImplementation` is called, the contract implementation is set to an address with no contract deployed to it. At this point, newly created accounts will be represented by an `ImmutableBeaconProxy` contract that delegatecalls into an address with no contract deployed to it. All calls to an address with no contract deployed will succeed and return true.

### Recommendations
- **Short term:** Update `BeaconDS.setImplementation` to check for contract existence using `extcodesize` before accepting a new implementation.
- **Long term:** Add a code review checklist item to ensure all proxy contracts check for the presence of the target contract before accepting a new implementation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Arkis DeFi Prime Brokerage Protocol |
| Report Date | N/A |
| Finders | Damilola Edwards, Benjamin Samuels |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-12-arkis-defi-prime-brokerage-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-12-arkis-defi-prime-brokerage-securityreview.pdf

### Keywords for Search

`vulnerability`

