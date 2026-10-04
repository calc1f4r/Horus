---
# Core Classification
protocol: Malt Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16080
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-02-malt-protocol-versus-contest
source_link: https://code4rena.com/reports/2023-02-malt
github_link: https://github.com/code-423n4/2023-02-malt-findings/issues/36

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
  - algo-stables
  - reserve_currency
  - liquid_staking
  - cdp
  - services

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - minhquanym
  - hansfriese
---

## Vulnerability Title

[M-02] The latest malt price can be less than the actual price target and `StabilizerNode.stabilize` will revert

### Overview


A bug was found in the code of the StabilizerNode contract, which is part of the StabilityPod project. The code snippet assumes that the latest sample of malt prices is greater than or equal to the price target. However, if the exchange rate is greater than the price target and the sender of the message is not an admin or whitelisted, it will assert that the live price is greater than the minThreshold. The minThreshold is calculated by subtracting the difference between the latest sample and the price target from the latest sample. This could cause the `stabilize` function to revert if the latest sample is less than the price target.

The bug was found using manual review. To mitigate this issue, the code should use `minThreshold = latestSample + (((priceTarget - latestSample) * sampleSlippageBps) / 10000)` when `priceTarget > latestSample`.

### Original Finding Content


<https://github.com/code-423n4/2023-02-malt/blob/main/contracts/StabilityPod/StabilizerNode.sol#L188> 

<https://github.com/code-423n4/2023-02-malt/blob/main/contracts/StabilityPod/StabilizerNode.sol#L201-L203>

### Impact

`StabilizerNode.stabilize` will revert when `latestSample < priceTarget`.

### Proof of Concept

In StabilizerNode.stabilize, when `exchangeRate > priceTarget` and `_msgSender` is not an admin and not whitelisted, it asserts `livePrice > minThreshold`.

And `minThreshold` is calculated as follows:

        uint256 priceTarget = maltDataLab.getActualPriceTarget();

<!---->

            uint256 latestSample = maltDataLab.maltPriceAverage(0);
            uint256 minThreshold = latestSample -
              (((latestSample - priceTarget) * sampleSlippageBps) / 10000);

This code snippet assumes that `latestSample >= priceTarget`. Although `exchangeRate > priceTarget`, `exchangeRate` is the malt average price during `priceAveragePeriod`. But `latestSample` is one of those malt prices. So `latestSample` can be less than `exchangeRate` and `priceTarget`, so `stabilize` will revert in this case.

### Recommended Mitigation Steps

Use `minThreshold = latestSample + (((priceTarget - latestSample) * sampleSlippageBps) / 10000)` when `priceTarget > latestSample`.

**[0xScotch (Malt) confirmed and commented](https://github.com/code-423n4/2023-02-malt-findings/issues/36#issuecomment-1446996158):**
 > We actually do want the tx to revert when `latestSample < priceTarget` as that means the most recent sample in the price average feed is below peg but we are in the above peg stabilization flow in the code. However, we do not want the revert to be subtraction overflow as that looks like something went wrong. So we should handle with an explicit error.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Malt Protocol |
| Report Date | N/A |
| Finders | minhquanym, hansfriese |

### Source Links

- **Source**: https://code4rena.com/reports/2023-02-malt
- **GitHub**: https://github.com/code-423n4/2023-02-malt-findings/issues/36
- **Contest**: https://code4rena.com/contests/2023-02-malt-protocol-versus-contest

### Keywords for Search

`vulnerability`

