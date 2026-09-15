---
# Core Classification
protocol: Putty
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2937
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-06-putty-contest
source_link: https://code4rena.com/reports/2022-06-putty
github_link: https://github.com/code-423n4/2022-06-putty-findings/issues/285

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

protocol_categories:
  - dexes
  - synthetics
  - leveraged_farming
  - payments
  - options_vault

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - swit
  - 0xsanson
  - Metatron
  - berndartmueller
  - Lambda
---

## Vulnerability Title

[M-04] Put options are free of any fees

### Overview


This bug report is about a vulnerability in PuttyV2.sol, a smart contract used for trading options. The vulnerability is that fees are not charged when put options are exercised. Put options are options that give the holder the right to sell an asset at a certain price. When a put option is exercised, the holder receives the strike price (the price the option was bought at) denominated in order.baseAsset. Call options, on the other hand, give the holder the right to buy an asset at a certain price, and when a call option is exercised, the holder sends the strike price to Putty and the short position holder is able to withdraw the strike amount. 

The bug report provides proof of concept for the vulnerability. It states that the protocol fee is correctly charged for exercised calls, but that put options are free of any fees. The code for this is provided in the report. 

The recommended mitigation step for this vulnerability is to charge fees also for exercised put options.

### Original Finding Content

_Submitted by berndartmueller, also found by 0xsanson, hubble, Lambda, Metatron, and swit_

Fees are expected to be paid whenever an option is exercised (as per the function comment on [L235](https://github.com/code-423n4/2022-06-putty/blob/3b6b844bc39e897bd0bbb69897f2deff12dc3893/contracts/src/PuttyV2.sol#L235)).

#### Put options

If a put option is exercised, the exerciser receives the strike price (initially deposited by the short position holder) denominated in `order.baseAsset`.

#### Call options

If a call option is exercised, the exerciser sends the strike price to Putty and the short position holder is able to withdraw the strike amount.

However, the current protocol implementation is missing to deduct fees for exercised put options. Put options are free of any fees.

### Proof of Concept

The protocol fee is correctly charged for exercised calls:

[PuttyV2.withdraw](https://github.com/code-423n4/2022-06-putty/blob/3b6b844bc39e897bd0bbb69897f2deff12dc3893/contracts/src/PuttyV2.sol#L494-L506)

```solidity
// transfer strike to owner if put is expired or call is exercised
if ((order.isCall && isExercised) || (!order.isCall && !isExercised)) {
    // send the fee to the admin/DAO if fee is greater than 0%
    uint256 feeAmount = 0;
    if (fee > 0) {
        feeAmount = (order.strike * fee) / 1000;
        ERC20(order.baseAsset).safeTransfer(owner(), feeAmount); // @audit DoS due to reverting erc20 token transfer (weird erc20 tokens, blacklisted or paused owner; erc777 hook on owner receiver side can prevent transfer hence reverting and preventing withdrawal) - use pull pattern @high  // @audit zero value token transfers can revert. Small strike prices and low fee can lead to rounding down to 0 - check feeAmount > 0 @high  // @audit should not take fees if renounced owner (zero address) as fees can not be withdrawn @medium
    }

    ERC20(order.baseAsset).safeTransfer(msg.sender, order.strike - feeAmount); // @audit fee should not be paid if strike is simply returned to short owner for expired put @high

    return;
}
```

Contrary, put options are free of any fees:

[PuttyV2.sol#L450-L451](https://github.com/code-423n4/2022-06-putty/blob/3b6b844bc39e897bd0bbb69897f2deff12dc3893/contracts/src/PuttyV2.sol#L450-L451)

```solidity
// transfer strike from putty to exerciser
ERC20(order.baseAsset).safeTransfer(msg.sender, order.strike);
```

### Recommended Mitigation Steps

Charge fees also for exercised put options.

**[outdoteth (Putty Finance) commented](https://github.com/code-423n4/2022-06-putty-findings/issues/285#issuecomment-1176533283):**
 > Fees are only applied on puts if they are expired.

**[HickupHH3 (judge) commented](https://github.com/code-423n4/2022-06-putty-findings/issues/285#issuecomment-1179907369):**
 > Making this the primary issue for the med severity issue, as per my comment in [#269](https://github.com/code-423n4/2022-06-putty-findings/issues/269):
> > "Put option not being charged fee upon exercising it. This can be considered to the "protocol leaked value" and thus be given a medium severity rating."

**[outdoteth (Putty Finance) confirmed and resolved](https://github.com/code-423n4/2022-06-putty-findings/issues/285#issuecomment-1185411614):**
 > PR with fix: https://github.com/outdoteth/putty-v2/pull/4.

**hyh (warden) reviewed mitigation:**
 > The same fix as in [H-01](https://github.com/code-423n4/2022-06-putty-findings/issues/269).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Putty |
| Report Date | N/A |
| Finders | swit, 0xsanson, Metatron, berndartmueller, Lambda, hubble |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-putty
- **GitHub**: https://github.com/code-423n4/2022-06-putty-findings/issues/285
- **Contest**: https://code4rena.com/contests/2022-06-putty-contest

### Keywords for Search

`vulnerability`

