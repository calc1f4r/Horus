---
# Core Classification
protocol: Dexe
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27326
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-10-cyfrin-dexe.md
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
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Dacian
  - 0kage
---

## Vulnerability Title

Missing `address(0)` checks when assigning values to address state variables

### Overview

See description below for full details.

### Original Finding Content

**Description:** Missing `address(0)` checks when assigning values to address state variables.

**Impact:** Address state variables may be unexpectedly set to `address(0)`.

**Proof of Concept:**
```solidity
File: gov/GovPool.sol

344:         _nftMultiplier = nftMultiplierAddress;

```

```solidity
File: gov/proposals/TokenSaleProposal.sol

63:         govAddress = _govAddress;

```

From Solarity library:

```solidity
File: contracts-registry/pools/AbstractPoolContractsRegistry.sol

51:         _contractsRegistry = contractsRegistry_;

```

```solidity
File: contracts-registry/pools/pool-factory/AbstractPoolFactory.sol

31:         _contractsRegistry = contractsRegistry_;

```

```solidity
File: contracts-registry/pools/proxy/ProxyBeacon.sol

33:         _implementation = newImplementation_;

```

**Recommended Mitigation:** Consider adding above `address(0)` checks.

**Dexe:**
Acknowledged; the provided examples are either related to PoolFactory (where no address(0) are possible) or to an NFTMultiplier which is intended to be zero under some business conditions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Dexe |
| Report Date | N/A |
| Finders | Dacian, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-10-cyfrin-dexe.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

