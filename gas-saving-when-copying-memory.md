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
solodit_id: 28450
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Oracle/README.md#4-gas-saving-when-copying-memory
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

Gas saving when copying memory

### Overview

See description below for full details.

### Original Finding Content

##### Description
In the function for copy memory when `len % WORD_SIZE == 0` it is possible to save some gas by adding simple check:
https://github.com/hamdiallam/Solidity-RLP/blob/4fa53119e6dd7c4a950586e21b6068cd9520a649/contracts/RLPReader.sol#L350-L355

##### Recommendation
We recommend to add following check:
```solidity=
if (len > 0)
{
    uint mask = 256 ** (WORD_SIZE - len) - 1;
    assembly {
        let srcpart := and(mload(src), not(mask)) // zero out src
        let destpart := and(mload(dest), mask) // retrieve the bytes
        mstore(dest, or(destpart, srcpart))
    }
}
```

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Oracle/README.md#4-gas-saving-when-copying-memory
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

