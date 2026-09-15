---
# Core Classification
protocol: USSD - Autonomous Secure Dollar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19140
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/82
source_link: none
github_link: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/909

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
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - WATCHPUG
  - T1MOH
---

## Vulnerability Title

H-11: Oracle price should be denominated in DAI instead of USD

### Overview


This bug report is about an issue in the implementation of a rebalancer in USSD which uses DAI as the target of the peg. The problem is that all current oracles return the price denominated in USD instead of DAI. This means that when DAI is over-pegged, the system will automatically drive itself away from the peg to DAI. The attack path described is still valid in the original report. 

The code snippet referenced in the report is from the StableOracleWETH.sol file and can be found at https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/oracles/StableOracleWETH.sol#L12-L27.

The impact of this bug is that when DAI is over-pegged, the system will automatically drive itself away from the peg to DAI. This can lead to the system consuming all its collateral and the profit will be extracted by the arbitrator.

The recommendation is to either change the unit of Oracle price from USD to DAI or change the peg target from DAI to USD. This means that the `getOwnValuation()` should not be used as the peg deviation check standard.

The issue was found by T1MOH and WATCHPUG and was reviewed manually. After discussion, the issue was resolved successfully with the escalations being rejected.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/909 

## Found by 
T1MOH, WATCHPUG
## Summary

## Vulnerability Detail

Per the whitepaper, USSD aims to be pegged to DAI.

The implementation of rebalancer is also using the DAI price of USSD (`getOwnValuation()`) as the target of the peg.

However, all current oracles return the price denominated in USD.

Additionally, all collateral tokens can be used to mint at the oracle price with no fee.

As a result, when DAI is over-pegged, the system will automatically drive itself away from the peg to DAI. The proof of concept for this is as follows:

When the DAI price is 1.1 (over-pegged), and the system is actively maintaining its peg to DAI, the user can:

1. Mint 1100 USSD with 1000 DAI (worth 1100 USD).
2. Sell 1100 USSD for 1100 DAI, driving the USSD to a lower price against DAI, say 1 USSD to 0.98 DAI.
3. Trigger the `rebalance()` function which sells collateral to DAI and buys back USSD to push its price back to 1:1 with DAI.

By repeating steps 1-3, the system will consume all its collateral, and the profit will be extracted by the arbitrator.

## Impact

## Code Snippet

https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/oracles/StableOracleWETH.sol#L12-L27

## Tool used

Manual Review

## Recommendation

Change the unit of Oracle price from USD to DAI.

- DAI should return 1
- WBTC should use WBTC/ETH ETH/DAI
- WETH should use WETH/DAI
- WBGL should use WBGL/WETH ETH/DAI

Or, change the peg target from DAI to USD, which means the `getOwnValuation()` should not be used as the peg deviation check standard.



## Discussion

**0xJuancito**

Escalate for 10 USDC

The report assumes that the attacker would be able to sell 1100 USSD for 1100 DAI:

> 2. Sell 1100 USSD for 1100 DAI, driving the USSD to a lower price against DAI, say 1 USSD to 0.98 DAI.

This wouldn't be possible, as the USSD/DAI pool would be arbitraged and the attacker will only be losing money on each mint. It also assumes manipulating the price, which is already mentioned in https://github.com/sherlock-audit/2023-05-USSD-judging/issues/451.

This can be considered either informational or a duplicate

**sherlock-admin**

 > Escalate for 10 USDC
> 
> The report assumes that the attacker would be able to sell 1100 USSD for 1100 DAI:
> 
> > 2. Sell 1100 USSD for 1100 DAI, driving the USSD to a lower price against DAI, say 1 USSD to 0.98 DAI.
> 
> This wouldn't be possible, as the USSD/DAI pool would be arbitraged and the attacker will only be losing money on each mint. It also assumes manipulating the price, which is already mentioned in https://github.com/sherlock-audit/2023-05-USSD-judging/issues/451.
> 
> This can be considered either informational or a duplicate

You've created a valid escalation for 10 USDC!

To remove the escalation from consideration: Delete your comment.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**ctf-sec**

Emm do not see why this is not possible

> Sell 1100 USSD for 1100 DAI, driving the USSD to a lower price against DAI, say 1 USSD to 0.98 DAI.

the attack path described is still valid in the original report

**hrishibhat**

Result:
High
Has duplicates
The attack is possible and the rebalance is design to create maintain the 1:1 ratio between USSD to DAI.

**sherlock-admin**

Escalations have been resolved successfully!

Escalation status:
- [0xJuancito](https://github.com/sherlock-audit/2023-05-USSD-judging/issues/909/#issuecomment-1605924088): rejected

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | USSD - Autonomous Secure Dollar |
| Report Date | N/A |
| Finders | WATCHPUG, T1MOH |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/909
- **Contest**: https://app.sherlock.xyz/audits/contests/82

### Keywords for Search

`vulnerability`

