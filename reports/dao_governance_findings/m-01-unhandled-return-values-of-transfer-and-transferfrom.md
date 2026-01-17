---
# Core Classification
protocol: Inverse Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42985
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-10-inverse
source_link: https://code4rena.com/reports/2022-10-inverse
github_link: https://github.com/code-423n4/2022-10-inverse-findings/issues/10

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
  - cdp
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 2997ms
---

## Vulnerability Title

[M-01] Unhandled return values of `transfer` and `transferFrom`

### Overview


The report states that there is a potential issue with the consistency of ERC20 implementations. Some implementations of the transfer and transferFrom functions may return 'false' instead of reverting on failure. As a precaution, it is recommended to wrap these calls in 'require()' statements or use OpenZeppelin's SafeERC20 wrapper functions. The report also provides links to the specific code lines where this issue was found. The team behind the project has acknowledged the issue and commented on it, stating that they will ensure the tokens used in their deployment are trusted and audited by the DAO and governance. 

### Original Finding Content


ERC20 implementations are not always consistent. Some implementations of transfer and transferFrom could return ‘false’ on failure instead of reverting. It is safer to wrap such calls into `require()` statements to these failures.

### Proof of Concept

<https://github.com/code-423n4/2022-10-inverse/blob/main/src/Market.sol#L205><br>
<https://github.com/code-423n4/2022-10-inverse/blob/main/src/Market.sol#L280><br>
<https://github.com/code-423n4/2022-10-inverse/blob/main/src/Market.sol#L399><br>
<https://github.com/code-423n4/2022-10-inverse/blob/main/src/Market.sol#L537><br>
<https://github.com/code-423n4/2022-10-inverse/blob/main/src/Market.sol#L570><br>
<https://github.com/code-423n4/2022-10-inverse/blob/main/src/Market.sol#L602><br>

### Recommended Mitigation Steps

Check the return value and revert on `0/false` or use OpenZeppelin’s SafeERC20 wrapper functions.

**[08xmt (Inverse) acknowledged and commented](https://github.com/code-423n4/2022-10-inverse-findings/issues/10#issuecomment-1351551238):**
 > Every deployment of a market will use a trusted token, and be audited by the DAO and governance. Even when using safe transfer, there's no guarantee that an ERC20 token will behave as expected.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Inverse Finance |
| Report Date | N/A |
| Finders | 2997ms |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-inverse
- **GitHub**: https://github.com/code-423n4/2022-10-inverse-findings/issues/10
- **Contest**: https://code4rena.com/reports/2022-10-inverse

### Keywords for Search

`vulnerability`

