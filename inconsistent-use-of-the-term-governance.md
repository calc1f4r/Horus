---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17884
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

Inconsistent use of the term “governance”

### Overview

See description below for full details.

### Original Finding Content

## Data Validation

**Type:** Data Validation  
**Target:** contracts/*

**Difficulty:** High

## Description

`FRAXStablecoin` contains the modifiers `onlyByOwnerOrGovernance` and `onlyByOwnerGovernanceOrPool`, which use the word “governance” in different ways. In the former, it refers to the `timelock_address` or `controller_address`, and in the latter, it refers only to the `timelock_address`. This inconsistency may cause the introduction of errors during development.

```solidity
modifier onlyByOwnerOrGovernance() {
    require(msg.sender == owner_address || msg.sender == timelock_address || msg.sender == controller_address, "You are not the owner, controller, or the governance timelock");
    _;
}

modifier onlyByOwnerGovernanceOrPool() {
    require(
        msg.sender == owner_address
        || msg.sender == timelock_address
        || frax_pools[msg.sender] == true,
        "You are not the owner, the governance timelock, or a pool"
    );
    _;
}
```

**Figure 4.1:** contracts/Frax/Frax.sol#L92-L104

## Exploit Scenario

Developer Bob adds the modifier `onlyByOwnerOrGovernance`, thinking it is callable only by the `owner_address` and `timelock_address`. However, it is also callable by the `controller_address`, meaning that this party can unexpectedly execute privileged operations.

## Recommendations

**Short term:** Either rename the modifiers or standardize the rights that they grant.  
**Long term:** To prevent developers and users from making incorrect assumptions, use terms consistently within the components or throughout the system.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels, Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf

### Keywords for Search

`vulnerability`

