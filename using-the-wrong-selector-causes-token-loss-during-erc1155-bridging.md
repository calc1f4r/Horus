---
# Core Classification
protocol: Boba 1 (Bridges and LP floating fee)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60699
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/boba-1-bridges-and-lp-floating-fee/1e5a1e09-bde0-417d-83cd-083234b1409c/index.html
source_link: https://certificate.quantstamp.com/full/boba-1-bridges-and-lp-floating-fee/1e5a1e09-bde0-417d-83cd-083234b1409c/index.html
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
finders_count: 5
finders:
  - Pavel Shabarkin
  - Ibrahim Abouzied
  - Andy Lin
  - Adrian Koegl
  - Valerian Callens
---

## Vulnerability Title

Using the Wrong Selector Causes Token Loss During ERC1155 Bridging

### Overview


The bug report describes an issue where the `L1ERC1155Bridge.finalizeWithdrawalBatch()` function encodes the wrong selector when `replyNeeded` is true. This can cause the message to fail and result in the user losing their tokens. The recommended fix is to use the correct selector, `iL2ERC1155Bridge.finalizeDepositBatch.selector`, instead. The report also suggests adding integration and end-to-end tests to prevent future issues.

### Original Finding Content

**Update**
The team fixed the issue as recommended in the commit `535c64c9`.

**Description:** The `L1ERC1155Bridge.finalizeWithdrawalBatch()` function encodes the wrong selector when `replyNeeded` is true. The line `bytes memory message = abi.encodeWithSelector(...)` uses `iL2ERC1155Bridge.finalizeDeposit.selector` as the selector where the correct one should be `iL2ERC1155Bridge.finalizeDepositBatch.selector` instead. The message will fail because it will not fit the interface of the `iL2ERC1155Bridge.finalizeDeposit()` function. Once failed, the user will lose his/her tokens.

**Exploit Scenario:** Alice tries to bridge a ERC1155 token where the base network is L2. Somehow, the function fails to batch mint the tokens and tries to send a revert message. However, due to the bug, the revert message would not work and Alice will lose her tokens.

**Recommendation:** We suggest the following fixes:

1.   Use the `iL2ERC1155Bridge.finalizeDepositBatch.selector` instead.
2.   This indicates a lack of integration / end-to-end tests. We strongly recommend the Boba team adding the tests and also check if other tests should be added to cover all expected use cases.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Boba 1 (Bridges and LP floating fee) |
| Report Date | N/A |
| Finders | Pavel Shabarkin, Ibrahim Abouzied, Andy Lin, Adrian Koegl, Valerian Callens |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/boba-1-bridges-and-lp-floating-fee/1e5a1e09-bde0-417d-83cd-083234b1409c/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/boba-1-bridges-and-lp-floating-fee/1e5a1e09-bde0-417d-83cd-083234b1409c/index.html

### Keywords for Search

`vulnerability`

