---
# Core Classification
protocol: Harvestflow
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44083
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/HarvestFlow-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[L-04] Incomplete Validation

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Description

In the `NftFactory.sol` contract the following validation checks are missing:

- `constructor()` missing zero-address check for `_nftImplementation` parameter.

The `InitializationParams` struct input, is the parameter of the `deploy()` function. The following validation checks are missing:

- The `cap`, `price`, `lendingAt`, `yield` and `lendingPeriod` parameters are missing zero-value checks.
- The `payableToken`, `owner` and `signerAddress` parameters are missing zero-address checks.

In the `TokTokNft.sol` contract the following validation checks are missing:

- `withdraw()` function missing zero-address check for `receiver` parameter.
- `withdraw()` function missing zero-value check for `amount` parameter.
- `addBonusToken()` function missing zero-address check for `token` parameter.
- `removeBonusToken()` function missing zero-address check for `token` and `receiver` parameters.
- `claimToken()` function missing zero-address check for `token ` parameter.

## Location of Affected Code

File: [contracts/src/NftFactory.sol](https://github.com/tokyoweb3/HarvestFlow/blob/bfb24f9b9c6fdec935dfc0cb1c99c1285d29daf2/contracts/src/NftFactory.sol)

File: [contracts/src/TokTokNft.sol](https://github.com/tokyoweb3/HarvestFlow/blob/bfb24f9b9c6fdec935dfc0cb1c99c1285d29daf2/contracts/src/TokTokNft.sol)

## Recommendation

Consider implementing the validation checks from above.

## Team Response

Fixed.

## [R-01] Centralization Risks

## Severity

Recommendation

## Description

Currently, the owner privileges in the `TokTokNft` contract pose a significant centralization risk due to the following reasons:

1. The `withdraw()` function permits the contract owner to withdraw the entire balance of funds to any specified address. This capability grants the owner excessive control over the contract's funds, potentially leading to misuse or exploitation.
2. Users might not be able to claim their funds if the contract balance is less than their token for claiming, in this case, their funds will be stuck until the Apas Port team refills the contract.
3. The contract's owner is able to pause the `claim()`, `claimAll()`, `redeem()` and `redeemAll()` functions therefore leaving the users unable to claim/redeem their funds.
4. The contract's owner is solely responsible for providing the accurately denominated amount of a bonus token in the `addBonusToken()` function, in case of a wrong value the calculation might be wrong which could result in loss of funds for a user.

## Location of Affected Code

File: [contracts/src/TokTokNft.sol](https://github.com/tokyoweb3/HarvestFlow/blob/bfb24f9b9c6fdec935dfc0cb1c99c1285d29daf2/contracts/src/TokTokNft.sol)

## Recommendation

Consider implementing a Timelock mechanism. This mechanism introduces a delay between the initiation of an important state-changing request and its execution, providing an opportunity for stakeholders to review and potentially intervene in case of any suspicious or unauthorized withdrawal attempts. Additionally, it is recommended to use a multi-sig or governance as the protocol owner.

## Team Response

N/A

## [I-01] The `preMint()` Method does Not Follow the `Checks-Effects-Interactions` Pattern

## Severity

Informational

## Description

The `preMint()` function in the `TokTokNft.sol` contract does not follow the `Checks-Effects-Interactions` (CEI) pattern.
It is recommended to always first change the state before doing external calls.

Particularly important is the `preMint()` function, as it calls the signer verification (`_verifyAddressSigner()`) after the token transfer. Applying the recommended fix to address one of the other issues involves using `safeTransferFrom()`, which includes a callback. Without adhering to the Checks-Effects-Interactions (CEI) pattern and/or adding the `nonReentrant` modifier, a non-whitelisted user could exploit the function to mint the `cappedMintAmount` without proper authorization.

## Location of Affected Code

File: [contracts/src/TokTokNft.sol#L197](https://github.com/tokyoweb3/HarvestFlow/blob/bfb24f9b9c6fdec935dfc0cb1c99c1285d29daf2/contracts/src/TokTokNft.sol#L197)

```solidity
function preMint(uint256 mintAmount, uint256 maxMintAmount, bytes memory signature)
    public
    whenNotPaused
    returns (uint256)
{
   // code

       payableToken.transferFrom(msg.sender, address(this), cost);
@> whitelistUserMintedCount[msg.sender] += cappedMintAmount;

     // code
}
```

## Recommendation

Consider sticking to the `CEI(Checks-Effects-Interactions)` pattern in `preMint()` function in the following way:

```diff
function preMint(uint256 mintAmount, uint256 maxMintAmount, bytes memory signature)
    public
    whenNotPaused
    returns (uint256)
{
   // code

+     whitelistUserMintedCount[msg.sender] += cappedMintAmount;
       payableToken.transferFrom(msg.sender, address(this), cost);
-     whitelistUserMintedCount[msg.sender] += cappedMintAmount;

     // code
}
```

## Team Response

N/A

## [I-02] Incorrect NatSpec Comment

The tokens intended to be used in `InitializationParams` will be ERC721A, not ERC1155, therefore consider editing the comment.

```solidity
struct InitializationParams {
    /// @param name Name of the ERC1155
    string name;
    /// @param symbol Symbol of the ERC1155
    string symbol;

   // code
}
```

## [I-03] Use `Ownable2StepUpgradeable` instead of `OwnableUpgradeable`

The current ownership transfer process for all the contracts inheriting from Ownable involves the current owner calling the `transferOwnership()` function. If the nominated EOA account is not a valid account, it is entirely possible that the owner may accidentally transfer ownership to an uncontrolled account, losing access to all functions with the `onlyOwner` modifier.

It is recommended to implement a two-step process where the owner nominates an account and the nominated account needs to call an acceptOwnership() function for the transfer of the ownership to fully succeed. This ensures the nominated EOA account is a valid and active account. This can be easily achieved by using OpenZeppelin’s `Ownable2StepUpgradeable` contract instead of `OwnableUpgradeable`.

## [I-04] Missing events

File: TokTokNft.sol

```solidity
function setPresale(bool value) public onlyOwner whenNotPaused {
function setPublicsale(bool value) public onlyOwner whenNotPaused {
function setPresalePrice(uint256 value) public onlyOwner whenNotPaused {
function setPublicPrice(uint256 value) public onlyOwner whenNotPaused {
function setRoyaltyAddress(address _royaltyAddress, uint96 _royaltyFee) public onlyOwner whenNotPaused {
```

File: NftFactory.sol

```solidity
function claimAll(address[] memory nfts, uint256[] memory tokenIds) public {
```

## [I-05] Some Event Parameters Are Not `indexed`

## Description

Some event parameters are not `indexed`. While this does not pose any threat to the code, it makes it cumbersome for the off-chain scripts to efficiently filter them. Making the event parameters `indexed` will improve the off-chain services’ ability to search and filter them.

## Location of Affected Code

File: NftFactory.sol

```solidity
event NftDeployed(address nft);
```

## Recommendation

Consider making up to three of the most important parameters in these events `indexed`.

## [I-06] Change Function Visibility from `public` to `external`

## Description

It is best practice to mark functions that are not called internally as external instead, as this saves gas (especially in the case where the function takes arguments, as external functions can read arguments directly from calldata instead of having to allocate memory).

## Location of Affected Code

All `public` functions in `NftFactory.sol` and `TokTokNft.sol` except from `nextTokenId()`, `claim()` and `claimAll()`.

## [I-07] Use a More Recent Solidity Version

## Description:

Currently, version `^0.8.20` is used across the whole codebase. Use the latest stable Solidity version to get all compiler features, bug fixes, and optimizations. However, when upgrading to a new Solidity version, it's crucial to carefully review the release notes, consider any breaking changes, and thoroughly test your code to ensure compatibility and correctness. Additionally, be aware that some features or changes may not be backward compatible, requiring adjustments in your code.

## Location of Affected Code

All of the smart contracts use a relatively old solidity version.

## Recommendation

Consider, upgrading all smart contracts to Solidity version `0.8.26`.

## [G-01] Cache array length outside of a loop

If not cached, the solidity compiler will always read the length of the array during each iteration. That is, if it is a storage array, this is an extra sload operation (100 additional extra gas for each iteration except for the first) and if it is a memory array, this is an extra mload operation (3 additional gas for each iteration except for the first).

File: NftFactory.sol

```solidity
while (i < nfts.length) {
while (i < nfts.length - 1 && nfts[i] == nfts[i + 1]) {
```

File: TokTokNft.sol

```solidity
 for (uint256 i; i < tokenIds.length; ) {
 for (uint256 i = 0; i < bonusTokenList.length; i++) {
 for (uint256 i; i < tokenIds.length; ) {
```

## [G-02] Don't initialize variables with a default value

File: NftFactory.sol

```solidity
for (uint256 j = 0; j < groupLength; j++) {
```

File: TokTokNft.sol

```solidity
for (uint256 i = 0; i < bonusTokenList.length; i++) {
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Harvestflow |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/HarvestFlow-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

