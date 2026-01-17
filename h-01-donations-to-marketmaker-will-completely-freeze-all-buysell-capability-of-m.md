---
# Core Classification
protocol: Ubet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55687
audit_firm: 0x52
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-12-06-Ubet.md
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
  - @IAm0x52
---

## Vulnerability Title

[H-01] Donations to MarketMaker will completely freeze all buy/sell capability of market

### Overview


The bug report highlights an issue in the code of the MarketMaker contract. In the function `getTargetBalance`, an assert statement is used to ensure that all underlying tokens are either split or returned to the parent funding pool. However, this can be exploited by donating a single wei of underlying token, causing the function to revert and breaking the buy/sell capability of the pool. The report recommends removing the assert statement and the issue has been fixed in a recent commit.

### Original Finding Content

**Details**

[MarketMaker.sol#L672-L679](https://github.com/SportsFI-UBet/ubet-contracts-v1/blob/64157824f67d6000588ae4235a49ccd24dede5c3/contracts/markets/MarketMaker.sol#L672-L679)

    function getTargetBalance()
        public
        view
        returns (AmmMath.TargetContext memory targetContext, uint256[] memory fairPriceDecimals)
    {
        // The logic is such that any excess collateral is always returned to the parent
        uint256 localReserves = reserves();
        assert(localReserves == 0);

Inside `getTargetBalance`, an assert statement is used to make sure that all underlying tokens are either split to provide liquidity or returned back to the parent funding pool. While this is true in normal operations, this can be easily DOS'd by donating a single wei of underlying token.

[MarketMaker.sol#L354-L373](https://github.com/SportsFI-UBet/ubet-contracts-v1/blob/64157824f67d6000588ae4235a49ccd24dede5c3/contracts/markets/MarketMaker.sol#L354-L373)

    function buyFor(
        ...
    ) public returns (uint256 outcomeTokensBought, uint256 feeAmount, uint256[] memory spontaneousPrices) {
        if (isHalted()) revert MarketHalted();
        if (investmentAmount < minInvestment) revert InvalidInvestmentAmount();

        uint256 tokensToMint;
        uint256 refundIndex;
        AmmMath.ParentOperations memory parentOps;
        {
            (AmmMath.TargetContext memory targetContext, uint256[] memory fairPriceDecimals) = getTargetBalance();
            refundIndex = AmmMath.getRefundIndex(targetContext);
            (outcomeTokensBought, tokensToMint, feeAmount, spontaneousPrices, parentOps) =
                _calcBuyAmount(investmentAmount, outcomeIndex, extraFeeDecimal, targetContext, fairPriceDecimals);
        }

As seen above `buyFor` calls `getTargetBalance`. After donation, this will revert and cause all buy/sell capability to be broken, rendering the pool mostly useless.

This could be used under a variety of circumstances such as trying to force refunds to certain markets or block other users from buying or selling their choice.

**Lines of Code**

[MarketMaker.sol#L672-L700](https://github.com/SportsFI-UBet/ubet-contracts-v1/blob/64157824f67d6000588ae4235a49ccd24dede5c3/contracts/markets/MarketMaker.sol#L672-L700)

**Recommendation**

Remove the assert statement

**Remediation**

Fixed as recommended in commit [ed00ebf](https://github.com/SportsFI-UBet/ubet-contracts-v1/commit/ed00ebff8d981ebde33de9775e080c6be8b1e94f).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | 0x52 |
| Protocol | Ubet |
| Report Date | N/A |
| Finders | @IAm0x52 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-12-06-Ubet.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

