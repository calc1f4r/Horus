---
# Core Classification
protocol: RegnumAurum_2025-08-12
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63412
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/RegnumAurum-security-review_2025-08-12.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-07] Hard-coding Curve `price_oracle` index across chains yields wrong prices

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

The oracle fallback currently assumes a fixed Curve `price_oracle` index for ETH/crvUSD (e.g., calling `price_oracle(0)` and expecting it to be “WETH in crvUSD”).
Across chains and pools, **token ordering differs**, so the same index can reference a different asset, producing **wrong or inverted prices**. This propagates into `crvUSDPriceInUSD`, affecting LTV checks, liquidations, and circuit-breaker logic.

Concrete differences you’ll encounter:

* **TriCrypto/crypto v2** pools: `price_oracle(k)` returns the EMA price of `coin[k+1]` **in units of** `coin[0]`. If `coin[0] = crvUSD`, then:

  * If `coin[1] = WETH` → use **`k = 0`**.
  * If `coin[2] = WETH` → use **`k = 1`**.


Examples of cross-chain differences:

* Ethereum mainnet TriCRV ordered as `crvUSD, WETH, CRV` → **K = 0** (https://www.curve.finance/dex/ethereum/pools/factory-tricrypto-4/deposit).
* Optimism TriCrypto-crvUSD ordered as `crvUSD, WBTC, WETH` → **K = 1** (https://www.curve.finance/dex/optimism/pools/factory-tricrypto-0/deposit).
* Base `crvUSD/tBTC/WETH` ordered as `crvUSD, tBTC, WETH` → **K = 1** (https://www.curve.finance/dex/base/pools/factory-tricrypto-1/deposit).

Because “ETH” means chain-specific **WETH** with a different address per chain, relying on a fixed index is unsafe.

**Recommendations**

Adopt a deploy-time, immutable index K set by the owner.
Add `uint8 public immutable K;` and set it **once at deployment**.

```solidity
    uint8 public immutable K;  // 0 or 1 for TriCrypto (coin[K+1] vs coin[0])

    constructor(address initialOwner, uint8 _k) Ownable(initialOwner) {
        require(_k <= 1, "invalid K"); // TriCrypto supports k in {0,1}
        K = _k;
        fallbackPriceInUSD = 1e18;
        lastFallbackUpdateTimestamp = block.timestamp;
    }

    function _crvUSDPriceInUSDFromCurve() internal view returns (uint256 crvUSDPriceInUSD, uint256 lastUpdateTimestamp, bool success) {
<...>
        uint256 ETHPriceInCrvUSD = curveOracle.price_oracle(K);
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | RegnumAurum_2025-08-12 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/RegnumAurum-security-review_2025-08-12.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

