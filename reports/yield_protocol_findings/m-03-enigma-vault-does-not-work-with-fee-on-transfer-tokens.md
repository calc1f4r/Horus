---
# Core Classification
protocol: Steakhut
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44175
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/SteakHut-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-03] Enigma Vault Does Not Work With `Fee-On-Transfer` Tokens

### Overview


The report discusses a medium risk bug in the Enigma Vault contract. The bug affects tokens with a fee-on-transfer mechanism, causing problems with the deposit and withdrawal functions. This could potentially result in fund loss and stuck balances for users. The attack scenario outlines how the bug could be exploited and the recommendation is to check token balances before and after transfers to ensure accuracy. The team has acknowledged the bug and plans to update the whitepaper.

### Original Finding Content

## Severity

Medium Risk

## Description

Currently, the contract is not compatible with tokens that have a fee-on-transfer. This problem affects not only the deposit function, where users might receive more shares than the actual number of tokens received by the Enigma Vault but also poses a problem for the withdrawal function.

## Impact

It could lead to fund loss if a token with a fee-on-transfer mechanism is used and not properly handled in Enigma Vault, it can result in stuck balances of this token of users. Such tokens for example are `PAXG`, while `USDT` has a built-in fee-on-transfer mechanism that is currently switched off.

## Attack Scenario

1. Alice attempts to withdraw `10,000e18` shares from the vault using the `withdraw()` function.
2. The strategy separates the corresponding amount of liquidity tokens into `token0` and `token1`.
3. The vault initiates a transfer of the respective `amount0` and `amount1` from the strategy contract to the user. However, if the tokens include a fee on transfer, there's a possibility that the strategy might not have enough tokens to complete the transfer.
4. Due to the shortfall in tokens caused by the transfer fee, the `withdraw` function ultimately fails and reverts.

## Recommendation

As the protocol is intended to support any `ERC20` token, it is recommended to check the balance before and after the transfer and validate if the result is the same as the amount argument provided.

## Team Response

Acknowledged and decided to update the whitepaper.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Steakhut |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/SteakHut-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

