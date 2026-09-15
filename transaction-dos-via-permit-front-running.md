---
# Core Classification
protocol: EYWA
chain: everychain
category: economic
vulnerability_type: grief_attack

# Attack Vector Details
attack_type: grief_attack
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41155
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/EYWA/CLP/README.md#5-transaction-dos-via-permit-front-running
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - grief_attack
  - front-running
  - dos

protocol_categories:
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Transaction DOS via `permit()` front-running

### Overview


The `permit()` function is publicly accessible in the mempool, which means anyone can execute it by copying the transaction arguments. This can cause problems if the same arguments are used more than once, as the second call will fail. This bug could be exploited by a malicious actor to bypass the `start()` function and cause a legitimate user's transaction to fail. To fix this issue, it is recommended to use the `try/catch` pattern when using the `permit()` function.

### Original Finding Content

##### Description

The `permit()` data,  once submitted, is publicly accessible in the mempool, allowing anyone to execute the permit by replicating the transaction arguments. Once `permit()` has been called, the second call with identical parameters will revert.

In a scenario where a signed transaction includes `PERMIT_CODE`, a malicious actor could frontrun and "activate" this permit, bypassing the router's `start()` function. As a result, the legitimate user's `start()` transaction would fail:
- https://github.com/eywa-protocol/eywa-clp/blob/d68ba027ff19e927d64de123b2b02f15a43f8214/contracts/RouterV2.sol#L99-L109

Reference:
- https://www.trust-security.xyz/post/permission-denied

##### Recommendation

We recommended using the `try/catch` pattern for permit operations to prevent reverts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | MixBytes |
| Protocol | EYWA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/EYWA/CLP/README.md#5-transaction-dos-via-permit-front-running
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Grief Attack, Front-Running, DOS`

