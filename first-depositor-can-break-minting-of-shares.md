---
# Core Classification
protocol: Narwhal Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44678
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal Finance.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

First depositor can break minting of shares

### Overview


This report describes a bug in the TradingVaultV2 system where the first depositor can manipulate the share price by depositing a very small amount of liquidity and then artificially inflating the currentBalanceUSDT value. This allows them to withdraw a larger amount of USDT than they initially deposited. The bug has been resolved by implementing a solution used by Uniswap V2, which involves sending the first 1000 LP tokens to the zero address. Developers are advised to ensure that the number of shares to be minted is non-zero to prevent this issue from occurring.

### Original Finding Content

**Severity**: High

**Status**: Resolved

**Description**

The first depositor of an TradingVaultV2 can maliciously manipulate the share price by depositing the lowest possible amount of liquidity and then artificially inflating the currentBalanceUSDT value.
Attacker deposit (NarwhalTradingVault.deposit) 1 wei of USDT, minting 1 share. They receive 1e18 (1 wei) shares.
Attacker calls NarwhalTrading.openTrade, as a result of the calls chain the NarwhalTradingVault.currentBalanceUSDT value  increases to 100e18 + 1. 
Victim deposits 200e18 USDT. Due to a rounding issue in the inflated vault, they receive only 1 share.
Attacker withdraws their 1 share, which is now worth 150 USDT.

**Recommendation**:

Uniswap V2 solved this issue by sending the first 1000 LP tokens to the zero address. The same can be done in this case i.e. when totalSupply() == 0, mint the first min liquidity LP tokens to the zero address to enable share dilution.
Ensure the number of shares to be minted is non-zero: require(_shares != 0, "zero shares minted");

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Narwhal Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

