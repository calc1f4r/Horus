---
# Core Classification
protocol: Aave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19254
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/aave/aave-protocol/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/aave/aave-protocol/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Unused Errors

### Overview

See description below for full details.

### Original Finding Content

## Description

The following is a list of errors which are no longer used but appear as constants in `Errors`.

- `VL_CURRENT_AVAILABLE_LIQUIDITY_NOT_ENOUGH` = '4'
- `VL_DEPOSIT_ALREADY_IN_USE` = '20'
- `LP_NOT_ENOUGH_LIQUIDITY_TO_BORROW` = '24'
- `LP_REQUESTED_AMOUNT_TOO_SMALL` = '25'
- `LP_INCONSISTENT_PROTOCOL_ACTUAL_BALANCE` = '26'
- `LP_INCONSISTENT_FLASHLOAN_PARAMS` = '28'
- `CT_CANNOT_GIVE_ALLOWANCE_TO_HIMSELF` = '30'
- `CT_TRANSFER_AMOUNT_NOT_GT_0` = '31'
- `LPC_INVALID_ATOKEN_POOL_ADDRESS` = '35'
- `LPC_INVALID_STABLE_DEBT_TOKEN_POOL_ADDRESS` = '36'
- `LPC_INVALID_VARIABLE_DEBT_TOKEN_POOL_ADDRESS` = '37'
- `LPC_INVALID_STABLE_DEBT_TOKEN_UNDERLYING_ADDRESS` = '38'
- `LPC_INVALID_VARIABLE_DEBT_TOKEN_UNDERLYING_ADDRESS` = '39'
- `LPC_INVALID_ADDRESSES_PROVIDER_ID` = '40'
- `LP_INVALID_FLASHLOAN_MODE` = '47'
- `LP_FAILED_REPAY_WITH_COLLATERAL` = '57'
- `LP_FAILED_COLLATERAL_SWAP` = '60'
- `LP_INVALID_EQUAL_ASSETS_TO_SWAP` = '61'
- `LP_REENTRANCY_NOT_ALLOWED` = '62'
- `LP_INCONSISTENT_PARAMS_LENGTH` = '74'

## Recommendations

Consider commenting out these errors to save gas costs on deployment and reduce code size.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Aave |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/aave/aave-protocol/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/aave/aave-protocol/review.pdf

### Keywords for Search

`vulnerability`

