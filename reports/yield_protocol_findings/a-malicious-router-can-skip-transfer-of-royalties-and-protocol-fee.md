---
# Core Classification
protocol: Sudoswap LSSVM2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18303
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
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
finders_count: 5
finders:
  - Gerard Persoon
  - Shodan
  - Rajeev
  - Lucas Goiriz
  - David Chaparro
---

## Vulnerability Title

A malicious router can skip transfer of royalties and protocol fee

### Overview


This bug report concerns the LSSVMPairERC20.sol#L59-L91 code. It states that a malicious router, if whitelisted by the protocol, could implement functions that do not transfer the expected amount of tokens. This poses a risk as there are no balance checks for royalty and protocol fee payments. The recommendation is to add before-after balance checks for these transfers. Sudorandom Labs has decided to hold off on this fix due to the trade-off for gas, but Spearbit has verified that the issue is partially fixed in PR#40.

### Original Finding Content

## Security Advisory

## Severity: Medium Risk

### Context
- **File**: LSSVMPairERC20.sol
- **Lines**: L59-L91

### Description
A malicious router, if accidentally or intentionally whitelisted by the protocol, may implement `pair-TransferERC20From()` functions which do not actually transfer the number of tokens as expected. This is within the protocol's threat model as evidenced by the use of before-after balance checks on the `_assetRecipient` for `saleAmount`. However, similar before-after balance checks are missing for transfers of royalties and protocol fee payments.

Royalty recipients do not receive their royalties from the malicious router if the protocol/factory intentionally or accidentally whitelists one. The protocol/factory may also accidentally whitelist a malicious router that does not transfer even the protocol fee.

### Recommendation
Add before-after balance checks for royalty and protocol fee transfers.

### Stakeholder Comments
- **Sudorandom Labs**: Talked internally, we're going to hold-off on this one for now. The factory owner has no incentive to not add routers which don't pay the fee, and if they do (e.g., by accident), they can always disable/add a new one. The gas trade-off here is one we're potentially willing to make.

- **Spearbit**: Verified that this is partially fixed in PR#40. Acknowledged the part about `protocolFee`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Sudoswap LSSVM2 |
| Report Date | N/A |
| Finders | Gerard Persoon, Shodan, Rajeev, Lucas Goiriz, David Chaparro |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

