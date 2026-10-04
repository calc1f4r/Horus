---
# Core Classification
protocol: Apollon Report
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53843
audit_firm: Recon Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-22-Apollon_Report.md
github_link: none

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
finders_count: 1
finders:
  - Alex The Entreprenerd
---

## Vulnerability Title

[M-03] `RedemptionOperations` allows redemption against stale prices

### Overview


The code for `_calculateTroveRedemption` does not check if the prices of collaterals and debts are up-to-date. This can lead to arbitrage opportunities where someone can receive more collateral than the fair market price by exploiting differences in prices from different sources. To fix this, the team needs to rethink how they check for stale prices to prevent these types of arbitrages.

### Original Finding Content

**Impact**

The code for `_calculateTroveRedemption` doesn't validate that collaterals nor debts prices are not stale

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/RedemptionOperations.sol#L231-L259

```solidity
  function _calculateTroveRedemption(
    PriceCache memory _priceCache,
    address _borrower,
    uint _redeemMaxAmount,
    bool _includePendingRewards
  ) internal view returns (SingleRedemptionVariables memory vars) {
    address stableCoinAddress = address(tokenManager.getStableCoin());

    // stable coin debt should always exists because of the gas comp
    TokenAmount[] memory troveDebt = _includePendingRewards
      ? troveManager.getTroveRepayableDebts(_priceCache, _borrower, true) // with pending rewards
      : troveManager.getTroveDebt(_borrower); // without pending rewards
    if (troveDebt.length == 0) revert InvalidRedemptionHint();
    for (uint i = 0; i < troveDebt.length; i++) {
      TokenAmount memory debtEntry = troveDebt[i];

      if (debtEntry.tokenAddress == stableCoinAddress) vars.stableCoinEntry = debtEntry;
      vars.troveDebtInUSD += priceFeed.getUSDValue(_priceCache, debtEntry.tokenAddress, debtEntry.amount);
    }

    vars.collLots = _includePendingRewards
      ? troveManager.getTroveWithdrawableColls(_borrower)
      : troveManager.getTroveColl(_borrower);
    for (uint i = 0; i < vars.collLots.length; i++) {
      uint p = priceFeed.getUSDValue(_priceCache, vars.collLots[i].tokenAddress, vars.collLots[i].amount);
      vars.troveCollInUSD += p;
      if (!tokenManager.isDebtToken(vars.collLots[i].tokenAddress)) vars.redeemableTroveCollInUSD += p;
    } /// @audit can change the ratio of a trove to have mostly `isDebtToken` debt | How does this relate to collateral?

```

This opens up to arbitrage opportunities where the pyth price may be higher for a certain collateral, while the fallback oracle price is lower, allowing the caller to receive more collateral than what would be the fair market price

**Mitigation**

Rethink oracle price staleness checks to prevent arbitrages

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Recon Audits |
| Protocol | Apollon Report |
| Report Date | N/A |
| Finders | Alex The Entreprenerd |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-22-Apollon_Report.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

