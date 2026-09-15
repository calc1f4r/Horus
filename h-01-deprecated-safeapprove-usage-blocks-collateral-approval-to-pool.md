---
# Core Classification
protocol: Hyperlend_2025-11-21
chain: everychain
category: uncategorized
vulnerability_type: erc20

# Attack Vector Details
attack_type: erc20
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63922
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperlend-security-review_2025-11-21.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.90
financial_impact: high

# Scoring
quality_score: 4.5
rarity_score: 3

# Context Tags
tags:
  - erc20

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] Deprecated `safeApprove()` usage blocks collateral approval to pool

### Overview


This bug report is about a medium severity issue in a project that uses Openzeppelin@v4.9.6. The problem is that the project is using a deprecated function called `safeApprove()` which is not safe to use in this case. This is because it blocks every approval if the approval for the collateral is non-zero. The report suggests using a different function called `forceApprove()` instead of `safeApprove()`.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

Project uses Openzeppelin@v4.9.6, which deprecates `safeApprove()`. Safe approve usage is not safe here because it blocks every approval if approval for the collateral is non-zero:

```solidity
//    function executeOperation()

        for (uint256 i = 0; i < _collateralActions.length; ++i){
            uint256 amount = _collateralActions[i].amount;
            IERC20 token = _collateralActions[i].token;

            //transfer tokens from the caller & approve pool contract to spend them
            token.safeTransferFrom(msg.sender, address(this), amount);
@>          token.safeApprove(address(pool), type(uint256).max);

            //supply tokens on behalf of the msg.sender
            pool.supply(address(token), amount, msg.sender, 0);
        }
```

https://github.com/OpenZeppelin/openzeppelin-contracts/blob/dc44c9f1a4c3b10af99492eed84f83ed244203f6/contracts/token/ERC20/utils/SafeERC20.sol#L45-L54

```solidity
    function safeApprove(IERC20 token, address spender, uint256 value) internal {
        // safeApprove should only be called when setting an initial allowance,
        // or when resetting it to zero. To increase and decrease it, use
        // 'safeIncreaseAllowance' and 'safeDecreaseAllowance'
        require(
            (value == 0) || (token.allowance(address(this), spender) == 0),
            "SafeERC20: approve from non-zero to non-zero allowance"
        );
        _callOptionalReturn(token, abi.encodeWithSelector(token.approve.selector, spender, value));
    }
```

After the first approval for collateral, every other call will fail because of the `require` line in `safeApprove()`.

## Recommendations

Consider using `forceApprove()` instead of `safeApprove()`.





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4.5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperlend_2025-11-21 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperlend-security-review_2025-11-21.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`ERC20`

