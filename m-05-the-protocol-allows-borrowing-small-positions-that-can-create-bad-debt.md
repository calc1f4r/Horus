---
# Core Classification
protocol: Wise Lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32094
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-02-wise-lending
source_link: https://code4rena.com/reports/2024-02-wise-lending
github_link: https://github.com/code-423n4/2024-02-wise-lending-findings/issues/255

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

protocol_categories:
  - lending

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - SBSecurity
  - serial-coder
---

## Vulnerability Title

[M-05] The protocol allows borrowing small positions that can create bad debt

### Overview


The WiseLending protocol has a bug that allows users to borrow small amounts without proper collateral, which can lead to bad debt for the protocol. This is because there is no minimum borrowing amount check in the protocol, and even if there is a minimum deposit amount check, it can be easily bypassed. This means that a user can deposit a small amount and then withdraw it later, leaving the protocol vulnerable to bad debt. The recommended solution is to implement a minimum borrowing amount check to limit the size of borrowing positions. 

### Original Finding Content


The `WiseLending` protocol allows users to borrow small positions. Even if the protocol has a minimum deposit (collateral) amount check to mitigate the small borrowing position from creating bad debt, this protection can be bypassed.

With a small borrowing position, there is no incentive for a liquidator to liquidate the position, as the liquidation profit may not cover the liquidation cost (gas). As a result, small liquidable positions will not be liquidated, leaving bad debt to the protocol.

### Proof of Concept

The protocol allows users to borrow small positions since no minimum borrowing amount is checked in the [`WiseSecurity::checksBorrow()`](https://github.com/code-423n4/2024-02-wise-lending/blob/79186b243d8553e66358c05497e5ccfd9488b5e2/contracts/WiseSecurity/WiseSecurity.sol#L306-L330).

```solidity
// FILE: https://github.com/code-423n4/2024-02-wise-lending/blob/main/contracts/WiseSecurity/WiseSecurity.sol
function checksBorrow(
    uint256 _nftId,
    address _caller,
    address _poolToken
)
    external
    view
    returns (bool specialCase) //@audit -- No minimum borrowing amount check
{
    _checkPoolCondition(
        _poolToken
    );

    checkTokenAllowed(
        _poolToken
    );

    if (WISE_LENDING.verifiedIsolationPool(_caller) == true) {
        return true;
    }

    if (WISE_LENDING.positionLocked(_nftId) == true) {
        return true;
    }
}
```

[No minimum borrowing amount check](<https://github.com/code-423n4/2024-02-wise-lending/blob/79186b243d8553e66358c05497e5ccfd9488b5e2/contracts/WiseSecurity/WiseSecurity.sol#L306-L330>).

Even if the protocol has a [minimum deposit (collateral) amount check](https://github.com/code-423n4/2024-02-wise-lending/blob/79186b243d8553e66358c05497e5ccfd9488b5e2/contracts/WiseCore.sol#L260-L263) in the `WiseCore::_checkDeposit()` to mitigate the small borrowing position from creating bad debt, this protection can be easily bypassed.

The `WiseCore::_checkMinDepositValue()` is a core function that checks a minimum deposit (collateral) amount. By default, [this deposit amount check would be overridden (disabled)](https://github.com/code-423n4/2024-02-wise-lending/blob/79186b243d8553e66358c05497e5ccfd9488b5e2/contracts/WiseSecurity/WiseSecurity.sol#L1100-L1102). Even though [this deposit amount check will be enabled](https://github.com/code-423n4/2024-02-wise-lending/blob/79186b243d8553e66358c05497e5ccfd9488b5e2/contracts/WiseSecurity/WiseSecurity.sol#L1104-L1106), this protection can be bypassed by withdrawing the deposited fund later, since there is no minimum withdrawal amount check in the [`WiseSecurity::checksWithdraw()`](https://github.com/code-423n4/2024-02-wise-lending/blob/79186b243d8553e66358c05497e5ccfd9488b5e2/contracts/WiseSecurity/WiseSecurity.sol#L237-L270).

```solidity
    // FILE: https://github.com/code-423n4/2024-02-wise-lending/blob/main/contracts/WiseCore.sol
    function _checkDeposit(
        uint256 _nftId,
        address _caller,
        address _poolToken,
        uint256 _amount
    )
        internal
        view
    {

        if (WISE_ORACLE.chainLinkIsDead(_poolToken) == true) {
            revert DeadOracle();
        }

        _checkAllowDeposit(
            _nftId,
            _caller
        );

        _checkPositionLocked(
            _nftId,
            _caller
        );

@1      WISE_SECURITY.checkPoolWithMinDeposit( //@audit -- Even if there is a minimum deposit amount check, this protection can be bypassed
@1          _poolToken,
@1          _amount
@1      );

        _checkMaxDepositValue(
            _poolToken,
            _amount
        );
    }

    // FILE: https://github.com/code-423n4/2024-02-wise-lending/blob/main/contracts/WiseSecurity/WiseSecurity.sol
    function _checkMinDepositValue(
        address _token,
        uint256 _amount
    )
        private
        view
        returns (bool)
    {
@2      if (minDepositEthValue == ONE_WEI) { //@audit -- By default, the minimum deposit amount check would be overridden (disabled)
@2          return true;
@2      }

@3      if (_getTokensInEth(_token, _amount) < minDepositEthValue) { //@audit -- Even though the minimum deposit amount check will be enabled, this protection can be bypassed by withdrawing the deposited fund later
@3          revert DepositAmountTooSmall();
@3      }

        return true;
    }
```

`@1 -- Even if there is a minimum deposit amount check, this protection can be bypassed`: see [here](<https://github.com/code-423n4/2024-02-wise-lending/blob/79186b243d8553e66358c05497e5ccfd9488b5e2/contracts/WiseCore.sol#L260-L263>).

`@2 -- By default, the minimum deposit amount check would be overridden (disabled)`: see [here](<https://github.com/code-423n4/2024-02-wise-lending/blob/79186b243d8553e66358c05497e5ccfd9488b5e2/contracts/WiseSecurity/WiseSecurity.sol#L1100-L1102>).

`@3 -- Even though the minimum deposit amount check will be enabled, this protection can be bypassed by withdrawing the deposited fund later`: see [here](<https://github.com/code-423n4/2024-02-wise-lending/blob/79186b243d8553e66358c05497e5ccfd9488b5e2/contracts/WiseSecurity/WiseSecurity.sol#L1104-L1106>).

As you can see, there is no minimum withdrawal amount check in the [`WiseSecurity::checksWithdraw()`](https://github.com/code-423n4/2024-02-wise-lending/blob/79186b243d8553e66358c05497e5ccfd9488b5e2/contracts/WiseSecurity/WiseSecurity.sol#L237-L270). Hence, a user can deposit collateral at or above the minimum deposit amount (i.e., `minDepositEthValue`) and then withdraw the deposited fund to be under the `minDepositEthValue`. Later, they can borrow a small amount with small collateral.

With a small borrowing position (and small collateral), there is no incentive for a liquidator to liquidate the position, as the liquidation profit may not cover the liquidation cost (gas). As a result, small liquidable positions will not be liquidated, leaving bad debt to the protocol.

```solidity
// FILE: https://github.com/code-423n4/2024-02-wise-lending/blob/main/contracts/WiseSecurity/WiseSecurity.sol
function checksWithdraw(
    uint256 _nftId,
    address _caller,
    address _poolToken
)
    external
    view
    returns (bool specialCase) //@audit -- No minimum withdrawal amount check
{
    if (_checkBlacklisted(_poolToken) == true) {

        if (overallETHBorrowBare(_nftId) > 0) {
            revert OpenBorrowPosition();
        }

        return true;
    }

    if (WISE_LENDING.verifiedIsolationPool(_caller) == true) {
        return true;
    }

    if (WISE_LENDING.positionLocked(_nftId) == true) {
        return true;
    }

    if (_isUncollateralized(_nftId, _poolToken) == true) {
        return true;
    }

    if (WISE_LENDING.getPositionBorrowTokenLength(_nftId) == 0) {
        return true;
    }
}
```

[No minimum withdrawal amount check](<https://github.com/code-423n4/2024-02-wise-lending/blob/79186b243d8553e66358c05497e5ccfd9488b5e2/contracts/WiseSecurity/WiseSecurity.sol#L237-L270>).

### Recommended Mitigation Steps

Implement the **minimum borrowing amount check** to limit the minimum size of borrowing positions.

**[vonMangoldt (Wise Lending) commented via duplicate issue #277](https://github.com/code-423n4/2024-02-wise-lending-findings/issues/277#issuecomment-2004003575):**
> Can also be circumvented by just paying back after borrowing. Doesn't really add any value, in my opinion.

**[Trust (judge) commented](https://github.com/code-423n4/2024-02-wise-lending-findings/issues/255#issuecomment-2020946526):**
 > The bug class is valid, in my honest opinion; as either liquidator will liquidate at a loss or protocol will be losing money to protect from bad debt over time.

**[Wise Lending commented](https://github.com/code-423n4/2024-02-wise-lending-findings/issues/255#issuecomment-2082909729):**
> Mitigated [here](https://github.com/wise-foundation/lending-audit/commit/ac68b5a93976969d582301fee9f873ecec606df9).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Wise Lending |
| Report Date | N/A |
| Finders | SBSecurity, serial-coder |

### Source Links

- **Source**: https://code4rena.com/reports/2024-02-wise-lending
- **GitHub**: https://github.com/code-423n4/2024-02-wise-lending-findings/issues/255
- **Contest**: https://code4rena.com/reports/2024-02-wise-lending

### Keywords for Search

`vulnerability`

