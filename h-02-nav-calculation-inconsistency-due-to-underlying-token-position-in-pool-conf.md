---
# Core Classification
protocol: Panoptic
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62093
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-06-panoptic-hypovault
source_link: https://code4rena.com/reports/2025-06-panoptic-hypovault
github_link: https://code4rena.com/audits/2025-06-panoptic-hypovault/submissions/F-219

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
finders_count: 2
finders:
  - kvar
  - dhank
---

## Vulnerability Title

[H-02] NAV calculation inconsistency due to underlying token position in pool configuration

### Overview


The `computeNAV` function in `PanopticVaultAccountant.sol` has a problem that causes identical vault positions to report different NAV values based on their pool configuration. This is due to inconsistent handling of the vault's underlying token balance when calculating NAV. When pools contain the underlying token, the balance is included in the calculation within the loop, but when pools don't contain the underlying token, the balance is added after the calculation is complete. This can result in different NAV values for economically identical vaults. To fix this issue, the recommended mitigation step is to put the NAV calculation outside of the for loop and apply the `Math.max` function to the final aggregated exposure. This will ensure that the NAV value is calculated correctly for all vaults. 

### Original Finding Content



The `computeNAV` function in `PanopticVaultAccountant.sol` contains a logical flaw that causes identical vault positions to report different NAV values based on their pool configuration. The issue comes from inconsistent handling of the vault’s underlying token balance when calculating nav.

The problem:

1. `When pools contain the underlying token`: The underlying token balance is included in `poolExposure` calculations [code](https://github.com/code-423n4/2025-06-panoptic/blob/8ef6d867a5fb6ffd1a6cc479a2380a611d452b4a/src/accountants/PanopticVaultAccountant.sol# L197-L202) within the loop, and the per-pool `Math.max(poolExposure0 + poolExposure1, 0)` is applied to the combined exposure.

   [PanopticVaultAccountant.sol# L250](https://github.com/code-423n4/2025-06-panoptic/blob/8ef6d867a5fb6ffd1a6cc479a2380a611d452b4a/src/accountants/PanopticVaultAccountant.sol# L250)
2. `When pools don't contain the underlying token`: The underlying token balance is added after all pool calculations are complete and after the `Math.max(_, 0)` protection has already been applied per pool.

   [PanopticVaultAccountant.sol# L254-L258](https://github.com/code-423n4/2025-06-panoptic/blob/8ef6d867a5fb6ffd1a6cc479a2380a611d452b4a/src/accountants/PanopticVaultAccountant.sol# L254-L258)

This creates a scenario where the timing of when underlying token balances are included in the NAV calculation determines whether they can offset negative pool exposures or are lost entirely.
```

// Inside the pool processing loop:
nav += uint256(Math.max(poolExposure0 + poolExposure1, 0)); // Applied per pool

// After loop completion:
if (!skipUnderlying) {
    nav += IERC20Partial(underlyingToken).balanceOf(_vault); // Added to already-processed NAV
}
```

Hence, Vaults with underlying tokens in their pool configuration report lower NAV values than economically identical vaults without such configuration.

Managers while executing `fulfillDeposit()` or `fullfillWithdrawals()`, the txn will execute without any reverts. Otherwise, it would have been underflowed [here](https://github.com/code-423n4/2025-06-panoptic/blob/8ef6d867a5fb6ffd1a6cc479a2380a611d452b4a/src/HypoVault.sol# L522-L524) and the calculated share price will be incorrect putting the protocol and users to risk.

**Example:**

Two vaults with identical economic positions:

* **Pool exposure**: -150 USDC (net losses from options trading)
* **Underlying balance**: +50 USDC (cash reserves)
* **Expected NAV**: max (-150 + 50, 0) = 0 USDC

**Vault A** (underlying token USDC appears in ETH/USDC pool):
```

poolExposure = -150 + 50 = -100 USDC (underlying included)
nav += max(-100, 0) = 0
skipUnderlying = true
Final NAV = 0 USDC  (Correct by coincidence)
```

**Vault B** (underlying token USDC not in ETH/WBTC pool):
```

poolExposure = -150 USDC (underlying not included)
nav += max(-150, 0) = 0
skipUnderlying = false
nav += 50 USDC (underlying added after)
Final NAV = 50 USDC  (Incorrect - should be 0)
```

### Recommended mitigation steps

Put nav calculation outside of the `for loop`.
```

    {
        for loop pools
        ....
    }
    bool skipUnderlying = false;
    for (uint256 i = 0; i < underlyingTokens.length; i++) {
        if (underlyingTokens[i] == underlyingToken) skipUnderlying = true;
    }
    if (!skipUnderlying) {
        totalExposure += int256(IERC20Partial(underlyingToken).balanceOf(_vault));
    }

    // Apply Math.max to final aggregated exposure
    nav = uint256(Math.max(totalExposure, 0));
    
```

    where totalExposure is net poolExposure0 + poolExposure1 for all pools
```

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Panoptic |
| Report Date | N/A |
| Finders | kvar, dhank |

### Source Links

- **Source**: https://code4rena.com/reports/2025-06-panoptic-hypovault
- **GitHub**: https://code4rena.com/audits/2025-06-panoptic-hypovault/submissions/F-219
- **Contest**: https://code4rena.com/reports/2025-06-panoptic-hypovault

### Keywords for Search

`vulnerability`

