---
# Core Classification
protocol: Sublime
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1189
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-sublime-contest
source_link: https://code4rena.com/reports/2021-12-sublime
github_link: https://github.com/code-423n4/2021-12-sublime-findings/issues/96

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
  - leveraged_farming
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - harleythedog
---

## Vulnerability Title

[H-06] Anyone can liquidate credit line when autoLiquidation is false without supplying borrow tokens

### Overview


This bug report concerns the Sublime Finance platform, which allows users to set up credit lines and liquidate them. The issue is that if a credit line has autoLiquidation set to false, anyone can liquidate the position, rather than just the lender, as intended. Worse yet, when autoLiquidation is set to false, the liquidator does not have to supply the initial amount of borrow tokens that normally have to be transferred when autoLiquidation is true. This means that the liquidator will be sent all of the collateral that is supposed to be sent to the lender, resulting in a huge loss to the lender. 

The code responsible for this issue can be found in the CreditLine.sol file, where the autoLiquidation value is only used in one place. The proof of concept was confirmed with the Hardhat tool, and the recommended mitigation step is to add a require statement somewhere in the liquidate function.

### Original Finding Content

_Submitted by harleythedog_

#### Impact

It is intended that if a credit line has autoLiquidation as false, then only the lender can be the liquidator (see docs here: <https://docs.sublime.finance/sublime-docs/smart-contracts/creditlines>). However, this is not correctly implemented, and anyone can liquidate a position that has autoLiquidation set to false.

Even worse, when autoLiquidation is set to false, the liquidator does not have to supply the initial amount of borrow tokens (determined by `_borrowTokensToLiquidate`) that normally have to be transferred when autoLiquidation is true. This means that the liquidator will be sent all of the collateral that is supposed to be sent to the lender, so this represents a huge loss to the lender. Since the lender will lose all of the collateral that they are owed, this is a high severity issue.

#### Proof of Concept

The current implementation of liquidate is here: <https://github.com/code-423n4/2021-12-sublime/blob/9df1b7c4247f8631647c7627a8da9bdc16db8b11/contracts/CreditLine/CreditLine.sol#L996>.

Notice that the autoLiquidation value is only used in one place within this function, which is in this segment of the code:
```solidity
...
    if (creditLineConstants[_id].autoLiquidation && _lender != msg.sender) {
        uint256 _borrowTokens = _borrowTokensToLiquidate(_borrowAsset, _collateralAsset, _totalCollateralTokens);
        if (_borrowAsset == address(0)) {
            uint256 _returnETH = msg.value.sub(_borrowTokens, 'Insufficient ETH to liquidate');
            if (_returnETH != 0) {
                (bool success, ) = msg.sender.call{value: _returnETH}('');
                require(success, 'Transfer fail');
            }
        } else {
        IERC20(_borrowAsset).safeTransferFrom(msg.sender, _lender, _borrowTokens);
        }
    }
    
    _transferCollateral(_id, _collateralAsset, _totalCollateralTokens, _toSavingsAccount); 
    emit  CreditLineLiquidated(_id, msg.sender);
}
```

So, if `autoLiquidation` is false, the code inside of the if statement will simply not be executed, and there are no further checks that the sender HAS to be the lender if `autoLiquidation` is false. This means that anyone can liquidate a non-autoLiquidation credit line, and receive all of the collateral without first transferring the necessary borrow tokens.

For a further proof of concept, consider the test file here: <https://github.com/code-423n4/2021-12-sublime/blob/main/test/CreditLines/2.spec.ts>. If the code on line 238 is changed from `let  _autoLiquidation: boolean  =  true;` to `let  _autoLiquidation: boolean  =  false;`, all the test cases will still pass. This confirms the issue, as the final test case "Liquidate credit line" has the `admin` as the liquidator, which should not work in non-autoLiquidations since they are not the lender.

#### Tools Used

Inspection and confirmed with Hardhat.

#### Recommended Mitigation Steps

Add the following require statement somewhere in the `liquidate` function:
```solidity
require(
    creditLineConstants[_id].autoLiquidation || 
    msg.sender == creditLineConstants[_id].lender,
    "not autoLiquidation and not lender");
```

#### [ritik99 (Sublime) labeled](https://github.com/code-423n4/2021-12-sublime-findings/issues/96) sponsor confirmed




### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sublime |
| Report Date | N/A |
| Finders | harleythedog |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-sublime
- **GitHub**: https://github.com/code-423n4/2021-12-sublime-findings/issues/96
- **Contest**: https://code4rena.com/contests/2021-12-sublime-contest

### Keywords for Search

`vulnerability`

