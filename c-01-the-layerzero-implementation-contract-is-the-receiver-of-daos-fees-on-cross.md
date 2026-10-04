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
solodit_id: 41382
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

[C-01] The LayerZero implementation contract is the receiver of DAOs fees on cross-chain buy operations

### Overview


This bug report addresses a problem with creating a cross-chain DAO using `createCrossChainERC20DAO()` or `createCrossChainERC721DAO()`. The issue is that the `msg.sender` is always assigned as the `ownerAddress`, which is actually the LayerZero Deployer contract. This means that the fees for cross-chain buy operations will be sent to the LayerZero Deployer instead of the actual DAO owner. The report recommends allowing the DAO creator to specify an `ownerAddress` for each cross-chain deployment.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

Whenever a cross-chain DAO is created via `createCrossChainERC20DAO()` or `createCrossChainERC721DAO()`, it assigns the `ownerAddress` as the `msg.sender`. The problem is that the `msg.sender` will always be the LayerZero Deployer contract:

```solidity
    function createCrossChainERC20DAO(...) {
@>      require(msg.sender == commLayer, "Caller not LZ Deployer");
        bytes memory _payload = abi.encode(_daoAddress, msg.sender, _numOfTokensToBuy, _tokenURI, _merkleProof);
        ccDetails[_daoAddress] =
            CrossChainDetails(
                _commLayerId,
                _depositChainIds,
                false,
@>              msg.sender,          // @audit ownerAddress
                _onlyAllowWhitelist
            );
    }
```

So, each time a cross-chain buy operation is performed, the fee will be attempted to be sent to the LayerZero Deployer, instead of the DAO owner address:

```solidity
    payable(
        ccDetails[_daoAddress].ownerAddress != address(0)
@>          ? ccDetails[_daoAddress].ownerAddress
            : IERC20DAO(_daoAddress).getERC20DAOdetails().ownerAddress
    ).call{value: ownerShare}("");
```

The fee won't be sent anywhere as the LayerZero Deployer doesn't have a `receive() payable {}` function, and the result from the `call` is not checked. In any case, the DAO owner's address will not receive the corresponding fees.

## Recommendations

Allow the DAO creator to specify an `ownerAddress` for each cross-chain DAO deployment (as they may not have control over the same address on all chains).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

