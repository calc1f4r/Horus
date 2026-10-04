---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25842
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/134

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

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - ladboy233
---

## Vulnerability Title

[M-26] CollateralToken should allow to execute token owner's action to approved addresses

### Overview


This bug report is about the code in the Astaria project's VaultImplementation and CollateralToken smart contracts. In the VaultImplementation contract, the code needs to be updated to check if the `msg.sender` is the same as the operator in order to make the check complete. In the CollateralToken contract, functions flashAction and releaseToAddress are restricted to the owner of the token only, but should be allowed for approved addresses as well.

The recommended mitigation steps are to add the ability for approved operators to call functions that can be called by the collateral token owner. This was confirmed by SantiagoGregory (Astaria).

### Original Finding Content


<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/CollateralToken.sol#L274><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/CollateralToken.sol#L266><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/VaultImplementation.sol#L238>

Let us look into the code below in `VaultImplementation#_validateCommitment`

```solidity
function _validateCommitment(
IAstariaRouter.Commitment calldata params,
address receiver
) internal view {
uint256 collateralId = params.tokenContract.computeId(params.tokenId);
ERC721 CT = ERC721(address(COLLATERAL_TOKEN()));
address holder = CT.ownerOf(collateralId);
address operator = CT.getApproved(collateralId);
if (
  msg.sender != holder &&
  receiver != holder &&
  receiver != operator &&
  !CT.isApprovedForAll(holder, msg.sender)
) {
  revert InvalidRequest(InvalidRequestReason.NO_AUTHORITY);
}
```

the code check should also check that `msg.sender != operator` to make the check complete, if the msg.sender comes from an approved operator, the call should be valid.

```solidity
if (
  msg.sender != holder &&
  receiver != holder &&
  receiver != operator &&
  msg.sender != operator &&
  !CT.isApprovedForAll(holder, msg.sender)
) {
  revert InvalidRequest(InvalidRequestReason.NO_AUTHORITY);
}
```

AND

CollateralToken functions flashAction, releaseToAddress are restricted to the owner of token only. But they should be allowed for approved addresses as well.

For example, in flashAuction, only the owner of the collateral token can start the flashAction, then approved operator by owner cannot start flashAction.

```solidity
  function flashAction(
    IFlashAction receiver,
    uint256 collateralId,
    bytes calldata data
  ) external onlyOwner(collateralId) {
```

Note the check onlyOwner(collateralId) does not check if the msg.sender is an approved operator.

```solidity
modifier onlyOwner(uint256 collateralId) {
	require(ownerOf(collateralId) == msg.sender);
	_;
}
```

### Recommended Mitigation Steps

Add ability for approved operators to call functions that can be called by the collateral token owner.

**[SantiagoGregory (Astaria) confirmed](https://github.com/code-423n4/2023-01-astaria-findings/issues/134)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | ladboy233 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/134
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

