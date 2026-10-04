---
# Core Classification
protocol: Linea V2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32575
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/linea-v2-audit
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Sequencer Censorship Issues

### Overview

See description below for full details.

### Original Finding Content

The design of the system exposes multiple points at which the sequencer can apply censorship. While the documentation mentions building towards ["enabling Censorship Resistant Withdrawals"](https://docs.linea.build/decentralization-roadmap#phase-2), the current implementation of the contracts and the sequencer has broader censorship implications than withdrawals (L2→L1 transactions):


#### L1→L2 Messages


While L1 messages sent via `sendMessage` after the migration have to be anchored on L2 for the rollup to finalize and continue processing messages, the L1 contract only validates anchoring and does not ensure that they have been claimed. Consequently, if the sequencer chooses to censor the mandatory L2 `claimMessage` transaction for a message, it may never be included, trapping the users' funds inside the L1 contract.


#### Opaque Censorship Due to Uneconomical Content


Gas costs incurred by L2s for including user transactions typically differ in their pricing structure from those of similar L1 transactions. For instance, L1 calldata is significantly more expensive than L2 execution costs, often dominating transaction inclusion costs. This discrepancy usually necessitates a distinct gas pricing model for users compared to the L1 gas pricing model, whereby L1 calldata costs are explicitly calculated and borne directly by the users.


However, Linea's gas pricing model [mimics L1 gas pricing](https://docs.linea.build/use-mainnet/gas-import) and scales the average gas price by a factor of ~15x, without accounting for factors such as L1 calldata costs. Consequently, users posting large calldata transactions, which are relatively more expensive to include, end up paying much less than their actual share of the costs. This shortfall is partially covered by other users, who subsidize calldata-heavy users through higher payments for execution, and partially by the operators if an aggregate shortfall is realized. Moreover, proving costs are also mispriced, with some opcodes/operations being significantly more expensive to prove than others.


Crucially, due to these limitations, the Linea's sequencer's [undocumented role](https://docs.linea.build/architecture/sequencer#what-does-it-do) involves censoring uneconomical transactions. It is tasked with selectively excluding transactions that are economically unviable, deviating from the transparent gas pricing model presented to its users.


This is in contrast to a typical sequencer's role of ordering transactions and including all the correctly submitted ones. Certain design choices allow a documented possibility of censorship, such as the sequencer's ability to censor both L1→L2 and L2→L1 transactions (without the ability to enforce a transaction inclusion from L1). However, such censorship would be detected and considered malicious. In contrast, censorship related to gas pricing is undocumented and likely to occur in practice if needed (e.g., if prompted by a calldata-heavy surge, such as the numerous instances of [inscriptions-related outages and surges](https://www.dlnews.com/articles/defi/arbitrum-blames-hour-long-outage-on-surge-in-network-traffic/)). Relying on censorship as a design decision contradicts the system's intention to be an L2 inheriting the safety and liveness of L1, as censorship represents a liveness failure.


Consider, in the short term, documenting the expected censorship functionality and its implementation in the sequencer so that expected censorship can be distinguished by third-party observers from malicious censorship. In the long term, consider incorporating transaction inclusion rules into the protocol or revising the gas pricing model.


***Update:** Acknowledged, will resolve. The Linea team stated:*



> *The gas pricing model is being revised and a pricing API will be available in the near term. We will add additional documentation explaining how transactions are processed to sustain a working system.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Linea V2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/linea-v2-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

