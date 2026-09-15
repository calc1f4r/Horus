---
# Core Classification
protocol: OpenSea
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2622
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-opensea-seaport-contest
source_link: https://code4rena.com/reports/2022-05-opensea-seaport
github_link: https://github.com/code-423n4/2022-05-opensea-seaport-findings/issues/75

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Saw-mon__Natalie
  - Spearbit
---

## Vulnerability Title

[H-02] `_aggregateValidFulfillmentOfferItems()` can be tricked to accept invalid inputs

### Overview


A bug was discovered in the code of an OpenSea Seaport contract, specifically in the `_aggregateValidFulfillmentOfferItems()` function. This function is used to check if an order has a valid value or not. It is supposed to revert on orders with zero value or where a total consideration amount overflows. However, the code is vulnerable to an unhandled error code of 3, which is not detected and could lead to the order being executed with malformed values.

To recreate this bug, an offer containing two errors (e.g. with zero amount and overflow) needs to be crafted. Then by calling the `matchOrders()` function, the `_aggregateValidFulfillmentOfferItems()` will be called and the `errorBuffer` will get a value of 3. As this value is not detected, no error will be thrown and the order will be executed, including the malformed values.

The recommended mitigation steps are to change the check on [FulfillmentApplier.sol#L465](https://github.com/code-423n4/2022-05-opensea-seaport/blob/main/contracts/lib/FulfillmentApplier.sol#L465) to consider `case 3` and introduce an early abort in case `errorBuffer != 0` on [FulfillmentApplier.sol#L338](https://github.com/code-423n4/2022-05-opensea-seaport/blob/main/contracts/lib/FulfillmentApplier.sol#L338).

In summary, a bug was discovered in the OpenSea Seaport contract code which could lead to orders being executed with malformed values. To recreate the bug, an offer containing two errors (e.g. with zero amount and overflow) needs to be crafted. The recommended mitigation steps are to change the check on [FulfillmentApplier.sol#L465](https://github.com/code-423n4/2022-05-opensea-seaport/blob/main/contracts/lib/FulfillmentApplier.sol#L465) and introduce an early abort in case `errorBuffer != 0` on [FulfillmentApplier.sol

### Original Finding Content


[FulfillmentApplier.sol#L406](https://github.com/code-423n4/2022-05-opensea-seaport/blob/main/contracts/lib/FulfillmentApplier.sol#L406)<br>

The `_aggregateValidFulfillmentOfferItems()` function aims to revert on orders with zero value or where a total consideration amount overflows. Internally this is accomplished by having a temporary variable `errorBuffer`, accumulating issues found, and only reverting once all the items are processed in case there was a problem found. This code is optimistic for valid inputs.

Note: there is a similar issue in `_aggregateValidFulfillmentConsiderationItems()`, which is reported separately.

The problem lies in how this `errorBuffer` is updated:

```solidity
                // Update error buffer (1 = zero amount, 2 = overflow).
                errorBuffer := or(
                  errorBuffer,
                  or(
                    shl(1, lt(newAmount, amount)),
                    iszero(mload(amountPtr))
                  )
                )
```

The final error handling code:

```solidity
            // Determine if an error code is contained in the error buffer.
            switch errorBuffer
            case 1 {
                // Store the MissingItemAmount error signature.
                mstore(0, MissingItemAmount_error_signature)

                // Return, supplying MissingItemAmount signature.
                revert(0, MissingItemAmount_error_len)
            }
            case 2 {
                // If the sum overflowed, panic.
                throwOverflow()
            }
```

While the expected value is `0` (success),  `1` or `2` (failure), it is possible to set it to `3`, which is unhandled and considered as a "success". This can be easily accomplished by having both an overflowing item and a zero item in the order list.

This validation error could lead to fulfilling an order with a consideration (potentially \~0) lower than expected.

### Proof of Concept

Craft an offer containing two errors (e.g. with  zero amount and overflow).<br>
Call `matchOrders()`. Via calls to `_matchAdvancedOrders()`, `_fulfillAdvancedOrders()`, `_applyFulfillment()`, `_aggregateValidFulfillmentOfferItems()` will be called.<br>
The `errorBuffer` will get a value of 3  (the `or` of 1 and 2).<br>
As the value of 3 is not detected, no error will be thrown and the order will be executed, including the mal formed values.

### Recommended Mitigation Steps

1.  Change the check on [FulfillmentApplier.sol#L465](https://github.com/code-423n4/2022-05-opensea-seaport/blob/main/contracts/lib/FulfillmentApplier.sol#L465)  to consider `case 3`.
2.  Potential option: Introduce an early abort in case `errorBuffer != 0` on [FulfillmentApplier.sol#L338](https://github.com/code-423n4/2022-05-opensea-seaport/blob/main/contracts/lib/FulfillmentApplier.sol#L338)

**[0age (OpenSea) confirmed](https://github.com/code-423n4/2022-05-opensea-seaport-findings/issues/75)**

**[HardlyDifficult (judge) decreased severity to Medium](https://github.com/code-423n4/2022-05-opensea-seaport-findings/issues/75)**

**[cmichel (warden) commented](https://github.com/code-423n4/2022-05-opensea-seaport-findings/issues/75#issuecomment-1172848110):**
 > > This validation error could lead to fulfilling an order with a consideration (potentially ~0) lower than expected.
> 
> That's correct, you can use this to fulfill an order essentially for free, that's why I'd consider this high severity.
> They could have done a better job demonstrating it with a POC test case but this sentence imo shows that they were aware of the impact.
> 
> See [this test case](https://github.com/ProjectOpenSea/seaport/blob/5c6a628cb152d731e956682dd748d30e8bf1f1c9/test/findings/FulfillmentOverflowWithMissingItems.spec.ts#L136) showing how to buy an NFT for 1 DAI instead of 1000 DAI.

**0age (OpenSea) disagreed with Medium severity:**
 > This is the highest-severity finding. If it were me, I'd switch this to high.

**[HardlyDifficult (judge) increased severity to High](https://github.com/code-423n4/2022-05-opensea-seaport-findings/issues/75)**

**[0xleastwood (judge) commented](https://github.com/code-423n4/2022-05-opensea-seaport-findings/issues/75#issuecomment-1183115107):**
 > After further consideration and discussion with @HardlyDifficult, we agree with @cmichel that this should be of high severity. As the protocol allows for invalid orders to be created, users aware of this vulnerability will be able to fulfill an order at a considerable discount. This fits the criteria of a high severity issue as it directly leads to lost funds.

**[0age (OpenSea) resolved](https://github.com/code-423n4/2022-05-opensea-seaport-findings/issues/75):**
 > PR: [ProjectOpenSea/seaport#320](https://github.com/ProjectOpenSea/seaport/pull/320)



***

 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | OpenSea |
| Report Date | N/A |
| Finders | Saw-mon__Natalie, Spearbit |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-opensea-seaport
- **GitHub**: https://github.com/code-423n4/2022-05-opensea-seaport-findings/issues/75
- **Contest**: https://code4rena.com/contests/2022-05-opensea-seaport-contest

### Keywords for Search

`Business Logic`

