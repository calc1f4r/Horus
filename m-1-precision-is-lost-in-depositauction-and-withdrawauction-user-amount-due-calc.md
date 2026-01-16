---
# Core Classification
protocol: Opyn Crab Netting
chain: everychain
category: uncategorized
vulnerability_type: overflow/underflow

# Attack Vector Details
attack_type: overflow/underflow
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5650
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/26
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-opyn-judging/issues/201

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
  - overflow/underflow
  - truncation

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - hyh
  - CRYP70
  - yixxas
---

## Vulnerability Title

M-1: Precision is lost in depositAuction and withdrawAuction user amount due calculations

### Overview


This bug report is about an issue with the depositAuction and withdrawAuction user amount due calculations in the code for the Opyn project, which leads to a loss of precision and fund loss in numerical corner cases. The issue was found by CRYP70, yixxas, and hyh.

The formulas used in depositAuction() and withdrawAuction() for queued distributions perform division first, which leads to truncation and fund loss in the numerical corner cases. An example is when the `withdraw.amount` is 900 and the `_p.crabToWithdraw` is 1000e18, the `usdcAmount` should be 1, but instead it is 0 due to the integer division. This means that the corresponding depositor or withdrawer will experience the loss as less funds to be distributed to them.

The severity of the issue is set to medium as it has material impact in numerical corner cases only. The code snippet provided in the report shows the formula used for `usdcAmount` in withdrawAuction(), and the same approach for `portion.crab` and `portion.eth` in depositAuction().

The recommended fix is to perform multiplication first in all the cases, as shown in the code snippet provided. The fix was lgtm'd by thec00n and the severity was set to medium as suggested by the author.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-opyn-judging/issues/201 

## Found by 
CRYP70, yixxas, hyh

## Summary

Formulas for `usdcAmount`, `portion.crab`, `portion.eth` used in depositAuction() and withdrawAuction() for queued distributions perform division first, which lead to truncation and fund loss in the numerical corner cases.

## Vulnerability Detail

depositAuction() and withdrawAuction() use the same approach for USDC and crab amount calculation. Let's focus on withdrawAuction(), there it is `usdcAmount = (((withdraw.amount * 1e18) / _p.crabToWithdraw) * usdcReceived) / 1e18`.

When `_p.crabToWithdraw` is big compared to `withdraw.amount`, the `((withdraw.amount * 1e18) / _p.crabToWithdraw)` can become zero as result of integer division.

As an example there can be an ordinary user and a whale situation, for the user it can be `withdraw.amount = 900`, while `_p.crabToWithdraw = 1000e18`, `usdcReceived = 2e18`, then `usdcAmount = (((withdraw.amount * 1e18) / _p.crabToWithdraw) * usdcReceived) / 1e18 = 0`, while it should be `usdcAmount = (withdraw.amount * usdcReceived) / _p.crabToWithdraw = (900 * 2e18) / 1000e18 = 1`.

## Impact

When truncation occurs the corresponding depositor or withdrawer will experience the loss as less funds to be distributed to them.

Setting the severity to medium as this have material impact in a numerical corner cases only.

## Code Snippet

withdrawAuction() use `usdcAmount = (((withdraw.amount * 1e18) / _p.crabToWithdraw) * usdcReceived) / 1e18`:

https://github.com/sherlock-audit/2022-11-opyn/blob/main/crab-netting/src/CrabNetting.sol#L697-L718

```solidity
            if (withdraw.amount <= remainingWithdraws) {
                // full usage
                remainingWithdraws -= withdraw.amount;
                crabBalance[withdraw.sender] -= withdraw.amount;

                // send proportional usdc
                usdcAmount = (((withdraw.amount * 1e18) / _p.crabToWithdraw) * usdcReceived) / 1e18;
                IERC20(usdc).transfer(withdraw.sender, usdcAmount);
                emit CrabWithdrawn(withdraw.sender, withdraw.amount, usdcAmount, j);
                delete withdraws[j];
                j++;
            } else {
                withdraws[j].amount -= remainingWithdraws;
                crabBalance[withdraw.sender] -= remainingWithdraws;

                // send proportional usdc
                usdcAmount = (((remainingWithdraws * 1e18) / _p.crabToWithdraw) * usdcReceived) / 1e18;
                IERC20(usdc).transfer(withdraw.sender, usdcAmount);
                emit CrabWithdrawn(withdraw.sender, remainingWithdraws, usdcAmount, j);

                remainingWithdraws = 0;
            }
```

depositAuction() use the same approach for `portion.crab` and `portion.eth`:

https://github.com/sherlock-audit/2022-11-opyn/blob/main/crab-netting/src/CrabNetting.sol#L584-L618

```solidity
            if (queuedAmount <= remainingDeposits) {
                remainingDeposits = remainingDeposits - queuedAmount;
                usdBalance[deposits[k].sender] -= queuedAmount;

                portion.crab = (((queuedAmount * 1e18) / _p.depositsQueued) * to_send.crab) / 1e18;

                IERC20(crab).transfer(deposits[k].sender, portion.crab);

                portion.eth = (((queuedAmount * 1e18) / _p.depositsQueued) * to_send.eth) / 1e18;
                if (portion.eth > 1e12) {
                    IWETH(weth).transfer(deposits[k].sender, portion.eth);
                } else {
                    portion.eth = 0;
                }
                emit USDCDeposited(deposits[k].sender, queuedAmount, portion.crab, k, portion.eth);

                delete deposits[k];
                k++;
            } else {
                usdBalance[deposits[k].sender] -= remainingDeposits;

                portion.crab = (((remainingDeposits * 1e18) / _p.depositsQueued) * to_send.crab) / 1e18;
                IERC20(crab).transfer(deposits[k].sender, portion.crab);

                portion.eth = (((remainingDeposits * 1e18) / _p.depositsQueued) * to_send.eth) / 1e18;
                if (portion.eth > 1e12) {
                    IWETH(weth).transfer(deposits[k].sender, portion.eth);
                } else {
                    portion.eth = 0;
                }
                emit USDCDeposited(deposits[k].sender, remainingDeposits, portion.crab, k, portion.eth);

                deposits[k].amount -= remainingDeposits;
                remainingDeposits = 0;
            }
```

## Tool used

Manual Review

## Recommendation

Consider performing multiplication first in all the case, for example for withdrawAuction():

https://github.com/sherlock-audit/2022-11-opyn/blob/main/crab-netting/src/CrabNetting.sol#L697-L718

```solidity
            if (withdraw.amount <= remainingWithdraws) {
                // full usage
                remainingWithdraws -= withdraw.amount;
                crabBalance[withdraw.sender] -= withdraw.amount;

                // send proportional usdc
-               usdcAmount = (((withdraw.amount * 1e18) / _p.crabToWithdraw) * usdcReceived) / 1e18;
+               usdcAmount = (withdraw.amount * usdcReceived) / _p.crabToWithdraw;
                IERC20(usdc).transfer(withdraw.sender, usdcAmount);
                emit CrabWithdrawn(withdraw.sender, withdraw.amount, usdcAmount, j);
                delete withdraws[j];
                j++;
            } else {
                withdraws[j].amount -= remainingWithdraws;
                crabBalance[withdraw.sender] -= remainingWithdraws;

                // send proportional usdc
-               usdcAmount = (((remainingWithdraws * 1e18) / _p.crabToWithdraw) * usdcReceived) / 1e18;
+               usdcAmount = (remainingWithdraws * usdcReceived) / _p.crabToWithdraw;
                IERC20(usdc).transfer(withdraw.sender, usdcAmount);
                emit CrabWithdrawn(withdraw.sender, remainingWithdraws, usdcAmount, j);

                remainingWithdraws = 0;
            }
```

`withdraw.amount` and `_p.crabToWithdraw` have 18 decimals here, `usdcReceived` and resulting `usdcAmount` have 6 decimals.

## Discussion

**sanandnarayan**

fix : https://github.com/opynfinance/squeeth-monorepo/pull/804


**thec00n**

Fix lgtm. 

I think this should be set to medium severity, as the author suggests.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Sherlock |
| Protocol | Opyn Crab Netting |
| Report Date | N/A |
| Finders | hyh, CRYP70, yixxas |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-opyn-judging/issues/201
- **Contest**: https://app.sherlock.xyz/audits/contests/26

### Keywords for Search

`Overflow/Underflow, Truncation`

