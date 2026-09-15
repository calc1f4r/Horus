---
# Core Classification
protocol: Union Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25604
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-10-union
source_link: https://code4rena.com/reports/2021-10-union
github_link: https://github.com/code-423n4/2021-10-union-findings/issues/63

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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-11] Rebalance will fail if a market has high utilization

### Overview


This bug report discusses an issue with the `AssetManager.rebalance` function in the code-423n4/2021-10-union-findings repository. This function iterates through the markets and withdraws all tokens in the `moneyMarkets[i].withdrawAll` call, which could cause rebalancing to fail if a single market has a liquidity crunch. The issue was acknowledged by kingjacob (Union) and commented on by GalloDaSballo (judge), who recommended rewriting the `rebalance` function to account for liquidity crunches in the long term.

### Original Finding Content

_Submitted by cmichel_

The `AssetManager.rebalance` function iterates through the markets and withdraws **all** tokens in the `moneyMarkets[i].withdrawAll` call.

Note that in peer-to-peer lending protocols like Compound/Aave the borrower takes the tokens from the supplier and it might not be possible for the supplier to withdraw all tokens if the utilisation ratio of the market is high.

See this check for example in [Compound's cToken](https://github.com/compound-finance/compound-protocol/blob/master/contracts/CToken.sol#L680).

#### Impact
Rebalancing will fail if a single market has a liquidity crunch.

#### Recommended Mitigation Steps
Withdraw only what's available and rebalance on that instead of trying to pull all tokens from each market first.
Admittedly, this might be hard to compute for some protocols.

**[kingjacob (Union) acknowledged](https://github.com/code-423n4/2021-10-union-findings/issues/63)**

**[GalloDaSballo (judge) commented](https://github.com/code-423n4/2021-10-union-findings/issues/63#issuecomment-966611620):**
 > Agree with the finding, at this time this potential vulnerability is a feature of the protocol
>
> I recommend in the long term, that the sponsor rewrites the `rebalance` function to account for liquidity crunches




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Union Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-union
- **GitHub**: https://github.com/code-423n4/2021-10-union-findings/issues/63
- **Contest**: https://code4rena.com/reports/2021-10-union

### Keywords for Search

`vulnerability`

