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
solodit_id: 63363
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

[M-06] Users Can Bypass the Minimum Deposit Check via Partial Withdrawal

### Overview


The userDeposit() function in the Vault contract is not properly validating the minimum deposit amount. This allows users to withdraw their deposits partially, which can lead to spamming the system with small deposits. This bug has a medium risk and is located in the Vault.sol file. The impact of this bug includes bypassing the minimum deposit requirement and potential malicious spamming. To fix this, the team recommends either removing the partial withdraw option or checking that the remaining deposits are above the minimum requirement after processing a withdrawal. This bug has been fixed by the team.

### Original Finding Content


## Severity

Medium Risk

## Description

The `userDeposit()` function is meant to validate the amount against the contract's specified minimum and maximum values, to make sure the position is correctly created. However, this mechanism can be bypassed in terms of the minimum deposit, since the contract allows users to withdraw their unprocessed deposits partially.

This creates the scenario in which:

1. Bob deposits a value X, which is perfectly `X > minDeposit` and `X < maxDeposit`
2. Bob invokes `requestWithdrawDeposit()` and passes `X - 1` as the amount
3. Bob's original deposit is reduced below the minimum

This has the same impact as being able to spam the system with dust deposits to overwhelm the processing during the minting phase.

## Location of Affected Code

File: [contracts/vault/Vault.sol#L457](https://github.com/COLB-DEV/SmartContracts/blob/809055574cb7d7bd7c711b87745c081524547eb4/contracts/vault/Vault.sol#L457)

```solidity
function requestWithdrawDeposit(uint256 amount) external {
    if (block.timestamp > investmentEnd) {
        revert InvestmentPeriodFinish();
    }

    address user = msg.sender;
    UserStat memory userStat = usersStat[user];
    if (userStat.totalDeposit < amount) {
        revert OverflowAmountToWithdraw();
    }

    WithdrawInfo memory withdrawInfo = WithdrawInfo(
        user,
        uint32(block.timestamp),
        false,
        false,
        amount
    );

    uint256 index = withdraws.length;

    withdraws.push(withdrawInfo);

    withdrawToProcess.push(index);
    usersWithdraw[user].push(index);
    factory.emitRequestWithdraw(user, amount, index);
}
```

File: [contracts/vault/Vault.sol#L530](https://github.com/COLB-DEV/SmartContracts/blob/809055574cb7d7bd7c711b87745c081524547eb4/contracts/vault/Vault.sol#L530)

```solidity
function processWithdrawDeposit(
    uint256 processIndex
) external onlyOperator {
    uint256 indexWithdraw = withdrawToProcess[processIndex];
    WithdrawInfo storage withdrawInfo = withdraws[indexWithdraw];
    if (withdrawInfo.processed) {
        revert AlreadyProcessed();
    }
    if (withdrawInfo.nativeToken) {
        revert IncorrectWithdrawMethod();
    }
    withdrawInfo.processed = true;
    address user = withdrawInfo.sender;
    uint256 amount = withdrawInfo.amount;
    uint256 restToReimbourse = amount;

    UserStat storage userStat = usersStat[user];
    userStat.totalDeposit -= amount;

    uint256[] memory userDepos = usersDeposit[user];
    uint256 totalDifferentDeposit = userDepos.length;
    if (totalDifferentDeposit == 0) {
        revert NothingToReimboursed();
    }

    // if  user make deposit in different token, we withdraw from these different deposit if it's possible
    for (uint256 index = 0; index < totalDifferentDeposit; index++) {
        uint256 indexDeposit = userDepos[index];
        DepositInfo storage deposit = deposits[indexDeposit];
        if (deposit.processed == false && deposit.reimboursed == false) {
            uint256 amountDeposited = deposit.amount;
            // we reimbourse in token deposited
            uint256 amountToUse = restToReimbourse > amountDeposited
                ? amountDeposited
                : restToReimbourse;
            deposit.amount = 0;
            restToReimbourse -= amountToUse;
            IERC20(deposit.token).safeTransfer(user, amountToUse);
        }

        if (restToReimbourse == 0) {
            break;
        }
    }

    factory.emitWithdraw(msg.sender, amount, indexWithdraw);
}
```

## Impact

- Bypassing the minimum deposit per position.
- Ability to maliciously spam low-value deposits.

## Recommendation

There are two ways of mitigation:

- Force the `requestWithdrawDeposit()` to withdraw the entire deposit amount, removing the partial withdraw option.
- The `processWithdrawDeposit()` should check at the end if the non-depleted deposits touched by the function remain above the minimum required amount.

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

