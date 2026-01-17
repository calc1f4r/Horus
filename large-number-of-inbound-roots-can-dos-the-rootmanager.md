---
# Core Classification
protocol: Connext
chain: everychain
category: uncategorized
vulnerability_type: broken_loop

# Attack Vector Details
attack_type: broken_loop
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7138
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - broken_loop

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Xiaoming90
  - Blockdev
  - Gerard Persoon
  - Sawmon and Natalie
  - Csanuragjain
---

## Vulnerability Title

Large number of inbound roots can DOS the RootManager

### Overview


This bug report is about a possible Denial of Service (DOS) attack against the RootManager.sol of the Gnosis Hub. The attack would involve a malicious user calling the permissionless GnosisSpokeConnector.send function multiple times within a single transaction/block, which would cause a large number of outboundRoots to be forwarded to GnosisHubConnector on Ethereum. This would result in a large number of outboundRoots with the same commit-Block being added to the pendingInboundRoots queue. When the RootManager.propagate function is triggered, the dequeueVerified function is called to dequeue the verified outboundRoots from the queue, which could result in an Out-of-Gas error and cause a revert. If the RootManager.propagate function reverts, the latest aggregated Merkle root cannot be forwarded to the spokes, and none of the messages can be proven and processed on the destination chains. 

To mitigate this issue, two solutions are recommended: (1) Place restrictions on the SpokeConnector's send function so that the outbound root will only be forwarded to the hub when the last root sent is different from the current root to be sent, and an execution interval has elapsed; (2) Bound the number of outbound roots that can be aggregated per call, and allow them to be processed in batches (if needed). The issue has been solved in PR 2199 and PR 2545, and verified by Spearbit.

### Original Finding Content

## Severity: High Risk

## Context
RootManager.sol#L154-L163

## Description
It is possible to perform a DOS against the RootManager by exploiting the `dequeueVerified` function or `insert` function of the RootManager.sol. The following describes the possible attack path:

1. Assume that a malicious user calls the permissionless `GnosisSpokeConnector.send` function 1000 times (or any number of times that will cause an Out-of-Gas error later) within a single transaction/block on Gnosis, causing a large number of Gnosis's outboundRoots to be forwarded to `GnosisHubConnector` on Ethereum.
2. Since the 1000 outboundRoots were sent at the same transaction/block earlier, all of them should arrive at the `GnosisHubConnector` within the same block/transaction on Ethereum.
3. For each of the 1000 outboundRoots received, the `GnosisHubConnector.processMessage` function will be triggered to process it, which will in turn call the `RootManager.aggregate` function to add the received outboundRoot into the pendingInboundRoots queue. As a result, 1000 outboundRoots with the same commit block will be added to the pendingInboundRoots queue.
4. After the delay period, the `RootManager.propagate` function will be triggered. The function will call the `dequeueVerified` function to dequeue 1000 verified outboundRoots from the pendingInboundRoots queue by looping through the queue. This might result in an Out-of-Gas error and cause a revert.
5. If the above `dequeueVerified` function does not revert, the `RootManager.propagate` function will attempt to insert 1000 verified outboundRoots to the aggregated Merkle tree, which might also result in an Out-of-Gas error and cause a revert.

If the `RootManager.propagate` function reverts when called, the latest aggregated Merkle root cannot be forwarded to the spokes. As a result, none of the messages can be proven and processed on the destination chains.

**Note:** The processing on the Hub (which is on mainnet) can also become very expensive, as the mainnet usually has a far higher gas cost than the Spoke.

## Recommendation
Both solutions should be implemented to sufficiently mitigate this issue.

1. Place restrictions on the `SpokeConnector`'s `send` function. The `send` function should be restricted so that the domain's outbound root will only be forwarded to the hub when the following conditions are met:
   - If the last root sent is different from the current root to be sent.
   - After the execution interval has lapsed (e.g. only able to trigger the `send` function once every few minutes) - This is to prevent a malicious user from bypassing the first measure (`lastRootSent != outboundRoot`) by sending a cheap message to trigger the dispatch function to change the outboundRoot to a new one before calling the `send` function.

2. Bound the number of outbound roots that can be aggregated per call, and allow them to be processed in batches (if needed).

## Connext
Solved in PR 2199 and PR 2545.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | Xiaoming90, Blockdev, Gerard Persoon, Sawmon and Natalie, Csanuragjain |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf

### Keywords for Search

`Broken Loop`

