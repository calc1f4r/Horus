---
# Core Classification
protocol: Flexa
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17878
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Flexa.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Flexa.pdf
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
finders_count: 2
finders:
  - Robert Tonic
  - Josselin Feist
---

## Vulnerability Title

Missing validations on administration functions

### Overview


This bug report concerns the access controls of the Staking.sol contract. It is classified as a high difficulty issue. The issue is that several administration functions lack proper input validation, which can lead to a misconfigured system or loss of privileged access.

In particular, the setOwner function has no check to ensure the 0x0 address is not provided as the newOwnerAddress parameter. This could lead to an accidental invocation of setOwner with an uninitialized value, resulting in an irrevocable loss of contract ownership.

Additionally, the addWithdrawalRoot and setFallbackRoot functions have the potential to have the root parameter set to 0, and the nonce parameter can potentially be set to 0 as well. The setFallbackWithdrawalDelay function has the potential to have the newFallbackDelaySeconds parameter set to 0.

Exploit Scenario:

Alice deploys the Staking contract. She calls setOwner, but incorrectly sets the owner to zero. As a result, she loses administration access.

Recommendation:

Short term, ensure all inputs are appropriately validated for their zero values, including newOwnerAddress != 0 in setOwner, newFallbackDelaySeconds != 0 in setFallbackWithdrawalDelay, root != 0 in addWithdrawalRoot and setFallbackRoot.

Long term, expand testing to include zero-value tests and ensure validation is appropriate even for unexpected inputs. Document the expected inputs for each function.

### Original Finding Content

## Access Controls

**Target:** Staking.sol

**Diﬃculty:** High

## Description

Staking relies on correct parametrization from the owner. Several administration functions lack proper input validation, which might lead to a misconfigured system or loss of privileged access.

Within the `setOwner` function (Figure 5.1), there is no check to ensure the `0x0` address is not provided as the `newOwnerAddress` parameter. This could lead to an accidental invocation of `setOwner` with an uninitialized value, resulting in an irrevocable loss of contract ownership.

```solidity
function setOwner(address newOwnerAddress) external {
    require(
        msg.sender == _owner,
        "Only the owner can set the new owner"
    );
    address oldValue = _owner;
    _owner = newOwnerAddress;
    emit OwnerUpdate(oldValue, _owner);
}
```
_Figure 5.1: The `setOwner` function definition._

Additional validations are missing within the `addWithdrawalRoot` (Figure 5.2) and `setFallbackRoot` (Figure 5.3) functions, where the `root` parameter could potentially be `0` in both, and the `nonce` can potentially be `0`. In the `setFallbackWithdrawalDelay` function (Figure 5.4), the `newFallbackDelaySeconds` could be `0`.

```solidity
function addWithdrawalRoot(
    bytes32 root,
    uint256 nonce,
    bytes32[] calldata replacedRoots
) external {
    require(
        msg.sender == _owner || msg.sender == _withdrawalPublisher,
        "Only the owner and withdrawal publisher can add and replace withdrawal root hashes"
    );
    require(
        _maxWithdrawalRootNonce + 1 == nonce,
        "Nonce must be exactly max nonce + 1"
    );
    require(
        _withdrawalRootToNonce[root] == 0,
        "Root already exists and is associated with a different nonce"
    );
    _withdrawalRootToNonce[root] = nonce;
    _maxWithdrawalRootNonce = nonce;
    emit WithdrawalRootHashAddition(root, nonce);
    for (uint256 i = 0; i < replacedRoots.length; i++) {
        deleteWithdrawalRoot(replacedRoots[i]);
    }
}
```
_Figure 5.2: The `addWithdrawalRoot` function definition._

```solidity
function setFallbackRoot(bytes32 root, uint256 maxDepositIncluded) external {
    require(
        msg.sender == _owner || msg.sender == _fallbackPublisher,
        "Only the owner and fallback publisher can set the fallback root hash"
    );
    require(
        maxDepositIncluded >= _fallbackMaxDepositIncluded,
        "Max deposit included must remain the same or increase"
    );
    require(
        maxDepositIncluded <= _depositNonce,
        "Cannot invalidate future deposits"
    );
    _fallbackRoot = root;
    _fallbackMaxDepositIncluded = maxDepositIncluded;
    _fallbackSetDate = block.timestamp;
    emit FallbackRootHashSet(
        root,
        _fallbackMaxDepositIncluded,
        block.timestamp
    );
}
```
_Figure 5.3: The `setFallbackRoot` function definition._

```solidity
function setFallbackWithdrawalDelay(uint256 newFallbackDelaySeconds) external {
    require(
        msg.sender == _owner,
        "Only the owner can set the fallback withdrawal delay"
    );
    uint256 oldDelay = _fallbackWithdawalDelaySeconds;
    _fallbackWithdawalDelaySeconds = newFallbackDelaySeconds;
    emit FallbackWithdrawalDelayUpdate(oldDelay, newFallbackDelaySeconds);
}
```
_Figure 5.4: The `setFallbackWithdrawalDelay` function definition._

## Exploit Scenario

- Alice deploys the Staking contract.
- She calls `setOwner`, but incorrectly sets the owner to zero.
- As a result, she loses administration access.

## Recommendation

**Short term:** Ensure all inputs are appropriately validated for their zero values, including:
- `newOwnerAddress != 0` in `setOwner` (Staking.sol#L362-370).
- `newFallbackDelaySeconds != 0` in `setFallbackWithdrawalDelay` (Staking.sol#L442-L451).
- `root != 0` in `addWithdrawalRoot` (Staking.sol#L460-L488) and `setFallbackRoot` (Staking.sol#L517-L540).

**Long term:** Expand testing to include zero-value tests and ensure validation is appropriate even for unexpected inputs. Document the expected inputs for each function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Flexa |
| Report Date | N/A |
| Finders | Robert Tonic, Josselin Feist |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Flexa.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Flexa.pdf

### Keywords for Search

`vulnerability`

