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
solodit_id: 45346
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Lending%20Proxy/README.md#2-overstated-withdrawals-when-existing-tokens-are-held
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

Overstated Withdrawals When Existing Tokens Are Held

### Overview


The report describes a bug in the withdraw function of the P2pLendingProxy contract. This bug causes the contract's post-withdrawal token balance to be used to calculate the amount of tokens withdrawn, which can result in an inflated withdrawn amount. This can lead to users paying more fees if the contract already held tokens. The bug is classified as medium severity and the recommended solution is to capture the balance before the withdrawal call and compute the difference to determine the exact tokens retrieved from the external protocol. This will ensure the correct number of tokens is used for fee calculations.

### Original Finding Content

##### Description
In the `withdraw` function of `P2pLendingProxy`, the contract’s post-withdrawal token balance is used to calculate how many tokens were withdrawn. This can inflate the perceived withdrawn amount if the contract already held tokens. Consequently, users may pay more fees if they (or others) previously sent tokens directly to the proxy.

The issue is classified as **medium** severity because it causes inaccurate fee or profit calculations, although it does not enable direct theft.
##### Recommendation
We recommend capturing the balance before the withdrawal call, then computing the difference to determine the exact tokens retrieved from the external protocol. This ensures the correct number of tokens withdrawn is used for fee calculations.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Lending%20Proxy/README.md#2-overstated-withdrawals-when-existing-tokens-are-held
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

