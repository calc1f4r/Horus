---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24839
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-08-frax
source_link: https://code4rena.com/reports/2022-08-frax
github_link: https://github.com/code-423n4/2022-08-frax-findings/issues/200

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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-10] Decimals limitation limits the tokens that can be used

### Overview


A bug report submitted by CertoraInc has been identified that limits the tokens that can be used due to a limitation in decimals. This bug occurs when the calculation `oracleNormalization = 10 ^(18 + n - d + a - c)` is used to calculate `_exchangeRate = _price / oracleNormalization;` and `a >18 +c`. This means that tokens with decimals less than 24 are not possible to use in this system when USDC is used. 

Initially, the severity of the bug was marked as high, however, DrakeEvans (Frax) disputed the severity, noting that no funds or incorrect functionality were at risk, and as such, the severity was decreased to Medium. GititGoro (judge) also decreased the severity to Medium, noting that since deployments can't occur, it is a Medium severity issue.

### Original Finding Content

_Submitted by CertoraInc_

Decimals limitation limits the tokens that can be used.

### Proof of Concept

Let's give some name to the decimals of certain numbers:
n = decimals of numerator oracle.
d =  decimals denominator oracle.
a = decimals of the asset.
c= decimals of the collateral.

Now, the `oracleNormalization = 10 ^(18 + n - d + a - c)`.

And here: <https://github.com/code-423n4/2022-08-frax/blob/main/src/contracts/FraxlendPairCore.sol#L536> , `price` has decimals of `36 + n -d`, so `here()` when we calculate `_exchangeRate = _price / oracleNormalization;` it would underflow and revert if `a >18 +c`.

And that's a pretty big limitation on the tokens options. We have USDC which have 6 decimals so all the tokens the their decimals < 24 are not possible to use in this system (with USDC together).

**[DrakeEvans (Frax) disputed, disagreed with severity and commented](https://github.com/code-423n4/2022-08-frax-findings/issues/200#issuecomment-1238077975):**
 > Known issue, prevents certain combinations of tokens from being deployed.  No high risk as no deployment will occur.  No funds at risk, no incorrect functionality. Low at best.

**[gititGoro (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-08-frax-findings/issues/200#issuecomment-1266177019):**
 > This hasn't been listed as a known issue so it can't be marked invalid but since deployments can't occur, it's a Medium severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-frax
- **GitHub**: https://github.com/code-423n4/2022-08-frax-findings/issues/200
- **Contest**: https://code4rena.com/reports/2022-08-frax

### Keywords for Search

`vulnerability`

