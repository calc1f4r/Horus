---
# Core Classification
protocol: NUTS Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62675
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Tapio/README.md#5-fee-on-transfer-tokens-not-supported
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
  - MixBytes
---

## Vulnerability Title

Fee-On-Transfer Tokens Not Supported

### Overview

See description below for full details.

### Original Finding Content

##### Description
This issue has been identified in the contract’s token-handling logic (for example, in the `mint`, `swap`, and `redeem` functions). The contract assumes standard ERC20 transfers without accounting for fee-on-transfer tokens (e.g., USDT and USDC, which currently have fees set at 0%). This can result in smaller received amounts than expected, causing unpredictable behavior or potential loss of funds.

The issue is classified as **low** severity because it only affects scenarios where a token has a fee-on-transfer mechanism.

##### Recommendation
We recommend either disallowing fee-on-transfer tokens in the `swap` and `mint` functions by reverting when the received balance does not match the expected amount, or calculating the invariants after the transfer is performed, using the actual balance increase.


### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | NUTS Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Tapio/README.md#5-fee-on-transfer-tokens-not-supported
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

