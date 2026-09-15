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
solodit_id: 32273
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-revert-lend
source_link: https://code4rena.com/reports/2024-03-revert-lend
github_link: https://github.com/code-423n4/2024-03-revert-lend-findings/issues/409

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

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - JecikPo
  - kfx
  - kennedy1030
  - KupiaSec
  - SpicyMeatball
---

## Vulnerability Title

[M-07] Large decimal of `referenceToken` causes overflow at oracle price calculation

### Overview


This bug report discusses an issue with the price calculation at `V3Oracle.sol` when using a high decimal value for the `referenceToken`. This causes the calculation to revert and makes the Chainlink price feed unusable, potentially leading to reduced security of the pricing. The issue can occur after the project is already live and the price reaches a certain point. A proof of concept is provided to demonstrate the issue and recommended mitigation steps are suggested by Chainlink. The assessed type of the bug is decimal and it has been confirmed and mitigated by the team. More details can be found in the reports from other researchers.

### Original Finding Content


The price calculation at the `V3Oracle.sol` will revert upon reaching certain level when `referenceToken` is used with high decimal value (e.g. 18). The revert (specifically happening when calling `getValue()`) would make the Chainlink price feed useless; yet the TWAP price source would still be available. The protocol team would have to disable Chainlink and rely exclusively on the TWAP source reducing security of the pricing. The issue could manifest itself after certain amount of time once the project is already live and only when price returned by the feed reaches certain point.

### Proof of Concept

The following code line has an issue:

    chainlinkPriceX96 = (10 ** referenceTokenDecimals) * chainlinkPriceX96 * Q96 / chainlinkReferencePriceX96
                    / (10 ** feedConfig.tokenDecimals);

When `referenceTokenDecimals` is 18, `chainlinkPriceX96` is higher than some threshold between 18 and 19 (in Q96 notation), which will cause arithmetic overflow.

### Recommended Mitigation Steps

Instead of calculating the price this way:

    chainlinkPriceX96 = (10 ** referenceTokenDecimals) * chainlinkPriceX96 * Q96 / chainlinkReferencePriceX96
                    / (10 ** feedConfig.tokenDecimals);

It could be done the following way as per Chainlink's recommendation:

    if (referenceTokenDecimals > feedConfig.tokenDecimals)
                chainlinkPriceX96 = (10 ** referenceTokenDecimals - feedConfig.tokenDecimals) * chainlinkPriceX96 * Q96 
                / chainlinkReferencePriceX96;
            else if (referenceTokenDecimals < feedConfig.tokenDecimals)
                chainlinkPriceX96 = chainlinkPriceX96 * Q96 / chainlinkReferencePriceX96 
                / (10 ** feedConfig.tokenDecimals - referenceTokenDecimals);
            else 
                chainlinkPriceX96 = chainlinkPriceX96 * Q96 / chainlinkReferencePriceX96;

Reference [here](<https://docs.chain.link/data-feeds/using-data-feeds#getting-a-different-price-denomination>).

### Assessed type

Decimal

**[kalinbas (Revert) confirmed](https://github.com/code-423n4/2024-03-revert-lend-findings/issues/409#issuecomment-2021064600)**

**[Revert mitigated](https://github.com/code-423n4/2024-04-revert-mitigation?tab=readme-ov-file#scope):**
> Fixed [here](https://github.com/revert-finance/lend/pull/21).

**Status:** Mitigation confirmed. Full details in reports from [ktg](https://github.com/code-423n4/2024-04-revert-mitigation-findings/issues/3), [thank_you](https://github.com/code-423n4/2024-04-revert-mitigation-findings/issues/84) and [b0g0](https://github.com/code-423n4/2024-04-revert-mitigation-findings/issues/62).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Revert Lend |
| Report Date | N/A |
| Finders | JecikPo, kfx, kennedy1030, KupiaSec, SpicyMeatball, linmiaomiao, t4sk |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-revert-lend
- **GitHub**: https://github.com/code-423n4/2024-03-revert-lend-findings/issues/409
- **Contest**: https://code4rena.com/reports/2024-03-revert-lend

### Keywords for Search

`vulnerability`

