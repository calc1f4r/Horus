---
# Core Classification
protocol: zkSync Bootloader Audit Report
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10370
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/zksync-bootloader-audit-report/
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.20
financial_impact: medium

# Scoring
quality_score: 1
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Unprotected Initialization Function

### Overview


This bug report is about the `L2EthToken` contract. It states that the `initialization` function is unprotected, meaning anyone can set the `l2Bridge` address if they call the function before the legitimate operator. The report suggests using the TypeScript-based templating system which is already present in the codebase to inject a constant address that limits the `initialization` call to one specific `msg.sender`. The Matter Labs team has acknowledged this issue and stated they plan to rethink the approach of bridging ether in the new upgrade, and the issue will be resolved there.

### Original Finding Content

In the `L2EthToken` contract, an [unresolved comment](https://github.com/matter-labs/system-contracts/blob/4ad1f26ae205d5a973216d141833e0ac37d72ec8/contracts/L2EthToken.sol#L35) acknowledges the fact that the `initialization` function is unprotected and anyone could set the `l2Bridge` address if they call the function before the legitimate operator. The comment describes the problem without presenting a solution.


Consider using the TypeScript-based templating system that is already present in the codebase to inject a constant address that limits the `initialization` call to one specific `msg.sender`.


***Update:** Acknowledged, not resolved. The Matter Labs team stated:*



> *We plan to rethink the approach of bridging ether in the new upgrade, the issue will be resolved there.*
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 1/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | zkSync Bootloader Audit Report |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/zksync-bootloader-audit-report/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

