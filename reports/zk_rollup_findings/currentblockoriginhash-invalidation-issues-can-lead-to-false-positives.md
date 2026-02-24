---
# Core Classification
protocol: SphereX Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33037
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/spherex-audit
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
  - OpenZeppelin
---

## Vulnerability Title

currentBlockOriginHash Invalidation Issues Can Lead to False Positives

### Overview


The bug being reported is related to a known issue where a certain condition can cause false positives in transactions. This issue is particularly severe in some situations, such as on certain L2s like Arbitrum, Optimism, and zkSync, where the block number remains constant for a period of time. This can also occur in chains that use relayers and Account Abstraction. The suggested solution is to add `block.timestamp` to the hash, and it is also possible that `block.difficulty`, `tx.gasPrice`, and `block.baseFee` could help. The bug has been resolved in a recent pull request on GitHub.

### Original Finding Content

Although reported as a known issue, this can be particularly severe in some circumstances:


* On some L2s, such as Arbitrum, where `block.number` is the L1 block number, so it will [remain constant for some time](https://developer.arbitrum.io/time#example). Similarly [for Optimism](https://community.optimism.io/docs/developers/build/differences/#added-opcodes), and [zkSync](https://era.zksync.io/docs/dev/developer-guides/transactions/blocks.html#block-number-and-timestamp-considerations).
* In chains that rely on relayers and Account Abstraction (quite possibly zkSync).


This can cause intermittent false positives as the second transaction could be rejected for producing a disallowed pattern.


Consider adding `block.timestamp` (will help with Arbitrum and Optimism) into the hash. It is possible that `block.difficulty`, `tx.gasPrice`, `block.baseFee` can also help.


***Update**: Resolved in [pull request #11](https://github.com/spherex-collab/spherex-protect/pull/11) at commit [51e369f](https://github.com/spherex-collab/spherex-protect/pull/11/commits/51e369f2237f827993184ee7bf5a90570695d710).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | SphereX Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/spherex-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

