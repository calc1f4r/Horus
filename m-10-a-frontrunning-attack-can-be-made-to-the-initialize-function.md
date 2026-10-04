---
# Core Classification
protocol: QuickSwap and StellaSwap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28858
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-09-quickswap
source_link: https://code4rena.com/reports/2022-09-quickswap
github_link: https://github.com/code-423n4/2022-09-quickswap-findings/issues/84

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
  - dexes

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-10] A "FrontRunning attack" can be made to the `initialize` function

### Overview


This bug report is about the `initialize` function in AlgebraPool.sol#L193-L206 which is an important function that sets the liquidity price at the beginning of the pool. This function performs some checks (e.g. if the price is not 0) but is unprotected against frontrunning, which means that a bot could listen to the mempool and run from the front and cause the pool to start at too high or too low of a price.

The severity of the bug was initially set to High but was later downgraded to Medium. It is important to note that users should not trust on-chain pricing for new pools or pools with low liquidity.

To mitigate this bug, it is recommended to add a modifier that ensures that only the authorized person, that is, the first liquidator to the pool, initiates the `initialize` function. Alternatively, the process of determining the price of the pool could be divided into parts, first printing the price amounts to the state variable, and then making the `initialize` run before this price can be changed.

### Original Finding Content


[AlgebraPool.sol#L193-L206](https://github.com/code-423n4/2022-09-quickswap/blob/main/src/core/contracts/AlgebraPool.sol#L193-L206)<br>

The initialize function in `AlgebraPool.sol#L193-L206` is a very important function and sets the liquidity price at the beginning of the pool.

Performs some checks (For example, if the price is not 0).

However it is unprotected against running from the front, and a bot listening to Mempool will run from the front and cause its pool to start at too high or too low of a price.

It is very important that this function is not enabled for FrontRunning operation.

```js
function initialize(uint160 initialPrice) external override {
    require(globalState.price == 0, 'AI');
    // getTickAtSqrtRatio checks validity of initialPrice inside
    int24 tick = TickMath.getTickAtSqrtRatio(initialPrice);

    uint32 timestamp = _blockTimestamp();
    IDataStorageOperator(dataStorageOperator).initialize(timestamp, tick);

    globalState.price = initialPrice;
    globalState.unlocked = true;
    globalState.tick = tick;

    emit Initialize(initialPrice, tick);
  }

```

### Proof of Concept

1- Alice starts a new pool in Algebra and triggers the price determination transaction with `initialize`.<br>
2- Bob listens to the mempool with the following code, which is a minimal example, and sees at what price the `initialize` function is triggered with the `initialPrice` argument, and starts the pool at the price he wants by pre-executing it and makes Alice deposit the wrong amount at the wrong price.

```js
mempool.js
 var customWsProvider = new ethers.providers.WebSocketProvider(url);
 customWsProvider.on("pending", (tx) => { 
 let pendingTx = await connect.provider.getTransaction(txHash);
        if (pendingTx) {
            // filter pendingTx.data
            if (pendingTx.data.indexOf("0xf637731d") !== -1) {      //  func. signature : f637731d  =>  initialize(uint160) 
               console.log(pendingTx);
            }
        }
```

### Recommended Mitigation Steps

Add a `modifier` that ensures that only the authorized person, that is, the first liquidator to the pool, initiates the `initialize` function.

Or, divide the process of determining the price of the pool into parts, first print the price amounts to the state variable, and then make the `initialize` run before this price can be changed.

**[0xean (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-09-quickswap-findings/issues/84#issuecomment-1264733697):**
 > Downgrading to Medium. Alice shouldn't be relying on this initial price to determine the "fair" market price. When there is very limited liquidity the price is extremely easy to move along the x*y=k curve in any case so even after the initialized call is made someone could manipulate the pools pricing very easily when liquidity is low.

**[sameepsi (QuickSwap & StellaSwap) disputed and commented](https://github.com/code-423n4/2022-09-quickswap-findings/issues/84#issuecomment-1266443768):**
 > I don't think it's a bug. Even if someone sets the wrong price initially then it will be arbitraged. That's how AMMs work by design.

**[0xean (judge) commented](https://github.com/code-423n4/2022-09-quickswap-findings/issues/84#issuecomment-1267000678):**
 > Going to leave as Medium - even if for nothing else as to warn users in the future to not trust on-chain pricing for new pools or pools with low liquidity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | QuickSwap and StellaSwap |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-quickswap
- **GitHub**: https://github.com/code-423n4/2022-09-quickswap-findings/issues/84
- **Contest**: https://code4rena.com/reports/2022-09-quickswap

### Keywords for Search

`vulnerability`

