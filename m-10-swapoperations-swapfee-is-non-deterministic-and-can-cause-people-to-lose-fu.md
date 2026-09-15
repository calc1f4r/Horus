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
solodit_id: 53850
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

[M-10] `SwapOperations` `swapFee` is non deterministic and can cause people to lose funds

### Overview


The SwapOperations feature of the SwapPair contract charges a fee for transactions based on the spot ratio of the reserves. However, this can lead to unexpected fees if the reserves are altered between when a user signs their transaction and when it is included in a block. This could potentially allow malicious users to manipulate the fees for their own gain. To mitigate this issue, an additional check should be added to ensure that fees are within an acceptable range.

### Original Finding Content

**Impact**

SwapOperations charges a fee that is computed by `SwapPair` as follows:

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/SwapPair.sol#L187-L209

```solidity
  function getSwapFee(uint postReserve0, uint postReserve1) public view override returns (uint feePercentage) {
    address nonStableCoin = token1; // find stable coin
    if (tokenManager.isDebtToken(nonStableCoin) && totalSupply > 0) {
      // query prices
      (uint oraclePrice, ) = priceFeed.getPrice(nonStableCoin); /// @audit not validated for staleness
      uint preDexPrice = _getDexPrice(reserve0, reserve1); /// @audit this is spot and can be altered in some way
      uint postDexPrice = _getDexPrice(postReserve0, postReserve1);

      // only apply the dynamic fee if the swap trades against the oracle peg
      if ( /// @audit ??? | No deviation threshold | Spot vs Oracle (Donate to reserves?)
        (postDexPrice > oraclePrice && postDexPrice > preDexPrice) ||
        (postDexPrice < oraclePrice && preDexPrice > postDexPrice)
      ) {
        uint avgDexPrice = (preDexPrice + postDexPrice) / 2;
        uint priceRatio = (oraclePrice * DECIMAL_PRECISION) / avgDexPrice; // 1e18
        return
          _calcFee(priceRatio > DECIMAL_PRECISION ? priceRatio - DECIMAL_PRECISION : DECIMAL_PRECISION - priceRatio) +
          swapOperations.getSwapBaseFee();
      }
    }

    return swapOperations.getSwapBaseFee();
  }
```

The fee uses the previous "spot ratio" and compares it against the new pre-fee "spot ratio"

This means that any transaction that alters the reserves between when a user signs their transaction and when it get's included in a block may alter the fee that a user pays

This creates scenario where, if a minority of users owns the majority of the LP tokens, they can perform donations to front-run swaps, which will cause benign users to pay an additional fee that they didn't intend to pay

**Mitigation**

Add an explicit check for the fees that will be paid on a swap as to ensure that's intended or within an acceptable range

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

