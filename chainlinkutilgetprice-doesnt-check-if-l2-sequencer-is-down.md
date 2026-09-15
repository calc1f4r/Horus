---
# Core Classification
protocol: Zaros
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34829
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
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
  - Dacian
---

## Vulnerability Title

`ChainlinkUtil::getPrice` doesn't check if L2 Sequencer is down

### Overview


The bug report describes an issue with using Chainlink on L2 chains like Arbitrum. Due to this bug, smart contracts may not have accurate pricing data, potentially causing users to lose funds. To avoid this issue, the report recommends implementing a check for L2 sequencers, which is demonstrated in Chainlink's official documentation. The bug has been fixed by Zaros in their commits c927d94 and 0ddd913, and has been verified by Cyfrin.

### Original Finding Content

**Description:** When using Chainlink with L2 chains like Arbitrum, smart contracts must [check whether the L2 Sequencer is down](https://medium.com/zaros-labs/chainlink-oracle-defi-attacks-93b6cb6541bf#0faf) to avoid stale pricing data that appears fresh.

**Impact:** Code will execute with prices that don’t reflect the current pricing resulting in a potential loss of funds for users.

**Recommended Mitigation:** Chainlink’s official documentation provides an [example](https://docs.chain.link/data-feeds/l2-sequencer-feeds#example-code) implementation of checking L2 sequencers.

**Zaros:** Fixed in commits [c927d94](https://github.com/zaros-labs/zaros-core/commit/c927d94d20f74c6c4e5bc7b7cca1038a6a7aa5e9) & [0ddd913](https://github.com/zaros-labs/zaros-core/commit/0ddd913eb9d8c7ac440f2814db8bff476f827c7b#diff-dc206ca4ca1f5e661061478ee4bd43c0c979d77a1ce1e0f30745d766bcd65394R42-R53).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Zaros |
| Report Date | N/A |
| Finders | Dacian |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

