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
solodit_id: 25457
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

[N-08] Missing zero address checks

### Overview

See description below for full details.

### Original Finding Content


```solidity
File: /src/ERC20/ERC20PermitPermissionedMint.sol

26        address _timelock_address,
```

```solidity
File: /src/sfrxETH.sol

42    constructor(ERC20 _underlying, uint32 _rewardsCycleLength)
```

```solidity
File: /src/frxETHMinter.sol

 53        address depositContractAddress,

 54        address frxETHAddress,

 55        address sfrxETHAddress,

 57        address _timelock_address,

 70    function submitAndDeposit(address recipient) external payable returns (uint256 shares) {

166    function moveWithheldETH(address payable to, uint256 amount) external onlyByOwnGov {
```

```solidity
File: /src/OperatorRegistry.sol

/*_timelock_address parameter*/
40     constructor(address _owner, address _timelock_address, bytes memory _withdrawal_pubkey) Owned(_owner) {
```


***



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

