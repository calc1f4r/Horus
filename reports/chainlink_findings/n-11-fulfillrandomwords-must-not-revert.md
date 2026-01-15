---
# Core Classification
protocol: Forgeries
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24258
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-12-forgeries
source_link: https://code4rena.com/reports/2022-12-forgeries
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

protocol_categories:
  - dexes
  - cdp
  - services
  - synthetics
  - gaming

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[N-11] `fulfillRandomWords` must not revert

### Overview

See description below for full details.

### Original Finding Content


Accordingly to ChainLinks' [documentation]():

> `fulfillRandomWords` must not revert
> If your `fulfillRandomWords()` implementation reverts, the VRF service will not attempt to call it a second time. Make sure your contract logic does not revert. Consider simply storing the randomness and taking more complex follow-on actions in separate contract calls made by you, your users, or an Automation Node.

This project's current implementation does revert [in two instances](https://github.com/code-423n4/2022-12-forgeries/blob/main/src/VRFNFTRandomDraw.sol#L230-L260), although they are not expected to materialize.

Nevertheless, consider altering the logic to drop the random generated whenever the requestId does not match and ignore extra words if the array received is greater than the expected amount.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Forgeries |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-forgeries
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-12-forgeries

### Keywords for Search

`vulnerability`

