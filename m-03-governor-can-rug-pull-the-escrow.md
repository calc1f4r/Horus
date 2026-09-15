---
# Core Classification
protocol: The Graph
chain: everychain
category: uncategorized
vulnerability_type: admin

# Attack Vector Details
attack_type: admin
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6180
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-the-graph-l2-bridge-contest
source_link: https://code4rena.com/reports/2022-10-thegraph
github_link: https://github.com/code-423n4/2022-10-thegraph-findings/issues/300

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - admin

protocol_categories:
  - dexes
  - bridge
  - cdp
  - yield
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - cccz
  - d3e4
  - joestakey
  - catchup
---

## Vulnerability Title

[M-03] Governor can rug pull the escrow

### Overview


This bug report is about a vulnerability in the BridgeEscrow contract of the Graph protocol. This vulnerability allows the Governor to approve an arbitrary address to spend any amount from the BridgeEscrow and thus steal all escrowed tokens. This is a severe undermining of decentralization and the reputation of the protocol. The bug was discovered by code inspection. 

The recommended mitigation steps are to restrict access to the `approveAll()` function to the bridge that manages the GRT funds held by the escrow. Alternatively, spending should only be allowed via other protocol functions.

### Original Finding Content


[BridgeEscrow.sol#L28-L30](https://github.com/code-423n4/2022-10-thegraph/blob/309a188f7215fa42c745b136357702400f91b4ff/contracts/gateway/BridgeEscrow.sol#L28-L30)<br>

Governor can rug pull all GRT held by BridgeEscrow, which is a severe undermining of decentralization.

### Proof of Concept

The governor can approve an arbitrary address to spend any amount from BridgeEscrow, so they can steal all escrowed tokens. Even if the governor is well intended, the contract can still be called out which would degrade the reputation of the protocol (e.g. see here: <https://twitter.com/RugDocIO/status/1411732108029181960>). This is especially an issue as the escrowed tokens are never burnt, so the users would need to trust the governor perpetually (not about stealing their L2 tokens, but about not taking a massive amount of L1 tokens for free for themselves).

This seems an unnecessary power granted to the governor and turns a decentralized bridge into a needless bottleneck of centralization.

### Recommended Mitigation Steps

Restrict access to `approveAll()` to the ["bridge that manages the GRT funds held by the escrow"](https://github.com/code-423n4/2022-10-thegraph/blob/309a188f7215fa42c745b136357702400f91b4ff/contracts/gateway/BridgeEscrow.sol#L25). Or, similarly to how `finalizeInboundTransfer` in the gateways is restricted to its respective counterpart, only allow spending via other protocol functions.

**0xean (judge) commented [via issue [#40](https://github.com/code-423n4/2022-10-thegraph-findings/issues/40#issuecomment-1279851479)]:**
 > This is the intended design to allow for multiple bridges in the future. Going to leave open for sponsor review, but may decide to close as invalid.

**pcarranzav (The Graph) disputed and commented [via issue [#40](https://github.com/code-423n4/2022-10-thegraph-findings/issues/40#issuecomment-1282847604)]:**
 > Yes, this is intentional to allow multiple bridges but also to allow for recovery of the funds in case of a critical issue in Arbitrum.

> Note that the Governor is not a regular EOA, but a Gnosis Safe managed by The Graph Council; this account is already able to control many protocol parameters, including adding minters to the GRT contract, so adding this control over the escrow does not change the trust assumption significantly imo.

**0xean (judge) commented [via issue [#40](https://github.com/code-423n4/2022-10-thegraph-findings/issues/40#issuecomment-1287472176)]:**
 > @pcarranzav - totally understand that.  I personally would happily close this issue as invalid, but Code4rena seems to have a pattern of awarding these as Medium to ensure that users are aware of the risk, even as low as it may be.  

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | The Graph |
| Report Date | N/A |
| Finders | cccz, d3e4, joestakey, catchup |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-thegraph
- **GitHub**: https://github.com/code-423n4/2022-10-thegraph-findings/issues/300
- **Contest**: https://code4rena.com/contests/2022-10-the-graph-l2-bridge-contest

### Keywords for Search

`Admin`

