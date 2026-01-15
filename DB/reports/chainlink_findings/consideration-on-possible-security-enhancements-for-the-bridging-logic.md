---
# Core Classification
protocol: Cryptex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52947
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/cc661600-b854-49ec-8d9a-90d164b65f28
source_link: https://cdn.cantina.xyz/reports/cantina_cryptex_february2025.pdf
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
finders_count: 2
finders:
  - Anurag Jain
  - StErMi
---

## Vulnerability Title

Consideration on possible security enhancements for the bridging logic 

### Overview

See description below for full details.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
Depending on the client's needs and logic requirements, the following topics should be researched and documented:

1. **Ordered Execution of Messages**  
   Does the execution of the messages need to be performed in an ordered way? In this case, the `Client.EVM2AnyMessage` message should be configured with the `allowOutOfOrderExecution` flag turned to false (see the relative Chainlink documentation). It's important to note that not every chain supports this flag.

2. **Out of Order Message Delivery**  
   There could be scenarios where, even if the `allowOutOfOrderExecution` flag is false, the messages could be delivered out of order (see the Chainlink documentation relative to CCIP Manual Execution). In this case, the client should implement custom logic on the receiving side that ignores (without reverting) all the messages that are "older" compared to the last message that has been successfully processed. This scenario is needed only if the client requires that the messages must be processed in order.

3. **Ignoring Messages with Long Delays**  
   Should a message arrive with a "too long" delay be ignored? The process of bridging a message has some "natural" delay (for example, 15 minutes to wait for a block's finalization on mainnet). Moreover, we need to consider some delay needed for the CCIP processes to verify the message, and there could be accidental delays given by network congestion or additional unexpected scenarios (see the CCIP Manual Execution documentation for more details). Should a message that has taken too long to be delivered, and could be considered "stale", be ignored by the receiver? In this case, the client should attach a `block.timestamp` as part of the payload when the message is delivered, and verify that the time passed since then is below some defined threshold.

4. **Restricting GovernanceCCIPReceiver's Power**  
   The client should consider restricting the "power" of the `GovernanceCCIPReceiver` by using specific roles when it interacts with the target contract. When the message is received and processed inside `GovernanceCCIPReceiver._ccipReceive`, the function's logic will execute a low-level call `target.call(payload)`. The target contract should define and restrict, without providing full-owner access, the logic that the `GovernanceCCIPReceiver` can execute.

## Recommendation
Cryptex should consider all the above questions and implement the needed security measures depending on their needs and expectations. The above list should be seen as a non-exhaustive example of the possible topics to further research.

## Cryptex
1. **Ordered Execution of Messages**  
   We have evaluated our use cases and we currently do not have any requirements for ordered transactions. However, any transaction that requires order, we take it upon ourselves to create the following transaction after the previous one has successfully executed.

2. **Out of Order Message Delivery**  
   We have set `allowOutOfOrderExecution` to true for all transactions. This way we take it upon ourselves to handle order manually.

3. **Ignoring Messages with Long Delays**  
   We don't have any need for time-sensitive messages at the moment.

4. **Restricting GovernanceCCIPReceiver's Power**  
   The client should consider restricting the "power" of the `GovernanceCCIPReceiver` by using specific roles when it interacts with the target contract. Almost all contracts that will be owned by `GovernanceCCIPReceiver` inherit from `AccessControl`, and we will make sure that we will limit the roles for `GovernanceCCIPReceiver`.

## Cantina Managed
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Cryptex |
| Report Date | N/A |
| Finders | Anurag Jain, StErMi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_cryptex_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/cc661600-b854-49ec-8d9a-90d164b65f28

### Keywords for Search

`vulnerability`

