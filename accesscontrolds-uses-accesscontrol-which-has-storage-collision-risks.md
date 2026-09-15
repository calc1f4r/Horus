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
solodit_id: 43785
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

AccessControlDS uses AccessControl, which has storage collision risks

### Overview


This bug report discusses a high difficulty issue related to data validation in the AccessControlDS contract. The contract inherits from OpenZeppelin's AccessControl contract, which can lead to storage collisions when used in upgradeable contracts. This means that when a new facet is added to a diamond proxy that already uses AccessControlDS, there is a risk of undefined behavior due to conflicting storage variables. The report recommends short-term solutions such as using AccessControlUpgradeable instead of AccessControl, and long-term solutions like using Slither to detect storage collision risks in upgradeable contracts. 

### Original Finding Content

## Diﬃculty: High

## Type: Data Validation

### Description
The `AccessControlDS` contract inherits from OpenZeppelin’s `AccessControl` contract, creating a risk of storage collisions due to `AccessControlDS`’s use in upgradeable contracts. The definition of `AccessControlDS` and the variable creating the collision risk are shown in figures 1.1 and 1.2.

```solidity
abstract contract AccessControlDS is AccessControl, OwnableReadonlyDS {
    function hasRole(bytes32 _role, address _account) public view virtual override
        returns (bool) {
            return (isOwnerRole(_role) && _owner() == _account) || super.hasRole(_role, _account);
    }
}
```

**Figure 1.1:** The facet contract `AccessControlDS` inherits from OpenZeppelin’s `AccessControl` contract. (contracts/base/auth/AccessControlDS.sol#7–10)

```solidity
abstract contract AccessControl is Context, IAccessControl, ERC165 {
    struct RoleData {
        mapping(address account => bool) hasRole;
        bytes32 adminRole;
    }
    mapping(bytes32 role => RoleData) private _roles;
}
```

**Figure 1.2:** The OpenZeppelin `AccessControl` contract is not upgrade-aware and stores role information in the first slot. (openzeppelin-contracts/contracts/access/AccessControl.sol#49–55)

### Exploit Scenario
A new facet is added to a diamond proxy that already implements a facet using `AccessControlDS`. This new facet stores a variable in slot 0 (or inherits from a contract that stores a variable in slot 0), so these two storage variables collide, causing undefined behavior.

### Recommendations
- **Short Term:** Replace `AccessControl` with `AccessControlUpgradeable`. This contract is upgrade-aware and uses EIP-7201 to store role information at non-colliding storage slots.
- **Long Term:** Use Slither to detect storage collision risks in upgradeable contracts. The `slither --print variable-order` command can be used manually or in a CI pipeline to detect when upgradeable contracts store variables in contentious slots, as shown in figure 1.3.

**Figure 1.3:** Slither can be used to quickly identify problematic storage slot usage in upgradeable or diamond facet contracts.

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

