---
# Core Classification
protocol: LMAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46973
audit_firm: OtterSec
contest_link: https://lmao.fun/
source_link: https://lmao.fun/
github_link: https://github.com/LMAOFUN/lmao-program

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
  - Robert Chen
---

## Vulnerability Title

Lack of Slippage Checks in Trading

### Overview


The report highlights a vulnerability in the coin_trade instruction that can result in unexpected losses for users. This is due to a lack of slippage checks, which can lead to trades being executed at significantly different prices than anticipated. A similar issue exists in the raydium_trade instruction, making it vulnerable to price manipulation through front-running attacks. To fix this issue, slippage checks need to be enforced in both instructions. The vulnerability has been addressed in the latest patches, 0ee201f and ee97ae4.

### Original Finding Content

## Vulnerabilities in Trading Instructions

The lack of slippage checks in the `coin_trade` instruction presents a significant vulnerability, primarily because it exposes the trading process to risks associated with market volatility, rendering the trades vulnerable to sudden market price changes and potential front-running attacks. Due to a lack of enforcement of slippage checks, if the asset price moves unfavorably, the user may buy or sell at a significantly different price than anticipated, resulting in unexpected losses. A similar issue exists in `raydium_trade`.

Moreover, the instruction lacks a mechanism to limit the maximum acceptable price change for a trade, making it vulnerable to price manipulation through sandwich attacks via front-running. In this scenario, an attacker monitoring the network identifies a large trade about to be executed. Consequently, they may front-run this transaction to submit their own transactions to manipulate the price, resulting in the victim’s trade being executed at an unfavorable price. After the victim’s trade is executed, the attacker may reverse their initial trade, reversing their initial position and profiting from the manipulated price.

## Remediation

Ensure that slippage checks are mandatorily performed in the `raydium_trade` and `coin_trade` instructions.

### Patch

Resolved in `0ee201f` and `ee97ae4`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | LMAO |
| Report Date | N/A |
| Finders | Robert Chen |

### Source Links

- **Source**: https://lmao.fun/
- **GitHub**: https://github.com/LMAOFUN/lmao-program
- **Contest**: https://lmao.fun/

### Keywords for Search

`vulnerability`

