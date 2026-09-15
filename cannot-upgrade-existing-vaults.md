---
# Core Classification
protocol: Cyan
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59446
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/cyan/5ef87add-ca0f-43eb-b6bb-758ec81a7e85/index.html
source_link: https://certificate.quantstamp.com/full/cyan/5ef87add-ca0f-43eb-b6bb-758ec81a7e85/index.html
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
finders_count: 3
finders:
  - Jennifer Wu
  - Ibrahim Abouzied
  - Jonathan Mevs
---

## Vulnerability Title

Cannot Upgrade Existing Vaults

### Overview


The client has marked a bug as "Fixed" and it has been addressed in the code. The issue was with the `initializer()` modifier in the `CyanVaultV2.sol` file, which only allows the `initialize()` function to be called once. However, the new version of the code requires additional initialization, which cannot be done due to the `initializer()` modifier. The recommendation is to add a new function called `initializeV2()` that uses the `reinitializer()` modifier to support the upgraded version's new state. More information can be found in the [Initializable](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/v4.9.6/contracts/proxy/utils/Initializable.sol#L8-L57) contract.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `ed5a2525c02f0d2668130f2a08cbcde2783fff49`.

Upgrades of existing vaults is now supported through the use of the `reinitializer()` modifier.

**File(s) affected:**`CyanVaultV2.sol`

**Description:** The `initializer()` modifier ensures that a proxy's implementation contract can only have the `initialize()` function invoked once. `CyanVaultV2` introduces new states that are required to be initialized in the `initialize()` function. However, this `initialize()` function will not be able to be called on the new implementation, as the `initializer()` modifier will prevent it.

**Recommendation:** Include a second initialize function, such as `initializeV2()` that utilizes the `reinitializer()` modifier to specify a version 2. This will ensure that the proxy can support the upgraded implementation's new state. More details can be found in the [Initializable](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/v4.9.6/contracts/proxy/utils/Initializable.sol#L8-L57) contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Cyan |
| Report Date | N/A |
| Finders | Jennifer Wu, Ibrahim Abouzied, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/cyan/5ef87add-ca0f-43eb-b6bb-758ec81a7e85/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/cyan/5ef87add-ca0f-43eb-b6bb-758ec81a7e85/index.html

### Keywords for Search

`vulnerability`

