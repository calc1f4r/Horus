---
# Core Classification
protocol: Ajna Update
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19767
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/75
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-ajna-judging/issues/86

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - hyh
---

## Vulnerability Title

H-2: kickWithDeposit removes the deposit without HTP pool state check

### Overview


This bug report is about the KickerActions kickWithDeposit() function which removes deposits from the pool but does not check the `new_LUP >= HTP` condition, which is a core system invariant. This can lead to a range of outcomes, such as freezing other deposit operations. The code snippet provided shows how the function works, and the lack of a HTP check. The impact of this bug is high, as it violates the core system invariant.

A recommendation is made to add a HTP check to the kickWithDeposit() function, similarly to other functions such as removeQuoteToken(). A discussion between grandizzy and dmitriia is included in the report, with the latter linking to pull request 894 which looks to fix the issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-ajna-judging/issues/86 

## Found by 
hyh
## Summary

In order to cover kick bond KickerActions kickWithDeposit() removes the deposit from the pool, but misses the `new_LUP >= HTP` check, allowing for the invariant breaking state. 

## Vulnerability Detail

Every deposit removal in the protocol comes with the `LUP >= HTP` final state check, that ensures that active loans aren't eligible for liquidation (Ajna white paper `4.1 Deposit`).

kickWithDeposit() can effectively remove deposits, either partially or fully, but performs no such check, potentially leaving the pool in the `LUP < HTP` state.

## Impact

A range of outcomes becomes possible after that, for example all other deposit operations can be frozen as long as they will not move LUP in the opposite direction, as their HTP checks will revert.

There is no low-probability prerequisites and the impact is a violation of the core system invariant, so setting the severity to be high.

## Code Snippet

kickWithDeposit() can effectively remove quote tokens from any bucket to cover kick bond:

https://github.com/sherlock-audit/2023-04-ajna/blob/main/ajna-core/src/base/Pool.sol#L321-L336

```solidity
    function kickWithDeposit(
        uint256 index_,
        uint256 npLimitIndex_
    ) external override nonReentrant {
        PoolState memory poolState = _accruePoolInterest();

        // kick auctions
        KickResult memory result = KickerActions.kickWithDeposit(
            auctions,
            deposits,
            buckets,
            loans,
            poolState,
            index_,
            npLimitIndex_
        );
```

https://github.com/sherlock-audit/2023-04-ajna/blob/main/ajna-core/src/libraries/external/KickerActions.sol#L149-L243

```solidity
    function kickWithDeposit(
        ...
    ) external returns (
        KickResult memory kickResult_
    ) {
        ...

        // kick top borrower
        kickResult_ = _kick(
            ...
        );

        ...

        // remove amount from deposits
        if (vars.amountToDebitFromDeposit == vars.bucketDeposit && vars.bucketCollateral == 0) {
            // In this case we are redeeming the entire bucket exactly, and need to ensure bucket LP are set to 0
            vars.redeemedLP = vars.bucketLP;

>>          Deposits.unscaledRemove(deposits_, index_, vars.bucketUnscaledDeposit);
            vars.bucketUnscaledDeposit = 0;

        } else {
            ...

>>          Deposits.unscaledRemove(deposits_, index_, unscaledAmountToRemove);
            vars.bucketUnscaledDeposit -= unscaledAmountToRemove;
        }
```

But there is no HTP check:

https://github.com/sherlock-audit/2023-04-ajna/blob/main/ajna-core/src/libraries/external/KickerActions.sol#L242-L273

```solidity
            vars.bucketUnscaledDeposit -= unscaledAmountToRemove;
        }

        vars.redeemedLP = Maths.min(vars.lenderLP, vars.redeemedLP);

        // revert if LP redeemed amount to kick auction is 0
        if (vars.redeemedLP == 0) revert InsufficientLP();

        uint256 bucketRemainingLP = vars.bucketLP - vars.redeemedLP;

        if (vars.bucketCollateral == 0 && vars.bucketUnscaledDeposit == 0 && bucketRemainingLP != 0) {
            bucket.lps            = 0;
            bucket.bankruptcyTime = block.timestamp;

            emit BucketBankruptcy(
                ..
            );
        } else {
            // update lender and bucket LP balances
            lender.lps -= vars.redeemedLP;
            bucket.lps -= vars.redeemedLP;
        }

        emit RemoveQuoteToken(
            ...
        );
    }
```

## Tool used

Manual Review

## Recommendation

Consider checking `LUP >= HTP` condition in the final state of the operation, similarly to other functions, for example removeQuoteToken():

https://github.com/sherlock-audit/2023-04-ajna/blob/main/ajna-core/src/libraries/external/LenderActions.sol#L413-L424

```solidity
        lup_ = Deposits.getLup(deposits_, poolState_.debt);

        uint256 htp = Maths.wmul(params_.thresholdPrice, poolState_.inflator);

        if (
            // check loan book's htp doesn't exceed new lup
            htp > lup_
            ||
            // ensure that pool debt < deposits after removal
            // this can happen if lup and htp are less than min bucket price and htp > lup (since LUP is capped at min bucket price)
            (poolState_.debt != 0 && poolState_.debt > Deposits.treeSum(deposits_))
        ) revert LUPBelowHTP();
```



## Discussion

**grandizzy**

https://github.com/ajna-finance/contracts/pull/894

**dmitriia**

> [ajna-finance/contracts#894](https://github.com/ajna-finance/contracts/pull/894)

Looks ok, `lenderKick()` no longer removes deposit, obtaining bond funds directly from the sender, so HTP check now isn't needed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Ajna Update |
| Report Date | N/A |
| Finders | hyh |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-ajna-judging/issues/86
- **Contest**: https://app.sherlock.xyz/audits/contests/75

### Keywords for Search

`vulnerability`

