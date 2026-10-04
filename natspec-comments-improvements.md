---
# Core Classification
protocol: Hooks Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52488
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/tren-finance/hooks-contracts
source_link: https://www.halborn.com/audits/tren-finance/hooks-contracts
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

NatSpec Comments Improvements

### Overview

See description below for full details.

### Original Finding Content

##### Description

The NatSpec documentation of the contracts and interfaces in scope contain inconsistencies and omissions that reduce clarity and could lead to misunderstandings for developers and auditors:

  

* **Inconsistent Caller Documentation**

The `unstake()` function in `SwapManager` checks for `trenBoxStorage` as the caller, but the NatSpec comment incorrectly states that the caller should be `borrowerOperations`:

```
/// @inheritdoc ISwapManager
function unstake(address coll, uint256 collAmount) external {
  if (msg.sender != trenBoxStorage) {
    revert SwapManager__CallerIsNotTrenBoxStorage();
  }
...
```

```
/**
 * @notice Unstakes collateral
 * @dev Only BorrowerOperations contract can call
 * We just unstake LP token from Gauge without claiming rewards
 * @param coll The address of collateral asset
 * @param collAmount The amount of collateral to unstake
 */
function unstake(address coll, uint256 collAmount) external;
```

  

* **Misordered Parameters**

In the `_swapExactInput()` function in `SwapManager`, the NatSpec comments list `@param stablecoin` and `@param directSwap` in the wrong order, leading to confusion when reviewing the code:

```
/**
 ...
 * @param stablecoin The address of stablecoin if the swap is indirect
 * @param directSwap True if the swap is direct, false if it's indirect
 ...
 */
function _swapExactInput(
  ...
  bool directSwap,
  address stablecoin,
  ...
)
```

  

* **Missing NatSpec in** `ISwapper` **Interface**

The `ISwapper` interface lacks NatSpec comments for its functions, creating inconsistency with the rest of the codebase and reducing overall readability.

##### BVSS

[AO:S/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U (0.0)](/bvss?q=AO:S/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U)

##### Recommendation

In order to improve the NatSpec documentation of the project, consider the following recomendations:

* **Correct NatSpec Comments:** Update the `unstake()` function's NatSpec to reflect that `trenBoxStorage` is the intended caller, ensuring consistency between the comments and the code.
* **Reorder Parameters in NatSpec:** Fix the order of `@param stablecoin` and `@param directSwap` in `_swapExactInput()` to match the function signature.
* **Add NatSpec to** `ISwapper`: Include comprehensive NatSpec comments for all functions in the `ISwapper` interface to ensure consistency and clarity across the codebase.

  

These improvements will enhance readability, minimize misunderstandings, and ensure a more maintainable and developer-friendly codebase.

##### Remediation

**SOLVED:** The **Tren finance team** fixed this finding in commit `1820f68` by implementing the recommendation.

##### Remediation Hash

<https://github.com/Tren-Finance/Tren-Contracts/commit/1820f683fbd19cd839c6688a38a00911df95cafc>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Hooks Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/tren-finance/hooks-contracts
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/tren-finance/hooks-contracts

### Keywords for Search

`vulnerability`

