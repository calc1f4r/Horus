---
# Core Classification
protocol: Mantle Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19468
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/mantle/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/mantle/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

TSS Nodes Reporting Slashing Are Vulnerable To Front Running

### Overview


A bug was reported in Mantle L2 Rollup that TSS nodes can be frontrun and miss out on rewards. This happens because the information needed to report a node slashing does not contain any information unique to the sender, meaning it can be copied and if the new sender submits a higher gas price their transaction will be included prior to the original node sender. To resolve this issue, Mantle suggested that TSS node operators should use a submission mechanism that does not display their transaction to the Ethereum mempool such as flashbots. Alternatively, the node who reported the slashing off-chain should be stored as part of the signed message. The issue was resolved in PR #826 by paying all slashing rewards directly to a regulatory account.

### Original Finding Content

## Description

Reporting nodes can be front run and miss out on rewards. TSS nodes are responsible for broadcasting off-chain node slashing decisions on-chain; however, it is possible for any other user to read this transaction information while it is in the Ethereum mempool and front-run the report. This will result in the reporting node not receiving the reward they are entitled to for sending the transaction.

This happens because the information needed to report a node slashing does not contain any information unique to the sender, meaning it can be copied and if the new sender submits a higher gas price, their transaction will be included prior to the original node sender. Then, the main slashing reward is allocated to `msg.sender` on line [306] in `packages/contracts/contracts/L1/tss/TssStakingSlashing.sol`. This conflicts with Mantle’s intention, which is outlined in documentation as "rewards the TSS-node that submits the slashing message, and rewards the person who participates in the report."

## Recommendations

One possible solution would be to make TSS node operators aware that this can happen and that they need to use a submission mechanism that does not display their transaction to the Ethereum mempool, such as Flashbots. Alternatively, the node who reported the slashing off-chain should be stored as part of the signed message; this way, it can be used to verify that the addressing being rewarded matches the reporting node. While this could cause problems if this node then goes offline and is unable to report on-chain, other participating nodes do have an incentive to report the issue as they receive a (smaller) bounty too.

## Resolution

The issue has been resolved in PR #826. The resolution is to pay all slashing rewards directly to a regulatory account. On line [309], the second parameter to `slashShares()` has been modified to `regulatoryAccount`, which represents the address to receive payouts from a slashing.

`TssDelegationManager(tssDelegationManagerContract).slashShares(stakerS[i], regulatoryAccount, delegationShares, tokens, delegationShareIndexes, shareAmounts);`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Mantle Network |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/mantle/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/mantle/review.pdf

### Keywords for Search

`vulnerability`

