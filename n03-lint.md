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
solodit_id: 25452
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-09-frax
source_link: https://code4rena.com/reports/2022-09-frax
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
finders_count: 0
finders:
---

## Vulnerability Title

[N‑03] Lint

### Overview

See description below for full details.

### Original Finding Content


Wrong indentation:

```solidity
File: /src/ERC20/ERC20PermitPermissionedMint.sol

From:
30    ERC20(_name, _symbol)
31    ERC20Permit(_name)
32    Owned(_creator_address)
To:
30        ERC20(_name, _symbol)
31        ERC20Permit(_name)
32        Owned(_creator_address)
```

```solidity
File: /src/frxETH.sol

From:
37      address _creator_address,
38      address _timelock_address
To:
37        address _creator_address,
38        address _timelock_address

From:
40    ERC20PermitPermissionedMint(_creator_address, _timelock_address, "Frax Ether", "frxETH")
To:
40        ERC20PermitPermissionedMint(_creator_address, _timelock_address, "Frax Ether", "frxETH")
```

Don't use extra parenthesis:

```solidity
File: /src/sfrxETH.sol

70        return (deposit(assets, receiver));

86        return (mint(shares, receiver));
```

Missed space:

```solidity
File: /src/ERC20/ERC20PermitPermissionedMint.sol

84:56        for (uint i = 0; i < minters_array.length; i++){
```

Remove space:

```solidity
File: /src/ERC20/ERC20PermitPermissionedMint.sol

63 \n
```

```solidity
File: /src/frxETH.sol

34 \n

42 \n
```

```solidity
File: /src/sfrxETH.sol

88 \n
```

```solidity
File: /src/OperatorRegistry.sol

29 \n
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-frax
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-09-frax

### Keywords for Search

`vulnerability`

