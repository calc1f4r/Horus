---
# Core Classification
protocol: Sharwafinance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36472
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/SharwaFinance-security-review.md
github_link: none

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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[C-01] Using Uniswap spot price is subject to manipulation

### Overview


This bug report highlights a high severity issue in the protocol that uses the Uniswap V3 quoter contract. The quoter is used to get the current value of supported tokens in terms of a base token (USDC). However, these values can be easily manipulated, which could result in losses for other users. This is because the quote of tokens is used in critical parts of the protocol such as withdrawal, borrowing, repayment, and liquidation. Additionally, in some transactions, there are multiple swaps involved, which can further complicate the issue. The report provides a proof of concept that demonstrates how an attacker could manipulate the price of a token in their favor and cause losses to other users. To prevent this, the report recommends using Chainlink oracles to get the price of assets instead of relying on the quoter.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** High

**Description**

The protocol uses the Uniswap V3 quoter contract to get the current value of the supported tokens in terms of the base token (USDC). The values returned by the quoter are the result of a simulated swap, given the current state of the pools. This means that these values can be easily manipulated, for example, by using a flash loan to add liquidity and remove it after interacting with the protocol.

The quote of tokens is used in the most critical parts of the protocol, such as withdrawal, borrowing, repayment, and liquidation. This means that an attacker could manipulate current the price of a token in their favor and cause losses to other users.

Additionally, in some transactions, there are multiple swaps involved. This means that the result of a swap can cause a change in the pool that will affect the next swap, and this is not taken into account in the quote process.

**Proof of concept**

```solidity
function test_priceManipulation() public {
    provideInitialLiquidity();

    vm.startPrank(alice);
    // Provide 1 WETH = 4_000 USDC
    marginTrading.provideERC20(marginAccountID[alice], address(WETH), 1e18);

    // Simulate price manipulation (2x WETH price in USDC)
    quoter.setSwapPrice(address(WETH), address(USDC), 8_000e6);

    // Borrow 7_000 USDC
    marginTrading.borrow(marginAccountID[alice], address(USDC), 7_000e6);

    // Withdraw 7_000 USDC
    marginTrading.withdrawERC20(marginAccountID[alice], address(USDC), 7_000e6);
    vm.stopPrank();

    // Simulate price manipulation recovery
    quoter.setSwapPrice(address(WETH), address(USDC), 4_000e6);

    // Alice got 3_000 USDC profit and left her position with bad debt
    uint256 accountRatio = marginTrading.getMarginAccountRatio(marginAccountID[alice]);
    assert(accountRatio < 0.6e5);
}
```

**Recommendations**

Use Chainlink oracles to get the price of the assets.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Sharwafinance |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/SharwaFinance-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

