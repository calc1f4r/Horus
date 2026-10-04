---
# Core Classification
protocol: Superform
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40364
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/bd046a21-6683-498a-b0e0-fc641e47191a
source_link: https://cdn.cantina.xyz/reports/cantina_solo_superform_jul2024.pdf
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
finders_count: 3
finders:
  - cergyk
  - GiuseppeDeLaZara
  - Akshay Srivastav
---

## Vulnerability Title

DeBridgeValidator::validateTxData missing destination chain equals liquidity destination chain check 

### Overview


The bug report is about a potential issue in the DeBridgeForwarderValidator and DeBridgeValidator smart contracts. When making a cross-chain deposit, a message is sent through the AMB (Arbitrary Message Bridge) to the same chain. However, not all IBridgeValidator implementations check for this message, which could result in lost funds if the destination chains are set differently. The recommendation is to add a check in SocketValidator.sol and DeBridgeValidator.sol to ensure that the destination chain matches the liquidity destination chain. This issue has been fixed in a recent commit.

### Original Finding Content

## Cross-Chain Deposit Security Check

## Context
- **File Locations**: 
  - `DeBridgeForwarderValidator.sol#L95`
  - `DeBridgeValidator.sol#L64`

## Description
In the case of a cross-chain deposit, an arbitrary message is sent through the AMB alongside liquidity and to the same chain. This is checked in some of the `IBridgeValidator` implementations but not all, and could cause lost funds if there is a user mistake setting these destination chains to be different.

## Recommendation
Add a check that `args_.dstChainId == args_.liqDstChainId` in the deposit case in `SocketValidator.sol` and `DeBridgeValidator.sol`:

- **DebridgeValidator.sol#L72**:
  ```solidity
  if (args_.deposit) {
      if (args_.srcChainId == args_.dstChainId) {
          revert Error.INVALID_ACTION();
      }
      + if (args_.dstChainId != args_.liqDstChainId) {
      +    revert Error.INVALID_ACTION();
      + }
  }
  ```

## Superform
Fixed in commit `2766fac0`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Superform |
| Report Date | N/A |
| Finders | cergyk, GiuseppeDeLaZara, Akshay Srivastav |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_solo_superform_jul2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/bd046a21-6683-498a-b0e0-fc641e47191a

### Keywords for Search

`vulnerability`

