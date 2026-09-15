---
# Core Classification
protocol: Ethena
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54376
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/b3a172b2-f80b-4240-935a-75d6b49d0910
source_link: https://cdn.cantina.xyz/reports/cantina_ethena_oct2023.pdf
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
  - Kurt Barry
  - 0x4non
---

## Vulnerability Title

Unusual Choice of Indexing For Some Event Parameters 

### Overview

See description below for full details.

### Original Finding Content

## Event Parameter Indexing in Smart Contracts

## Context

- `IEthenaMintingEvents.sol#L9-L16`
- `IEthenaMintingEvents.sol#L18-L26`
- `IStakedUSDe.sol#L8`
- `IEthenaMintingEvents.sol#L52-L56`

## Description

Generally, it makes sense to mark event parameters as indexed when there is an expectation that consumers of the event will likely only care about the event when that parameter has a certain value. For example, it is logical to make token recipient or source addresses indexed in events, as owners of those addresses will want to know when their address gains or loses tokens. It makes less sense to index the amount of tokens transferred, as it is rare to care about all transfers of a specific value.

Some events make unusual choices about indexing. For example, the Mint and Redeem events in `IEthenaMintingEvents.sol` index the collateral asset, the collateral amount, and the USDe amount; they leave the minter, benefactor, and beneficiary un-indexed. It would be more typical to index the addresses (so involved parties can monitor transactions relevant to them), and to not index the token amounts (which could be confusing if unrelated transactions are being done with identical amounts between different parties; this could even provide a vector for grieving event listeners by intentionally causing them to examine irrelevant events).

Other non-standard choices include indexing the amount parameter of the `RewardsReceived` event in `IStakedUSDe.sol` and the parameters to `MaxMintPerBlockChanged` and `MaxRedeemPerBlockChanged` in `IEthenaMintingEvents.sol#L52-L56`.

## Recommendation

Critically examine the decision to mark each event parameter as indexed or not with a focus on the intended use-case.

## Changes

- **Ethena:** Fixed in commit `99f33341`.
- **Cantina:** Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Ethena |
| Report Date | N/A |
| Finders | Kurt Barry, 0x4non |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_ethena_oct2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/b3a172b2-f80b-4240-935a-75d6b49d0910

### Keywords for Search

`vulnerability`

