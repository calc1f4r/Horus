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
solodit_id: 48891
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Ethereum bridge cannot handle chain reorganizations

### Overview


Report Summary:

This bug report is about a problem with the SORA Network's integration with Ethereum through the eth-bridge pallet. The code does not detect Ethereum chain reorganizations, which can lead to an exploit scenario where an attacker can deposit ETH and have it added to their account on the SORA Network. The report recommends adding code to detect reorganizations and implementing a strategy for handling them in the short and long term. References to similar issues with Ethereum Classic are also provided.

### Original Finding Content

## Type: Data Validation
**Target:** eth-bridge

**Diﬃculty:** High

## Description
The SORA Network integrates with Ethereum through the `eth-bridge` pallet, which monitors events emitted by the bridge contract. The `eth-bridge` code does not detect Ethereum chain reorganizations or include any strategy for handling them. The code processes all blocks through the highest block except for the newest blocks (specifically the 30 newest blocks, since the `CONFIRMATION_INTERVAL` constant is set to 30). This reduces the likelihood that the SORA Network will observe a reorganization.

## Exploit Scenario
An attacker deposits ETH by calling the `sendEthToSidechain` function, and `eth-bridge` registers the event and adds funds to the attacker’s account on the SORA Network. An Ethereum chain reorganization occurs, and the `Deposit` event does not exist in the reorganized chain. The funds added to the attacker’s account are not reclaimed by the chain.

## Recommendations
**Short term:** Add code to `eth-bridge` to detect Ethereum reorganizations by comparing block hashes. Ensure that the code fetches blocks starting from the last processed block and compares that block’s hash to the hash of the corresponding block (the block at the same height) returned by the API. If the hashes differ, a reorganization has occurred. Finally, design and document a reorganization-handling strategy.

**Long term:** Implement a strategy for automated reorganization handling. After detecting a reorganization, the algorithm should calculate which events need to be unapplied and which new events are missing from the blockchain. Additionally, design a strategy for handling negative balances, which can occur when events are unapplied.

## References
- Ethereum Classic Suffers Reorganization That Resembles 51% Attack Amid Miner Complications

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

