---
# Core Classification
protocol: Illuminate
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25282
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-illuminate
source_link: https://code4rena.com/reports/2022-06-illuminate
github_link: https://github.com/code-423n4/2022-06-illuminate-findings/issues/347

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-14] `Redeemer.sol#redeem()` can be called by anyone before maturity, which may lead to loss of user funds

### Overview


A bug has been reported in the Illuminate contract's `redeem()` function, which is a public function. This bug could potentially cause fund loss to stakeholders of the protocol as anyone can call this function before maturity, and force the protocol to sell its holdings at a discounted price. To prevent this, it is recommended to only allow unauthenticated calls after maturity. This bug has been confirmed by JTraversa (Illuminate).

### Original Finding Content

_Submitted by WatchPug, also found by csanuragjain, datapunk, and Lambda_

```solidity
function redeem(
    uint8 p,
    address u,
    uint256 m
) public returns (bool) {
    // Get the principal token that is being redeemed by the user
    address principal = IMarketPlace(marketPlace).markets(u, m, p);

    // Make sure we have the correct principal
    if (
        p != uint8(MarketPlace.Principals.Swivel) &&
        p != uint8(MarketPlace.Principals.Element) &&
        p != uint8(MarketPlace.Principals.Yield) &&
        p != uint8(MarketPlace.Principals.Notional)
    ) {
        revert Invalid('principal');
    }

    // The amount redeemed should be the balance of the principal token held by the Illuminate contract
    uint256 amount = IERC20(principal).balanceOf(lender);

    // Transfer the principal token from the lender contract to here
    Safe.transferFrom(IERC20(principal), lender, address(this), amount);

    if (p == uint8(MarketPlace.Principals.Swivel)) {
        // Redeems zc tokens to the sender's address
        ISwivel(swivelAddr).redeemZcToken(u, m, amount);
    } else if (p == uint8(MarketPlace.Principals.Element)) {
        // Redeems principal tokens from element
        IElementToken(principal).withdrawPrincipal(amount, marketPlace);
    } else if (p == uint8(MarketPlace.Principals.Yield)) {
        // Redeems prinicipal tokens from yield
        IYieldToken(principal).redeem(address(this), address(this), amount);
    } else if (p == uint8(MarketPlace.Principals.Notional)) {
        // Redeems the principal token from notional
        amount = INotional(principal).maxRedeem(address(this));
    }

    emit Redeem(p, u, m, amount);
    return true;
}
```

There are some protocols (eg Notional) that allows redeem before maturity, when doing so, they will  actually make a market sell, usually means a discounted sale.

Since `redeem()` is a public function, anyone can call it before maturity, and force the whole protocol to sell it's holdings at a discounted price, causing fund loss to the stake holders.

<https://github.com/notional-finance/wrapped-fcash/blob/8f76be58dda648ea58eef863432c14c940e13900/contracts/wfCashERC4626.sol#L155-L169>

```solidity
function previewRedeem(uint256 shares) public view override returns (uint256 assets) {
    if (hasMatured()) {
        assets = convertToAssets(shares);
    } else {
        // If withdrawing non-matured assets, we sell them on the market (i.e. borrow)
        (uint16 currencyId, uint40 maturity) = getDecodedID();
        (assets, /* */, /* */, /* */) = NotionalV2.getPrincipalFromfCashBorrow(
            currencyId,
            shares,
            maturity,
            0,
            block.timestamp
        );
    }
}
```

#### Recommendation

Consider only allow unauthenticated call after maturity.

**[JTraversa (Illuminate) confirmed](https://github.com/code-423n4/2022-06-illuminate-findings/issues/347)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Illuminate |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-illuminate
- **GitHub**: https://github.com/code-423n4/2022-06-illuminate-findings/issues/347
- **Contest**: https://code4rena.com/reports/2022-06-illuminate

### Keywords for Search

`vulnerability`

