---
# Core Classification
protocol: Telcoin
chain: everychain
category: uncategorized
vulnerability_type: refund_ether

# Attack Vector Details
attack_type: refund_ether
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3636
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/25
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/76

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:
  - refund_ether

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - launchpad

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - hyh
---

## Vulnerability Title

M-4: Native funds can be lost by submit() as msg.value isn't synchronized with amount

### Overview


This bug report is about a vulnerability found in the FeeBuyback#submit() function in the Telcoin project. When used with native funds, the function does not check for the `amount` argument to correspond to `msg.value` actually linked to the call, leading to either bloating or underpaying of the actual fee. This can result in a fund loss proportional to the difference of the `amount` and `msg.value`. The severity of this issue has been set to medium, as it is conditional on the actual usage of submit(). The bug was found manually and the recommended fix is to require that `amount` does exactly correspond to `msg.value`, when MATIC is used. This will ensure that the uniform approach is maintained and that the funds in the native case are checked.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/76 

## Found by 
hyh

## Summary

When used with native funds FeeBuyback#submit() doesn't check for the `amount` argument to correspond to `msg.value` actually linked to the call. 

## Vulnerability Detail

This can lead either to bloating or to underpaying of the actual fee depending on the mechanics that will be used to call submit(). I.e. as two values can differ, and only one can be correct, the difference is a fund loss either to the `owner` (when the fee is overpaid) or to `recipient` (when the fee is underpaid vs correct formula).

## Impact

Net impact is a fund loss proportional to the difference of the `amount` and `msg.value`. This can be either incomplete setup (native funds case isn't fully covered in a calling script) or an operational mistake (it is covered correctly, but a wrong value was occasionally left from a testing, and so on) situation.

Setting the severity to be medium as this is conditional on the actual usage of submit().

## Code Snippet

submit() uses `msg.value`, which can differ from `amount`:

https://github.com/sherlock-audit/2022-11-telcoin/blob/main/contracts/fee-buyback/FeeBuyback.sol#L35-L82

```solidity
  /**
   * @notice submits wallet transactions
   * @dev a secondary swap may occur
   * @dev staking contract updates may be made
   * @dev function can be paused
   * @param wallet address of the primary transaction
   * @param walletData bytes wallet data for primary transaction
   * @param token address the token that is being swapped from in a secondary transaction
   * @param amount uint256 the quantity of the token being swapped
   * @param swapData bytes swap data from primary transaction
   * @return boolean representing if a referral transaction was made
   */
  function submit(address wallet, bytes memory walletData, address token, address recipient, uint256 amount, bytes memory swapData) external override payable onlyOwner() returns (bool) {
    //Perform user swap first
    ...

    //check if this is a referral transaction
    //if not exit execution
    if (token == address(0) || recipient == address(0) || amount == 0 ) {
      return false;
    }

    //if swapped token is in TEL, no swap is necessary
    //do simple transfer from and submit
    if (token == address(_telcoin)) {
      ...
    }

    //MATIC does not allow for approvals
    //ERC20s only
    if (token != MATIC) {
      IERC20(token).transferFrom(_safe, address(this), amount);
      IERC20(token).approve(_aggregator, amount);
    }

    //Perform secondary swap from fee token to TEL
    //do simple transfer from and submit
    (bool swapResult,) = _aggregator.call{value: msg.value}(swapData);
    require(swapResult, "FeeBuyback: swap transaction failed");
    _telcoin.approve(address(_referral), _telcoin.balanceOf(address(this)));
    require(_referral.increaseClaimableBy(recipient, _telcoin.balanceOf(address(this))), "FeeBuyback: balance was not adjusted");
    return true;
  }
```

I.e. the funds in the native case aren't checked (can be zero, can be 100x of the fee needed), provided `amount` is just ignored.

## Tool used

Manual Review

## Recommendation

In order to maintain the uniform approach consider requiring that `amount` does exactly correspond to `msg.value`, when MATIC is used, for example:

https://github.com/sherlock-audit/2022-11-telcoin/blob/main/contracts/fee-buyback/FeeBuyback.sol#L68-L73

```solidity
    //MATIC does not allow for approvals
    //ERC20s only
    if (token != MATIC) {
      IERC20(token).transferFrom(_safe, address(this), amount);
      IERC20(token).approve(_aggregator, amount);
+   } else {
+     require(amount == msg.value, "FeeBuyback: wrong amount");    
    }
```

## Discussion

**amshirif**

https://github.com/telcoin/telcoin-staking/pull/10

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Sherlock |
| Protocol | Telcoin |
| Report Date | N/A |
| Finders | hyh |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/76
- **Contest**: https://app.sherlock.xyz/audits/contests/25

### Keywords for Search

`Refund Ether`

