---
# Core Classification
protocol: Colbfinance Vault
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63360
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/ColbFinance-Vault-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-03] Withdrawing A Partial Deposit Amount Leads To Loss Of Assets

### Overview


This bug report discusses an issue with the `Vault` contract that allows users to withdraw their funds. The problem occurs when a user requests to withdraw their unprocessed deposits and reclaim their initial transfer. The code for this process is meant to check if the requested amount is greater than the current deposit and only use the smaller amount to reduce the request. However, the code then completely resets the deposit amount, resulting in 100 tokens being stuck in the contract. This issue can be temporarily resolved by the operator manually processing the deposits, but it is still a problem that needs to be fixed. The team has acknowledged the bug and has fixed it by not fully resetting the deposit amount, but rather reducing it according to the reimbursement. This bug has a medium risk severity and impacts the internal accounting of the contract and temporarily freezes funds. 

### Original Finding Content


## Severity

Medium Risk

## Description

The `Vault` contract allows users to send 2 types of withdrawal requests: withdraw vault shares for underlying tokens or withdraw their unprocessed deposits and reclaim their initial transfer.
The latter is done by first invoking `requestWithdrawDeposit()`, which creates the request with the amount, which could be used to only partially reduce our initial unprocessed deposit.
Then, the operator is meant to call `processWithdrawDeposit()`, which iterates over all of the user's unprocessed deposits and checks if `requestAmount > currentDeposit` and uses the smaller amount to reduce the `requestAmount`. The code, however, then completely resets the deposit amount: `deposit.amount = 0`, no matter if not all of the deposit was required to reimburse the user.

For example:

1. A user accidentally deposits 110 USC instead of 100
2. Before their request gets processed, they invoke a deposit withdrawal of 10 USC
3. The code goes over their only request and checks if 10 > 100
4. 10 is smaller, so the code reduces the amount to reimburse to 0, transfers 10 USC to the user and resets their entire 110 deposit to 0
5. 100 tokens are stuck inside the contract.

Currently, the manual operator processing of deposits is unrestricted, so they can mint shares to back those 100 stuck tokens and rescue them, which makes the freezing of funds only temporary.

## Location of Affected Code

File: [contracts/vault/Vault.sol#L565](https://github.com/COLB-DEV/SmartContracts/blob/809055574cb7d7bd7c711b87745c081524547eb4/contracts/vault/Vault.sol#L565)

```solidity
function processWithdrawDeposit( uint256 processIndex ) external onlyOperator {
  // code
  uint256 amountDeposited = deposit.amount;

  uint256 amountToUse = restToReimbourse > amountDeposited
      ? amountDeposited
      : restToReimbourse;

  deposit.amount = 0; //<--------
  restToReimbourse -= amountToUse;
  IERC20(deposit.token).safeTransfer(user, amountToUse);
  // code
}
```

## Impact

- Incorrect internal accounting
- Temporarily frozen funds inside the contract

## Recommendation

Do not fully reset the deposit amount, reduce it according to the reimbursement.

## Team Response

Fixed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Colbfinance Vault |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/ColbFinance-Vault-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

