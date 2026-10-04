---
# Core Classification
protocol: Revert Lend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32298
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-revert-lend
source_link: https://code4rena.com/reports/2024-03-revert-lend
github_link: https://github.com/code-423n4/2024-03-revert-lend-findings/issues/220

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - t4sk
  - kennedy1030
---

## Vulnerability Title

Improper return of `chainlinkReferencePriceX96` in V3Oracle.`_getReferenceTokenPriceX96()`

### Overview

See description below for full details.

### Original Finding Content



*Note: Since the sponsor team chose to [mitigate](https://github.com/code-423n4/2024-04-revert-mitigation?tab=readme-ov-file#additional-scope-to-be-reviewed), this downgraded issue has been included in this report for completeness.*

In certain situations, `cachedChainlinkReferencePriceX96` cannot prevent the reevaluation of the price of `referenceToken` in [V3Oracle.getValue()](https://github.com/code-423n4/2024-03-revert-lend/blob/main/src/V3Oracle.sol#L95-L131).

### Proof of Concept

In `V3Oracle._getReferenceTokenPriceX96()` at [L278](https://github.com/code-423n4/2024-03-revert-lend/blob/main/src/V3Oracle.sol#L278), for the scenario where `token = referenceToken`, the returned value of `chainlinkReferencePriceX96` is `0`.

```javascript
    function _getReferenceTokenPriceX96(address token, uint256 cachedChainlinkReferencePriceX96)
        internal
        view
        returns (uint256 priceX96, uint256 chainlinkReferencePriceX96)
    {
        if (token == referenceToken) {
278         return (Q96, chainlinkReferencePriceX96);
        }

        TokenConfig memory feedConfig = feedConfigs[token];

        if (feedConfig.mode == Mode.NOT_SET) {
            revert NotConfigured();
        }

        uint256 verifyPriceX96;

        bool usesChainlink = (
            feedConfig.mode == Mode.CHAINLINK_TWAP_VERIFY || feedConfig.mode == Mode.TWAP_CHAINLINK_VERIFY
                || feedConfig.mode == Mode.CHAINLINK
        );
        bool usesTWAP = (
            feedConfig.mode == Mode.CHAINLINK_TWAP_VERIFY || feedConfig.mode == Mode.TWAP_CHAINLINK_VERIFY
                || feedConfig.mode == Mode.TWAP
        );

        if (usesChainlink) {
            uint256 chainlinkPriceX96 = _getChainlinkPriceX96(token);
300         chainlinkReferencePriceX96 = cachedChainlinkReferencePriceX96 == 0
                ? _getChainlinkPriceX96(referenceToken)
                : cachedChainlinkReferencePriceX96;

            chainlinkPriceX96 = (10 ** referenceTokenDecimals) * chainlinkPriceX96 * Q96 / chainlinkReferencePriceX96
                / (10 ** feedConfig.tokenDecimals);

            if (feedConfig.mode == Mode.TWAP_CHAINLINK_VERIFY) {
                verifyPriceX96 = chainlinkPriceX96;
            } else {
                priceX96 = chainlinkPriceX96;
            }
        }

        if (usesTWAP) {
            uint256 twapPriceX96 = _getTWAPPriceX96(feedConfig);
            if (feedConfig.mode == Mode.CHAINLINK_TWAP_VERIFY) {
                verifyPriceX96 = twapPriceX96;
            } else {
                priceX96 = twapPriceX96;
            }
        }

        if (feedConfig.mode == Mode.CHAINLINK_TWAP_VERIFY || feedConfig.mode == Mode.TWAP_CHAINLINK_VERIFY) {
            _requireMaxDifference(priceX96, verifyPriceX96, feedConfig.maxDifference);
        }
    }
```

It sets the value of `cachedChainlinkReferencePriceX96` to `0` in [V3Oracle.getValue()](https://github.com/code-423n4/2024-03-revert-lend/blob/main/src/V3Oracle.sol#L95-L131).

```javascript
    function getValue(uint256 tokenId, address token)
        external
        view
        override
        returns (uint256 value, uint256 feeValue, uint256 price0X96, uint256 price1X96)
    {
        (address token0, address token1, uint24 fee,, uint256 amount0, uint256 amount1, uint256 fees0, uint256 fees1) =
            getPositionBreakdown(tokenId);

        uint256 cachedChainlinkReferencePriceX96;

106     (price0X96, cachedChainlinkReferencePriceX96) =
            _getReferenceTokenPriceX96(token0, cachedChainlinkReferencePriceX96);
108     (price1X96, cachedChainlinkReferencePriceX96) =
            _getReferenceTokenPriceX96(token1, cachedChainlinkReferencePriceX96);

        uint256 priceTokenX96;
        if (token0 == token) {
            priceTokenX96 = price0X96;
        } else if (token1 == token) {
            priceTokenX96 = price1X96;
        } else {
117         (priceTokenX96,) = _getReferenceTokenPriceX96(token, cachedChainlinkReferencePriceX96);
        }

        value = (price0X96 * (amount0 + fees0) / Q96 + price1X96 * (amount1 + fees1) / Q96) * Q96 / priceTokenX96;
        feeValue = (price0X96 * fees0 / Q96 + price1X96 * fees1 / Q96) * Q96 / priceTokenX96;
        price0X96 = price0X96 * Q96 / priceTokenX96;
        price1X96 = price1X96 * Q96 / priceTokenX96;

        // checks derived pool price for price manipulation attacks
        // this prevents manipulations of pool to get distorted proportions of collateral tokens - for borrowing
        // when a pool is in this state, liquidations will be disabled - but arbitrageurs (or liquidator himself)
        // will move price back to reasonable range and enable liquidation
        uint256 derivedPoolPriceX96 = price0X96 * Q96 / price1X96;
        _checkPoolPrice(token0, token1, fee, derivedPoolPriceX96);
    }
```

In fact, `cachedChainlinkReferencePriceX96` is established to prevent the reevaluation of the price of `referenceToken` in `V3Oracle._getReferenceTokenPriceX96()` at [L300](https://github.com/code-423n4/2024-03-revert-lend/blob/main/src/V3Oracle.sol#L300).

However, when `token1 = referenceToken` in [V3Oracle.getValue()](https://github.com/code-423n4/2024-03-revert-lend/blob/main/src/V3Oracle.sol#L108), the `cachedChainlinkReferencePriceX96` value is set to `0`, and it fails to prevent the recalculation in the subsequent call of `_getReferenceTokenPriceX96()` at [L117](https://github.com/code-423n4/2024-03-revert-lend/blob/main/src/V3Oracle.sol#L117).

### Recommended Mitigation Steps

```diff
    function _getReferenceTokenPriceX96(address token, uint256 cachedChainlinkReferencePriceX96)
        internal
        view
        returns (uint256 priceX96, uint256 chainlinkReferencePriceX96)
    {
        if (token == referenceToken) {
-           return (Q96, chainlinkReferencePriceX96);
+           return (Q96, cachedChainlinkReferencePriceX96);
        }

        [...]
    }
```

**[kalinbas (Revert) confirmed, but disagreed with severity](https://github.com/code-423n4/2024-03-revert-lend-findings/issues/220#issuecomment-2020820925)**

**[ronnyx2017 (judge) decreased severity to QA](https://github.com/code-423n4/2024-03-revert-lend-findings/issues/220#issuecomment-2028747004)**

**[Revert mitigated](https://github.com/code-423n4/2024-04-revert-mitigation?tab=readme-ov-file#scope):**
> Fixed [here](https://github.com/revert-finance/lend/pull/13).

**Status:** Mitigation Confirmed. Full details in reports from [b0g0](https://github.com/code-423n4/2024-04-revert-mitigation-findings/issues/59), [thank_you](https://github.com/code-423n4/2024-04-revert-mitigation-findings/issues/70) and [ktg](https://github.com/code-423n4/2024-04-revert-mitigation-findings/issues/6).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Revert Lend |
| Report Date | N/A |
| Finders | t4sk, kennedy1030 |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-revert-lend
- **GitHub**: https://github.com/code-423n4/2024-03-revert-lend-findings/issues/220
- **Contest**: https://code4rena.com/reports/2024-03-revert-lend

### Keywords for Search

`vulnerability`

