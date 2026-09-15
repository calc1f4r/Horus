---
# Core Classification
protocol: Alchemix
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2369
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-alchemix-contest
source_link: https://code4rena.com/reports/2022-05-alchemix
github_link: https://github.com/code-423n4/2022-05-alchemix-findings/issues/60

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
  - liquid_staking
  - dexes
  - yield
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Ruhum
---

## Vulnerability Title

[M-04] YearnTokenAdapter allows a maximum loss of 100% when withdrawing

### Overview


This bug report is about the YearnTokenAdapter which allows a 100% slippage when withdrawing from the vault. This will cause a loss of funds for users. The Yearn vault contract allows the user to specify the 'maxLoss' as the last parameter which determines how many shares can be burned to fulfill the withdrawal. Currently, the contract uses 10.000 which is 100%. This means there is no slippage check at all. 

The proof of concept for this bug is the current 'maxLoss' value (https://github.com/code-423n4/2022-05-alchemix/blob/main/contracts-full/adapters/yearn/YearnTokenAdapter.sol#L13) and the call to the Yearn vault's 'withdraw()' function (https://github.com/code-423n4/2022-05-alchemix/blob/main/contracts-full/adapters/yearn/YearnTokenAdapter.sol#L43).

The recommended mitigation step is to allow the user to specify the slippage value themselves. If the user does not want to change the ITokenAdapter interface, they can also leave the value blank. The vault will then use the default value (0.01%).

### Original Finding Content

_Submitted by Ruhum_

[YearnTokenAdapter.sol#L13](https://github.com/code-423n4/2022-05-alchemix/blob/main/contracts-full/adapters/yearn/YearnTokenAdapter.sol#L13)<br>
[YearnTokenAdapter.sol#L43](https://github.com/code-423n4/2022-05-alchemix/blob/main/contracts-full/adapters/yearn/YearnTokenAdapter.sol#L43)<br>

YearnTokenAdapter allows slippage of 100% when withdrawing from the vault which will cause a loss of funds.

Here's the documentation straight from the vault contract: <https://github.com/yearn/yearn-vaults/blob/main/contracts/Vault.vy#L1025-L1073>
It allows the user to specify the `maxLoss` as the last parameter. It determines how many shares can be burned to fulfill the withdrawal. Currently, the contract uses 10.000 which is 100%. Meaning there is no slippage check at all. This is bound to cause a loss of funds.

I'd suggest letting the user determine the slippage check themselves instead of hardcoding it.

### Proof of Concept

Current `maxLoss` value: <https://github.com/code-423n4/2022-05-alchemix/blob/main/contracts-full/adapters/yearn/YearnTokenAdapter.sol#L13>

call to Yearn vault's `withdraw()` function: <https://github.com/code-423n4/2022-05-alchemix/blob/main/contracts-full/adapters/yearn/YearnTokenAdapter.sol#L43>

### Recommended Mitigation Steps

Allow the user to specify the slippage value themselves:

```sol
    function unwrap(uint256 amount, address recipient, uint maxLoss) external override returns (uint256) {
        TokenUtils.safeTransferFrom(token, msg.sender, address(this), amount);

        uint256 balanceBefore = TokenUtils.safeBalanceOf(token, address(this));

        uint256 amountWithdrawn = IYearnVaultV2(token).withdraw(amount, recipient, maxLoss);

        uint256 balanceAfter = TokenUtils.safeBalanceOf(token, address(this));

        // If the Yearn vault did not burn all of the shares then revert. This is critical in mathematical operations
        // performed by the system because the system always expects that all of the tokens were unwrapped. In Yearn,
        // this sometimes does not happen in cases where strategies cannot withdraw all of the requested tokens (an
        // example strategy where this can occur is with Compound and AAVE where funds may not be accessible because
        // they were lent out).
        if (balanceBefore - balanceAfter != amount) {
            revert IllegalState();
        }

        return amountWithdrawn;
    }
```

If you don't want to change the ITokenAdapter interface you can also leave the value blank. The vault will then use the default value (`0.01%`)


**[0xfoobar (Alchemix) acknowledged, disagreed with severity and commented](https://github.com/code-423n4/2022-05-alchemix-findings/issues/60#issuecomment-1133991312):**

> This could be made more configurable by the end user but yearn vaults do not frequently experience high slippage. Slippage is handled upstream in the Alchemist contract. The reason why this slippage is set to 100% is so to permit handling of slippage in the Alchemist for all cases.

**[0xleastwood (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-05-alchemix-findings/issues/60#issuecomment-1146206028):**
 > Because we can't know how the yearn strategy implements withdrawals, its possible that it might contain custom swap logic which exposes itself to sandwich attacks. However, at face value, the current use of `MAXIMUM_SLIPPAGE` allows the contract to successfully unwrap their tokens under poor network conditions, but it makes sense for the user to have more control over this. Downgrading this to medium risk as I believe it is more in line with that.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Alchemix |
| Report Date | N/A |
| Finders | Ruhum |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-alchemix
- **GitHub**: https://github.com/code-423n4/2022-05-alchemix-findings/issues/60
- **Contest**: https://code4rena.com/contests/2022-05-alchemix-contest

### Keywords for Search

`vulnerability`

