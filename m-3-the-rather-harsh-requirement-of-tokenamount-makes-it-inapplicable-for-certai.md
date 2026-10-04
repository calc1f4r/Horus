---
# Core Classification
protocol: NounsDAO
chain: everychain
category: uncategorized
vulnerability_type: decimals

# Attack Vector Details
attack_type: decimals
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5663
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/27
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-nounsdao-judging/issues/63

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - decimals

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - WATCHPUG
  - rvierdiiev
---

## Vulnerability Title

M-3: The rather harsh requirement of `tokenAmount` makes it inapplicable for certain tokens

### Overview


This bug report is about the requirement of `tokenAmount` which makes it inapplicable for certain tokens like WBTC and EURS. The requirement of `tokenAmount >= stopTime - startTime` is suitable for USDC and WETH, but it is too harsh for tokens with higher per wei value, such as WBTC and EURS. To meet this requirement, it must be `0.31536 WBTC` per year (worth about $5,400) and `315,360 EURS` per year (worth about $315,000). This will make the system inapplicable for certain tokens with higher per wei value. The recommendation is to change to `tokenAmount * RATE_DECIMALS_MULTIPLIER >= stopTime - startTime`. A fix PR has been submitted and is available at https://github.com/nounsDAO/streamer/pull/12.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-nounsdao-judging/issues/63 

## Found by 
WATCHPUG, rvierdiiev

## Summary

The requirements for `tokenAmount >= stopTime - startTime` will not be suitable for all tokens and therefore need to be made less applicable for certain tokens like WBTC and EURS.

## Vulnerability Detail

Requiring the `tokenAmount >= stopTime - startTime` is suitable for USDC and WETH.

However, such requirements will be a bit too harsh for other popular tokens, eg, WBTC (`decimals: 8`) and EURS (`decimals: 2`). Therefore, make the system less applicable for those tokens.

For WBTC, it must be `0.31536 WBTC` per year (worth about $5,400) to meet this requirement, and for EURS, it must be at least `315,360 EURS` per year (worth about $315,000).

## Impact

The system will be inapplicable for certain tokens with higher per wei value, eg, WBTC and EURS.

## Code Snippet

https://github.com/sherlock-audit/2022-11-nounsdao/blob/main/src/StreamFactory.sol#L200

## Tool used

Manual Review

## Recommendation

Consider changing to `tokenAmount * RATE_DECIMALS_MULTIPLIER >= stopTime - startTime`.

## Discussion

**eladmallel**

Fix PR: https://github.com/nounsDAO/streamer/pull/12

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | NounsDAO |
| Report Date | N/A |
| Finders | WATCHPUG, rvierdiiev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-nounsdao-judging/issues/63
- **Contest**: https://app.sherlock.xyz/audits/contests/27

### Keywords for Search

`Decimals`

