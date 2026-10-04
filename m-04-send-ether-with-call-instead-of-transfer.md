---
# Core Classification
protocol: Redacted Cartel
chain: everychain
category: uncategorized
vulnerability_type: call_vs_transfer

# Attack Vector Details
attack_type: call_vs_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1488
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-redacted-cartel-contest
source_link: https://code4rena.com/reports/2022-02-redacted-cartel
github_link: https://github.com/code-423n4/2022-02-redacted-cartel-findings/issues/2

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.20
financial_impact: medium

# Scoring
quality_score: 1.001075122243043
rarity_score: 1.0014334963240574

# Context Tags
tags:
  - call_vs_transfer

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - leastwood
  - Dravee
  - Jujic
  - z3s
  - hyh
---

## Vulnerability Title

[M-04] Send ether with call instead of transfer

### Overview


This bug report is about a vulnerability in the RewardDistributor.sol contract code. The issue is that the code is using the transfer function to send ether, which is no longer recommended. This could lead to potential losses of ether if the return value is not checked to ensure the transfer was successful. The proof of concept can be found at the link provided in the report. The recommended mitigation step is to use the call function instead, and to check the return value to ensure the transfer was successful.

### Original Finding Content

_Submitted by kenta, also found by Dravee, hyh, Jujic, leastwood, and z3s_

Use call instead of transfer to send ether. And return value must be checked if sending ether is successful or not.
Sending ether with the transfer is no longer recommended.

### Proof of Concept

[RewardDistributor.sol#L181](https://github.com/code-423n4/2022-02-redacted-cartel/blob/main/contracts/RewardDistributor.sol#L181)

### Recommended Mitigation Steps

(bool result, ) = payable(\_account).call{value: \_amount}("");
require(result, "Failed to send Ether");

**[kphed (Redacted Cartel) confirmed](https://github.com/code-423n4/2022-02-redacted-cartel-findings/issues/2)**


**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-02-redacted-cartel-findings/issues/2#issuecomment-1059781616):**
 > I believe the function would actually work with most Smart Contract Wallets and proxies. However this could change in the future.
> 
> Agree with the finding.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 1.001075122243043/5 |
| Rarity Score | 1.0014334963240574/5 |
| Audit Firm | Code4rena |
| Protocol | Redacted Cartel |
| Report Date | N/A |
| Finders | leastwood, Dravee, Jujic, z3s, hyh, kenta |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-redacted-cartel
- **GitHub**: https://github.com/code-423n4/2022-02-redacted-cartel-findings/issues/2
- **Contest**: https://code4rena.com/contests/2022-02-redacted-cartel-contest

### Keywords for Search

`call vs transfer`

