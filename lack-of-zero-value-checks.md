---
# Core Classification
protocol: Bunni v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57129
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-01-bacon-labs-bunniv2-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-01-bacon-labs-bunniv2-securityreview.pdf
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
finders_count: 3
finders:
  - Priyanka Bose
  - Elvis Skoždopolj
  - Michael Colburn
---

## Vulnerability Title

Lack of zero-value checks

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: Low

## Type: Data Validation

## Description
Certain functions fail to validate incoming arguments, so callers of these functions could mistakenly set important state variables to a zero value, misconfiguring the system. For example, the constructor in the BunniHub contract sets the `poolManager`, `weth`, and `bunniTokenImplementation` variables, which store the addresses of external contracts Bunni v2 relies on:

```solidity
constructor(
    IPoolManager poolManager_,
    WETH weth_,
    IPermit2 permit2_,
    IBunniToken bunniTokenImplementation_,
    address initialOwner
) Permit2Enabled(permit2_) {
    poolManager = poolManager_;
    weth = weth_;
    bunniTokenImplementation = bunniTokenImplementation_;
    _initializeOwner(initialOwner);
}
```
*Figure 12.1: The constructor of the BunniHub contract (src/BunniHub.sol#L75–L86)*

If `weth` is set to a zero value, this deployment of the Bunni v2 protocol would be unable to handle native ether. Since all of the variables mentioned above are tagged as immutable, the contract will have to be redeployed to update to the correct address. This misconfiguration may not be noticed immediately, and forcing LPs to migrate would create a poor user experience.

The following functions are missing zero-value checks:
- BunniHook.constructor
- The `inputAmount` returned by the call to `BunniSwapMath.computeSwap` in `BunnyHookLogic.beforeSwap` for an `exactOut` swap

## Recommendations
- **Short term**: Add zero-value checks to all function arguments to ensure that callers cannot set incorrect values, misconfiguring the system.
- **Long term**: Use the Slither static analyzer to catch common issues such as this one. Consider integrating a Slither scan into the project’s CI pipeline, pre-commit hooks, or build scripts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Bunni v2 |
| Report Date | N/A |
| Finders | Priyanka Bose, Elvis Skoždopolj, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-01-bacon-labs-bunniv2-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-01-bacon-labs-bunniv2-securityreview.pdf

### Keywords for Search

`vulnerability`

