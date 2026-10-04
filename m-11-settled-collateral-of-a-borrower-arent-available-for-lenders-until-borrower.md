---
# Core Classification
protocol: Ajna
chain: everychain
category: logic
vulnerability_type: don't_update_state

# Attack Vector Details
attack_type: don't_update_state
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6308
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/32
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/104

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - don't_update_state
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - hyh
---

## Vulnerability Title

M-11: Settled collateral of a borrower aren't available for lenders until borrower's debt is fully cleared

### Overview


This bug report is about an issue in the ERC721Pool smart contract. When a borrower settles their debt, their collateral remains locked and unavailable for lenders until the borrower's debt is fully cleared. The current code does not account for any of the borrower's collateral ids that are removed from them when the debt isn't fully settled, meaning they are still unavailable for lenders. This could lead to a permanent freeze of the collateral, resulting in a principal fund loss for the lenders. 

The code snippet provided shows that the `_rebalanceTokens()` function is not called when the debt isn't fully settled. The recommendation is to consider rebalancing each time when there is something to rebalance, as shown in the code snippet provided. This bug was found manually by hyh.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/104 

## Found by 
hyh

## Summary

ERC721Pool's settle() lacks collateral ids array rebalance when the settlement isn't full, i.e. when `t0DebtRemaining > 0`.

## Vulnerability Detail

Auctions's settlePoolDebt() returns current state of the borrower after the settlement. If any of borrower's collateral id were removed from them it needs to be accounted for, but when `t0DebtRemaining > 0` this doesn't happen, i.e. removed borrower's tokens aren't added to the buckets cumulative collateral ids array and so this collateral is still unavailable for lenders.

## Impact

The settled collateral of the borrower will not be available for LP's withdrawal as the corresponding function will revert on an attempt to extract token ids from `bucketTokenIds` array.

The length of such freeze can vary up to be permanent, for example if there is no funds (reserves and deposits) to fully settle the borrower. This is principal fund loss scenario for the lenders, but given the prerequisite of the full default setting the severity to be medium.

## Code Snippet

When a borrower has some unsettled debt, `t0DebtRemaining > 0`, all of their collateral remain locked with `borrowerTokenIds` as _rebalanceTokens() isn't called in this case:

https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/ERC721Pool.sol#L353-L385

```solidity
    function settle(
        address borrowerAddress_,
        uint256 maxDepth_
    ) external nonReentrant override {
        PoolState memory poolState = _accruePoolInterest();

        uint256 assets = Maths.wmul(poolBalances.t0Debt, poolState.inflator) + _getPoolQuoteTokenBalance();
        uint256 liabilities = Deposits.treeSum(deposits) + auctions.totalBondEscrowed + reserveAuction.unclaimed;

        SettleParams memory params = SettleParams(
            {
                borrower:    borrowerAddress_,
                reserves:    (assets > liabilities) ? (assets-liabilities) : 0,
                inflator:    poolState.inflator,
                bucketDepth: maxDepth_,
                poolType:    poolState.poolType
            }
        );
        (
            uint256 collateralRemaining,
            uint256 t0DebtRemaining,
            uint256 collateralSettled,
            uint256 t0DebtSettled
        ) = Auctions.settlePoolDebt(
            auctions,
            buckets,
            deposits,
            loans,
            params
        );

        // slither-disable-next-line incorrect-equality
        if (t0DebtRemaining == 0) _rebalanceTokens(params.borrower, collateralRemaining);
```

This can happen when settlement exits when `params_.bucketDepth == 0`: 

https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/libraries/external/Auctions.sol#L277-L337

```solidity
        // if there's still debt and no collateral
        if (borrower.t0Debt != 0 && borrower.collateral == 0) {
            // settle debt from reserves -- round reserves down however
            borrower.t0Debt -= Maths.min(borrower.t0Debt, (params_.reserves / params_.inflator) * 1e18);

            // if there's still debt after settling from reserves then start to forgive amount from next HPB
            // loop through remaining buckets if there's still debt to settle
            while (params_.bucketDepth != 0 && borrower.t0Debt != 0) {
                SettleLocalVars memory vars;

                (vars.index, , vars.scale) = Deposits.findIndexAndSumOfSum(deposits_, 1);
                vars.unscaledDeposit = Deposits.unscaledValueAt(deposits_, vars.index);
                vars.depositToRemove = Maths.wmul(vars.scale, vars.unscaledDeposit);
                vars.debt            = Maths.wmul(borrower.t0Debt, params_.inflator);

                // enough deposit in bucket to settle entire debt
                if (vars.depositToRemove >= vars.debt) {
                    Deposits.unscaledRemove(deposits_, vars.index, Maths.wdiv(vars.debt, vars.scale));
                    borrower.t0Debt  = 0;                                                              // no remaining debt to settle

                // not enough deposit to settle entire debt, we settle only deposit amount
                } else {
                    borrower.t0Debt -= Maths.wdiv(vars.depositToRemove, params_.inflator);             // subtract from remaining debt the corresponding t0 amount of deposit

                    Deposits.unscaledRemove(deposits_, vars.index, vars.unscaledDeposit);              // Remove all deposit from bucket
                    Bucket storage hpbBucket = buckets_[vars.index];
                    
                    if (hpbBucket.collateral == 0) {                                                   // existing LPB and LP tokens for the bucket shall become unclaimable.
                        emit BucketBankruptcy(vars.index, hpbBucket.lps);
                        hpbBucket.lps            = 0;
                        hpbBucket.bankruptcyTime = block.timestamp;
                    }
                }

                --params_.bucketDepth;
            }
        }

        t0DebtRemaining_ =  borrower.t0Debt;
        t0DebtSettled_   -= t0DebtRemaining_;

        emit Settle(params_.borrower, t0DebtSettled_);

        if (borrower.t0Debt == 0) {
            // settle auction
            borrower.collateral = _settleAuction(
                auctions_,
                buckets_,
                deposits_,
                params_.borrower,
                borrower.collateral,
                params_.poolType
            );
        }

        collateralRemaining_ =  borrower.collateral;
        collateralSettled_   -= collateralRemaining_;

        // update borrower state
        loans_.borrowers[params_.borrower] = borrower;
    }
```

## Tool used

Manual Review

## Recommendation

Consider rebalancing each time when there is something to rebalance, for example:

https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/ERC721Pool.sol#L353-L385

```solidity
    function settle(
        address borrowerAddress_,
        uint256 maxDepth_
    ) external nonReentrant override {
        ...
        (
            uint256 collateralRemaining,
            uint256 t0DebtRemaining,
            uint256 collateralSettled,
            uint256 t0DebtSettled
        ) = Auctions.settlePoolDebt(
            ...
        );

        // slither-disable-next-line incorrect-equality
-        if (t0DebtRemaining == 0) _rebalanceTokens(params.borrower, collateralRemaining);
+        if (collateralSettled > 0) _rebalanceTokens(params.borrower, collateralRemaining);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Sherlock |
| Protocol | Ajna |
| Report Date | N/A |
| Finders | hyh |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/104
- **Contest**: https://app.sherlock.xyz/audits/contests/32

### Keywords for Search

`Don't update state, Business Logic`

