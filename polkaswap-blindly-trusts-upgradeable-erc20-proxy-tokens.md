---
# Core Classification
protocol: Polkaswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48888
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf
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
finders_count: 2
finders:
  - Dominik Czarnota
  - Artur Cygan
---

## Vulnerability Title

Polkaswap blindly trusts upgradeable ERC20 proxy tokens

### Overview


This bug report is about a problem with data validation in the eth-bridge component of the Polkaswap system. This component does not have a way to automatically track supported tokens that can be upgraded, and it also cannot pause interactions with upgraded tokens until they have been approved. This can lead to issues such as incorrect accounting and potential theft of funds. An attacker could exploit this by upgrading a token to make it de���ationary, causing them to receive more tokens on the SORA Network than they deposited. The report recommends temporarily disabling support for upgradeable tokens and implementing an automated upgrade-tracking mechanism to prevent this issue from occurring.

### Original Finding Content

## Type: Data Validation
## Target: eth-bridge

### Difficulty: High

### Description
The Polkaswap system does not have an automated mechanism for tracking supported tokens implemented via a proxy contract, which can be upgraded; nor can it pause interactions with a token that has been upgraded pending the token’s approval. As part of an upgrade, a token’s semantics may change such that the token violates the Polkaswap system’s assumptions. This can lead to problems such as incorrect accounting or could leave the Polkaswap system vulnerable to theft or a loss of funds.

### Exploit Scenario
A proxy token supported by the Polkaswap system performs an upgrade and changes its semantics, becoming deflationary. As a result, in each transfer of this token, a fraction of the transferred amount is burned. An attacker finds that Polkaswap cannot handle deflationary tokens and transfers his tokens to the SORA Network. The ERC20 balance of the attacker’s SORA Network account is then higher than the amount of his deposit, allowing the attacker to spend more tokens than he transferred.

### Recommendations
Short term, disable support for upgradeable (proxy) tokens in the Polkaswap system. (See Appendix D for a list of these tokens.) Then implement an automated upgrade-tracking mechanism and have the system pause interactions with upgraded tokens until they have received approval by consensus.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Polkaswap |
| Report Date | N/A |
| Finders | Dominik Czarnota, Artur Cygan |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf

### Keywords for Search

`vulnerability`

