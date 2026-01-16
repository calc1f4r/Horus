---
# Core Classification
protocol: Connext
chain: everychain
category: economic
vulnerability_type: sandwich_attack

# Attack Vector Details
attack_type: sandwich_attack
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7214
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
github_link: none

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
  - sandwich_attack

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

Use of spot price in SponsorVault leads to sandwich attack.

### Overview


This bug report describes an attack vector in the SponsorVault smart contract. The SponsorVault is used to provide liquidity fees and transfer fees to users, and can accept either adopted tokens or native tokens. The issue arises when the SponsorVault uses the spot AMM price when swapping tokens, as attackers can manipulate the value of getInGivenExpectedOut and make the SponsorVault sell the native token at an unfavorable price. 

To illustrate, assume the native token is ETH and the adopted token is USDC. If the SponsorVault tries to sponsor 100 USDC to the users, the attacker can manipulate the exchange rate of 1 ETH = 0.1 USDC, causing getInGivenExpectedOut to return 1000. The SponsorVault then buys 100 USDC with 1000 ETH, causing the ETH price to decrease even lower, allowing the attacker to buy ETH at a lower price and realize a profit.

The recommendation is to use an oracle price, such as a Chainlink price or Uniswap TWAP, instead of relying on the DEX spot price, and compare it against the spot price. The SponsorVault should either revert or use the oracle price when the spot price deviates from the oracle price. The issue has been solved in PR 1595 and verified.

### Original Finding Content

## Severity: Critical Risk

## Context
**File:** SponsorVault.sol  
**Line:** 208

## Description
There is a special role sponsor in the protocol. Sponsors can cover the liquidity fee and transfer fee for users, making it more favorable for users to migrate to the new chain. Sponsors can either provide liquidity for each adopted token or provide the native token in the `SponsorVault`. If the native token is provided, the `SponsorVault` will swap to the adopted token before transferring it to users.

```solidity
contract SponsorVault is ISponsorVault, ReentrancyGuard, Ownable {
    ...
    function reimburseLiquidityFees(
        address _token,
        uint256 _liquidityFee,
        address _receiver
    ) external override onlyConnext returns (uint256) {
        ...
        uint256 amountIn = tokenExchange.getInGivenExpectedOut(_token, _liquidityFee);
        amountIn = currentBalance >= amountIn ? amountIn : currentBalance;
        // sponsored fee may end being less than _liquidityFee due to slippage
        sponsoredFee = tokenExchange.swapExactIn{value: amountIn}(_token, msg.sender);
        ...
    }
}
```

The spot AMM price is used when doing the swap. Attackers can manipulate the value of `getInGivenExpectedOut` and make `SponsorVault` sell the native token at a bad price. By executing a sandwich attack, the exploiters can drain all native tokens in the sponsor vault.

For the sake of the following example, assume that `_token` is USDC and the native token is ETH. The sponsor tries to sponsor 100 USDC to the users:
- Attacker first manipulates the DEX and makes the exchange of 1 ETH = 0.1 USDC.
- `getInGivenExpectedOut` returns \( \frac{100}{0.1} = 1000 \).
- `tokenExchange.swapExactIn` buys 100 USDC with 1000 ETH, causing the ETH price to decrease even lower.
- Attacker buys ETH at a lower price and realizes a profit.

## Recommendation
Instead of relying on DEX's spot price, the sponsor vault should rely instead on price quotes which are harder to manipulate, like those provided by an oracle (e.g., Chainlink price, Uniswap TWAP). The `SponsorVault` should fetch the oracle price and compare it against the spot price. The `SponsorVault` should either revert or use the oracle price when the spot price deviates from the oracle price.

## Connext
Solved in PR 1595.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | 0xLeastwood, Jonah1005 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf

### Keywords for Search

`Sandwich Attack`

