---
# Core Classification
protocol: Sablier
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33414
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clvb9njmy00012dqjyaavpl44
source_link: none
github_link: https://github.com/Cyfrin/2024-05-Sablier

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
finders_count: 4
finders:
  - 0xspryon
  - 0xG0P1
  - 0xaman
  - Tripathi
---

## Vulnerability Title

Stream sender is unable to cancel a stream with a pausable asset that is paused

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2024-05-Sablier/blob/main/v2-core/src/abstracts/SablierV2Lockup.sol#L599">https://github.com/Cyfrin/2024-05-Sablier/blob/main/v2-core/src/abstracts/SablierV2Lockup.sol#L599</a>

<a data-meta="codehawks-github-link" href="https://github.com/tethercoin/USDT/blob/main/TetherToken.sol#L340">https://github.com/tethercoin/USDT/blob/main/TetherToken.sol#L340</a>


## Summary

When the stream sender cancels a stream, we call the asset transfer method to reimburse the amount that is yet to be streamed to the sender. If this call reverts, then the call to cancel the stream reverts as well.

## Vulnerability Details

There exists ERC20 tokens that are pausable.
For example [USDT on ethereum](https://github.com/tethercoin/USDT/blob/main/TetherToken.sol#L340) ( verifiable on etherscan )
If for whatever reason the stream asset is paused, then the stream Sender is unable to cancel the stream until the asset is unpaused.

### POC

<details>
	<summary>
		Replace the content of `v2-core/test/mocks/erc20/ERC20Mock.sol` with the below code block
	</summary>

```solidity
// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity >=0.8.22;

import { ERC20 } from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol";
import "forge-std/src/console.sol";

contract ERC20Mock is ERC20, ERC20Pausable {

    constructor(string memory name, string memory symbol) ERC20(name, symbol) { }

    function pause() public {
        _pause();
        console.log("Contract paused");
    }

    function transfer(address to, uint256 value) override public whenNotPaused returns (bool) {
       return super.transfer(to, value) ;
    }

    function _update(address from, address to, uint256 value)
        internal
        override(ERC20, ERC20Pausable)
    {

        super._update(from, to, value);
    }
}
```
</details>

<details>
	<summary>
		 Add the below codeblock in `v2-core/test/integration/concrete/lockup/cancel/cancel.t.sol` Notice the importation of the ERC20Mock file.
	</summary>

```solidity
	import { ERC20Mock } from "../../../../../test/mocks/erc20/ERC20Mock.sol";

    function test_CancelAssetPaused()
        external
        whenNotDelegateCalled
        givenNotNull
        givenStreamWarm
        whenCallerAuthorized
        givenStreamCancelable
        givenStatusStreaming
        givenRecipientContract
        givenRecipientImplementsHook
        whenRecipientDoesNotRevert
        whenNoRecipientReentrancy
    {
        // Create the stream.
        uint256 streamId = createDefaultStreamWithRecipient(address(goodRecipient));

        // Pause the stream Asset
        ERC20Mock(address(lockup.getAsset(defaultStreamId))).pause();

        // Cancel the stream.
        vm.expectRevert();
        lockup.cancel(streamId);

        // Assert that the stream's status is still "STREAMING".
        Lockup.Status actualStatus = lockup.statusOf(streamId);
        Lockup.Status expectedStatus = Lockup.Status.STREAMING;
        assertEq(actualStatus, expectedStatus);

        // Assert that the stream is still cancelable.
        bool isCancelable = lockup.isCancelable(streamId);
        assertTrue(isCancelable, "isCancelable");

        // Assert that the refunded amount has not been updated.
        uint128 actualRefundedAmount = lockup.getRefundedAmount(streamId);
        uint128 expectedRefundedAmount = 0;
        assertEq(actualRefundedAmount, expectedRefundedAmount, "refundedAmount");
    }
```
</details>

run the below command in the terminal
`forge test --mt test_CancelAssetPaused -vvv`


## Impact

The stream sender is temporarily unable to cancel the stream which leads to a loss of funds as the stream will continue streaming the assets to the Stream Receiver. The impact of the loss of funds depends on how long the asset has been paused for, relative to how fast the asset is being streamed. For the sake of an example, imagine the asset is paused just as the stream is about to get past the Stream's cliff period and the sender wishes to cancel the stream.

likelihood: medium as assets are paused only under cases of force majeure but taking into account that Sablier supports all ERC20 assets on all EVM compatible chains, the probability of a pausing on an asset happening is not low.

impact: high as all cancelable asset streams effectively become uncancelable while the asset is paused. Knowing USDT's stature as one of the well respected and transacted stablecoins, this will translate to a lot of streams(without taking into account the other pausable assets on all the evm compatible chains where Sablier is/would be deployed).

## Tools Used

Fuzzing with foundry

## Recommendations

Similar to how when the Stream is canceled the Stream Receiver is expected to withdraw the streamed assets by himself in a call seperate to the call to cancel the stream, we should seperate the transfer of the Senders funds from the cancel funtion into a seperate function

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Sablier |
| Report Date | N/A |
| Finders | 0xspryon, 0xG0P1, 0xaman, Tripathi |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-05-Sablier
- **Contest**: https://www.codehawks.com/contests/clvb9njmy00012dqjyaavpl44

### Keywords for Search

`vulnerability`

