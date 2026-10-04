---
# Core Classification
protocol: Origin Dollar Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10785
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/origin-dollar-audit/
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

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[L02] Cannot redeem from both accounts simultaneously

### Overview

See description below for full details.

### Original Finding Content

When redeeming OUSD tokens, the `VaultCore` contract will retrieve all the tokens from either [its own buffer](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L202) or [the default strategy](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultCore.sol#L208). However, if neither the buffer nor the strategy has sufficient balance individually, the transfer will fail, even if the combined balance is large enough and the redemption is valid. This could occur for large redemptions or unbalanced stablecoin reserves, and gets worse when the [`vaultBuffer`](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultStorage.sol#L74) is high.


Consider withdrawing from both the buffer and the strategies when required.


**Update:** *Not fixed. The Origin team states:*



> We are going to keep this the way it for now. We would rather have less complexity in the code here. The buffer in OUSD is a gas optimization to keep gas usage from being extremely expensive during non-huge mints and redeems, and only needs to keep a very small portion of the total vault value in the buffer. Right now, it’s targeting a half a percent of the assets, and as the asset amount goes up further, this percentage will be lowered more. While there remains a reasonable amount of assets in OUSD, this shouldn’t be a problem. In the case that almost all assets are being withdrawn, it should still be possible to get funds out, it just may take carefully chosen withdrawal amounts.
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Origin Dollar Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/origin-dollar-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

