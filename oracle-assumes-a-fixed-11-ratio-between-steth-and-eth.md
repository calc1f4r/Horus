---
# Core Classification
protocol: Venus wstETH Oracle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59670
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/venus-wst-eth-oracle/52f5b094-8058-4ca2-9290-2067bde79438/index.html
source_link: https://certificate.quantstamp.com/full/venus-wst-eth-oracle/52f5b094-8058-4ca2-9290-2067bde79438/index.html
github_link: none

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
finders_count: 4
finders:
  - Shih-Hung Wang
  - Faycal Lalidji
  - Mostafa Yassin
  - Hytham Farah
---

## Vulnerability Title

Oracle Assumes a Fixed 1:1 Ratio Between stETH and ETH

### Overview

See description below for full details.

### Original Finding Content

**Update**
The Venus team added a constructor parameter, `ASSUME_STETH_ETH_EQUIVALENCE`, to the `WstETHOracle` contract, indicating whether the oracle should assume a 1:1 ratio between `stETH` and `ETH`. If not, the market price of `stETH` will be obtained through the `ResilientOracle`.

This change allows the Venus team to deploy two `wstETH` oracles and configure which oracle (or both) to use in the `ResilientOracle` based on their assessment of the `stETH` market conditions. Note that the correctness of the configuration in the `ResilientOracle` and how the market price of `stETH` is obtained was out of scope and not examined through this audit.

We also note that this mitigation increases centralization risk as it would be up to the team to identify what constitutes a "long-term depeg" and act accordingly.

![Image 15: Alert icon](https://certificate.quantstamp.com/full/venus-wst-eth-oracle/52f5b094-8058-4ca2-9290-2067bde79438/static/media/info-icon-alert.3c9578483b1cf3181c9bfb6fec7dc641.svg)

**Update**
Marked as "Mitigated" by the client. Addressed in: `dd0fba403de31545b979dd1513eaf53e085ffd7d`. The client provided the following explanation:

> We agree that in some cases assuming 1:1 ratio between `stETH/ETH` might be wrong. There is an option to add an `stETH/USD` price feed as pivot oracle in our `ResilientOracle` in order to have an on-chain kill switch in case of depeg. However we believe that if there is depeg of this ratio, it will be a short term depeg. In case of a short term depeg and configuring a pivot price feed (`stETH/USD`) in our `ResilientOracle` users will not be able to use the protocol, since the resilient oracle will return invalid price, meaning borrowing, repaying and liquidations will be not possible. Another option is to use only the `stETH/USD` price feed and not assume 1:1 ratio at all. This solution is again not really optimal. Usually `ETH` and `stETH` are on peg, meaning that users will borrow near the maximum allowed amount they can. Meaning that in case of a short term depeg a lot of false liquidations will be forced which will end up in users loosing their positions. Short term depegs are expected happen from time to time in case of big `stETH` redemptions or network congestion, but the peg always tends to restore. In a case of a long term depeg (or a black swan event) we propose the following mitigation:
> 
> 
> 1.   We will have 2 deployed `wstETH` oracles on-chain:
>     *   One oracle will return price based on 1:1 ratio assumption between `stETH/ETH`
>     *   One oracle will return price based on `stETH/USD` market price feed
> 
> 2.   By default in the `ResilientOracle` we will have only configured the oracle assuming 1:1 ratio between `stETH/ETH`, as main oracle
> 3.   The other oracle (getting price from `stETH/USD`price feed and not assuming 1:1 ratio) will not be configured in our `ResilientOracle`
> 4.   We will have an off chain monitoring system in place, monitoring the prices returned from both oracles. In case of a big deviation, our team will decide if to replace the oracle assuming 1:1 ratio with the oracle not assuming it, or to add the latter as a pivot oracle for the time being. In order to maintain the same code base, we have implemented a logic with a boolean flag, based on it the oracle will either assume 1:1 ratio, or will check `stETH/USD` price. We have added also this mitigation plan in our [documentation](https://github.com/VenusProtocol/venus-protocol-documentation/pull/169/commits/97c1bacbeea6623767cc893213113f02c427324d)

**File(s) affected:**`WstETHOracle.sol`

**Description:** The `WstETHOracle` contract returns the price of the `wstETH` token in USD, which is calculated as follows:

PWSTETH/USD=PWSTETH/STETH×PWETH/USDP_{WSTETH/USD} = P_{WSTETH/STETH} \times P_{WETH/USD}

where PWSTETH/STETHP_{WSTETH/STETH} represents the amount of `stETH` equivalent to 1 `wstETH` token, and PWETH/USDP_{WETH/USD} represents the price of `WETH` in USD. The former is fetched from the on-chain `stETH` token contract and reflects the actual exchange rate between `wstETH` and `stETH` in the Lido protocol when querying the price. The latter is fetched and returned from the `ResilientOracle`.

This pricing formula assumes a 1:1 ratio between `stETH` and `ETH`, i.e., `stETH` is pegged to `ETH`. Such a design raises the following security concerns:

1.   The oracle is unable to reflect the market price of `stETH`. Suppose `stETH` depegs from `ETH`, which may be due to reasons such as a large amount of `ETH` being removed from the Curve `stETH/ETH` pool. The market price of `stETH` has dropped, while the protocol may overvalue `stETH` temporarily during the depeg event. Assuming the depeg does not recover in time (note that withdrawals from Lido are not confirmed instantly compared to deposits), positions with `wstETH` as collateral will have an advantage in terms of borrowing power during this period.
2.   Suppose the depeg continues so that the spread between the exchange rate and the market price is larger than 1−LT1 - LT (where LTLT represents the liquidation threshold). In that case, it will become profitable to deposit `stETH` as collateral to the protocol, borrow `ETH`, and sell it in the secondary market. The utilization rate of `ETH` may increase, leading to potential issues such as lacking liquidity for withdrawals.
3.   In an extreme scenario where the depeg cannot be recovered, the protocol may accrue bad debts if underwater positions with `wstETH` as collateral cannot be liquidated in time.

**Recommendation:** Consider implementing off-chain monitoring of the `stETH/ETH` exchange rate and react promptly if `stETH` depegs to an abnormal threshold. Possible actions could be pausing the `wstETH` market or adjusting the market parameters (e.g., the liquidation threshold), depending on the protocol choice and acceptance of associated risks.

An alternative approach is to obtain the `stETH/ETH` price from Chainlink price feeds or on-chain oracles to ensure that the market price of `stETH` is within an acceptable range.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Venus wstETH Oracle |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Faycal Lalidji, Mostafa Yassin, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/venus-wst-eth-oracle/52f5b094-8058-4ca2-9290-2067bde79438/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/venus-wst-eth-oracle/52f5b094-8058-4ca2-9290-2067bde79438/index.html

### Keywords for Search

`vulnerability`

