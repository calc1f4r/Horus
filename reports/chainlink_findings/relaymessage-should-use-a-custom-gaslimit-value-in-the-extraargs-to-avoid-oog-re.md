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
solodit_id: 52941
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

relayMessage should use a custom gasLimit value in the extraArgs to avoid OOG reverts on the receiving side 

### Overview

See description below for full details.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
The CCIP framework allows the call of `ccipRouter.ccipSend` to specify in the `Client.EVM2AnyMessage` extra arguments. One of these arguments is `gasLimit` that, by default (when unspecified), is set to `200,000`. The `gasLimit` parameter is quite critical, given that it is the amount of gas used by the CCIP protocol to execute the `ccipReceive()` on the receiving side. If the amount is too low, it could result in a revert because of an Out of Gas exception.

## Recommendation
Cryptex should consider applying the following changes:
- Define a default value of `gasLimit` for every supported destination chain.
- Allow `relayMessage` to specify a custom optional `gasLimit` that will override the default one.
- If the final value of `gasLimit` is not empty (`!= 0`), override it when `Client.EVM2AnyMessage` is created; otherwise, do not specify it to automatically use the default one used by Chainlink.
- Add sanity checks to ensure that the `gasLimit` in the destination's configuration and the input parameter of `relayMessage` is between some safe lower and upper bound.

Cryptex should implement the above suggestions, keeping in mind that:
1. `gasLimit` contributes to the fee paid to Chainlink when `ccipRouter.ccipSend` is executed.
2. The amount of gas needed will be the one to both execute `GovernanceCCIPReceiver._ccipReceive` and the custom logic on the target contract when `(bool success, ) = target.call(payload);` is executed.

For this reason, it is also suggested to evaluate for each case what the correct custom value that should be specified for `gasLimit` is when `GovernanceCCIPRelay.relayMessage` is executed. More information related to the `gasLimit` extra attribute can be found in the Chainlink CCIP Best Practice documentation.

## Cryptex
Implemented in PR 172. The following changes were made:
- `gasLimit` has been made a parameter in the `relayMessage` function.
- Min and Max checks are added for the `gasLimit`.

## Cantina Managed
Fix verified.

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

