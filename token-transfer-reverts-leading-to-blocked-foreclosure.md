---
# Core Classification
protocol: Spokes V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51920
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/concrete/spokes-v1
source_link: https://www.halborn.com/audits/concrete/spokes-v1
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
  - Halborn
---

## Vulnerability Title

Token Transfer Reverts Leading to Blocked Foreclosure

### Overview


This bug report discusses an issue with the `_executeForeclosure` function in the Blueprint-Finance/spokes-v1 contract. This function is used to repay unsecured debt during the foreclosure process. The problem arises when the transfer of tokens to the owner's address fails, causing the entire foreclosure process to revert. This prevents the liquidation of the unsecured position. 

The report suggests using the pull pattern instead, where the tokens are not transferred directly to the owner's address, but rather increase the internal balance of pending withdrawals. This would also introduce a claim functionality that allows the owner to manually withdraw the remaining funds. 

The recommended remediation code is provided, along with a reference to the relevant line of code in the contract. The BVSS score for this bug is 5.0, indicating a medium severity issue. 

### Original Finding Content

##### Description

The `_executeForeclosure` function is invoked during the foreclosure flow to execute the logic required to repay unsecured debt. Using the assets withdrawn from the lender, it repays the borrowed amount, subtracts the fee, and sends the remaining collateral back to the position owner.

```
        // ------ repay to the claimRouter/fundRequester(flashloan) ------
        params.amountInBorrowTokenLeft -= params.totalRepayAmountInToken;
        if (isEarnFlashloan) {
            _increaseAllowanceIfNecessary(params.claimRouter, borrowToken, params.totalRepayAmountInToken);
        } else {
            IERC20(borrowToken).transfer(params.fundRequester, params.totalRepayAmountInToken);
        }
        // ------ deduct foreclosure fee ------
        uint256 foreclosureFeeInBorrow = repayAmount.mulDiv(foreclosureFeeFractionInWad, WAD);
        if (foreclosureFeeInBorrow > params.amountInBorrowTokenLeft) {
            foreclosureFeeInBorrow = params.amountInBorrowTokenLeft;
        }
        params.amountInBorrowTokenLeft -= foreclosureFeeInBorrow;
        _deductFee(
            TempAddresses(params.claimRouter, TreasuryAndRevenueSplit.getAddress(), beneficiary),
            params.borrowTokenInfo,
            foreclosureFeeInBorrow,
            TreasuryAndRevenueSplit.getMax96BitNumber()
        );

        // ------ send back the remaining amount to the owner ------
        IERC20(borrowToken).transfer(_owner(), params.amountInBorrowTokenLeft);
```

  

Some tokens implement a blacklist functionality (e.g., USDC), forbidding transfers to or from blocked addresses. Moreover, some tokens revert when attempting to transfer 0 tokens. If the transfer fails for any reason, the entire foreclosure process will revert, preventing the liquidation of the unsecured position.

##### BVSS

[AO:A/AC:L/AX:M/C:N/I:N/A:N/D:H/Y:N/R:N/S:U (5.0)](/bvss?q=AO:A/AC:L/AX:M/C:N/I:N/A:N/D:H/Y:N/R:N/S:U)

##### Recommendation

Consider using the pull pattern. Instead of transferring tokens to the owner's address directly, increase the internal balance of pending withdrawals and introduce a claim functionality that allows the owner to manually withdraw the remaining funds.

##### Remediation

```
        if (params.amountInBorrowTokenLeft > 0) {
            try IERC20(borrowToken).transfer(_owner(), params.amountInBorrowTokenLeft) {}
            catch {
                IERC20(borrowToken).safeIncreaseAllowance(_owner(), params.amountInBorrowTokenLeft);
            }
        }
```

##### Remediation Hash

<https://github.com/Blueprint-Finance/sc_spokes-v1/commit/cb3429119651a43f0e189a11cb9c7cdf88495e23>

##### References

[Blueprint-Finance/sc\_spokes-v1/src/userBase/utils/ProtectionHandler.sol#L424](https://github.com/Blueprint-Finance/sc_spokes-v1/blob/984a7f00cf76281bd56278d4991b7676e151a792/src/userBase/utils/ProtectionHandler.sol#L424)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Spokes V1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/concrete/spokes-v1
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/concrete/spokes-v1

### Keywords for Search

`vulnerability`

