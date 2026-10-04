---
# Core Classification
protocol: Quadrata Lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61655
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/quadrata-lending/a3d2d9c8-6ebd-4c3e-a146-501cecf3e98c/index.html
source_link: https://certificate.quantstamp.com/full/quadrata-lending/a3d2d9c8-6ebd-4c3e-a146-501cecf3e98c/index.html
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
  - Roman Rohleder
  - Ibrahim Abouzied
  - Cristiano Silva
---

## Vulnerability Title

`Maximillion.setCEther()` Callable Multiple Times By Anyone

### Overview


The development team has found an issue with the `Maximillion.sol` file, which is only used for testing and is not deployed to the main network. The team made changes to the Compound code base, specifically changing the constructor to a publicly callable function called `setCEther()`. This means that anyone can call the contract and re-initialize it, which can modify the `cEther` state variable. To fix this issue, the team recommends changing the `setCEther()` function back to a constructor, adding a check for an `IS_INITIALIZED` variable, or using the `Initializable` library from OpenZeppelin. Alternatively, if re-initialization is desired, access controls should be added using the `Access Control` library from OpenZeppelin.

### Original Finding Content

**Update**
From dev team:

> `Maximillion.sol` is used only for testing purposes and is never deployed to mainnet. The team has chosen to keep the original Compound implementation.

**File(s) affected:**`Maximillion.sol`

**Description:** One of the custom changes to the Compound code base was changing the constructors to publicly callable normal functions. The `Maximillion` constructor changed to a publicly callable function `setCEther()`. As it is no longer a constructor, or has an `initializer` modifier as i.e. known from [OpenZeppelin's `Initializable` library](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#initializers), or any other way of preventing multiple calls and is public, anyone can call said contract and re-initialize it and thereby modify the `cEther` state variable.

**Recommendation:** We recommend changing the `setCEther()` functions back to a constructor, adding and checking the `IS_INITIALIZED` Boolean variable, or using [said `Initializable` library](https://github.com/OpenZeppelin/openzeppelin-upgrades/blob/master/packages/core/contracts/Initializable.sol), to prevent multiple re-initializations/calls by anyone. Alternatively, if this re-initialization is desired, add corresponding access controls, i.e. via [OpenZeppelin's `Access Control` library](https://docs.openzeppelin.com/contracts/2.x/access-control).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Quadrata Lending |
| Report Date | N/A |
| Finders | Roman Rohleder, Ibrahim Abouzied, Cristiano Silva |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/quadrata-lending/a3d2d9c8-6ebd-4c3e-a146-501cecf3e98c/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/quadrata-lending/a3d2d9c8-6ebd-4c3e-a146-501cecf3e98c/index.html

### Keywords for Search

`vulnerability`

