---
# Core Classification
protocol: Panoptic
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33634
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-11-panoptic
source_link: https://code4rena.com/reports/2023-11-panoptic
github_link: https://github.com/code-423n4/2023-11-panoptic-findings/issues/221

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
finders_count: 0
finders:
---

## Vulnerability Title

[12] `ERC1155Minimal::safeBatchTransferFrom` **MUST** revert if the length of ids is not the same as the length of amounts to comply with the ERC1155 token standard

### Overview

See description below for full details.

### Original Finding Content


*Note: At the judge’s request [here](https://github.com/code-423n4/2023-11-panoptic-findings/issues/481#issuecomment-1875219281), this downgraded issue from the same warden has been included in this report for completeness.*

`ERC1155Minimal` and `SemiFungiblePositionManager` contracts do not comply with ERC1155 token standard.

### Proof of Concept

`SemiFungiblePositionManager` is the ERC1155 version of Uniswap's `NonFungiblePositionManager` contract and it is stated that `SemiFungiblePositionManager` should comply with the ERC1155.

EIP-1155 and all the rules for this token standard can be found here:  
[https://eips.ethereum.org/EIPS/eip-1155](https://eips.ethereum.org/EIPS/eip-1155)

Let's check the **safeBatchTransferFrom rules:**

>
> MUST revert if length of `_ids` is not the same as length of `_values`.
>     

However, `ERC1155Minimal` contract does not check these array lengths and does not revert when there is a mismatch.

This contract is modified from the Solmate to be more gas efficient, but the input length mismatch check is missed while modifying.

[Here](https://github.com/code-423n4/2023-11-panoptic/blob/f75d07c345fd795f907385868c39bafcd6a56624/contracts/tokens/ERC1155Minimal.sol#L128C5-L171C6) is the ERC1155Minimal contract `safeBatchTransferFrom` function:  

```solidity
// ERC1155Minimal.sol
    function safeBatchTransferFrom(
        address from,
        address to,
        uint256[] calldata ids,
        uint256[] calldata amounts,
        bytes calldata data
    ) public virtual {
        if (!(msg.sender == from || isApprovedForAll[from][msg.sender])) revert NotAuthorized();

        // Storing these outside the loop saves ~15 gas per iteration.
        uint256 id;
        uint256 amount;

-->     for (uint256 i = 0; i < ids.length; ) { //@audit-issue according to EIP-1155, it MUST revert if "ids" length is not the same as "amounts" length. There is no check in this function. If amounts.length > ids.length, the function will only iterate "ids.length" times in the for loop but will NOT revert.
            id = ids[i];
            amount = amounts[i];

            balanceOf[from][id] -= amount;

            // balance will never overflow
            unchecked {
                balanceOf[to][id] += amount;
            }

            // An array can't have a total length
            // larger than the max uint256 value.
            unchecked {
                ++i;
            }
        }

        afterTokenTransfer(from, to, ids, amounts);

        emit TransferBatch(msg.sender, from, to, ids, amounts);

        if (to.code.length != 0) {
            if (
                ERC1155Holder(to).onERC1155BatchReceived(msg.sender, from, ids, amounts, data) !=
                ERC1155Holder.onERC1155BatchReceived.selector
            ) {
                revert UnsafeRecipient();
            }
        }
    }
```

As we can see above, there is no check in terms of `ids` length and the `amounts` length.

EIP-1155 compliant version of this implementation on Solmate can be found [here](https://github.com/transmissions11/solmate/blob/4b47a19038b798b4a33d9749d25e570443520647/src/tokens/ERC1155.sol#L85):  

```solidity
// Solmate safeBatchTransferFrom:
   require(ids.length == amounts.length, "LENGTH_MISMATCH");
```

EIP-1155 compliant version of this implementation on OpenZeppelin can be found [here](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/ef699fa6a224de863ffe48347a5ab95d3d8ba2ba/contracts/token/ERC1155/ERC1155.sol#L148C5-L151C10) (`_safeBatchTransferFrom` will call `_update` function and the check is in this `_update` function):  

```solidity
// OZ _update function (called during batch transfer)
    function _update(address from, address to, uint256[] memory ids, uint256[] memory values) internal virtual {
        if (ids.length != values.length) {
            revert ERC1155InvalidArrayLength(ids.length, values.length);
        }
```

NOTE: I also submitted another EIP compliance issue which is related to `to` address being zero. This issue is a separate breach of the rules and a different root cause. Therefore, I submitted this one as a separate issue since fixing only one of them will not make the contract EIP compliant.

### Coded PoC

The code snippet below shows successful transfer action with mismatching array length. You can use protocol's test suite to run it.
- Copy the snippet and paste it in the `SemiFungiblePositionManager.t.sol` test file.
- Run it with `forge test --match-test testSuccess_afterTokenTransfer_Batch_ArrayLengthsMismatch -vvv`:

```solidity
function testSuccess_afterTokenTransfer_Batch_ArrayLengthsMismatch(
        uint256 x,
        uint256 widthSeed,
        int256 strikeSeed,
        uint256 positionSizeSeed
    ) public {
        // Initial part of this test is the same as the protocol's own tests.
        _initPool(x);

        (int24 width, int24 strike) = PositionUtils.getOutOfRangeSW(
            widthSeed,
            strikeSeed,
            uint24(tickSpacing),
            currentTick
        );

        populatePositionData(width, strike, positionSizeSeed);

        /// position size is denominated in the opposite of asset, so we do it in the token that is not WETH
        uint256 tokenId = uint256(0).addUniv3pool(poolId).addLeg(
            0,
            1,
            isWETH,
            0,
            1,
            0,
            strike,
            width
        );

        sfpm.mintTokenizedPosition(
            tokenId,
            uint128(positionSize),
            TickMath.MIN_TICK,
            TickMath.MAX_TICK
        );

        uint256 tokenId2 = uint256(0).addUniv3pool(poolId).addLeg(
            0,
            1,
            isWETH,
            0,
            0,
            0,
            strike,
            width
        );

        sfpm.mintTokenizedPosition(
            tokenId2,
            uint128(positionSize),
            TickMath.MIN_TICK,
            TickMath.MAX_TICK
        );

        // Up until this point it is the same setup as the protocol's own batch transfer test.
        // We will only change the amounts array.
        // TokenIds array length is 2, amounts array length is 3.
        uint256[] memory tokenIds = new uint256[](2);
        tokenIds[0] = tokenId;
        tokenIds[1] = tokenId2;
        uint256[] memory amounts = new uint256[](3);
        amounts[0] = positionSize;
        amounts[1] = positionSize;
        amounts[2] = positionSize;
        sfpm.safeBatchTransferFrom(Alice, Bob, tokenIds, amounts, "");

        // The transfer is completed successfully. However, it MUST have been reverted according to the EIP standard.
        assertEq(sfpm.balanceOf(Alice, tokenId), 0);
        assertEq(sfpm.balanceOf(Bob, tokenId), positionSize);
    }
```

Results after running the test:

```solidity
Running 1 test for test/foundry/core/SemiFungiblePositionManager.t.sol:SemiFungiblePositionManagerTest
[PASS] testSuccess_afterTokenTransfer_Batch_ArrayLengthsMismatch(uint256,uint256,int256,uint256) (runs: 1, μ: 1981414, ~: 1981414)
Test result: ok. 1 passed; 0 failed; 0 skipped; finished in 7.84s
 
Ran 1 test suites: 1 tests passed, 0 failed, 0 skipped (1 total tests)
```

### Recommended Mitigation Steps

I would recommend checking input array lengths and reverting if there is a mismatch.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Panoptic |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-11-panoptic
- **GitHub**: https://github.com/code-423n4/2023-11-panoptic-findings/issues/221
- **Contest**: https://code4rena.com/reports/2023-11-panoptic

### Keywords for Search

`vulnerability`

