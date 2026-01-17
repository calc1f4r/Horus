---
# Core Classification
protocol: DIA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57937
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DIA/Lumina%20Staking/README.md#8-multiple-legacy-and-safety-issues-in-wdia-inherited-from-weth9
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
  - MixBytes
---

## Vulnerability Title

Multiple legacy and safety issues in `WDIA` inherited from WETH9

### Overview

See description below for full details.

### Original Finding Content

##### Description
The `WDIA` contract inherits several known issues from the WETH9 implementation that collectively reduce its safety, clarity, and compatibility with modern standards:

- **Silent fallback behavior**: The fallback function accepts all calls, regardless of calldata. This causes unexpected ETH deposits when non-existent functions are called, a vulnerability observed in prior hacks such as the Multicoin bridge incident.
- **No overflow/underflow protection**: Arithmetic operations in key functions like `deposit()`, `withdraw()`, and `transferFrom()` are vulnerable due to reliance on Solidity versions prior to 0.8.0, which lack built-in overflow checks.
- **Unrestricted compiler version**: The contract uses `pragma solidity >=0.4.23`, allowing compilation with a wide range of versions. This introduces inconsistencies in behavior, optimization, and gas usage.
- **Missing zero address validation**: Transfers using `transfer()` and `transferFrom()` lack checks for zero addresses, risking accidental token burns without warning.
- **Front-running risk in `approve()`**: The `approve()` function directly updates allowances without requiring them to be reset to zero, creating a vulnerability where attackers can drain both old and new allowances during front-running scenarios.
<br/>
##### Recommendation
We recommend modernizing and securing the `WDIA` contract:
1. Adding `require(msg.data.length == 0)` to the fallback function to block unintended calldata-based ETH deposits.
2. Upgrading to Solidity ^0.8.0 or integrate SafeMath to ensure arithmetic safety.
3. Fixing the compiler version (e.g., `pragma solidity 0.4.26`) to maintain predictable compilation behavior.
4. Adding `require(dst != address(0), "Transfer to zero address")` checks in `transfer()` and `transferFrom()`.
5. Modifying `approve()` to follow a two-step pattern or implement `increaseAllowance()` and `decreaseAllowance()` for safer token approvals.

> **Client's Commentary:**
> recommended changes are done

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | DIA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DIA/Lumina%20Staking/README.md#8-multiple-legacy-and-safety-issues-in-wdia-inherited-from-weth9
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

