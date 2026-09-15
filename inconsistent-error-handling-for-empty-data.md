---
# Core Classification
protocol: Symbiotic
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64354
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
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
finders_count: 4
finders:
  - 0kage
  - Aleph-v
  - ChainDefenders](https://x.com/DefendersAudits) ([@1337web3](https://x.com/1337web3) & [@PeterSRWeb3
  - Farouk
---

## Vulnerability Title

Inconsistent error handling for empty data

### Overview

See description below for full details.

### Original Finding Content

**Description:** In `_getSelector()`, when data is empty, it returns `0xEEEEEEEE` which is not a standard practice.

```solidity
function _getSelector(bytes memory data) internal pure returns (bytes4 selector) {
    if (data.length == 0) {
        return 0xEEEEEEEE;
    }
    // ...
}
```

**Impact:** Potentially unexpected return values confusing functions interacting with the `_getSelector` function.

**Recommended Mitigation:** Consider documenting the chosen behaviour so developers and future auditors know whether it is expected behaviour.

**Symbiotic:** Fixed in [8667780](https://github.com/symbioticfi/relay-contracts/pull/36/commits/8667780b0653a83f68a2cdb1c630ad8582eaa787).

**Cyfrin:** Verified.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Symbiotic |
| Report Date | N/A |
| Finders | 0kage, Aleph-v, ChainDefenders](https://x.com/DefendersAudits) ([@1337web3](https://x.com/1337web3) & [@PeterSRWeb3, Farouk |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

