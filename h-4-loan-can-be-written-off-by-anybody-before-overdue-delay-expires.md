---
# Core Classification
protocol: Union Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3569
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/11
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-union-finance-judging/issues/115

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
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Bahurum
---

## Vulnerability Title

H-4: Loan can be written off by anybody before overdue delay expires

### Overview


This bug report is about an issue found in the Union Finance smart contract. When a borrower takes a second loan after a loan that has been written off, this second loan can be written off instantly by any other member due to missing update of last repay block, leaving the staker at a loss. This is because the `lastRepay` block is not updated when the debt is written off completely, leaving it with a stale value. This allows anyone to write off the debt before the overdue delay expires and the staker loses the staked amount. The tool used to find this issue was manual review. The recommendation is to reset the `lastRepay` block to 0 when the debt is written off completely.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-union-finance-judging/issues/115 

## Found by 
Bahurum

## Summary
When a borrower takes a second loan after a loan that has been written off, this second loan can be written off instantly by any other member due to missing update of last repay block, leaving the staker at a loss.

## Vulnerability Detail
1. A staker stakes and vouches a borrower
2. the borrower borrows calling `UToken:borrow`: `accountBorrows[borrower].lastRepay` is updated with the current block number
3. the staker writes off the entire debt of the borrower calling `UserManager:debtWriteOff`. In the internal call to `UToken:debtWriteOff` the principal is set to zero but `accountBorrows[borrower].lastRepay` is not updated
4. 90 days pass and a staker vouches for the same borrower
5. the borrower borrows calling `UToken:borrow`: `accountBorrows[borrower].lastRepay` is not set to the current block since non zero and stays to the previous value.
6. `accountBorrows[borrower].lastRepay` is now old enough to allow the check in 
`UserManager:debtWriteOff` at line 738 to pass. The debt is written off by any other member immediatly after the loan is given. The staker looses the staked amount immediatly.

```solidity
        if (block.number <= lastRepay + overdueBlocks + maxOverdueBlocks) {
            if (staker != msg.sender) revert AuthFailed();
        }
```

7. The last repay block is still stale and a new loan can be taken and written off immediatly many times as long as stakers are trusting the borrower

Note that this can be exploited maliciously by the borrower, who can continously ask for loans and then write them off immediatly.

## Impact
The staker of the loan looses the staked amount well before the overdue delay is expired

## Code Snippet
https://github.com/sherlock-audit/2022-10-union-finance/blob/main/union-v2-contracts/contracts/market/UToken.sol#L666-L672

```solidity
    function debtWriteOff(address borrower, uint256 amount) external override whenNotPaused onlyUserManager {
        uint256 oldPrincipal = getBorrowed(borrower);
        uint256 repayAmount = amount > oldPrincipal ? oldPrincipal : amount;

        accountBorrows[borrower].principal = oldPrincipal - repayAmount;
        totalBorrows -= repayAmount;
    }
```
## Tool used

Manual Review

## Recommendation
Reset `lastRepay` for the borrower to 0 when the debt is written off completely

```diff
    function debtWriteOff(address borrower, uint256 amount) external override whenNotPaused onlyUserManager {
        uint256 oldPrincipal = getBorrowed(borrower);
        uint256 repayAmount = amount > oldPrincipal ? oldPrincipal : amount;

+       if (oldPrincipal == repayAmount) accountBorrows[borrower].lastRepay = 0;
        accountBorrows[borrower].principal = oldPrincipal - repayAmount;
        totalBorrows -= repayAmount;
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Union Finance |
| Report Date | N/A |
| Finders | Bahurum |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-union-finance-judging/issues/115
- **Contest**: https://app.sherlock.xyz/audits/contests/11

### Keywords for Search

`vulnerability`

