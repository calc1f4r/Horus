---
# Core Classification
protocol: AegisVault
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41329
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/AegisVault-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-06] Bypassing `MIN_INITIAL_DEPOSIT`

### Overview


The bug report discusses a vulnerability in the Aegis vault, where users can bypass a check designed to prevent attacks by first depositors. The check is not properly enforced in the withdraw operation, allowing users to withdraw shares until the remaining shares or total supply is lower than the minimum initial deposit. The report recommends implementing a check in the withdraw operation to ensure that the total supply is not lower than the minimum initial deposit. This will prevent potential attacks by first depositors.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

When users first deposit into the Aegis vault (`aegisTotalSupply` is 0), the operation will check if `aegisShares` minted is greater than `MIN_INITIAL_DEPOSIT`. This is designed to prevent attacks from first depositors.

```solidity
    function __deposit(
        uint256 depositSharesAmount,
        uint256 aegisTotalSupply,
        uint256 depositSpotPrice,
        uint256 targetSpotPrice
    )
        private
        returns (uint256 aegisShares)
    {
        // ...
        if (aegisTotalSupply == 0) {
            // better to use userDepositValue than userValueContribution here, because userValueContribution could be very small
            aegisShares = ctx.userDepositValue;
            // simplified check for initial deposit
            // @audit - can this exploited by withdrawing immediately until aegisShares lower than minimum
>>>         require(aegisShares >= MIN_INITIAL_DEPOSIT, "VTS");
        } else {
            /// @dev invariant check for guaranteed safety, since at this point the AegisVault has received any ICHIVault shares
            /// either from a depositToken deposit or for a depositVault share transfer therefore given existing prior deposits
            /// the user's contribution to the whole must necessarily be less than the whole i.e. PRECISION i.e. 1e18
            require(ctx.userValueContribution < PRECISION, "VTS");
            aegisShares = _mulDiv(ctx.userValueContribution, aegisTotalSupply, PRECISION.sub(ctx.userValueContribution));
        }
    }
```

However, this can be easily bypassed by immediately withdrawing shares until it becomes feasible to perform a first depositor attack since there is no check in the withdraw operation to ensure that the remaining shares or total supply are greater than `MIN_INITIAL_DEPOSIT`.

## Recommendations

Check the new total supply after the `withdraw` operation. If it is not zero and is lower than `MIN_INITIAL_DEPOSIT`, revert the operation.

```diff
    function _withdraw(
        uint256 aegisShares,
        uint256 aegisTotalSupply,
        address to,
        WithdrawSlippageData memory minSlippage,
        WithdrawType withdrawType
    )
        internal
        returns (WithdrawSlippageData memory actualSlippage, uint256 aegisSharesWithdrawn)
    {
        // ...

+      uint256 newAegisTotalSupply = aegisTotalSupply - aegisSharesWithdrawn;
+      require(newAegisTotalSupply == 0  || newAegisTotalSupply >= MIN_INITIAL_DEPOSIT, "VTS");
        _checkWithdrawSlippage(actualSlippage, minSlippage);
        emit Withdraw(msg.sender, to, aegisShares, actualSlippage);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | AegisVault |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/AegisVault-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

