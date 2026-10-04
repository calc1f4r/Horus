---
# Core Classification
protocol: Tigris Trade
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6327
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-tigris-trade-contest
source_link: https://code4rena.com/reports/2022-12-tigris
github_link: https://github.com/code-423n4/2022-12-tigris-findings/issues/462

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - derivatives
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 11
finders:
  - 8olidity
  - __141345__
  - 0xhacksmithh
  - Secureverse
  - SamGMK
---

## Vulnerability Title

[H-08] Incorrect Assumption of Stablecoin Market Stability

### Overview


The StableVault contract attempts to group all types of stablecoins under a single token, which can be minted or burned for any of the supported stablecoins. This is a medium-severity vulnerability as the balance sheet of the contract consists of multiple assets which do not have a one-to-one exchange ratio between them. This means that the contract exposes a 0% slippage 1-to-1 exchange between assets that in reality have varying prices. This can be exploited by an attacker to arbitrage the balance sheet of the contract, especially using flash-loans, to swap an undesirable asset for a more desirable one and gain an arbitrage in the price.

To illustrate the issue, the attacker can simply view the exchange output they would get for swapping their USDC to USDT in a stablecoin pool and then invoke the deposit with their USDC asset and withdraw the incorrectly calculated USDT equivalent. The arbitrage can be observed by assessing the difference in the trade outputs and can be capitalized by selling the newly acquired USDT for USDC on the stablecoin pair.

The issue was identified by manual review of the codebase, Chainlink oracle resources, and Curve Finance pools. To mitigate the issue, it is advised to utilize Chainlink oracles for evaluating the inflow of assets instead, ensuring that all inflows and outflows of stablecoins are fairly evaluated based on their "neutral" USD price rather than their subjective on-chain price or equality assumption.

### Original Finding Content


<https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/StableVault.sol#L39-L51> 

<https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/StableVault.sol#L60-L72>

### Impact

The `StableVault` contract attempts to group all types of stablecoins under a single token which can be minted for any of the stablecoins supported by the system as well as burned for any of them.

This is at minimum a medium-severity vulnerability as the balance sheet of the `StableVault` will consist of multiple assets which do not have a one-to-one exchange ratio between them as can be observed by trading pools such as [Curve](https://curve.fi/#/ethereum/pools/3pool/deposit) as well as the [Chainlink oracle reported prices themselves](https://data.chain.link/ethereum/mainnet/stablecoins/usdc-usd).

Given that the contract exposes a 0% slippage 1-to-1 exchange between assets that in reality have varying prices, the balance sheet of the contract can be arbitraged (especially by flash-loans) to swap an undesirable asset (i.e. USDC which at the time of submission was valued at `0.99994853` USD) for a more desirable asset (i.e. USDT which at the time of submission was valued at `1.00000000` USD) acquiring an arbitrage in the price by selling the traded asset.

### Proof of Concept

To illustrate the issue, simply view the exchange output you would get for swapping your USDC to USDT in a stablecoin pool (i.e. CurveFi) and then proceed to [invoke `deposit`](https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/StableVault.sol#L39-L51) with your USDC asset and retrieve your [incorrectly calculated `USDT` equivalent via `withdraw`](https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/StableVault.sol#L60-L72).

The arbitrage can be observed by assessing the difference in the trade outputs and can be capitalized by selling our newly acquired `USDT` for `USDC` on the stablecoin pair we assessed earlier, ultimately ending up with a greater amount of `USDC` than we started with. This type of attack can be extrapolated by utilizing a flash-loan rather than our personal funds.

### Tools Used

[Chainlink oracle resources](https://data.chain.link/popular)

[Curve Finance pools](https://curve.fi/#/ethereum/pools)

### Recommended Mitigation Steps

We advise the `StableVault` to utilize Chainlink oracles for evaluating the inflow of assets instead, ensuring that all inflows and outflows of stablecoins are fairly evaluated based on their "neutral" USD price rather than their subjective on-chain price or equality assumption.

**[Alex the Entreprenerd (judge) increased severity to High and commented](https://github.com/code-423n4/2022-12-tigris-findings/issues/462#issuecomment-1359639245):**
 > The warden has shown how, due to an incorrect assumption, the system offers infinite leverage.
> 
> This can be trivially exploited by arbitraging with any already available exchange.
> 
> Depositors will incur a loss equal to the size of the arbitrage as the contract is always taking the losing side.
> 
> I believe this should be High because of it's consistently losing nature.

**[TriHaz (Tigris Trade) acknowledged and commented](https://github.com/code-423n4/2022-12-tigris-findings/issues/462#issuecomment-1377373227):**
 > We are aware of this issue, we will keep the vault with one token for now.


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Tigris Trade |
| Report Date | N/A |
| Finders | 8olidity, __141345__, 0xhacksmithh, Secureverse, SamGMK, rotcivegaf, Ruhum, 0xsomeone, Tointer, aviggiano, Critical |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tigris
- **GitHub**: https://github.com/code-423n4/2022-12-tigris-findings/issues/462
- **Contest**: https://code4rena.com/contests/2022-12-tigris-trade-contest

### Keywords for Search

`vulnerability`

