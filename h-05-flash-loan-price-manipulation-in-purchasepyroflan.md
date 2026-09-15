---
# Core Classification
protocol: Behodler
chain: everychain
category: oracle
vulnerability_type: oracle

# Attack Vector Details
attack_type: oracle
affected_component: oracle

# Source Information
source: solodit
solodit_id: 1363
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-behodler-contest
source_link: https://code4rena.com/reports/2022-01-behodler
github_link: https://github.com/code-423n4/2022-01-behodler-findings/issues/231

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 4.999242017104216

# Context Tags
tags:
  - oracle
  - flash_loan
  - twap

protocol_categories:
  - cross_chain
  - services
  - cdp
  - dexes
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - sirhashalot
---

## Vulnerability Title

[H-05] Flash loan price manipulation in purchasePyroFlan()

### Overview


This bug report is about the potential for price manipulation through flash loans in the FlanBackstop.sol code. Flashloan price manipulation is the cause for many major hacks, including bZx, Harvest, and others. The code calculates the price of flan to stablecoin in the Uniswap pool based on the balances at a single point in time, which can be manipulated with flash loans. A user can manipulate the LP, especially when the LP is new with low liquidity, in order to achieve large amounts of flan and pyroflan. The code attempts to protect against this manipulation, but the attack can still be repeated multiple times. The recommended mitigation steps are to use a TWAP instead of the pool price at a single point in time to increase the cost of performing a flashloan sandwich attack. TWAP is a Uniswap v2 price oracle solution that provides asset prices while reducing the change of manipulation.

### Original Finding Content

## Handle

sirhashalot


## Vulnerability details

## Impact

The comment on [line 54](https://github.com/code-423n4/2022-01-behodler/blob/cedb81273f6daf2ee39ec765eef5ba74f21b2c6e/contracts/FlanBackstop.sol#L54) of FlanBackstop.sol states "the opportunity for price manipulation through flash loans exists", and I agree that this is a serious risk. While the acceptableHighestPrice variable attempts to limit the maximum price change of the flan-stablecoin LP, a flashloan sandwich attack can still occur within this limit and make up for the limitation with larger volumes or multiple flashloan attacks. Flashloan price manipulation is the cause for many major hacks, including [bZx](https://bzx.network/blog/postmortem-ethdenver), [Harvest](https://rekt.news/harvest-finance-rekt/), and others.

## Proof of Concept

[Line 83](https://github.com/code-423n4/2022-01-behodler/blob/cedb81273f6daf2ee39ec765eef5ba74f21b2c6e/contracts/FlanBackstop.sol#L83) of FlanBackstop.sol calculates the price of flan to stablecoin in the Uniswap pool based on the balances at a single point in time. Pool balances at a single point in time can be manipulated with flash loans, which can skew the numbers to the extreme. The single data point of LP balances is used to calculate [the growth variable in line 103](https://github.com/code-423n4/2022-01-behodler/blob/cedb81273f6daf2ee39ec765eef5ba74f21b2c6e/contracts/FlanBackstop.sol#L103), and the growth variable influences the quantity of pyroflan a user receives in [the premium calculation on line 108](https://github.com/code-423n4/2022-01-behodler/blob/cedb81273f6daf2ee39ec765eef5ba74f21b2c6e/contracts/FlanBackstop.sol#L108).
```
uint256 priceBefore = (balanceOfFlanBefore * getMagnitude(stablecoin)) / balanceOfStableBefore;
uint256 growth = ((priceBefore - tiltedPrice) * 100) / priceBefore;
uint256 premium = (flanToMint * (growth / 2)) / 100;
```

Problems can occur when the volumes that the `purchasePyroFlan()` function sends to the Uniswap pool are large compared to the pool's liquidity volume, or if the Uniswap pool price is temporarily tilted with a flashloan (or a whale). Because this function purposefully changes the exchange rate of the LP, by transferring tokens to the LP in a 2-to-1 ratio, a large volume could caught a large price impact in the LP. The code attempts to protect against this manipulation in [line 102](https://github.com/code-423n4/2022-01-behodler/blob/cedb81273f6daf2ee39ec765eef5ba74f21b2c6e/contracts/FlanBackstop.sol#L102) with a require statement, but this can be worked around by reducing the volume per flashloan and repeating the attack multiple times. A user can manipulate the LP, especially when the LP is new with low liquidity, in order to achieve large amounts of flan and pyroflan.

## Recommended Mitigation Steps

Use a TWAP instead of the pool price at a single point in time to increase the cost of performing a flashloan sandwich attack. See [the Uniswap v2 price oracle solution ](https://docs.uniswap.org/protocol/V2/concepts/core-concepts/oracles)documentation for more explanations on how Uniswap designed an approach to providing asset prices while reducing the change of manipulation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 4.999242017104216/5 |
| Audit Firm | Code4rena |
| Protocol | Behodler |
| Report Date | N/A |
| Finders | sirhashalot |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-behodler
- **GitHub**: https://github.com/code-423n4/2022-01-behodler-findings/issues/231
- **Contest**: https://code4rena.com/contests/2022-01-behodler-contest

### Keywords for Search

`Oracle, Flash Loan, TWAP`

