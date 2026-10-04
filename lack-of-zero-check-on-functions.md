---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17885
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

Lack of zero check on functions

### Overview

See description below for full details.

### Original Finding Content

## Data Validation

**Type:** Data Validation  
**Target:** contracts/Curve/veFXS.vy, CurveAMO_V3.sol  

**Difficulty:** High  

## Description
Certain setter functions fail to validate incoming arguments, so callers can accidentally set important state variables to the zero address. For example, FXS’ `setOwner` function sets the owner address meant to interact with tokens to calculate values:

```solidity
function setOwner(address _owner_address) external onlyByOwnerOrGovernance {
    owner_address = _owner_address;
}
```
*Figure 5.1: FXS/FXS.sol#L115-L117*

Immediately after this address has been set to `address(0)`, the admin must reset the value; failure to do so may result in unexpected contract behavior. This issue is also present in the following contracts:

- **FraxPool.sol**
  - constructor - `_frax_contract_address`, `_fxs_contract_address`, `_collateral_address`, `_creator_address`, `_timelock_address`
  - `setCollatETHOracle` - `_collateral_weth_oracle_address`, `_weth_address`
  - `setTimelock` - `new_timelock`
  - `setOwner` - `_owner_address`
  
- **Frax.sol**
  - constructor - `_creator_address`, `_timelock_address`
  - `setOwner` - `_owner_address`
  - `setFXSAddress` - `_fxsAddress`
  - `setETHUSDOracle` - `_eth_usd_consumer_address`
  - `setTimelock` - `new_timelock`
  - `setController` - `_controller_address`
  - `setPriceBand` - `_price_band`
  - `setFXSEthOracle` - `_fxs_oracle_addr`, `_weth_address`
  - `setFRAXEthOracle` - `_frax_oracle_addr`, `_weth_address`
  
- **FXS.sol**
  - constructor - `_owner_address`, `_oracle_address`, `_timelock_address`
  - `setOwner` - `_owner_address`
  - `setOracle` - `new_oracle`
  - `setTimelock` - `new_timelock`
  - `setFRAXAddress` - `frax_contract_address`
  
- **Pool_USDC.sol**
  - constructor - `_frax_contract_address`, `_fxs_contract_address`, `_collateral_address`, `_creator_address`, `_timelock_address`, `_pool_ceiling`

## Exploit Scenario
Alice sets up a multisig that she wants to set as the new address. When she invokes `setOwner` to replace the address, she accidentally enters the zero address. As a result, only a governance process will be able to reset the address, if it can be reset at all.

## Recommendations
**Short term:** Add zero-value checks to the functions mentioned above to ensure users cannot accidentally set incorrect values, misconfiguring the system.  
**Long term:** Add checks to ensure that user-supplied arguments are not set to `address(0)`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels, Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf

### Keywords for Search

`vulnerability`

