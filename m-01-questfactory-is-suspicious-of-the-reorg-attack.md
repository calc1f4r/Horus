---
# Core Classification
protocol: RabbitHole
chain: everychain
category: uncategorized
vulnerability_type: chain_reorganization_attack

# Attack Vector Details
attack_type: chain_reorganization_attack
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8852
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-rabbithole-quest-protocol-contest
source_link: https://code4rena.com/reports/2023-01-rabbithole
github_link: https://github.com/code-423n4/2023-01-rabbithole-findings/issues/661

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 2.8

# Context Tags
tags:
  - chain_reorganization_attack

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - V_B
---

## Vulnerability Title

[M-01] QuestFactory is suspicious of the reorg attack

### Overview


A bug has been discovered in the QuestFactory.sol contract, which is part of the Quest Protocol. The `createQuest` function deploys a quest contract using the `create` command, where the address derivation depends only on the `QuestFactory` nonce. This is a problem for some of the chains (Polygon, Optimism, Arbitrum) to which the `QuestFactory` will be deployed, as they are vulnerable to reorg attacks. 

In a reorg attack, Bob can call `createQuest` and create a quest with an address to which Alice sends funds. As a result, Alice's funds can be withdrawn by Bob. This could lead to the theft of user funds, which is a serious issue.

To mitigate this issue, it is recommended to deploy the quest contract via `create2` with `salt` that includes `msg.sender` and `rewardTokenAddress_`. This will help to ensure that the address derivation is secure, and users will not be at risk of having their funds stolen.

### Original Finding Content

## Lines of code

https://github.com/rabbitholegg/quest-protocol/blob/8c4c1f71221570b14a0479c216583342bd652d8d/contracts/QuestFactory.sol#L75
https://github.com/rabbitholegg/quest-protocol/blob/8c4c1f71221570b14a0479c216583342bd652d8d/contracts/QuestFactory.sol#L108


## Vulnerability details

## Description

The `createQuest` function deploys a quest contract using the `create`, where the address derivation depends only on the `QuestFactory` nonce. 

At the same time, some of the chains (Polygon, Optimism, Arbitrum) to which the `QuestFactory` will be deployed are suspicious of the reorg attack.

- https://polygonscan.com/blocks_forked

![](https://i.imgur.com/N8tDUVX.png)

Here you may be convinced that the Polygon has in practice subject to reorgs. Even more, the reorg on the picture is 1.5 minutes long. So, it is quite enough to create the quest and transfer funds to that address, especially when someone uses a script, and not doing it by hand.

Optimistic rollups (Optimism/Arbitrum) are also suspect to reorgs since if someone finds a fraud the blocks will be reverted, even though the user receives a confirmation and already created a quest.

## Attack scenario

Imagine that Alice deploys a quest, and then sends funds to it. Bob sees that the network block reorg happens and calls `createQuest`. Thus, it creates `quest` with an address to which Alice sends funds. Then Alices' transactions are executed and Alice transfers funds to Bob's controlled quest. 

## Impact

If users rely on the address derivation in advance or try to deploy the wallet with the same address on different EVM chains, any funds sent to the wallet could potentially be withdrawn by anyone else. All in all, it could lead to the theft of user funds.

## Recommended Mitigation Steps

Deploy the quest contract via `create2` with `salt` that includes `msg.sender` and `rewardTokenAddress_`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 2.8/5 |
| Audit Firm | Code4rena |
| Protocol | RabbitHole |
| Report Date | N/A |
| Finders | V_B |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-rabbithole
- **GitHub**: https://github.com/code-423n4/2023-01-rabbithole-findings/issues/661
- **Contest**: https://code4rena.com/contests/2023-01-rabbithole-quest-protocol-contest

### Keywords for Search

`Chain Reorganization Attack`

