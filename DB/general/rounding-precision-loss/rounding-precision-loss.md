---
vulnerability_class: rounding-precision-loss
title: "Rounding and Precision Loss Vulnerabilities"
category: Mathematical Operations
severity_range: "LOW to HIGH"

    protocol: "Virtuals Protocol"
    severity: "MEDIUM"
    auditor: "Code4rena"
  - file: "reports/yield_protocol_findings/funds-allocated-for-rewards-can-be-locked-in-the-contract.md"
    protocol: "Subscription Token - Fabric"
    severity: "HIGH"
    auditor: "Quantstamp"
  - file: "reports/yield_protocol_findings/m-13-first-erc4626-deposit-can-break-share-calculation.md"
    protocol: "ERC4626 Vault"
    severity: "MEDIUM"
    auditor: "Various"

# Pattern Identity (Required)
root_cause_family: rounding_error
pattern_key: rounding_error | unknown | unknown

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - _convertToShares
  - calculateLiquidity
  - convertToAssets
  - convertToShares
  - deposit
  - launchFor
  - previewMint
  - receive
  - rounding
  - slash
  - totalSupply
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [Virtuals Protocol] | reports/yield_protocol_findings/m-26-imprecise-calculations-in-launchfor-lead-to-less-liquidity-be-added-to-the-.md | MEDIUM | Code4rena | - |
| [Subscription Token - Fabric] | reports/yield_protocol_findings/funds-allocated-for-rewards-can-be-locked-in-the-contract.md | HIGH | Quantstamp | - |
| [ERC4626 Vault] | reports/yield_protocol_findings/m-13-first-erc4626-deposit-can-break-share-calculation.md | MEDIUM | Various | - |


# Rounding and Precision Loss Vulnerabilities

## Overview

Rounding and precision loss vulnerabilities occur when integer arithmetic in Solidity (which lacks native floating-point support) causes unexpected truncation of values, loss of precision in calculations, or accumulation of rounding errors. These issues commonly lead to fund loss, incorrect share calculations, locked funds, or unfair distribution of rewards.

**Root Cause Statement**: This vulnerability exists because Solidity integer division rounds down (truncates) and division before multiplication amplifies precision loss, allowing attackers to exploit rounding to extract value or causing users to lose funds through accumulated truncation errors.

**Observed Frequency**: Very common pattern (20+ reports analyzed)
**Consensus Severity**: LOW to HIGH (depending on exploitability and fund impact)

---



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of rounding_error"
- Pattern key: `rounding_error | unknown | unknown`
- Interaction scope: `single_contract`
- Primary affected component(s): `unknown`
- High-signal code keywords: `_convertToShares`, `calculateLiquidity`, `convertToAssets`, `convertToShares`, `deposit`, `launchFor`, `previewMint`, `receive`
- Typical sink / impact: `fund_loss`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Division before multiplication truncates intermediate result
- Signal 2: Reward/share calculation uses insufficient decimal precision
- Signal 3: Rounding direction favors attacker during mint/redeem operations
- Signal 4: Fee calculation rounds to zero for small amounts enabling free operations

#### False Positive Guards

- Not this bug when: Multiplication performed before division to preserve precision
- Safe if: Scaling factor (1e18, 1e27) applied before division operations
- Requires attacker control of: specific conditions per pattern

## Vulnerable Code Patterns

### Example 1: Division Before Multiplication (MEDIUM - Virtuals Protocol)

**Reference**: m-26-imprecise-calculations-in-launchfor-lead-to-less-liquidity-be-added-to-the-.md

    // VULNERABLE: Division before multiplication causes up to 25% precision loss
    function launchFor(...) public returns (address, address, uint) {
        uint256 k = ((K * 10000) / assetRate);  // First division
        uint256 liquidity = (((k * 10000 ether) / supply) * 1 ether) / 10000;
        // Hidden division before multiplication loses precision
    }
    
    // Test case: assetRate=7.98e15, supply=1.9283e18
    // Current: 1555700000000000000
    // Actual:  1949592125831354822
    // Error:   ~25% precision loss!

**Fix**: Multiply before dividing:

    uint256 liquidity = (K * 10000 * 10000 ether * 1 ether) / (assetRate * supply * 10000);

### Example 2: Rounding Causes Locked Funds (HIGH - Fabric)

**Reference**: funds-allocated-for-rewards-can-be-locked-in-the-contract.md

    // VULNERABLE: Rounding in slashing causes locked funds
    uint256 slashed = (sub.rewardPoints * bps) / _MAX_BIPS;
    // If rewardPoints=50 and bps=100, slashed = 0 (rounds to zero)
    
    uint256 slashedValue = (sub.rewardsWithdrawn * bps) / _MAX_BIPS;
    // Similar issue - can result in 0 even when values are non-zero

**Impact**: 
- Points slashed but value not updated (or vice versa)
- Rewards incorrectly distributed
- Funds permanently locked in contract

### Example 3: Share Calculation Rounding (MEDIUM - ERC4626)

**Reference**: m-13-first-erc4626-deposit-can-break-share-calculation.md

    // VULNERABLE: Rounding down in share calculation
    function convertToShares(uint256 assets) public view returns (uint256) {
        uint256 supply = totalSupply();
        return supply == 0 ? assets : assets.mulDivDown(supply, totalAssets());
        // Rounds DOWN - depositor can receive 0 shares and lose funds
    }

**Attack Scenario**:
1. First depositor deposits 1 wei, gets 1 share
2. Attacker donates 1e18 tokens directly to vault
3. Share price now 1:1e18
4. Next depositor deposits 0.9e18, receives 0 shares (rounds down)
5. Depositor loses all funds

---

## Secure Implementation Patterns

### Fix 1: Multiply Before Divide

    // SECURE: Perform all multiplications before divisions
    // Bad:  (a / b) * c
    // Good: (a * c) / b
    
    uint256 result = (numerator1 * numerator2 * numerator3) / (denominator1 * denominator2);

### Fix 2: Use High-Precision Libraries

    // SECURE: Use PRBMath or similar fixed-point libraries
    import {UD60x18, ud} from "@prb/math/UD60x18.sol";
    
    function calculateLiquidity(uint256 k, uint256 supply) public pure returns (uint256) {
        UD60x18 kFixed = ud(k);
        UD60x18 supplyFixed = ud(supply);
        return kFixed.mul(ud(10000 ether)).div(supplyFixed).unwrap();
    }

### Fix 3: Check for Zero Results

    // SECURE: Revert if calculation rounds to zero when it shouldn't
    function slash(uint256 rewardPoints, uint256 bps) internal {
        uint256 slashed = (rewardPoints * bps) / _MAX_BIPS;
        require(slashed > 0 || rewardPoints == 0, "Rounding to zero");
        // ... rest of logic
    }

### Fix 4: Round Up When Appropriate

    // SECURE: Round up for amounts user pays, round down for amounts user receives
    function convertToShares(uint256 assets) public view returns (uint256) {
        // Round DOWN when user receives shares (favors protocol)
        return assets.mulDivDown(supply, totalAssets());
    }
    
    function convertToAssets(uint256 shares) public view returns (uint256) {
        // Round DOWN when user receives assets (favors protocol)
        return shares.mulDivDown(totalAssets(), supply);
    }
    
    function previewMint(uint256 shares) public view returns (uint256) {
        // Round UP when calculating what user must pay
        return shares.mulDivUp(totalAssets(), supply);
    }

### Fix 5: Virtual Shares/Offset (ERC4626)

    // SECURE: Use virtual shares to prevent rounding manipulation
    function _convertToShares(uint256 assets) internal view returns (uint256) {
        uint256 supply = totalSupply() + VIRTUAL_SHARES;  // e.g., 1e3
        uint256 totalAssets = _totalAssets() + VIRTUAL_ASSETS;
        return assets.mulDivDown(supply, totalAssets);
    }

---

## Impact Analysis

| Scenario | Frequency | Severity |
|----------|-----------|----------|
| Division before multiplication | Very Common | MEDIUM |
| Share calculation rounding | Very Common | MEDIUM-HIGH |
| Reward distribution rounding | Common | HIGH |
| Zero result from rounding | Common | MEDIUM |
| Accumulated rounding errors | Moderate | MEDIUM |

### Business Impact
- **Fund Loss**: Users receive fewer tokens/shares than entitled
- **Locked Funds**: Rewards or tokens permanently stuck in contract
- **Unfair Distribution**: Some users gain at expense of others
- **First Depositor Attack**: Vault inflation via rounding exploitation

---

## Detection Checklist

- [ ] All divisions performed AFTER multiplications
- [ ] Calculations checked for potential zero results
- [ ] Rounding direction appropriate for context (favor protocol vs user)
- [ ] ERC4626 vaults use virtual shares or dead shares
- [ ] High-precision math library used for complex calculations
- [ ] Minimum deposit/share amounts enforced

---

## Real-World Examples

| Protocol | Vulnerability | Severity | Auditor |
|----------|--------------|----------|---------|
| Virtuals Protocol | Division before multiplication | MEDIUM | Code4rena |
| Fabric | Rounding causes locked funds | HIGH | Quantstamp |
| Multiple ERC4626 | Share calculation rounding | MEDIUM | Various |

---

## Keywords

rounding, precision loss, division, truncation, mulDivDown, mulDivUp, integer division, share calculation, dust, locked funds, PRBMath, fixed-point

### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`Mathematical Operations`, `_convertToShares`, `calculateLiquidity`, `convertToAssets`, `convertToShares`, `deposit`, `launchFor`, `previewMint`, `receive`, `rounding`, `slash`, `totalSupply`
