---
# Core Classification
protocol: P2P.org
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45345
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Lending%20Proxy/README.md#1-missing-permit2-front-run-protection
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Missing `PERMIT2` Front-Run Protection

### Overview


The `deposit` function in the `P2pLendingProxy` contract has a bug that allows attackers to interfere with a user's transaction by calling `Permit2.permit` beforehand. This can cause unexpected issues with the transaction, but does not result in direct loss of funds. To fix this, it is recommended to use a try-catch pattern to prevent unintended reverts caused by an invalidated nonce.

### Original Finding Content

##### Description
This issue has been identified within the `deposit` function of the `P2pLendingProxy` contract. 

An attacker can front-run a legitimate user’s transaction by preemptively calling `Permit2.permit`, causing reverts or unexpected over-allowances granted to the proxy.

The issue is classified as **medium** severity because while it might lead to transaction failure or confusion, it does not necessarily result in direct fund loss.
##### Recommendation
We recommend wrapping Permit2.permit into a try-catch pattern preventing unintended reverts due to invalidated nonce.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | P2P.org |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Lending%20Proxy/README.md#1-missing-permit2-front-run-protection
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

