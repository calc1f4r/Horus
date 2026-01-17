---
# Core Classification
protocol: Securitize Dstokenswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64259
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-01-10-cyfrin-securitize-dstokenswap-v2.0.md
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
  - Hans
---

## Vulnerability Title

Missing zero address validation in initialize function

### Overview

See description below for full details.

### Original Finding Content

**Description:** The `initialize` function in `DSTokenClassSwap` contract does not validate that the input addresses `_sourceDSToken` and `_targetDSToken` are non-zero addresses.

```solidity
DSTokenClassSwap.sol
40:     function initialize(address _sourceDSToken, address _targetDSToken) public override onlyProxy initializer {
41:         __BaseDSContract_init();
42:         sourceDSToken = IDSToken(_sourceDSToken);//@audit-issue INFO check zero address
43:         sourceServiceConsumer = IDSServiceConsumer(_sourceDSToken);
44:         targetDSToken = IDSToken(_targetDSToken);
45:         targetServiceConsumer = IDSServiceConsumer(_targetDSToken);
46:     }
```

**Recommended Mitigation:** Add zero address validation checks.

**Securitize:** Fixed in commit [b26a16](https://bitbucket.org/securitize_dev/bc-dstoken-class-swap-sc/commits/b26a167524dfa96fc92dc18a863998a50e533bf2).

**Cyfrin:** Verified.


\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Dstokenswap |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-01-10-cyfrin-securitize-dstokenswap-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

