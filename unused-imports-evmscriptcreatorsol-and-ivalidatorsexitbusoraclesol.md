---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62658
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Easy%20Track%20(3)/README.md#3-unused-imports-evmscriptcreatorsol-and-ivalidatorsexitbusoraclesol
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
  - MixBytes
---

## Vulnerability Title

Unused Imports: EVMScriptCreator.sol and IValidatorsExitBusOracle.sol

### Overview

See description below for full details.

### Original Finding Content

##### Description
In `SubmitExitRequestHashesUtils.sol`, the following imports are declared but never used within the library:

```solidity=
import "../libraries/EVMScriptCreator.sol";
import "../interfaces/IValidatorsExitBusOracle.sol";
```

These files are not referenced in any function or type within the current implementation of the library.

##### Recommendation
We recommend removing the mentioned unused imports.




---
    

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Easy%20Track%20(3)/README.md#3-unused-imports-evmscriptcreatorsol-and-ivalidatorsexitbusoraclesol
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

