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
solodit_id: 52847
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

Missing check for polFeeCollector initialization

### Overview

See description below for full details.

### Original Finding Content

Severity: Low Risk
Context: ProtocolFeesCollector.sol#L98
Description: The withdrawCollectedFeesToPOLFeeCollector() function allows to withdraw fees to the
polFeeCollector address. The constructor does not set this address to keep the changes as small as possible.
As a result, the address needs to be set via an external setter by an admin.
function setPOLFeeCollector(address _polFeeCollector) external override authenticate {
polFeeCollector = _polFeeCollector;
emit POLFeeCollectorChanged(_polFeeCollector);
}
If an admin forgets to set the address and calls withdrawCollectedFeesToPOLFeeCollector() before, the funds
will be burned/sent to the zero address.
Recommendation: The issue can be mitigated by adding a check that verifies that thepolFeeCollector is set to
a different address than address(0) .
/// @notice Function to transfer fees to POL fee collector
function withdrawCollectedFeesToPOLFeeCollector(IERC20[] calldata tokens, uint256[] calldata amounts)
external
override
nonReentrant
authenticate
{
InputHelpers.ensureInputLengthMatch(tokens.length, amounts.length);
require(polFeeCollector != address(0), "polFeeCollector not set");
for (uint256 i = 0; i < tokens.length; ++i) {
IERC20 token = tokens[i];
uint256 amount = amounts[i];
token.safeTransfer(polFeeCollector, amount);
}
}
Berachain: Fixed by checking that the POLFeeCollector can't be set to 0 in the constructor in PR 6.
Spearbit: Mitigated by the fix provided by the protocol.

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

