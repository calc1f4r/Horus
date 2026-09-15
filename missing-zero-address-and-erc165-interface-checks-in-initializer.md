---
# Core Classification
protocol: WeightedLiquidityPool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52429
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/dexodus/weightedliquiditypool
source_link: https://www.halborn.com/audits/dexodus/weightedliquiditypool
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
  - Halborn
---

## Vulnerability Title

Missing Zero Address and ERC165 Interface Checks in Initializer

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `initialize` function does not perform zero address validation or check for ERC165 interface compliance for the provided contract addresses (`_usdc`, `_weth`, `_uniswapRouter`, `_priceFeed`). This omission can lead to the initialization of the contract with invalid or misconfigured dependencies, potentially causing unexpected behavior or failure during runtime.

##### BVSS

[AO:S/AC:L/AX:L/C:N/I:H/A:N/D:N/Y:N/R:N/S:U (1.5)](/bvss?q=AO:S/AC:L/AX:L/C:N/I:H/A:N/D:N/Y:N/R:N/S:U)

##### Recommendation

In the `initialize` function, implement checks to ensure that the provided addresses are non-zero and validate the compliance of contracts (e.g., `IERC165` support) when applicable. For example:

* Check if each address is non-zero, using `require(address != address(0), "Invalid address")`.
* Validate that contracts implementing interfaces support required functions using `IERC165.supportsInterface`.

Adding these validations during initialization will enhance the robustness of the contract and prevent potential misconfigurations.

##### Remediation

**SOLVED**: The code now checks for 0 address.

##### Remediation Hash

1f89558c1394d2c6a59238172e3e17ed50e32265

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | WeightedLiquidityPool |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/dexodus/weightedliquiditypool
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/dexodus/weightedliquiditypool

### Keywords for Search

`vulnerability`

