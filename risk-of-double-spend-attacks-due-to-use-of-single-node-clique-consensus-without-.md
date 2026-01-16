---
# Core Classification
protocol: Scroll, l2geth
chain: everychain
category: uncategorized
vulnerability_type: chain_reorganization_attack

# Attack Vector Details
attack_type: chain_reorganization_attack
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26696
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-08-scrollL2geth-initial-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-08-scrollL2geth-initial-securityreview.pdf
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
  - chain_reorganization_attack

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Damilola Edwards
  - Benjamin Samuels
---

## Vulnerability Title

Risk of double-spend attacks due to use of single-node Clique consensus without ﬁnality API

### Overview


This bug report is about a Denial of Service vulnerability in l2geth, a decentralized platform that uses the Clique consensus protocol. This protocol is not designed for single-node networks, and an attacker-controlled sequencer node can exploit the vulnerability to produce multiple conflicting forks of the chain and double-spend attacks. This vulnerability is compounded by the lack of an API for end-users to determine whether their transaction has been finalized on the L1 network, forcing them to use ineffective block/time delays.

Clique consensus is a replacement for proof-of-work consensus for Ethereum testnets. It uses the same fork choice rule as Ethereum's proof-of-work consensus, where the fork with the highest difficulty should be considered the canonical fork. However, Clique consensus does not use proof-of-work and cannot update block difficulty using the traditional calculation. This means that in a single-node network, all forks produced by the sequencer will have the same difficulty value, making it impossible to determine which fork is canonical at a given block height.

The exploit scenario involves an attacker taking control of l2geth's centralized sequencer node and modifying it to produce two forks: one with a deposit transaction to a centralized exchange, and one without. The attacker publishes the first fork and the exchange processes the deposit. The attacker then stops generating blocks on the public fork, generates an extra block on the private fork, and publishes the private fork to cause a re-organization across syncing nodes.

To mitigate this vulnerability, short-term recommendations include adding API methods and documentation to ensure that bridges and centralized exchanges query only for transactions that have been proved and finalized on the L1 network. Long-term recommendations include decentralizing the sequencer in such a way that a majority of sequencers must collude in order to successfully execute a double-spend attack, as well as introducing a slashing mechanism to penalize sequencers that sign conflicting blocks.

### Original Finding Content

## Diﬃculty: Medium

## Type: Denial of Service

## Description
l2geth uses the proof-of-authority Clique consensus protocol, defined by EIP-255. This consensus type is not designed for single-node networks, and an attacker-controlled sequencer node may produce multiple conflicting forks of the chain to facilitate double-spend attacks.

The severity of this finding is compounded by the fact that there is no API for an end user to determine whether their transaction has been finalized by L1, forcing L2 users to use ineffective block/time delays to determine finality.

Clique consensus was originally designed as a replacement for proof-of-work consensus for Ethereum testnets. It uses the same fork choice rule as Ethereum’s proof-of-work consensus; the fork with the highest “difficulty” should be considered the canonical fork.

Clique consensus does not use proof-of-work and cannot update block difficulty using the traditional calculation; instead, block difficulty may be one of two values:
- “1” if the block was mined by the designated signer for the block height
- “2” if the block was mined by a non-designated signer for the block height

This means that in a network with only one authorized signer, all of the blocks and forks produced by the sequencer will have the same difficulty value, making it impossible for syncing nodes to determine which fork is canonical at the given block height.

In a normal proof-of-work network, one of the proposed blocks will have a higher difficulty value, causing syncing nodes to reorganize and drop the block with the lower difficulty value. In a single-validator proof-of-authority network, neither block will be preferred, so each syncing node will simply prefer the first block they received.

This finding is not unique to l2geth; it will be endemic to all L2 systems that have only one authorized sequencer.

## Exploit Scenario
An attacker acquires control over l2geth’s centralized sequencer node. The attacker modifies the node to prove two forks: one fork containing a deposit transaction to a centralized exchange, and one fork with no such deposit transaction. The attacker publishes the first fork, and the centralized exchange picks up and processes the deposit transaction. The attacker continues to produce blocks on the second private fork. Once the exchange processes the deposit, the attacker stops generating blocks on the public fork, generates an extra block to make the private fork longer than the public fork, then publishes the private fork to cause a re-organization across syncing nodes. This attack must be completed before the sequencer is required to publish a proof to L1.

## Recommendations
Short term, add API methods and documentation to ensure that bridges and centralized exchanges query only for transactions that have been proved and finalized on the L1 network.

Long term, decentralize the sequencer in such a way that a majority of sequencers must collude in order to successfully execute a double-spend attack. This design should be accompanied by a slashing mechanism to penalize sequencers that sign conflicting blocks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Scroll, l2geth |
| Report Date | N/A |
| Finders | Damilola Edwards, Benjamin Samuels |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-08-scrollL2geth-initial-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-08-scrollL2geth-initial-securityreview.pdf

### Keywords for Search

`Chain Reorganization Attack`

