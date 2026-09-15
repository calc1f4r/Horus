---
# Core Classification
protocol: Inverse Finance
chain: everychain
category: oracle
vulnerability_type: oracle

# Attack Vector Details
attack_type: oracle
affected_component: oracle

# Source Information
source: solodit
solodit_id: 5744
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-inverse-finance-contest
source_link: https://code4rena.com/reports/2022-10-inverse
github_link: https://github.com/code-423n4/2022-10-inverse-findings/issues/533

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
  - oracle
  - decimals

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 15
finders:
  - 8olidity
  - pashov
  - codexploder
  - CertoraInc
  - sorrynotsorry
---

## Vulnerability Title

[M-15] Oracle assumes token and feed decimals will be limited to 18 decimals

### Overview


A bug has been identified in the Oracle contract of the code-423n4/2022-10-inverse repository. The `viewPrices` and `getPrices` functions are used to normalize prices to adjust for potential decimal differences between feed and token decimals and the expected return value. 

The bug is caused by an assumption that `feedDecimals` and `tokenDecimals` won't exceed 18, as the normalization calculation is `36 - feedDecimals - tokenDecimals`. This assumption is not safe for the general case, as it may cause an overflow (and a revert) if the sum of both is greater than 36, rendering the Oracle useless.

A proof of concept has been provided to demonstrate the vulnerability. If `feedDecimals + tokenDecimals > 36` then the expression `36 - feedDecimals - tokenDecimals` will be negative and will cause a revert.

The recommended mitigation step is to divide the price by `10 ** decimals` if `feedDecimals + tokenDecimals` exceeds 36. This should be done in place of the current normalization procedure.

### Original Finding Content


<https://github.com/code-423n4/2022-10-inverse/blob/main/src/Oracle.sol#L87><br>
<https://github.com/code-423n4/2022-10-inverse/blob/main/src/Oracle.sol#L121><br>

The `Oracle` contract normalizes prices in both `viewPrices` and `getPrices` functions to adjust for potential decimal differences between feed and token decimals and the expected return value.

However these functions assume that `feedDecimals` and `tokenDecimals` won't exceed 18 since the normalization calculation is `36 - feedDecimals - tokenDecimals`, or that at worst case the sum of both won't exceed 36.

This assumption should be safe for certain cases, for example WETH is 18 decimals and the ETH/USD chainlink is 8 decimals, but may cause an overflow (and a revert) for the general case, rendering the Oracle useless in these cases.

### Proof of Concept

If `feedDecimals + tokenDecimals > 36` then the expression `36 - feedDecimals - tokenDecimals` will be negative and (due to Solidity 0.8 default checked math) will cause a revert.

### Recommended Mitigation Steps

In case `feedDecimals + tokenDecimals` exceeds 36, then the proper normalization procedure would be to **divide** the price by `10 ** decimals`. Something like this:

    uint normalizedPrice;

    if (feedDecimals + tokenDecimals > 36) {
        uint decimals = feedDecimals + tokenDecimals - 36;
        normalizedPrice = price / (10 ** decimals)
    } else {
        uint8 decimals = 36 - feedDecimals - tokenDecimals;
        normalizedPrice = price * (10 ** decimals);
    }

**[08xmt (Inverse) confirmed and commented](https://github.com/code-423n4/2022-10-inverse-findings/issues/533#issuecomment-1351469171):**
 > Fixed in https://github.com/InverseFinance/FrontierV2/pull/25<br>
> Also pretty sure this is a dupe



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Inverse Finance |
| Report Date | N/A |
| Finders | 8olidity, pashov, codexploder, CertoraInc, sorrynotsorry, joestakey, RaoulSchaffranek, Ruhum, Chom, BClabs, Lambda, cryptphi, adriro, neumo, eierina |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-inverse
- **GitHub**: https://github.com/code-423n4/2022-10-inverse-findings/issues/533
- **Contest**: https://code4rena.com/contests/2022-10-inverse-finance-contest

### Keywords for Search

`Oracle, Decimals`

