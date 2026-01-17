---
# Core Classification
protocol: Backd
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2102
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-backd-contest
source_link: https://code4rena.com/reports/2022-04-backd
github_link: https://github.com/code-423n4/2022-04-backd-findings/issues/121

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
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WatchPug
---

## Vulnerability Title

[M-13] `CEthInterface#repayBorrowBehalf()` reading non-existing returns makes  `_repayAnyDebt()` with CEther always revert

### Overview


This bug report is about a vulnerability in the code of the 'CTokenInterfaces.sol' file on GitHub. The 'repayBorrowBehalf()' function for native cToken (CEther) will return nothing, while the current 'CEthInterface' interface defines the returns as '(uint256)'. This means that 'ether.repayBorrowBehalf()' will always revert. The 'Compound cToken Repay Borrow Behalf doc' and 'Compound CEther.repayBorrowBehalf()' and 'Compound CErc20.repayBorrowBehalf()' from Compound Finance are also mentioned in the report. 

The vulnerability is related to the 'repayBorrowBehalf()' function. This function is used to repay a loan on behalf of a borrower. The issue is that the 'repayBorrowBehalf()' function for native cToken (CEther) will return nothing, while the current 'CEthInterface' interface defines the returns as '(uint256)'. This means that 'ether.repayBorrowBehalf()' will always revert. This issue can be fixed by updating the 'CEthInterface' interface to return the correct value.

### Original Finding Content

_Submitted by WatchPug_

[CTokenInterfaces.sol#L355-L358](https://github.com/code-423n4/2022-04-backd/blob/c856714a50437cb33240a5964b63687c9876275b/backd/interfaces/vendor/CTokenInterfaces.sol#L355-L358)<br>

```solidity
function repayBorrowBehalf(address borrower, uint256 repayAmount)
        external
        payable
        returns (uint256);
```

`repayBorrowBehalf()` for native cToken (`CEther`) will return nothing, while the current `CEthInterface` interface defines the returns as `(uint256)`.

As a result, `ether.repayBorrowBehalf()` will always revert

[CompoundHandler.sol#L117-L118](https://github.com/code-423n4/2022-04-backd/blob/c856714a50437cb33240a5964b63687c9876275b/backd/contracts/actions/topup/handlers/CompoundHandler.sol#L117-L118)<br>

```solidity
CEther cether = CEther(address(ctoken));
err = cether.repayBorrowBehalf{value: debt}(account);
```

Ref:

| method              | CEther     | CErc20     |
| ------------------- | ---------- | ---------- |
| mint()              | revert     | error code |
| redeem()            | error code | error code |
| repayBorrow()       | revert     | error code |
| repayBorrowBehalf() | revert     | error code |

*   [Compound cToken Repay Borrow Behalf doc](https://compound.finance/docs/ctokens#repay-borrow-behalf)
*   [Compound CEther.repayBorrowBehalf()](https://github.com/compound-finance/compound-protocol/blob/v2.8.1/contracts/CEther.sol#L92-L95)
*   [Compound CErc20.repayBorrowBehalf()](https://github.com/compound-finance/compound-protocol/blob/v2.8.1/contracts/CErc20.sol#L94-L97)

**[chase-manning (Backd) confirmed](https://github.com/code-423n4/2022-04-backd-findings/issues/121)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Backd |
| Report Date | N/A |
| Finders | WatchPug |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-backd
- **GitHub**: https://github.com/code-423n4/2022-04-backd-findings/issues/121
- **Contest**: https://code4rena.com/contests/2022-04-backd-contest

### Keywords for Search

`vulnerability`

