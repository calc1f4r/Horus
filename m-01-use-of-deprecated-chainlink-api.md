---
# Core Classification
protocol: Wild Credit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 840
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-wild-credit-contest
source_link: https://code4rena.com/reports/2021-09-wildcredit
github_link: https://github.com/code-423n4/2021-09-wildcredit-findings/issues/55

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xRajeev
  - cmichel  leastwood.
---

## Vulnerability Title

[M-01] Use of deprecated Chainlink API

### Overview


This bug report is about a vulnerability in the WildCredit contest contract which uses Chainlink’s deprecated API latestAnswer(). This means that the API might suddenly stop working if Chainlink stops supporting deprecated APIs, which would cause the contract to become unusable and prices to be unable to be obtained. This was a Medium-severity finding even in the previous version of WildCredit contest as well. The proof of concept for this vulnerability can be found at the provided link. The recommended mitigation steps for this vulnerability is to use V3 interface functions as stated in the Chainlink documentation.

### Original Finding Content

_Submitted by 0xRajeev, also found by cmichel and leastwood_.

#### Impact

The contract uses Chainlink’s deprecated API `latestAnswer()`. Such functions might suddenly stop working if Chainlink stopped supporting deprecated APIs.

Impact: Deprecated API stops working. Prices cannot be obtained. Protocol stops and contracts have to be redeployed.

See similar Low-severity finding L11 from OpenZeppelin's Audit of Opyn Gamma Protocol: <https://blog.openzeppelin.com/opyn-gamma-protocol-audit/>

This was a Medium-severity finding even in the previous version of WildCredit contest as well: <https://github.com/code-423n4/2021-07-wildcredit-findings/issues/75> where it was reported that "`latestAnswer` method will return the last value, but you won’t be able to check if the data is fresh. On the other hand, calling the method `latestRoundData` allows you to run some extra validations.”

#### Proof of Concept

<https://github.com/code-423n4/2021-09-wildcredit/blob/c48235289a25b2134bb16530185483e8c85507f8/contracts/UniswapV3Oracle.sol#L101>

See <https://docs.chain.link/docs/deprecated-aggregatorinterface-api-reference/#latestanswer>.

#### Tools Used

Manual Analysis

#### Recommended Mitigation Steps

Use V3 interface functions: <https://docs.chain.link/docs/price-feeds-api-reference/>

**[talegift (Wild Credit) acknowledged:](https://github.com/code-423n4/2021-09-wildcredit-findings/issues/55#issuecomment-932200536):**
 > We'll remove dependence on Chainlink completely.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Wild Credit |
| Report Date | N/A |
| Finders | 0xRajeev, cmichel  leastwood. |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-wildcredit
- **GitHub**: https://github.com/code-423n4/2021-09-wildcredit-findings/issues/55
- **Contest**: https://code4rena.com/contests/2021-09-wild-credit-contest

### Keywords for Search

`vulnerability`

