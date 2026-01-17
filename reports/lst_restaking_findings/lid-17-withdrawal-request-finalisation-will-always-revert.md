---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53466
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Hexens
---

## Vulnerability Title

[LID-17] Withdrawal request finalisation will always revert

### Overview


A critical bug has been found in the Lido contract, specifically in the OracleReportSanityChecker.sol file. This bug causes withdrawal requests to fail and always revert. The issue is that the function `getWithdrawalRequestStatus` does not exist in the WithdrawalQueue contract, which is called by the OracleReportSanityChecker. This bug has not been noticed before due to the use of mock contracts in testing. To fix this, the function `getWithdrawalRequestStatus` should be added to the WithdrawalQueue contract. This issue has been resolved.

### Original Finding Content

**Severity:** Critical

**Path:** OracleReportSanityChecker.sol:_checkRequestIdToFinalizeUpTo#L571-L581

**Description:**

A withdrawal request gets finalised through an oracle report from the AccountingOracle to the Lido contract. Lido in turn checks the report’s data using the OracleReportSanityChecker.

With regard to the withdrawal requests data, Lido calls `checkWithdrawalQueueOracleReport` on the OracleReportSanityChecker, which in turn calls `getWithdrawalRequestStatus` with the request ID on the WithdrawalQueue contract.

However, the function `getWithdrawalRequestStatus` does not exist in the WithdrawalQueue contract.

As a result, withdrawal request finalisation will always revert.

We suspect that this vulnerability never surfaced due to the use mock contracts. For example, the tests for the OracleReportSanityChecker use a WithdrawalQueueStub contract, which has the missing function but returns mock values.

**Remediation:**  We would recommend to add the function `getWithdrawalRequestStatus` to the WithdrawalQueue contract.

For example:


```
function getWithdrawalRequestStatus(uint256 _requestId)
    external
    view
    returns (WithdrawalRequestStatus memory)
{
    return _getStatus(_requestId);
}
```

**Status:** Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

