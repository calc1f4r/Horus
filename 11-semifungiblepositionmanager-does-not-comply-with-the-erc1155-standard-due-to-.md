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
solodit_id: 33633
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-11-panoptic
source_link: https://code4rena.com/reports/2023-11-panoptic
github_link: https://github.com/code-423n4/2023-11-panoptic-findings/issues/214

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

[11] `SemiFungiblePositionManager` does not comply with the ERC1155 standard due to not reverting on transfer to zero address

### Overview

See description below for full details.

### Original Finding Content


*Note: At the judge’s request [here](https://github.com/code-423n4/2023-11-panoptic-findings/issues/481#issuecomment-1875219281), this downgraded issue from the same warden has been included in this report for completeness.*

### Lines of code

https://github.com/code-423n4/2023-11-panoptic/blob/f75d07c345fd795f907385868c39bafcd6a56624/contracts/tokens/ERC1155Minimal.sol#L110-L117<br>
https://github.com/code-423n4/2023-11-panoptic/blob/f75d07c345fd795f907385868c39bafcd6a56624/contracts/tokens/ERC1155Minimal.sol#L163-L170

### Impact

`ERC1155Minimal` contract and `SemiFungiblePositionManager` don't comply with ERC1155 token standard.

### Proof of Concept

`SemiFungiblePositionManager` is the ERC1155 version of Uniswap's `NonFungiblePositionManager` contract and it is stated that `SemiFungiblePositionManager` should comply with the ERC1155.

EIP-1155 and all the rules for this token standard can be found here:  
[https://eips.ethereum.org/EIPS/eip-1155](https://eips.ethereum.org/EIPS/eip-1155)

Let's check **safeTransferFrom rules:**

> 
> MUST revert if `_to` is the zero address.
> 
    
However, `ERC1155Minimal` contract does not revert when `to` is zero address. This contract is modified from the Solmate to be more gas efficient, but the transfer to zero address is missed while modifying.

[Here](https://github.com/code-423n4/2023-11-panoptic/blob/f75d07c345fd795f907385868c39bafcd6a56624/contracts/tokens/ERC1155Minimal.sol#L90C5-L118C6) is the `ERC1155Minimal` contract:  

```solidity
    function safeTransferFrom(
        address from,
        address to,
        uint256 id,
        uint256 amount,
        bytes calldata data
    ) public {
        if (!(msg.sender == from || isApprovedForAll[from][msg.sender])) revert NotAuthorized();

        balanceOf[from][id] -= amount;

        // balance will never overflow
        unchecked {
            balanceOf[to][id] += amount;
        }

        afterTokenTransfer(from, to, id, amount);

        emit TransferSingle(msg.sender, from, to, id, amount);

-->     if (to.code.length != 0) { //@audit-issue according to EIP-1155, it MUST revert if "to" is zero address. This check is missing.
            if (
                ERC1155Holder(to).onERC1155Received(msg.sender, from, id, amount, data) !=
                ERC1155Holder.onERC1155Received.selector
            ) {
                revert UnsafeRecipient();
            }
        }
    }
```

As you can see above, there is no check regarding `to` address being zero, which is not EIP-compliant.

The EIP-compliant version of Solmate can be seen [here](https://github.com/transmissions11/solmate/blob/4b47a19038b798b4a33d9749d25e570443520647/src/tokens/ERC1155.sol#L70C1-L71C35):  

```solidity
// Solmate safeTransferFrom:
        require(
            to.code.length == 0
                ? to != address(0)
                : // ...
```

The EIP-compliant version on OpenZeppelin can be seen [here](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/ef699fa6a224de863ffe48347a5ab95d3d8ba2ba/contracts/token/ERC1155/ERC1155.sol#L226C9-L228C10):  


```solidity
// OZ _safeTransferFrom:
        if (to == address(0)) {
            revert ERC1155InvalidReceiver(address(0));
        }
```

### Coded PoC

The code snippet below shows successful transfer action to zero address.
You can use protocol's test suite to run it
- Copy the snippet and paste it in the `SemiFungiblePositionManager.t.sol` test file.
- Run it with `forge test --match-test testSuccess_afterTokenTransfer_Single_ToAddressIsZero -vvv`:

```solidity
function testSuccess_afterTokenTransfer_Single_ToAddressIsZero(
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

        // Up until this point it is the same setup as the protocol's own single transfer test.
        // We will only change the "to" address to 0.
        sfpm.safeTransferFrom(Alice, address(0), tokenId, positionSize, "");

        // The transfer is completed successfully. However, it MUST have been reverted according to the EIP standard.
        assertEq(sfpm.balanceOf(Alice, tokenId), 0);
        assertEq(sfpm.balanceOf(address(0), tokenId), positionSize);
    }    
```

Result after running the test:

```solidity 
Running 1 test for test/foundry/core/SemiFungiblePositionManager.t.sol:SemiFungiblePositionManagerTest
[PASS] testSuccess_afterTokenTransfer_Single_ToAddressIsZero(uint256,uint256,int256,uint256) (runs: 1, μ: 1851440, ~: 1851440)
Test result: ok. 1 passed; 0 failed; 0 skipped; finished in 8.16s
 
Ran 1 test suite: 1 test passed, 0 failed, 0 skipped (1 total test)
```

### Recommended Mitigation Steps

Revert if `to` address is zero to comply with ERC1155 token standard.



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
- **GitHub**: https://github.com/code-423n4/2023-11-panoptic-findings/issues/214
- **Contest**: https://code4rena.com/reports/2023-11-panoptic

### Keywords for Search

`vulnerability`

