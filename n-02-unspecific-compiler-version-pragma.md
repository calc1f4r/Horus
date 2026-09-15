---
# Core Classification
protocol: Axelar Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25368
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-07-axelar
source_link: https://code4rena.com/reports/2022-07-axelar
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
  - dexes
  - bridge
  - services
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[N-02] Unspecific Compiler Version Pragma

### Overview

See description below for full details.

### Original Finding Content


Avoid floating pragmas for non-library contracts.

While floating pragmas make sense for libraries to allow them to be included with multiple different versions of applications, it may be a security risk for application implementations.

A known vulnerable compiler version may accidentally be selected or security tools might fall-back to an older compiler version ending up checking a different EVM compilation that is ultimately deployed on the blockchain.

It is recommended to pin to a concrete compiler version.

    IAxelarAuth.sol::3 => pragma solidity ^0.8.9;
    IAxelarAuthWeighted.sol::3 => pragma solidity ^0.8.9;
    IAxelarDepositService.sol::3 => pragma solidity ^0.8.9;
    IAxelarGasService.sol::3 => pragma solidity ^0.8.9;
    IDepositBase.sol::3 => pragma solidity ^0.8.9;

**[re1ro (Axelar) acknowledged and commented](https://github.com/code-423n4/2022-07-axelar-findings/issues/8#issuecomment-1205893984):**
 > **[L-01]**<br>
> Not applicable. We need `receive` to receive ether from `WETH` contract.
> 
> **[L-02]**<br>
> Not applicable. `axelarToken` is our own implementation in this context and it implements `decimals`
> 
> **[L-03]**<br>
> Nope.
> 
> **[L-04]**<br>
> Yes.
> 
> **[N-01]**<br>
> We allow Unspecific Compiler version for our interfaces, so they can be imported by other projects

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-07-axelar-findings/issues/8#issuecomment-1233585799):**
 > **[L-01] Unused receive() function**<br>
> For the proxy<br>
> Low
> 
> **[L-02] decimals() not part of ERC20 standard**<br>
> Low
> 
> **[L-03] Unsafe use of transfer()/transferFrom() with IERC20**<br>
> Low
> 
> **[L-04] Missing checks for zero address**<br>
> Low
> 
> **[N-01] Use a more recent version of solidity**<br>
> Non-critical
> 
> **[N-02] Unspecific Compiler Version Pragma**<br>
> Non-critical



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Axelar Network |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-axelar
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-07-axelar

### Keywords for Search

`vulnerability`

