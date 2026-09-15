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
solodit_id: 41407
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

[M-11] LayerZero channel for deployments can be blocked due to reverts

### Overview


The report describes a bug in the `LayerZeroDeployer` contract that can cause the whole channel to be blocked, preventing future DAO deployments. This happens because the contract uses LayerZero v1, which has a blocking nature by default, and its receiver function doesn't implement a non-blocking pattern. This means that if there is a revert during the cross-chain execution, the whole channel will be blocked until the protocol admin unlocks it. The bug can be exploited by an adversary by passing a large array of `_admins` to the cross-chain transaction, causing it to revert with an "Out of Gas" error. This is because the gas is limited to `2_000_000` on the destination chain, while the adversary can send any amount of gas on the source chain. To fix this, it is recommended to validate the size of the `_admins` array on the source chain and to implement a non-blocking pattern for cross-chain deployments.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `LayerZeroDeployer` contract uses LayerZero v1, which has a blocking nature by default, and its receiver function doesn't implement a non-blocking pattern. Any revert during the cross-chain execution will block the whole channel, preventing future DAO deployments, until the protocol admin unlocks it via `forceResume()`.

The cross-chain calls `createCrossChainERC20DAO()` and `createCrossChainERC721DAO()` should not revert in theory, but an adversary can craft a transaction that will pass validations and succeed on the source chain, but not on the destination chain.

One way to do so is by passing a large array of `_admins` to the cross-chain transaction. At some point, the function will revert with an "Out of Gas" error given the loop size:

```solidity
address _safe = IDeployer(deployer).deploySAFE(_admins, _safeThreshold, _daoAddress);

for (uint256 i; i < _admins.length;) {
    IEmitter(emitterAddress).newUserCC(
        _daoAddress, _admins[i], _depositTokenAddress, 0, block.timestamp, 0, true
    );

    unchecked {
        ++i;
    }
}
```

In the source chain, the adversary can send any amount of gas they want, so the transaction can succeed even with a reasonably big number of `_admins`. The problem is in the destination chain as the gas is limited to `2_000_000`:

```solidity
    endpoint.send{value: msg.value}(
        uint16(_dstChainId),
        abi.encodePacked(dstCommLayer[uint16(_dstChainId)], address(this)),
        _payload,
        payable(_refundAd),
        address(0x0),
@>      abi.encodePacked(uint16(1), uint256(2_000_000))
    );
```

So, it is possible to make a transaction run successfully on the source chain and revert to the destination chain, blocking all subsequent cross-chain transactions given LayerZero v1 default behavior.

## Recommendations

Validate that the `_admins` array is below the max limit on the source chain when calling `createERC20DAO()` and `createERC721DAO()`. Also, consider applying a non-blocking pattern to the cross-chain deployments.

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

