---
# Core Classification
protocol: Backed Protocol
chain: everychain
category: uncategorized
vulnerability_type: nft

# Attack Vector Details
attack_type: nft
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6204
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-papr-contest
source_link: https://code4rena.com/reports/2022-12-backed
github_link: https://github.com/code-423n4/2022-12-backed-findings/issues/183

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - nft

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - rotcivegaf
  - Jeiwan
  - Koolex
  - Ruhum
---

## Vulnerability Title

[H-03] Collateral NFT deposited to a wrong address, when transferred directly to PaprController

### Overview


This bug report is about a vulnerability found in the PaprController smart contract. The vulnerability allows users to lose their collateral Non-Fungible Tokens (NFTs) when they are transferred to the PaprController by an approved address or an operator. The issue is caused by the wrong argument used to identify token owner in the `onERC721Received` hook implementation. As a result, when an NFT is sent by an approved address or an operator, it is deposited to the vault of the approved address or operator, instead of the actual owner.

The vulnerability was discovered during a manual review. To mitigate the issue, the code should be changed by replacing the first argument with the second argument in the `onERC721Received` hook implementation. This change will ensure that the NFTs are deposited to the actual owner's vault.

### Original Finding Content

## Lines of code

https://github.com/with-backed/papr/blob/9528f2711ff0c1522076b9f93fba13f88d5bd5e6/src/PaprController.sol#L159


## Vulnerability details

## Impact
Users will lose collateral NFTs when they are transferred to `PaprController` by an approved address or an operator.
## Proof of Concept
The `PaprController` allows users to deposit NFTs as collateral to borrow Papr tokens. One of the way of depositing is by transferring an NFT to the contract directly via a call to `safeTransferFrom`: the contract implements the `onERC721Received` hook that will handle accounting of the transferred NFT ([PaprController.sol#L159](https://github.com/with-backed/papr/blob/9528f2711ff0c1522076b9f93fba13f88d5bd5e6/src/PaprController.sol#L159)). However, the hook implementation uses a wrong argument to identify token owner: the first argument, which is used by the contract to identify token owner, is the address of the `safeTransferFrom` function caller, which may be an approved address or an operator. The actual owner address is the second argument ([ERC721.sol#L436](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol#L436)):
```solidity
try IERC721Receiver(to).onERC721Received(_msgSender(), from, tokenId, data) returns (bytes4 retval) {
```

Thus, when an NFT is sent by an approved address or an operator, it'll be deposited to the vault of the approved address or operator:
```solidity
// test/paprController/OnERC721ReceivedTest.sol

function testSafeTransferByOperator_AUDIT() public {
    address operator = address(0x12345);

    vm.prank(borrower);
    nft.setApprovalForAll(operator, true);

    vm.prank(operator);
    nft.safeTransferFrom(borrower, address(controller), collateralId, abi.encode(safeTransferReceivedArgs));

    // NFT was deposited to the operator's vault.
    IPaprController.VaultInfo memory vaultInfo = controller.vaultInfo(operator, collateral.addr);
    assertEq(vaultInfo.count, 1);

    // Borrower has 0 tokens in collateral.
    vaultInfo = controller.vaultInfo(borrower, collateral.addr);
    assertEq(vaultInfo.count, 0);
}

function testSafeTransferByApproved_AUDIT() public {
    address approved = address(0x12345);

    vm.prank(borrower);
    nft.approve(approved, collateralId);

    vm.prank(approved);
    nft.safeTransferFrom(borrower, address(controller), collateralId, abi.encode(safeTransferReceivedArgs));

    // NFT was deposited to the approved address's vault.
    IPaprController.VaultInfo memory vaultInfo = controller.vaultInfo(approved, collateral.addr);
    assertEq(vaultInfo.count, 1);

    // Borrower has 0 tokens in collateral.
    vaultInfo = controller.vaultInfo(borrower, collateral.addr);
    assertEq(vaultInfo.count, 0);
}
```
## Tools Used
Manual review
## Recommended Mitigation Steps
Consider this change:
```diff
--- a/src/PaprController.sol
+++ b/src/PaprController.sol
@@ -156,7 +156,7 @@ contract PaprController is
     /// @param _id the id of the NFT
     /// @param data encoded IPaprController.OnERC721ReceivedArgs
     /// @return selector indicating succesful receiving of the NFT
-    function onERC721Received(address from, address, uint256 _id, bytes calldata data)
+    function onERC721Received(address, address from, uint256 _id, bytes calldata data)
         external
         override
         returns (bytes4)
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Backed Protocol |
| Report Date | N/A |
| Finders | rotcivegaf, Jeiwan, Koolex, Ruhum |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-backed
- **GitHub**: https://github.com/code-423n4/2022-12-backed-findings/issues/183
- **Contest**: https://code4rena.com/contests/2022-12-papr-contest

### Keywords for Search

`NFT`

