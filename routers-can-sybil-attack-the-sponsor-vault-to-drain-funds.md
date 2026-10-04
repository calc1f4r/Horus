---
# Core Classification
protocol: Connext
chain: everychain
category: uncategorized
vulnerability_type: sybil_attack

# Attack Vector Details
attack_type: sybil_attack
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7217
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - sybil_attack

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

Routers can sybil attack the sponsor vault to drain funds

### Overview


This bug report is about the BridgeFacet.sol contract, which is used to transfer funds from one chain to another. The contract checks if the domain is sponsored, and if so, the user is reimbursed for both liquidity fees paid when the transfer was initiated and for the fees paid to the relayer during message propagation. However, there is no mechanism to detect sybil attacks, which can be used by a router to perform several large value transfers in an effort to drain the sponsor vault of its funds. 

The recommendation is to consider re-thinking the sponsor vault design or to remove it altogether. A cap was implemented in PR 1631, but it does not completely mitigate sybil attacks on the vault. Anyone who decides to deploy and fund a vault should be aware of this. The bug report has been verified and acknowledged.

### Original Finding Content

## Security Report

## Severity
**High Risk**

## Context
*File:* BridgeFacet.sol  
*Lines:* 652-688

## Description
When funds are bridged from source to destination chain, messages must first go through optimistic verification before being executed on the destination BridgeFacet.sol contract. Upon transfer processing, the contract checks if the domain is sponsored. If such is the case, then the user is reimbursed for both liquidity fees paid when the transfer was initiated and for the fees paid to the relayer during message propagation.

There currently isn’t any mechanism to detect sybil attacks. Therefore, a router can perform several large-value transfers in an effort to drain the sponsor vault of its funds. Because liquidity fees are paid to the router by a user connected to the router, there isn’t any value lost in this type of attack.

## Recommendation
Consider re-thinking the sponsor vault design, or it may be safer to have it removed altogether. 

**Connext:** Cap implemented in PR 1631. There is no total mitigation of sybil attacks on the vault possible, and this should be clearly explained to anyone who decides to deploy and fund one.

**Spearbit:** Verified and acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | 0xLeastwood, Jonah1005 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf

### Keywords for Search

`Sybil Attack`

