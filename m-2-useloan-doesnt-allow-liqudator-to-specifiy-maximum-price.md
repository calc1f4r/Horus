---
# Core Classification
protocol: Kairos Loan
chain: everychain
category: uncategorized
vulnerability_type: chain_reorganization_attack

# Attack Vector Details
attack_type: chain_reorganization_attack
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 12279
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/56
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-kairos-judging/issues/25

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:
  - chain_reorganization_attack

protocol_categories:
  - dexes
  - cdp
  - rwa
  - nft_lending
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

M-2: useLoan doesn't allow liqudator to specifiy maximum price

### Overview


This bug report is about the useLoan feature in the kairos-contracts repository not allowing the liquidator to specify a maximum price they are willing to pay for the collateral they are liquidating. This can be problematic if the chain the contracts are deployed on suffers a reorg attack, which can place the transaction earlier than anticipated and therefore charge the user more than they meant to pay. On Ethereum this is unlikely, but this is meant to be deployed on any compatible EVM chain, many of which are frequently reorganized. It was found manually and the code snippet can be found at the given link. The recommendation is to allow liquidator to specify a max acceptable price to pay. The bug was fixed in a pull request.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-kairos-judging/issues/25 

## Found by 
0x52

## Summary

useLoan doesn't allow the liquidator to specify a max price they are will to pay for the collateral they are liquidating. On the surface this doesn't seem like an issue because the price is always decreasing due to the dutch auction. However this can be problematic if the chain the contracts are deployed suffers a reorg attack. This can place the transaction earlier than anticipated and therefore charge the user more than they meant to pay. On Ethereum this is unlikely but this is meant to be deployed on any compatible EVM chain many of which are frequently reorganized.

## Vulnerability Detail

See summary.

## Impact

Liquidator can be charged more than intended

## Code Snippet

https://github.com/sherlock-audit/2023-02-kairos/blob/main/kairos-contracts/src/AuctionFacet.sol#L59-L73

## Tool used

Manual Review

## Recommendation

Allow liquidator to specify a max acceptable price to pay



## Discussion

**npasquie**

fixed here https://github.com/kairos-loan/kairos-contracts/pull/50

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Kairos Loan |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-kairos-judging/issues/25
- **Contest**: https://app.sherlock.xyz/audits/contests/56

### Keywords for Search

`Chain Reorganization Attack`

