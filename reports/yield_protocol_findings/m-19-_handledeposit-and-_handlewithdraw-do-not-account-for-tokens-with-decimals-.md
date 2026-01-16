---
# Core Classification
protocol: Tigris Trade
chain: everychain
category: uncategorized
vulnerability_type: decimals

# Attack Vector Details
attack_type: decimals
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6349
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-tigris-trade-contest
source_link: https://code4rena.com/reports/2022-12-tigris
github_link: https://github.com/code-423n4/2022-12-tigris-findings/issues/533

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - decimals

protocol_categories:
  - dexes
  - services
  - derivatives
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 17
finders:
  - Avci
  - Deivitto
  - pwnforce
  - rbserver
  - 0xDecorativePineapple
---

## Vulnerability Title

[M-19] _handleDeposit and _handleWithdraw do not account for tokens with decimals higher than 18

### Overview


This bug report is about a vulnerability in the Trading.sol contract. This vulnerability can cause a deposit or withdrawal of tokens with decimals higher than 18 to always revert. This can be demonstrated by changing the 00.Mocks.js file and running the 07.Trading.js test. This will result in an error that says "Arithmetic operation underflowed or overflowed outside of an unchecked block". To fix this vulnerability, calculations in the contract should be updated to account for tokens with decimals higher than 18.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/Trading.sol#L650
https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/Trading.sol#L675


## Vulnerability details

## Impact 

In `Trading.sol` a [deposit](https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/Trading.sol#L675) or [withdrawal](https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/Trading.sol#L700) of tokens with decimals higher than 18 will always revert. 

This is the case e.g. for `NEAR` which is divisible into 10e24 `yocto` 

## Proof of Concept

Change [00.Mocks.js#L33](https://github.com/code-423n4/2022-12-tigris/blob/main/deploy/test/00.Mocks.js#L33) to:

```
args: ["USDC", "USDC", 24, deployer, ethers.utils.parseUnits("1000", 24)]
```

Then in [07.Trading.js](https://github.com/code-423n4/2022-12-tigris/blob/main/test/07.Trading.js):

```
Opening and closing a position with tigUSD output
Opening and closing a position with <18 decimal token output
```

are going to fail with:
```
Error: VM Exception while processing transaction: reverted with panic code 0x11 (Arithmetic operation underflowed or overflowed outside of an unchecked block)
```

## Tools Used

Visual Studio Code

## Recommended Mitigation Steps

Update calculations in the contract to account for tokens with decimals higher than 18.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Tigris Trade |
| Report Date | N/A |
| Finders | Avci, Deivitto, pwnforce, rbserver, 0xDecorativePineapple, Dinesh11G, izhelyazkov, Englave, Tointer, Critical, 0xdeadbeef0x, ak1, chaduke, unforgiven, rvierdiiev, yjrwkk, 0x4non |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tigris
- **GitHub**: https://github.com/code-423n4/2022-12-tigris-findings/issues/533
- **Contest**: https://code4rena.com/contests/2022-12-tigris-trade-contest

### Keywords for Search

`Decimals`

