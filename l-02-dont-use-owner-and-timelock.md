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
solodit_id: 25449
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

[L-02] Don't use `owner` and `timelock`

### Overview

See description below for full details.

### Original Finding Content


Using a `timelock` contract gives confidence to the user, but when check `onlyByOwnGov` allow the `owner` and the `timelock`
The `owner` manipulates the contract without a lock time period.

### Recommendation

*   Use only `Owned` permission
*   Remove the `timelock_address`
*   The owner should be the `timelock` contract

```solidity
File: /src/frxETH.sol

38      address _timelock_address

40    ERC20PermitPermissionedMint(_creator_address, _timelock_address, "Frax Ether", "frxETH")
```

```solidity
File: /src/ERC20/ERC20PermitPermissionedMint.sol

 16    address public timelock_address;

 26        address _timelock_address,

 34      timelock_address = _timelock_address;

 41        require(msg.sender == timelock_address || msg.sender == owner, "Not owner or timelock");

 94    function setTimelock(address _timelock_address) public onlyByOwnGov {
 95        require(_timelock_address != address(0), "Zero address detected");
 96        timelock_address = _timelock_address;
 97        emit TimelockChanged(_timelock_address);
 98    }

106    event TimelockChanged(address timelock_address);
```

```solidity
File: /src/frxETH.sol

38      address _timelock_address

40    ERC20PermitPermissionedMint(_creator_address, _timelock_address, "Frax Ether", "frxETH")
```

```solidity
File: /src/OperatorRegistry.sol

 38    address public timelock_address;

 40    constructor(address _owner, address _timelock_address, bytes memory _withdrawal_pubkey) Owned(_owner) {
 41        timelock_address = _timelock_address;

 46        require(msg.sender == timelock_address || msg.sender == owner, "Not owner or timelock");

202    function setTimelock(address _timelock_address) external onlyByOwnGov {
203        require(_timelock_address != address(0), "Zero address detected");
204        timelock_address = _timelock_address;
205        emit TimelockChanged(_timelock_address);
206    }

208    event TimelockChanged(address timelock_address);
```

```solidity
File: /src/frxETHMinter.sol

57        address _timelock_address,

59    ) OperatorRegistry(_owner, _timelock_address, _withdrawalCredential) {
```

## Non-Critical Issues

|     | Issue                                                                             | Instances |
| :----: | :-------------------------------------------------------------------------------- | :-------: |
| N‑01 | Unused imports                                                                    |     2     |
| N‑02 | Non-library/interface files should use fixed compiler versions, not floating ones |     6     |
| N‑03 | Lint                                                                              |     11    |
| N‑04 | Event is missing `indexed` fields                                                 |     19    |
| N‑05 | Functions, parameters and variables in snake case                                 |     31    |
| N‑06 | Wrong `event` parameter name                                                      |     2     |
| N‑07 | Simplify `depositWithSignature` function                                          |     1     |
| N‑08 | Missing zero address checks                                                       |     9     |

Total: 81 instances over 8 issues



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

