---
# Core Classification
protocol: GMX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18648
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/6
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-gmx-judging/issues/216

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
  - simon135
---

## Vulnerability Title

M-1: If block range it big and adl dosnt use currentblock in the order it will cause issues

### Overview


This bug report is about the potential issue of bad debt when using the Adl Order, which is a contract that is used to execute orders on the decentralized exchange. The issue is that if the block range is large and the Adl Order does not use the current block in the order, it can cause issues. The impact of this issue is bad debt, and the code snippet provided is from the Adl Order. Through discussion, it was determined that the impact of this issue is minimized if there is at least one honest Adl Keeper, but if all Adl Keepers are dishonest, it is possible for Adl orders to continually occur using older prices. The recommendation is to make it `chain.currentBLock`.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-gmx-judging/issues/216 

## Found by 
simon135

## Summary

if block range is a big range and since adl order uses` cache.minOracleBlockNumbers[0]` there can be an issue of the block not being in range because of the littlest block with max block being a lot bigger and adl wont happen and the protocol will get bad debt

## Vulnerability Detail

since the adl order updateBlock is `cache.minOracleBlockNumbers[0]` the block can be behind the  range check and fail and the protocol can end up in bad debt with the tokens price declining

## Impact

bad debt

## Code Snippet

```solidity
        cache.key = AdlUtils.createAdlOrder(
            AdlUtils.CreateAdlOrderParams(
                dataStore,
                eventEmitter,
                account,
                market,
                collateralToken,
                isLong,
                sizeDeltaUsd,
                cache.minOracleBlockNumbers[0]
            )

```

## Tool used

Manual Review

## Recommendation

make it `chain.currentBLock`



## Discussion

**xvi10**

doesn't seem to be a valid issue, cache.minOracleBlockNumbers[0] is from oracleParams which is provided by the ADL keeper, the ADL keeper should use the latest prices to execute ADL

**IllIllI000**

@xvi10 I know that the order keepers are intended to eventually be only semi-trusted. Is that not the case for ADL keepers - they'll always be fully trusted?

**xvi10**

i think the impact is minimized if there is at least one honest ADL keeper, if all ADL keepers are dishonest it is possible for ADLs to continually occur using older prices

**IllIllI000**

It sounds like ADL keepers are not fully trusted and therefore this is an unlikely, but possible risk

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | GMX |
| Report Date | N/A |
| Finders | simon135 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-gmx-judging/issues/216
- **Contest**: https://app.sherlock.xyz/audits/contests/6

### Keywords for Search

`vulnerability`

