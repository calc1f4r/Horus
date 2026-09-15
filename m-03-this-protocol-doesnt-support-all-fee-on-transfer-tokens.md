---
# Core Classification
protocol: Streaming Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42397
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-11-streaming
source_link: https://code4rena.com/reports/2021-11-streaming
github_link: https://github.com/code-423n4/2021-11-streaming-findings/issues/192

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
finders_count: 0
finders:
---

## Vulnerability Title

[M-03] This protocol doesn't support all fee on transfer tokens

### Overview


The user 0x0x0x has reported a bug in a contract that handles fee on transfer tokens. These tokens usually deduct the fee from the transferred amount, but this contract subtracts it from the sender's remaining balance. This can result in the recipient receiving less than the expected amount, causing potential loss of funds. The user suggests that the contract does not fully support fee on transfer tokens and recommends not claiming to do so. The issue has been acknowledged by the Streaming Protocol team and they plan to clarify this for stream creators. 

### Original Finding Content

_Submitted by 0x0x0x_

Some fee on transfer tokens, do not reduce the fee directly from the transferred amount, but subtracts it from remaining balance of sender. Some tokens prefer this approach, to make the amount received by the recipient an exact amount. Therefore, after funds are send to users, balance becomes less than it should be. So this contract does not fully support fee on transfer tokens. With such tokens, user funds can get lost after transfers.

#### Mitigation step

I don't recommend directly claiming to support fee on transfer tokens. Current contract only supports them, if they reduce the fee from the transfer amount.

**[brockelmore (Streaming Protocol) acknowldedged](https://github.com/code-423n4/2021-11-streaming-findings/issues/192#issuecomment-989261382):**
 > We will make this clear for stream creators





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Streaming Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-streaming
- **GitHub**: https://github.com/code-423n4/2021-11-streaming-findings/issues/192
- **Contest**: https://code4rena.com/reports/2021-11-streaming

### Keywords for Search

`vulnerability`

