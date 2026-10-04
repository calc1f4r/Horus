---
# Core Classification
protocol: Bucket Protocol V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63387
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/bucket-protocol-v-2/abd312d6-1a5e-45c5-963b-a6856daf6621/index.html
source_link: https://certificate.quantstamp.com/full/bucket-protocol-v-2/abd312d6-1a5e-45c5-963b-a6856daf6621/index.html
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
  - Hamed Mohammadi
  - Adrian Koegl
  - Rabib Islam
---

## Vulnerability Title

Functions Silently Fail

### Overview

See description below for full details.

### Original Finding Content

**Update**
Acknowledged by the client. The client provided the following explanation:

> Abort for unchanged state seems unnecessary. And in PTB if a moveCall abort the whole transaction fails. For example, we want to add checks to all CDP vaults and put all CDP vaults in transaction but one of the vault is already get added then we don't want the transaction to fail.

**File(s) affected:**`bucket_framework/sources/sheet.move`, `bucket_cdp/sources/vault.move`, `bucket_usd/sources/usdb.move`, `bucket_cdp/sources/acl.move`, `bucket_oracle/sources/collector.move`

**Description:** There are a number of `public` functions in the codebase that may be called with the intention of effecting some change in state, but that provide no feedback when there is no change. This can surprise users who expect some sort of feedback when a function does not do what it is supposed to do in the mind of the user.

The following is a list of instances:

1.   `sheet`
    1.   `add_creditor()`
    2.   `add_debtor()`
    3.   `ban()`
    4.   `unban()`

2.   `vault`
    1.   `add_request_check()`
    2.   `remove_request_check()`
    3.   `add_response_check()`
    4.   `remove_response_check()`

3.   `usdb`
    1.   `remove_module()`
    2.   `remove_version()`

4.   `acl`
    1.   `remove_role()`

5.   `collector`
    1.   `remove()`

**Recommendation:** Have each function either return a boolean indicating whether state was changed or throw an error if no state was changed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Bucket Protocol V2 |
| Report Date | N/A |
| Finders | Hamed Mohammadi, Adrian Koegl, Rabib Islam |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/bucket-protocol-v-2/abd312d6-1a5e-45c5-963b-a6856daf6621/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/bucket-protocol-v-2/abd312d6-1a5e-45c5-963b-a6856daf6621/index.html

### Keywords for Search

`vulnerability`

