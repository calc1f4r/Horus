---
# Core Classification
protocol: Maple Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25468
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-04-maple
source_link: https://code4rena.com/reports/2021-04-maple
github_link: https://github.com/code-423n4/2021-04-maple-findings/issues/4

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
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-01] Loans of tokens with >18 decimals can result in incorrect collateral calculation

### Overview


This bug report is about a vulnerability in the Maple Core protocol that can be exploited to mislead a Pool Delegate to a seemingly innocuous loan. The problem occurs when the collateral token of a loan has more than 18 decimals of precision, as there is no sanitization conducted on the creation of a Loan via the factory. This can cause an underflow to the power of 10 which will cause the division to yield 0 and thus cause the Loan to calculate 0 as collateral required for the loan. To fix the issue, the same paradigm as _toWad should be applied, which is secure. Lucas-Manuel (Maple) acknowledged that they are aware of this issue and will make it part of their onboarding criteria. Nick Johnson (Judge) judged this as a Medium Severity issue with Low Likelihood and High Impact.

### Original Finding Content


It is possible for a user to mislead a Pool Delegate to a seemingly innocuous loan by utilizing a token with more than 18 decimals as collateral and lucrative loan terms.

The [final calculation](https://github.com/maple-labs/maple-core/blob/031374b2609560ade825532474048eb5826dec20/contracts/library/LoanLib.sol#L235) within the `collateralRequiredForDrawdown` of `LoanLib` incorrectly assumes the collateral token of a loan to be less than `18` decimals, which can not be the case as there is no sanitization conducted on the creation of a `Loan` via the factory. This can cause an underflow to the power of `10` which will cause the division to yield `0` and thus cause the `Loan` to calculate `0` as collateral required for the loan. We advise the [same paradigm](https://github.com/maple-labs/maple-core/blob/031374b2609560ade825532474048eb5826dec20/contracts/library/LoanLib.sol#L247) as `_toWad` to be applied, which is secure.

**[lucas-manuel (Maple) acknowledged](https://github.com/code-423n4/2021-04-maple-findings/issues/4#issuecomment-824852669):**

> We are aware that we cannot onboard liquidityAssets or collateralAssets with more that 18 decimals of precision, and will make that part of our onboarding criteria.

**[Nick Johnson (Judge)](https://github.com/code-423n4/2021-04-maple-findings/issues/4#issuecomment-827193173):**

> This is 100% a legitimate issue that could be exploited against the contract, and using social mitigations (making this part of the onboarding strategy) when there's a technical mitigation (`require()`ing that the token have <= 18 decimals, or using the recommended mitigation) is insufficient and could easily lead to an exploit due to human error.
>
> Based on the OWASP methodogology, I'm judging this as Likelihood=Low (because of the requirement to get it past human review) and Impact=High (because of the impact of the bug if it were exploited to create a 0-collateral loan and default on it), resulting in a Severity of Medium.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Maple Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-04-maple
- **GitHub**: https://github.com/code-423n4/2021-04-maple-findings/issues/4
- **Contest**: https://code4rena.com/reports/2021-04-maple

### Keywords for Search

`vulnerability`

