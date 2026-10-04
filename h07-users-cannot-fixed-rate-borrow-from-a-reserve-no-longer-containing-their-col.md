---
# Core Classification
protocol: Aave Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11603
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/aave-protocol-audit/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - indexes
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[H07] Users cannot fixed-rate borrow from a reserve no longer containing their collateral

### Overview


This bug report is about a restriction implemented within the `borrow` function on lines 216 to 221 of `LendingPool.sol` which prevents users from borrowing at a fixed rate from a reserve where they previously had collateral (but no longer do). When the user attempts to borrow from that reserve, the condition in line 220 will fail, thus reverting the transaction. As a result, the user is unable to borrow from this reserve even if they are not currently holding any collateral in it.

The suggested solution is to programmatically toggle to `false` the `useAsCollateral` flag once a user has withdrawn all collateral from a reserve.

After applying a patch in MR#74, the Aave team correctly pointed out that the team misinterpreted the function’s behavior and this is not an issue. The fix will still remain in place, and the development team will include relevant test cases to programmatically confirm this is indeed not an issue.

### Original Finding Content

To prevent abuses in the protocol, borrowing at a fixed rate (from the same reserve where the borrower deposited collateral) is only allowed if the amount being borrowed is greater than the collateral. This restriction is implemented within the `borrow` function on [lines 216 to 221 of `LendingPool.sol`](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L216-221).


However, the restriction currently disallows users borrowing at a fixed rate from a reserve where they *previously* had collateral (but no longer do). After a user withdraws all collateral from a reserve, the system does not automatically toggle to `false` the [`isUserUseReserveAsCollateralEnabled` flag](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/libraries/CoreLibrary.sol#L35). When the user attempts to borrow from that reserve, the [condition in line 220](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L219) will fail, thus reverting the transaction. As a result, the user is unable to borrow from this reserve even if they are not currently holding any collateral in it.


Consider programmatically toggling to `false` the [`useAsCollateral` flag](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/libraries/CoreLibrary.sol#L35) once a user has withdrawn all collateral from a reserve.


**Update**: *After applying a patch in [MR#74](https://gitlab.com/aave-tech/dlp/contracts/merge_requests/74/diffs), the Aave team correctly pointed out that we misinterpreted the function’s behavior and this is not an issue. The fix will still remain in place, and the development team will include relevant test cases to programmatically confirm this is indeed not an issue.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Aave Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/aave-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

