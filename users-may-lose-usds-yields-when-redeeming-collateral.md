---
# Core Classification
protocol: Sperax - USDs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59825
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/index.html
source_link: https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/index.html
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
  - Shih-Hung Wang
  - Pavel Shabarkin
  - Ibrahim Abouzied
---

## Vulnerability Title

Users May Lose USDs Yields when Redeeming Collateral

### Overview


The report discusses an issue with the Sperax team's approach to the rebasing mechanism for USDs tokens. The rebasing mechanism is designed to allow users to earn additional tokens by simply holding them. However, the current implementation may result in users losing out on some of their USDs yield if they do not call the `rebase()` function before redeeming their tokens. This is because the `rebase()` function is currently called after the user's tokens are burned, rather than before. The report recommends that the team consider moving the `rebase()` function call before any token transfers or state updates to ensure that the user's balance is up to date before their tokens are burned. This will prevent users from losing out on their USDs yield or receiving less collateral when redeeming their tokens. 

### Original Finding Content

**Update**
**Quantstamp:** The Sperax team acknowledged the issue and explained the reason, however users should be aware that USDs yield could be lost if user will not call `rebase()` function before `redeem()`.

![Image 56: Alert icon](https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/static/media/info-icon-alert.3c9578483b1cf3181c9bfb6fec7dc641.svg)

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> We prefer maintaining the current approach for the following reasons:
> 
> 
> 1.   If we execute the rebase before _redeem, a user might face difficulty redeeming their entire USDs balance as the rebase could increase the user's balance.
> 2.   To address the first issue, we considered adding a redeemFull function that would redeem the entire USDs balance, including any additional amount from the internal rebase. However, this would necessitate users approving additional USDs upfront to accommodate the rebased amount, a step we want to avoid.
> 3.   Chronologically, it is logical for the user to initiate the rebase first by explicitly calling the rebase function and then proceed with redemption.

**File(s) affected:**`contracts/vault/VaultCore.sol`

**Description:** According to the rebasing mechanism design, USDs holders can earn additional USDs as yields by simply holding the token. In a rebasing event, the rebase manager determines the rebase amount, which will be distributed to all USDs holders (except those who opt out) in proportion to their token balance.

The`VaultCore.rebase()`function implements the rebasing logic, which will be triggered whenever a user calls the`mint()`or`redeem()`function on the vault contract. Anyone can also invoke the`rebase()`function.

However, in the`redeem()`function,`rebase()`is called after the user's USDs tokens are burned but not before, which may result in the user receiving less USDs yields if they have a non-zero amount of USDs left after the redemption. Users may receive less collateral in return if they provide all their USDs when redeeming.

In other words, whether the user explicitly calls`rebase()`before`redeem()`or not will affect the USDs yield they earned or the redeemed collateral amount. Users might suffer from fund loss if they did not call`rebase()`before`redeem()`.

**Recommendation:** In the`VaultCore._redeem()`function, consider moving the`rebase()`function call after the input validation checks but before any token transfers or state updates, similar to the approach in the`mint()`function. This way, it will ensure that before the user's USDs are burned, their USDs balance is up to date.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Sperax - USDs |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Pavel Shabarkin, Ibrahim Abouzied |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/index.html

### Keywords for Search

`vulnerability`

