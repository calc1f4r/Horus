---
# Core Classification
protocol: Berabot
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45357
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Berabot-Security-Review.md
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

[M-03] Not Being Able To Manage Configurations Appropriately Allows Users to Avoid Fees

### Overview


This bug report discusses a medium risk issue with the `isAmmPair` variable in the Berabot token. This variable is used to track AMMs (automated market makers) and apply fees on transfers to and from those pools. However, the constructor only sets one pool and there are no other functions to add more pools. This means that users can avoid paying fees by using a different pool. Additionally, there are several other settings that cannot be changed once set, such as the fee whitelist and trading status. The team has fixed this issue and recommends making all settings adjustable by the owner.

### Original Finding Content

## Severity

Medium Risk

## Description

The `isAmmPair` variable is used to track the AMMs in order for the Berabot token to know when to apply fees on transfers from and to such pools. The uniswap V2 WBERA/BerabotToken pool is the one being set in the constructor but there are no other functions that can add other pools to the `isAmmPair`.

Users can decide to avoid this pool and use another WBERA/BerabotToken pool for their swaps to not pay fees to the protocol.

On a separate note:

- Addresses can be added to the fee whitelist (`_feesWhitelisted`) but cannot be removed.
- `_isMaxWalletExcluded` can't be updated outside of the constructor.
- Trading can be turned on but not stopped (`isTradingOpen`) and `limitMaxWallet` can be turned off but not on after that.
- In BerabotRouter, `addRouterV2()` and `addRouterV3()` once the configurations are set they cannot be changed. If they are set incorrectly the contract might need to be upgraded in order to change the configs.

## Impact

Users can avoid paying fees by using different pools.

Once set many configurations cannot be changed without needing an upgrade or redeploy. If the token contract is already widely used redeploying might not be possible.

## Recommendation

It is recommended that all settings be adjustable by the owner.

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Berabot |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Berabot-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

