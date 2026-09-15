---
# Core Classification
protocol: Boba 1 (Bridges and LP floating fee)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60709
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/boba-1-bridges-and-lp-floating-fee/1e5a1e09-bde0-417d-83cd-083234b1409c/index.html
source_link: https://certificate.quantstamp.com/full/boba-1-bridges-and-lp-floating-fee/1e5a1e09-bde0-417d-83cd-083234b1409c/index.html
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
finders_count: 5
finders:
  - Pavel Shabarkin
  - Ibrahim Abouzied
  - Andy Lin
  - Adrian Koegl
  - Valerian Callens
---

## Vulnerability Title

Missing Input Validations

### Overview

See description below for full details.

### Original Finding Content

**Update**
The team added several validations as recommended in the commit `a20c6ca`. The following is the list of validations still missing after the fix:

`L1NFTBridge` contract:

*   `configureGas()`: the range of `_depositL2Gas` still lacks validation.
*   `_initiateNFTDeposit()`: validations for `_l2Gas` and `_data` are still missing.

`L2NFTBridge` and `L2NFTBridgeAltL1` contracts:

*   `configureGas()`: the range check of the `_exitL1Gas` is still missing.
*   `_initiateWithdrawal()`: the min value check for `_l1Gas` is still missing, and the `_data` size is not checked.

`L1ERC1155Bridge` contract:

*   `configureGas()`: the range check of the `_depositL2Gas` is still missing.
*   `_initiateDeposit()`: the min value check for the `_l2Gas` is still missing, and the `_data` size is not checked.
*   `_initiateDepositBatch()`: the min value check for the `_l2Gas` is still missing, and the `_data` size is not checked.

`L2ERC1155Bridge` and `L2ERC1155BridgeAltL1` contracts:

*   `configureGas()`: the range check of the `_exitL1Gas` is still missing. 
*   `_initiateWithdrawal()`: the min value check for the `_l1Gas` is still missing, and the `_data` size is not checked.
*   `_initiateWithdrawalBatch()`: the min value check for the `_l1Gas` is still missing, and the `_data` size is not checked.

**File(s) affected:**`ERC721Bridges/L1NFTBridge.sol`, `ERC721Bridges/L2NFTBridge.sol`, `ERC721Bridges/L2NFTBridgeAltL1.sol`, `ERC1155Bridges/L1ERC1155Bridge.sol`, `ERC1155Bridges/L2ERC1155Bridge.sol`, `ERC1155Bridges/L2ERC1155BridgeAltL1.sol`, `LP/*.sol`

**Description:** It is important to validate inputs, even if they only come from trusted addresses, to avoid human error. For instance, functions arguments of type `address` may be initialized with value `0x0`. The following is a list of places where we recommend adding more validations:

`L1NFTBridge` contract:

1.   `transferOwnership()`: consider validating that the `_newOwner` is not `address(0)` to avoid revoking the ownership. However, if it is intended to have the ability to revoke the ownership, please document this.
2.   `configureGas()`: consider having a minimal and maximal value that the `_depositL2Gas` should be in the range. Otherwise, if it is accidentally set to an impractical number, all cross-domain messages will fail.
3.   `_initiateNFTDeposit()`: 
    1.   This function should have validation that the `_from == msg.sender`. The reason is that in some parts of the function, it collects the NFT with `IERC721.safeTransferFrom(_from, ...)` while in the other part of the function, it checks the authorization of the NFT with `msg.sender` in the line `require(msg.sender == NFTOwner, ...)` before burning the NFT. The mix of the two makes the expected behavior unclear. Note that currently all functions calling `_initiateNFTDeposit()` passes the `msg.sender` as the `_from` input.
    2.   The input `_l2Gas` can potentially be insufficient for the message to relay. Consider validating against a minimum value otherwise, the message might fail.
    3.   Consider checking `_data` input against a max size limit. Otherwise, it can be spammed or even not able to process large data sizes.

4.   `registerNFTPair()`: 
    1.   Please validate that the `_l2Contract != address(0)`. Several places in this contract check that `pairNFT.l2Contract != address(0)` after the registration. If accidentally registered with a zero address, it can have unexpected consequences. 
    2.   We also recommend validating that `_l1Contract != address(0)` to avoid registering value for the empty key of the `pairNFTInfo[]` mapping.
    3.   Validate that the non-base contract points to its correct counterpart (e.g., `require(IL1StandardERC721(_l1Contract).l2Contract() == _l2contract)`)

`L2NFTBridge` and `L2NFTBridgeAltL1` contracts:

1.   `transferOwnership()`: consider validating that the `_newOwner` is not `address(0)` to avoid revoking the ownership. However, if it is intended to have the ability to revoke the ownership, please document this.
2.   `configureGas()`: consider having a minimal and maximal value that the `_exitL1Gas` should be in the range. Otherwise, if it is accidentally set to an impractical number, all cross-domain messages will fail.
3.   `_initiateWithdrawal()`: 
    1.   This function should have validation that the `_from == msg.sender`. The reason is that in some parts of the function, it collects the NFT with `IERC721.safeTransferFrom(_from, ...)` while in the other part of the function, it checks the authorization of the NFT with `msg.sender` in the line `require(msg.sender == NFTOwner, ...)` before burning the NFT. The mix of the two makes the expected behavior unclear. Note that currently, all functions calling `_initiateWithdrawal()` pass the `msg.sender` as the `_from` input.
    2.   The input `_l1Gas` can potentially be insufficient for the message to relay. Consider validating against a minimum value otherwise, the message might fail.
    3.   Consider checking `_data` input against a max size limit. Otherwise, it can be spammed or even not able to process large data sizes.

4.   `registerNFTPair()`: 
    1.   Please validate that the `_l1Contract != address(0)`. Several places in this contract check that `pairNFT.l1Contract != address(0)` after the registration. If accidentally registered with a zero address, it can have unexpected consequences. 
    2.   We also recommend validating that `_l2Contract != address(0)` to avoid registering value for the empty key of the `pairNFTInfo[]` mapping.
    3.   Validate that the non-base contract points to its correct counterpart (e.g., `require(IL1StandardERC721(_l1Contract).l2Contract() == _l2contract)`)

`L1ERC1155Bridge` contract:

1.   `transferOwnership()`: consider validating that the `_newOwner` is not `address(0)` to avoid revoking the ownership. However, if it is intended to have the ability to revoke the ownership, please document this.
2.   `configureGas()`: consider having a minimal and maximal value that the `_depositL2Gas` should be in the range. Otherwise, if it is accidentally set to an impractical number, all cross-domain messages will fail.
3.   `registerPair()`: 
    1.   Please validate that the `_l2Contract != address(0)`. Several places in this contract check that `l2Contract != address(0)` after the registration. If accidentally registered with a zero address, it can have unexpected consequences. 
    2.   We also recommend validating that `_l1Contract != address(0)` to avoid registering value for the empty key of the `pairTokenInfo[]` mapping.

4.   `_initiateDeposit()`: 
    1.   This function should have validation that the `_from == msg.sender`. The reason is that in some parts of the function, it collects the tokens with `IERC1155.safeTransferFrom(_from, ...)` while in the other part of the function, it checks the balance of the tokens with `msg.sender` in the line `IL1StandardERC1155(_l1Contract).balanceOf(msg.sender,...)` before burning the tokens of the `msg.sender`. The mix of the two makes the expected behavior unclear. Note that currently, all functions calling `_initiateDeposit()` pass the `msg.sender` as the `_from` input.
    2.   The input `_l2Gas` can potentially be insufficient for the message to relay. Consider validating against a minimum value otherwise, the message might fail.
    3.   Consider checking `_data` input against a max size limit. Otherwise, it can be spammed or even not able to process large data sizes.

5.   `_initiateDepositBatch()`: 
    1.   Same as `_initiateDeposit()`, this function should check that `_from == msg.sender`, `_l2Gas` is larger than a minimum size, and the `_data` input should be capped within a maximum size.
    2.   The function should also check that `_tokenIds.length == _amounts.length` in case the two arrays do not match. Currently, the function will only revert if `_tokenIds.length > _amounts.length` but the inverse situation will remain undetected and trigger a cross-chain action.

`L2ERC1155Bridge` and `L2ERC1155BridgeAltL1` contracts:

1.   `transferOwnership()`: consider validating that the `_newOwner` is not `address(0)` to avoid revoking the ownership. However, if it is intended to have the ability to revoke the ownership, please document this.
2.   `configureGas()`: consider having a minimal and maximal value that the `_exitL1Gas` should be in the range. Otherwise, if it is accidentally set to an impractical number, all cross-domain messages will fail.
3.   `registerPair()`: 
    1.   Please validate that the `_l1Contract != address(0)`. Several places in this contract check that `l1Contract != address(0)` after the registration. If accidentally registered with a zero address, it can have unexpected consequences. 
    2.   We also recommend validating that `_l2Contract != address(0)` to avoid registering value for the empty key of the `pairTokenInfo[]` mapping.
    3.   Validate that the non-base contract points to its correct counterpart (e.g., `require(IL1StandardERC721(_l1Contract).l2Contract() == _l2contract)`)

4.   `_initiateWithdrawal()`: 
    1.   This function should have validation that the `_from == msg.sender`. The reason is that in some parts of the function, it collects the tokens with `IERC1155.safeTransferFrom(_from, ...)` while in the other part of the function, it checks the balance of the tokens with `msg.sender` in the line `IL1StandardERC1155(_l1Contract).balanceOf(msg.sender,...)` before burning the tokens of the `msg.sender`. The mix of the two makes the expected behavior unclear. Note that currently, all functions calling `_initiateWithdrawal()` pass the `msg.sender` as the `_from` input.
    2.   The input `_l1Gas` can potentially be insufficient for the message to relay. Consider validating against a minimum value otherwise, the message might fail.
    3.   Consider checking `_data` input against a max size limit. Otherwise, it can be spammed or even not able to process large data sizes.

5.   `_initiateWithdrawalBatch()`: 
    1.   Same as `_initiateWithdrawal()`, this function should check that `_from == msg.sender`, `_l1Gas` is larger than a minimum size, and the `_data` input should be capped within a maximum size.
    2.   The function should also check that `_tokenIds.length == _amounts.length` if the two arrays do not match.

`L1LiquidityPool`, `L2LiquidityPool`, `L1LiquidityPoolAltL1`, and `L2LiquidityPoolAltL1` contracts:

1.   `withdrawLiquidity()`: consider adding a check that the amount is greater than zero. While this observation does not pose a direct security threat, it highlights a potential gap in the function's business logic. Ensuring that the withdrawal amount is greater than zero could help prevent unexpected behavior and improve the overall functionality of the smart contract.

**Recommendation:** Consider adding validations as pointed out in the description section.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Boba 1 (Bridges and LP floating fee) |
| Report Date | N/A |
| Finders | Pavel Shabarkin, Ibrahim Abouzied, Andy Lin, Adrian Koegl, Valerian Callens |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/boba-1-bridges-and-lp-floating-fee/1e5a1e09-bde0-417d-83cd-083234b1409c/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/boba-1-bridges-and-lp-floating-fee/1e5a1e09-bde0-417d-83cd-083234b1409c/index.html

### Keywords for Search

`vulnerability`

