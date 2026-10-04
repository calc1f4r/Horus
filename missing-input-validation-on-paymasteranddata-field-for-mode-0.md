---
# Core Classification
protocol: Pimlico ERC20 Paymaster
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59281
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/pimlico-erc-20-paymaster/ce056730-3f75-4711-9e81-c5dbfdfce74d/index.html
source_link: https://certificate.quantstamp.com/full/pimlico-erc-20-paymaster/ce056730-3f75-4711-9e81-c5dbfdfce74d/index.html
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
  - Shih-Hung Wang
  - Nikita Belenkov
  - Ruben Koch
---

## Vulnerability Title

Missing Input Validation on `paymasterAndData` Field for `mode = 0`

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `d3c891ee73fb4c6a4f456b83d2e414a4142092ca`.

**File(s) affected:**`ERC20PaymasterV06.sol`, `ERC20PaymasterV07.sol`

**Description:** In the validation of the case `mode = 0`, no validation is performed on `paymasterConfig` derived from the `paymasterAndData` field. While no third party can malform/bloat it because we can assume it is signed, the user could accidentally execute a `mode = 1` intended operation as `mode = 0`, where the constraints of the transaction are accidentally discarded, causing a user to be charged more than they are willing to spend.

Technically, the signer could insert an arbitrary long bytes array that the paymaster would still need to load as a parameter in, but since in `mode = 0`, the user ends up paying for the gas and since the operation is still constrained by `maxCost`, this is not a relevant factor.

**Recommendation:** Add input validation ensuring that `paymasterConfig.length = 0` in case of `mode = 0`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Pimlico ERC20 Paymaster |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Nikita Belenkov, Ruben Koch |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/pimlico-erc-20-paymaster/ce056730-3f75-4711-9e81-c5dbfdfce74d/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/pimlico-erc-20-paymaster/ce056730-3f75-4711-9e81-c5dbfdfce74d/index.html

### Keywords for Search

`vulnerability`

