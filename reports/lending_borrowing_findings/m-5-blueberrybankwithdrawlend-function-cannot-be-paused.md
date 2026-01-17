---
# Core Classification
protocol: Blueberry
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6652
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/41
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/204

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - leveraged_farming
  - dexes
  - cdp
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - rbserver
---

## Vulnerability Title

M-5: `BlueBerryBank.withdrawLend` function cannot be paused

### Overview


A bug was found in the `BlueBerryBank.withdrawLend` function of the `BlueBerryBank` contract. This function, which is used to reduce a position, cannot be paused when an extreme market condition occurs, an exploit is faced, or a legal requirement is issued. This means that users can still reduce their positions even when the protocol needs to pause this functionality. A function similar to the `BlueBerryBank.isBorrowAllowed`, `BlueBerryBank.isRepayAllowed`, and `BlueBerryBank.isLendAllowed` functions can be added in the `BlueBerryBank` contract for pausing the `BlueBerryBank.withdrawLend` function. This function can then be used to pause the `BlueBerryBank.withdrawLend` function when needed.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/204 

## Found by 
rbserver

## Summary
When an extreme market condition occurs, the protocol faces an exploit, or the authority issues a legal requirement, the protocol is able to pause the lending, borrowing, and repaying functionalities. However, the protocol is unable to pause the functionality for reducing a position.

## Vulnerability Detail
Because the `BlueBerryBank` contract does not have a function, which is like `BlueBerryBank.isBorrowAllowed`, `BlueBerryBank.isRepayAllowed`, and `BlueBerryBank.isLendAllowed`, for pausing the functionality for reducing a position, the `BlueBerryBank.withdrawLend` function, which is shown in the Code Snippet section, cannot be paused. Users can still call the `IchiVaultSpell.reducePosition` function that further calls the `BlueBerryBank.withdrawLend` function to reduce a position when there is a need for pausing this functionality.

## Impact
Just like pausing the lending, borrowing, and repaying functionalities, it is possible that the protocol needs to pause the functionality for reducing a position. However, when this need occurs, users can still reduce their positions through calling the `IchiVaultSpell.reducePosition` and `BlueBerryBank.withdrawLend` functions. The protocol cannot stop the outflow of the funds due to these position reductions even it is required to do so in this situation.

## Code Snippet
https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/spell/IchiVaultSpell.sol#L266-L274
```solidity
    function reducePosition(
        uint256 strategyId,
        address collToken,
        uint256 collAmount
    ) external {
        doWithdraw(collToken, collAmount);
        doRefund(collToken);
        _validateMaxLTV(strategyId);
    }
```

https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/BlueBerryBank.sol#L669-L704
```solidity
    function withdrawLend(address token, uint256 shareAmount)
        external
        override
        inExec
        poke(token)
    {
        Position storage pos = positions[POSITION_ID];
        Bank storage bank = banks[token];
        if (token != pos.underlyingToken) revert INVALID_UTOKEN(token);
        if (shareAmount == type(uint256).max) {
            shareAmount = pos.underlyingVaultShare;
        }

        uint256 wAmount;
        if (address(ISoftVault(bank.softVault).uToken()) == token) {
            ISoftVault(bank.softVault).approve(
                bank.softVault,
                type(uint256).max
            );
            wAmount = ISoftVault(bank.softVault).withdraw(shareAmount);
        } else {
            wAmount = IHardVault(bank.hardVault).withdraw(token, shareAmount);
        }

        wAmount = wAmount > pos.underlyingAmount
            ? pos.underlyingAmount
            : wAmount;

        pos.underlyingVaultShare -= shareAmount;
        pos.underlyingAmount -= wAmount;
        bank.totalLend -= wAmount;

        wAmount = doCutWithdrawFee(token, wAmount);

        IERC20Upgradeable(token).safeTransfer(msg.sender, wAmount);
    }
```

## Tool used

Manual Review

## Recommendation
A function, which is similar to the `BlueBerryBank.isBorrowAllowed`, `BlueBerryBank.isRepayAllowed`, and `BlueBerryBank.isLendAllowed` functions, can be added in the `BlueBerryBank` contract for pausing the `BlueBerryBank.withdrawLend` function. This function can then be used in the `BlueBerryBank.withdrawLend` function so the `BlueBerryBank.withdrawLend` function can be paused when needed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry |
| Report Date | N/A |
| Finders | rbserver |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/204
- **Contest**: https://app.sherlock.xyz/audits/contests/41

### Keywords for Search

`vulnerability`

