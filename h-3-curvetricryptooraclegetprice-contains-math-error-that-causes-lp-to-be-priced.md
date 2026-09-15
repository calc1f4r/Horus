---
# Core Classification
protocol: Blueberry Update #3
chain: everychain
category: oracle
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: oracle

# Source Information
source: solodit
solodit_id: 24318
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/104
source_link: none
github_link: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/100

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
  - wrong_math
  - oracle
  - decimals

protocol_categories:
  - rwa
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Kow
  - 0x52
---

## Vulnerability Title

H-3: CurveTricryptoOracle#getPrice contains math error that causes LP to be priced completely wrong

### Overview


This bug report is about an issue found in the CurveTricryptoOracle#getPrice function of the codebase. The bug causes the Liquidation Price (LP) to be priced completely wrong due to a math error. The code snippet in question is located at CurveTricryptoOracle.sol#L57-L62 and it incorrectly divides the LP price by the price of ETH which causes it to return the price of LP in terms of ETH instead of USD. This leads to healthy positions being liquidated due to incorrect LP pricing. 

The issue was initially found by 0x52 and Kow and then discussed by other members of the Sherlock Audit team. The team concluded that the code was borrowed from the Sentiment CurveTriCryptoOracle which is meant to return the price in terms of ETH. As the oracle is meant to return the valuation in USD, the division by the price of ETH needs to be dropped. The issue was then reopened for further investigation.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/100 

## Found by 
0x52, Kow

CurveTricryptoOracle#getPrice incorrectly divides the LP price by the price of ETH which causes it to return the price of LP in terms of ETH instead of USD

## Vulnerability Detail

[CurveTricryptoOracle.sol#L57-L62](https://github.com/sherlock-audit/2023-07-blueberry/blob/main/blueberry-core/contracts/oracle/CurveTricryptoOracle.sol#L57-L62)

                (lpPrice(
                    virtualPrice,
                    base.getPrice(tokens[1]),
                    ethPrice,
                    base.getPrice(tokens[0])
                ) * 1e18) / ethPrice;

After the LP price has been calculated in USD it is mistakenly divided by the price of ETH causing the contract to return the LP price in terms of ETH rather than USD. This leads to LP that is massively undervalued causing positions which are actually heavily over collateralized to be liquidated.

## Impact

Healthy positions are liquidated due to incorrect LP pricing

## Code Snippet

[CurveTricryptoOracle.sol#L48-L65](https://github.com/sherlock-audit/2023-07-blueberry/blob/main/blueberry-core/contracts/oracle/CurveTricryptoOracle.sol#L48-L65)

## Tool used

Manual Review

## Recommendation

Don't divide the price by the price of ETH



## Discussion

**sherlock-admin2**

2 comment(s) were left on this issue during the judging contest.

**0xyPhilic** commented:
> invalid because lpPrice is considered in ETH so dividing by ETH/USD price returns the final result in USD

**Kral01** commented:
> there is a precision value



**Gornutz**

Judges accurately state why the division by ETH/USD is required to return the proper USD value.

**Shogoki**

Closing in regards to other judges and sponsors comments.

**IAm0x52**

This is valid. The code being used here was borrowed from the Sentiment [CurveTriCryptoOracle](https://arbiscan.io/address/0x4e828a117ddc3e4dd919b46c90d4e04678a05504#code), which is specifically meant to return the price in terms of ETH. This oracle is meant to return the valuation in USD which means the division by the price of ETH needs to be dropped.

**Shogoki**

> This is valid. The code being used here was borrowed from the Sentiment [CurveTriCryptoOracle](https://arbiscan.io/address/0x4e828a117ddc3e4dd919b46c90d4e04678a05504#code), which is specifically meant to return the price in terms of ETH. This oracle is meant to return the valuation in USD which means the division by the price of ETH needs to be dropped.

Maybe was a bit quick in closing. Will reopen it and we will take a deeper look at it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update #3 |
| Report Date | N/A |
| Finders | Kow, 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/100
- **Contest**: https://app.sherlock.xyz/audits/contests/104

### Keywords for Search

`Wrong Math, Oracle, Decimals`

