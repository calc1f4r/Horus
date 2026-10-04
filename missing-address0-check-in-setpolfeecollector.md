---
# Core Classification
protocol: Bera Bex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52846
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Bex-Spearbit-Security-Review-September-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Bex-Spearbit-Security-Review-September-2024.pdf
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
finders_count: 3
finders:
  - J4X
  - Xiaoming90
  - 0xIcingdeath
---

## Vulnerability Title

Missing address(0) check in setPOLFeeCollector()

### Overview

See description below for full details.

### Original Finding Content

Severity: Low Risk
Context: ProtocolFeesCollector.sol#L98
Description: The setPOLFeeCollector() can be used to set the polFeeCollector variable.
function setPOLFeeCollector(address _polFeeCollector) external override authenticate {
polFeeCollector = _polFeeCollector;
emit POLFeeCollectorChanged(_polFeeCollector);
}
Unfortunately, this function never verifies that the variable is set to an actual address and was not accidentally
called with zero parameters.
Recommendation: We recommend checking that _polFeeCollector is not zero.
function setPOLFeeCollector(address _polFeeCollector) external override authenticate {
require(_polFeeCollector != address(0), "polFeeCollector can not be set to zero");
polFeeCollector = _polFeeCollector;
emit POLFeeCollectorChanged(_polFeeCollector);
}
Berachain: Fixed in PR 6.
Spearbit: Fixed in the PR provided by the protocol.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Bera Bex |
| Report Date | N/A |
| Finders | J4X, Xiaoming90, 0xIcingdeath |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Bex-Spearbit-Security-Review-September-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Bex-Spearbit-Security-Review-September-2024.pdf

### Keywords for Search

`vulnerability`

