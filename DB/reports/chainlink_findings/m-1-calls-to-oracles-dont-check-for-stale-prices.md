---
# Core Classification
protocol: USSD - Autonomous Secure Dollar
chain: everychain
category: oracle
vulnerability_type: stale_price

# Attack Vector Details
attack_type: stale_price
affected_component: oracle

# Source Information
source: solodit
solodit_id: 19141
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/82
source_link: none
github_link: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/31

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 1

# Context Tags
tags:
  - stale_price
  - oracle

protocol_categories:
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 88
finders:
  - J4de
  - Dug
  - 0xSmartContract
  - shaka
  - nobody2018
---

## Vulnerability Title

M-1: Calls to Oracles don't check for stale prices

### Overview


A bug report has been issued on the USSD-Judging repository on Github. The bug was found by a team of 33 members, who identified that calls to Oracles don't check for stale prices. This means that the Oracle price feeds can become stale due to a variety of reasons, resulting in incorrect calculations in most of the key functionality of USSD & USSDRebalancer contracts. The bug was identified through manual review and the recommendation is to read the ``updatedAt`` parameter from the calls to ``latestRoundData()`` and verify that it isn't older than a set amount. If it is, the call should be reverted with the message "stale price feed". This bug should be addressed as soon as possible to ensure accuracy in the calculations of the key functionality of USSD & USSDRebalancer contracts.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/31 

## Found by 
0x2e, 0xHati, 0xPkhatri, 0xRobocop, 0xSmartContract, 0xStalin, 0xeix, 0xlmanini, 0xyPhilic, Angry\_Mustache\_Man, Aymen0909, Bauchibred, Bauer, Brenzee, BugBusters, Delvir0, DevABDee, Diana, Dug, Fanz, GimelSec, HonorLt, J4de, Kodyvim, Kose, Lilyjjo, Madalad, MohammedRizwan, Nyx, PNS, PTolev, Pheonix, PokemonAuditSimulator, Proxy, RaymondFam, Saeedalipoor01988, SaharDevep, SanketKogekar, Schpiel, T1MOH, TheNaubit, VAD37, WATCHPUG, \_\_141345\_\_, ast3ros, berlin-101, capy\_, chainNue, chaithanya\_gali, chalex.eth, ctf\_sec, curiousapple, dacian, evilakela, georgits, giovannidisiena, immeas, josephdara, juancito, kiki\_dev, kutugu, lil.eth, martin, ni8mare, nobody2018, pavankv241, peanuts, qbs, qckhp, saidam017, sakshamguruji, sam\_gmk, sashik\_eth, sayan\_, shaka, shealtielanz, simon135, ss3434, tallo, theOwl, toshii, tsvetanovv, twicek, ustas, vagrant, w42d3n, warRoom, whiteh4t9527
## Summary
Calls to Oracles don't check for stale prices.

## Vulnerability Detail
None of the oracle calls check for stale prices, for example [StableOracleDAI.getPriceUSD()](https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/oracles/StableOracleDAI.sol#L48):
```solidity
(, int256 price, , , ) = priceFeedDAIETH.latestRoundData();

return
    (wethPriceUSD * 1e18) /
    ((DAIWethPrice + uint256(price) * 1e10) / 2);
```

## Impact
Oracle price feeds can become stale due to a variety of [reasons](https://ethereum.stackexchange.com/questions/133242/how-future-resilient-is-a-chainlink-price-feed/133843#133843). Using a stale price will result in incorrect calculations in most of the key functionality of USSD & USSDRebalancer contracts.

## Code Snippet
[StableOracleDAI.getPriceUSD()](https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/oracles/StableOracleDAI.sol#L48)
[StableOracleWBGL.getPriceUSD()](https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/oracles/StableOracleWBGL.sol#L36-L38)
[StableOracleWBTC.getPriceUSD()](https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/oracles/StableOracleWBTC.sol#L23-L25)
[StableOracleWETH.getPriceUSD()](https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/oracles/StableOracleWETH.sol#L23-L25)

## Tool used
Manual Review

## Recommendation
Read the ``updatedAt`` parameter from the calls to ``latestRoundData()`` and verify that it isn't older than a set amount, eg:

```solidity
if (updatedAt < block.timestamp - 60 * 60 /* 1 hour */) {
   revert("stale price feed");
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 1/5 |
| Audit Firm | Sherlock |
| Protocol | USSD - Autonomous Secure Dollar |
| Report Date | N/A |
| Finders | J4de, Dug, 0xSmartContract, shaka, nobody2018, qbs, lil.eth, Delvir0, giovannidisiena, 0xyPhilic, juancito, SaharDevep, Pheonix, MohammedRizwan, BugBusters, Angry\_Mustache\_Man, PNS, sam\_gmk, ss3434, pavankv241, Schpiel, Lilyjjo, VAD37, shealtielanz, qckhp, capy\_, immeas, Kose, Kodyvim, chalex.eth, sayan\_, kutugu, \_\_141345\_\_, HonorLt, curiousapple, chainNue, w42d3n, Nyx, WATCHPUG, peanuts, vagrant, ctf\_sec, tallo, saidam017, RaymondFam, Aymen0909, 0xRobocop, sakshamguruji, martin, GimelSec, ni8mare, warRoom, toshii, 0xPkhatri, twicek, T1MOH, Brenzee, georgits, simon135, Madalad, theOwl, Bauchibred, PokemonAuditSimulator, Proxy, PTolev, berlin-101, Fanz, 0x2e, chaithanya\_gali, evilakela, sashik\_eth, TheNaubit, 0xStalin, josephdara, dacian, SanketKogekar, 0xeix, DevABDee, tsvetanovv, 0xHati, kiki\_dev, ast3ros, Bauer, Diana, ustas, 0xlmanini, whiteh4t9527, Saeedalipoor01988 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/31
- **Contest**: https://app.sherlock.xyz/audits/contests/82

### Keywords for Search

`Stale Price, Oracle`

