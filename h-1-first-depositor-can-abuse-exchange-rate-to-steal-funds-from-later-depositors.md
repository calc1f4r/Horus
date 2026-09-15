---
# Core Classification
protocol: Surge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6701
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/51
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-surge-judging/issues/125

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 37
finders:
  - 0x52
  - chainNue
  - y1cunhui
  - Ace-30
  - bitx0x
---

## Vulnerability Title

H-1: First depositor can abuse exchange rate to steal funds from later depositors

### Overview


This bug report is about a vulnerability found in the code of the Surge Protocol v1, which is a decentralized finance protocol. The vulnerability allows the first depositor to abuse the exchange rate to steal funds from later depositors. The vulnerability is due to truncation when converting to shares. The code snippet which contains the vulnerability is available at the URL provided. The impact of this vulnerability is that the first depositor can steal funds due to truncation. A recommendation to fix this vulnerability is to either lock a small amount of the deposit during the creation of the vault or for the first depositor. The discussion section of the report is a comment from a user named "xeious".

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-surge-judging/issues/125 

## Found by 
0Kage, ck, usmannk, Ace-30, CRYP70, ak1, 0x52, chaduke, chainNue, dingo, rvi, ctf\_sec, carrot, unforgiven, y1cunhui, Chinmay, gryphon, GimelSec, peanuts, Bobface, gandu, Juntao, TrungOre, MalfurionWhitehat, cccz, Cryptor, VAD37, \_\_141345\_\_, 0xAsen, Breeje, 0xhacksmithh, RaymondFam, bin2chen, 0xc0ffEE, bytes032, SunSec, banditx0x

## Summary

Classic issue with vaults. First depositor can deposit a single wei then donate to the vault to greatly inflate share ratio. Due to truncation when converting to shares this can be used to steal funds from later depositors.

## Vulnerability Detail

See summary.

## Impact

First depositor can steal funds due to truncation

## Code Snippet

https://github.com/sherlock-audit/2023-02-surge/blob/main/surge-protocol-v1/src/Pool.sol#L307-L343

## Tool used

[Solidity YouTube Tutorial](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

## Recommendation

Either during creation of the vault or for first depositor, lock a small amount of the deposit to avoid this.

## Discussion

**xeious**

GG. We left this one intentionally. Glad to see this many duplicates.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Surge |
| Report Date | N/A |
| Finders | 0x52, chainNue, y1cunhui, Ace-30, bitx0x, 0xAsen, gryphon, SunSec, ck, usmannk, rvi, peanuts, Breeje, bytes032, dingo, Chinmay, ctf\_sec, Juntao, Cryptor, gu, VAD37, 0xhacksmithh, cccz, RaymondFam, chaduke, ak1, 0Kage, Bobface, TrungOre, bin2chen, MalfurionWhitehat, 0xc0ffEE, \_\_141345\_\_, CRYP70, unforgiven, GimelSec, carrot |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-surge-judging/issues/125
- **Contest**: https://app.sherlock.xyz/audits/contests/51

### Keywords for Search

`vulnerability`

