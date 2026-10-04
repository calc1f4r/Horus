---
# Core Classification
protocol: Olympus DAO
chain: everychain
category: arithmetic
vulnerability_type: precision_loss

# Attack Vector Details
attack_type: precision_loss
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3229
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-08-olympus-dao-contest
source_link: https://code4rena.com/reports/2022-08-olympus
github_link: https://github.com/code-423n4/2022-08-olympus-findings/issues/483

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
  - precision_loss

protocol_categories:
  - liquid_staking
  - yield
  - cross_chain
  - leveraged_farming
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - CertoraInc
  - d3e4
  - hyh
  - rbserver
---

## Vulnerability Title

[M-25] Moving average precision is lost

### Overview


A bug report has been issued for the code found in the GitHub repository https://github.com/code-423n4/2022-08-olympus/blob/2a0b515012b4a40076f6eac487f7816aafb8724a/src/modules/PRICE.sol#L134-L139. The vulnerability is that the precision is lost in moving average calculations as the difference is calculated separately and added each time, while it typically can be small enough to lose precision in the division involved. It is demonstrated with an example of `10000` moves of `990` size, `numObservations = 1000` which should yield `9900` increase in the moving average, but instead yields `0`.

The bug report suggests that the cumulative `sum` should be stored, while returning `sum / numObs` on request. This can be achieved by replacing the `return _movingAverage` line in the code with the line `return _movingAverage / numObservations`. This change should prevent the precision from being lost and ensure the moving average is calculated correctly.

### Original Finding Content

_Submitted by hyh, also found by CertoraInc, d3e4, and rbserver_

Now the precision is lost in moving average calculations as the difference is calculated separately and added each time, while it typically can be small enough to lose precision in the division involved.

For example, `10000` moves of `990` size, `numObservations = 1000`. This will yield `0` on each update, while must yield `9900` increase in the moving average.

### Proof of Concept

Moving average is calculated with the addition of the difference:

<https://github.com/code-423n4/2022-08-olympus/blob/2a0b515012b4a40076f6eac487f7816aafb8724a/src/modules/PRICE.sol#L134-L139>

```solidity
        // Calculate new moving average
        if (currentPrice > earliestPrice) {
            _movingAverage += (currentPrice - earliestPrice) / numObs;
        } else {
            _movingAverage -= (earliestPrice - currentPrice) / numObs;
        }
```

`/ numObs` can lose precision as `currentPrice - earliestPrice` is usually small.

It is returned on request as is:

<https://github.com/code-423n4/2022-08-olympus/blob/2a0b515012b4a40076f6eac487f7816aafb8724a/src/modules/PRICE.sol#L189-L193>

```solidity
    /// @notice Get the moving average of OHM in the Reserve asset over the defined window (see movingAverageDuration and observationFrequency).
    function getMovingAverage() external view returns (uint256) {
        if (!initialized) revert Price_NotInitialized();
        return _movingAverage;
    }
```

### Recommended Mitigation Steps

Consider storing the cumulative `sum`, while returning `sum / numObs` on request:

<https://github.com/code-423n4/2022-08-olympus/blob/2a0b515012b4a40076f6eac487f7816aafb8724a/src/modules/PRICE.sol#L189-L193>

```solidity
    /// @notice Get the moving average of OHM in the Reserve asset over the defined window (see movingAverageDuration and observationFrequency).
    function getMovingAverage() external view returns (uint256) {
        if (!initialized) revert Price_NotInitialized();
-       return _movingAverage;
+       return _movingAverage / numObservations;
    }
```

**[Oighty (Olympus) disagreed with severity and commented](https://github.com/code-423n4/2022-08-olympus-findings/issues/483#issuecomment-1238433469):**
 > Keeping track of the observations as a sum and then dividing is a good suggestion. The price values have 18 decimals and the max discrepancy introduced is very small (10**-15) with expected parameter ranges. The potential risk to the protocol seems low though.

**[hyh (warden) commented](https://github.com/code-423n4/2022-08-olympus-findings/issues/483#issuecomment-1240994248):**
 > Please notice that discrepancy here is unbounded, i.e. the logic itself does not have any max discrepancy, the divergence between fact and recorded value can pile up over time without a limit.
> 
> If you do imply that markets should behave in some way that minuses be matched with pluses, then I must say that they really shouldn't.

**[Oighty (Olympus) confirmed](https://github.com/code-423n4/2022-08-olympus-findings/issues/483)**

**[0xean (judge) commented](https://github.com/code-423n4/2022-08-olympus-findings/issues/483#issuecomment-1249930031):**
 > Debating between QA and Medium on this one. I am going to award it as medium because there is a potential to leak some value due to this imprecision compounding over time. 



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Olympus DAO |
| Report Date | N/A |
| Finders | CertoraInc, d3e4, hyh, rbserver |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-olympus
- **GitHub**: https://github.com/code-423n4/2022-08-olympus-findings/issues/483
- **Contest**: https://code4rena.com/contests/2022-08-olympus-dao-contest

### Keywords for Search

`Precision Loss`

