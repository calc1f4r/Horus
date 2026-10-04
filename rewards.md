---
# Core Classification
protocol: Futureswap V2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11130
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/futureswap-v2-audit/
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

protocol_categories:
  - dexes
  - services
  - derivatives
  - liquidity_manager
  - privacy

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Rewards

### Overview


Futureswap is a decentralized exchange that rewards users for providing liquidity and trading on the exchange. Liquidity providers who keep their liquidity on the exchange for an entire week-long window earn rewards in the form of Futureswap tokens (FST). Similarly, traders who use the exchange also earn FST. When users sign messages to close a trade, their message contains a “referral” address. This address also receives FST rewards, and is a way for third-party UIs to profit from users who use their UI. Users can also add their own address as the “referral” address. FST is a non-transferable token and is used to vote on governance decisions.

### Original Finding Content

Liquidity providers who keep their liquidity in an exchange for an entire week-long window earn rewards in the form of Futureswap tokens (FST). Similarly, users who trade on a Futureswap exchange also earn FST.


When users sign messages to close a trade, their message contains a “referral” address. This address also receives FST rewards, and is a way for third-party UIs to profit from users who user their UI. (Users can, of course, add their own address as the `referral` address).


The FST are non-transferable tokens, and are used to vote on governance decisions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Futureswap V2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/futureswap-v2-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

