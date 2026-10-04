---
# Core Classification
protocol: StationX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41411
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-15] Adversary can emit any event that needs the EMITTER role without restrictions

### Overview


The report discusses a bug in the `Emitter` contract that could potentially be exploited by malicious actors. The bug allows DAO proxies to gain access to the `EMITTER` role, which grants them the ability to make calls to the `Emitter` contract and emit deceptive events. This could be used to exploit off-chain logic. The report recommends disabling calls to the `Emitter` contract in the `updateProposalAndExecution()` function for both `ERC20DAO` and `ERC721DAO` to prevent this bug from being exploited.

### Original Finding Content

## Severity

**Impact:** Low

**Likelihood:** High

## Description

The `Emitter` contract has two functions that grant an `EMITTER` role to the DAO proxies. This role is granted to every DAO created via `createERC20DAO()` or `createERC721DAO()` in the factory contract.

```solidity
    function createDaoErc20(..., address _proxy, ...) {
        _grantRole(EMITTER, _proxy);
    }

    function createDaoErc721(..., address _proxy, ...) {
        _grantRole(EMITTER, _proxy);
    }
```

The problem is that the DAOs have a function that allows their Safe to execute a call to any contract with any data:

```solidity
    function updateProposalAndExecution(address _contract, bytes memory _data) external onlyGnosis(factoryAddress, address(this)) {
        (bool success,) = _contract.call(_data);
        require(success);
    }
```

This can be leveraged by an adversary to make calls to the `Emitter` contract to emit deceiving events that may exploit some off-chain logic. Here's an example of the 26 affected functions:

```solidity
    function deposited(address _daoAddress, address _depositor,
        address _depositTokenAddress, uint256 _amount, ...
    ) external onlyRole(EMITTER) {
        emit Deposited(_daoAddress, _depositor, _depositTokenAddress, _amount,
            _timestamp, _ownerFee, _adminShare);
    }
```

## Recommendations

A simple approach would be to disable calls to the `Emitter` contract in `updateProposalAndExecution()` for both `ERC20DAO` and `ERC721DAO`.

```diff
    function updateProposalAndExecution(address _contract, bytes memory _data) external onlyGnosis(factoryAddress, address(this)) {
+       require(_contract != emitterContractAddress);
        (bool success,) = _contract.call(_data);
        require(success);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | StationX |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

