---
# Core Classification
protocol: Kakarot
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45183
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-09-kakarot
source_link: https://code4rena.com/reports/2024-09-kakarot
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
finders_count: 0
finders:
---

## Vulnerability Title

[01] Missing boundary check in EVM transaction decoding

### Overview

See description below for full details.

### Original Finding Content


With the `account_contract.cairo`'s `execute_from_outside` function, callers submit a `calldata` blob of `calldata_len` length, out of which the transaction data is extracted by selecting `[call_array].data_len` bytes starting from position `[call_array].data_offset`.

Within the logic that makes this extraction, there is no check that `[call_array].data_offset + [call_array].data_len` fits within `calldata_len`, effectively allowing for the submission of transactions that pass or fail validation depending on what's allocated out of the boundaries of the input data.

Consider adding a boundary check to enforce `[call_array].data_offset + [call_array].data_len < calldata_len`.

Similar lack of validation for non-critical variables can be found in the actual length of the `signature` array vs `signature_len`, the actual length of the `call_array` vs `call_array_len`, as well as in `eth_transactions::parse_access_list()`, where the parsing of `address_item` misses a check that `address_item.data_len = 20`, that the `access_list.data_len = 2` (spec in the python snippet [here](https://eips.ethereum.org/EIPS/eip-2930#parameters)).

**Kakarot mitigated:**
> [PR 1633](https://github.com/kkrt-labs/kakarot/pull/1633): Check `call_array` within bounds `calldata`, `stack_size_diff`, remove setter native token and raise for invalid `y_parity` values 

**Status:** Mitigation confirmed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Kakarot |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-09-kakarot
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-09-kakarot

### Keywords for Search

`vulnerability`

