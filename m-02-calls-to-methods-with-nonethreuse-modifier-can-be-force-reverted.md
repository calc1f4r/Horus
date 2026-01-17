---
# Core Classification
protocol: Pino
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27252
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-09-01-Pino.md
github_link: none

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
  - Pashov
---

## Vulnerability Title

[M-02] Calls to methods with `nonETHReuse` modifier can be force reverted

### Overview


This bug report covers a security vulnerability in the contracts under the `protocols/` directory. These contracts contain the `nonETHReuse` modifier, which calls the `_nonReuseBefore()` method. This method checks the `_status` variable, and if it is `ENTERED`, it will revert the transaction. This means that if two transactions are called in a row, the second one will be reverted. The only way to "unlock" the contracts is through a `Multicall::multicall` call, which sets `_status = NOT_ENTERED;`.

This vulnerability can be exploited in the following way: Alice wants to call a method directly, but Bob front-runs it with another direct call. As a result, the `_status` variable is set to `ENTERED`, which reverts Alice's transaction. This has a medium impact, as the user will get their transaction reverted, but it can be replayed through a `Multicall` call. The likelihood of this attack is also medium, as it can only happen when there is a direct call to such methods, which isn't the usual way to use the app.

The recommendation to fix this vulnerability is to consider forbidding direct calls to methods and force them to be done through `Multicall`.

### Original Finding Content

**Severity**

**Impact:**
Medium, as the user will get its transaction reverted, but it can be replayed through a `Multicall` call

**Likelihood:**
Medium, as it can only happen when there is a direct call to such methods, which isn't the usual way to use the app

**Description**

In the contracts under `protocols/` we see a good amount of their methods having the `nonETHReuse` modifier. The modifier code calls the following method:

```solidity
    function _nonReuseBefore() private {
        // On the first call to nonETHReuse, _status will be NOT_ENTERED
        if (_status == ENTERED) {
            revert EtherReuseGuardCall();
        }

        // Any calls to nonETHReuse after this point will fail
        _status = ENTERED;
    }
```

This code means that if a method with the modifier is called two times in a row, the second call would be reverted. The only way to "unlock" the contracts is through a `Multicall::multicall` call, which sets `_status = NOT_ENTERED;`. Because of this, the following attack can be executed:

1. Alice wants to directly (not through `Multicall`) call a method that has the `nonETHReuse` modifier, for example `Compound::depositWETHV2`
2. Bob sees Alice's transaction and front-runs it with another direct call to a method that has the `nonETHReuse` modifier, for example `Compound::depositETHV2`
3. Since Bob's transaction was executed first, now we have `_status == ENTERED`, which would revert Alice's transaction

**Recommendations**

Consider forbidding direct calls to methods and force them to be done through `Multicall`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Pino |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-09-01-Pino.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

