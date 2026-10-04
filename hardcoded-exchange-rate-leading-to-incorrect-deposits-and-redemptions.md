---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57289
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
finders_count: 24
finders:
  - cd_pandora
  - 0xalexsr
  - oct0pwn
  - buggsyes
  - patitonar
---

## Vulnerability Title

Hardcoded Exchange Rate Leading to Incorrect Deposits and Redemptions

### Overview


The report discusses a bug in the `StabilityPool` smart contract that leads to incorrect deposits and redemptions. The issue is caused by a hardcoded exchange rate of `1e18`, which assumes a fixed 1:1 exchange rate between two tokens. This can result in financial imbalances and arbitrage exploits, potentially leading to protocol insolvency. The impact of this bug can be seen in previous cases of similar issues in DeFi lending protocols. The recommended solution is to replace the hardcoded value with a formula that accurately calculates the exchange rate based on token supply and balance.

### Original Finding Content

## Summary

The `StabilityPool::getExchangeRate()` function is hardcoded to return a fixed value of `1e18`, which assumes a static 1:1 exchange rate between `rToken and deToken`. This implementation does not account for real-time changes in token supply and demand. As a result, users may receive incorrect amounts when depositing or redeeming tokens, leading to potential financial imbalances and arbitrage exploits.

## Vulnerability Details

```Solidity
function getExchangeRate() public view returns (uint256) {
    // uint256 totalDeCRVUSD = deToken.totalSupply();
    // uint256 totalRcrvUSD = rToken.balanceOf(address(this));
    // if (totalDeCRVUSD == 0 || totalRcrvUSD == 0) return 10**18;

    // uint256 scalingFactor = 10**(18 + deTokenDecimals - rTokenDecimals);
    // return (totalRcrvUSD * scalingFactor) / totalDeCRVUSD;
    return 1e18;
}
```

### **Issue:**

1. **Static Exchange Rate:**

   * The function always returns `1e18`, meaning the exchange rate between `rToken` and `deToken` is assumed to be fixed at 1:1.
   * The commented-out code suggests an original intention to make the rate dynamic based on token supply but was removed.

2. **Incorrect Deposit and Redemption Calculations:**

   * The deposit function (`deposit()`) relies on `calculateDeCRVUSDAmount()`, which uses `getExchangeRate()`.
   * The redemption function (`calculateRcrvUSDAmount()`) also uses `getExchangeRate()`.
   * Since `getExchangeRate()` is hardcoded, these calculations may not reflect real market conditions.

3. **Arbitrage Risks:**

   * If the real market value of `rToken` fluctuates, users can **deposit undervalued tokens and redeem overvalued ones**, extracting unearned profits.
   * This could result in **protocol insolvency** if redemptions exceed available reserves.

4. **Liquidity Imbalance:**

   * The total supply of `deToken` may become misaligned with the actual available `rToken` balance.
   * If too many deposits occur before an update, redemptions may fail due to insufficient reserves.



## Impact

<https://github.com/Cyfrin/2025-02-raac/blob/main/contracts/core/pools/StabilityPool/StabilityPool.sol#L211-L212>

**Real-World Impact** A similar issue occurred in **DeFi lending protocols**, where mispriced exchange rates led to excessive borrowing and redemption exploits. A well-known case was the **Iron Finance Bank Run**, where an artificially pegged stablecoin lost parity, causing mass redemptions and liquidity depletion.

## Tools Used

## Recommendations

Replace the hardcoded `1e18` with a formula that correctly derives the rate based on `deToken.totalSupply()` and `rToken.balanceOf(address(this))`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | cd_pandora, 0xalexsr, oct0pwn, buggsyes, patitonar, kwakudr, foxb868, mahdikarimi, aariiif, classick11, santechie21, maze, mustaphaabdulaziz00, foufrix, invcbull, zebra, ibukunola, sala1, lin0x9a7a, alexczm, binaryreturns |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

