---
# Core Classification
protocol: Munchables
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36639
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-munchables
source_link: https://code4rena.com/reports/2024-07-munchables
github_link: https://github.com/code-423n4/2024-07-munchables-findings/issues/42

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
finders_count: 25
finders:
  - santipu\_
  - 0xrex
  - phoenixV110
  - forgebyola
  - nnez
---

## Vulnerability Title

[H-05] Failure to update dirty flag in `transferToUnoccupiedPlot` prevents reward accumulation on valid plot

### Overview


The function `transferToUnoccupiedPlot` allows users to transfer their Munchable to another unoccupied plot from the same landlord. This is useful for users who are currently staked in an invalid plot and want to move to a valid plot to start earning rewards again. However, there is a bug where the function does not update the user's dirty flag back to false, meaning they will still not earn any rewards even after moving to a valid plot. This unfairly penalizes users and should be fixed by updating the function to reset the dirty flag and update the lastToilDate when a user successfully transfers to a valid plot.

### Original Finding Content


The [`transferToUnoccupiedPlot`](https://github.com/code-423n4/2024-07-munchables/blob/94cf468aaabf526b7a8319f7eba34014ccebe7b9/src/managers/LandManager.sol#L199) function allows a user to transfer their Munchable to another unoccupied plot from the same landlord. This can be used for example by users currently staked in an invalid plot marked as “dirty”, meaning they will not be earning any rewards, to transfer to a valid plot so they can start earning rewards again.

Since the function checks that the transfer is to a valid plot, it should mean users are now eligible to start earning rewards again. However, it doesn’t update the user’s dirty flag back to false, meaning the user will still not be earning any rewards even after they have moved to a valid plot.

```solidity
    function transferToUnoccupiedPlot(uint256 tokenId, uint256 plotId)
        external
        override
        forceFarmPlots(msg.sender)
        notPaused
    {
        (address mainAccount,) = _getMainAccountRequireRegistered(msg.sender);
        ToilerState memory _toiler = toilerState[tokenId];
        uint256 oldPlotId = _toiler.plotId;
        uint256 totalPlotsAvail = _getNumPlots(_toiler.landlord);
        if (_toiler.landlord == address(0)) revert NotStakedError();
        if (munchableOwner[tokenId] != mainAccount) revert InvalidOwnerError();
        if (plotOccupied[_toiler.landlord][plotId].occupied) {
            revert OccupiedPlotError(_toiler.landlord, plotId);
        }
        if (plotId >= totalPlotsAvail) revert PlotTooHighError();

        toilerState[tokenId].latestTaxRate = plotMetadata[_toiler.landlord].currentTaxRate;
        plotOccupied[_toiler.landlord][oldPlotId] = Plot({occupied: false, tokenId: 0});
        plotOccupied[_toiler.landlord][plotId] = Plot({occupied: true, tokenId: tokenId});

        emit FarmPlotLeave(_toiler.landlord, tokenId, oldPlotId);
        emit FarmPlotTaken(toilerState[tokenId], tokenId);
    }
```

The next time [`_farmPlots`](https://github.com/code-423n4/2024-07-munchables/blob/94cf468aaabf526b7a8319f7eba34014ccebe7b9/src/managers/LandManager.sol#L232) is called, since dirty is still true, it’ll be skipped, accumulating no rewards.

```solidity
    function _farmPlots(address _sender) internal {
        ...
        for (uint8 i = 0; i < staked.length; i++) {
            ...
            if (_toiler.dirty) continue;
            ...
            );
        }
        accountManager.updatePlayer(mainAccount, renterMetadata);
    }
```

### Impact

Since the function does not update the user's dirty flag back to valid, users who transfer their Munchable to a valid plot and the landlord will still not earn any rewards. This results in a situation where users remain unfairly penalized even after moving to a valid plot

### Recommendation

Update the `transferToUnoccupiedPlot` function to reset the dirty flag to false and update the `lastToilDate` if it was previously marked as dirty when a user successfully transfers to a valid plot. This will ensure that users start earning rewards again once they are on a valid plot.

```solidity
    function transferToUnoccupiedPlot(uint256 tokenId, uint256 plotId)
        external
        override
        forceFarmPlots(msg.sender)
        notPaused
    {
        (address mainAccount,) = _getMainAccountRequireRegistered(msg.sender);
        ToilerState memory _toiler = toilerState[tokenId];
        uint256 oldPlotId = _toiler.plotId;
        uint256 totalPlotsAvail = _getNumPlots(_toiler.landlord);
        if (_toiler.landlord == address(0)) revert NotStakedError();
        if (munchableOwner[tokenId] != mainAccount) revert InvalidOwnerError();
        if (plotOccupied[_toiler.landlord][plotId].occupied) {
            revert OccupiedPlotError(_toiler.landlord, plotId);
        }
        if (plotId >= totalPlotsAvail) revert PlotTooHighError();
	// ADD HERE
        if (_toiler.dirty) {
            toilerState[tokenId].lastToilDate = block.timestamp;
            toilerState[tokenId].dirty = false;
        }
	//
        toilerState[tokenId].latestTaxRate = plotMetadata[_toiler.landlord].currentTaxRate;
        plotOccupied[_toiler.landlord][oldPlotId] = Plot({occupied: false, tokenId: 0});
        plotOccupied[_toiler.landlord][plotId] = Plot({occupied: true, tokenId: tokenId});

        emit FarmPlotLeave(_toiler.landlord, tokenId, oldPlotId);
        emit FarmPlotTaken(toilerState[tokenId], tokenId);
    }
```

**[0xinsanity (Munchables) confirmed via duplicate Issue #89](https://github.com/code-423n4/2024-07-munchables-findings/issues/89#event-13714284765)**

***
 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Munchables |
| Report Date | N/A |
| Finders | santipu\_, 0xrex, phoenixV110, forgebyola, nnez, typicalHuman, ke1caM, gajiknownnothing, Drynooo, Heaven, Tomas0707, rudhra, joaovwfreire, tedox, dhank, ironside, dontonka, Abdessamed, dimulski, Bozho, McToady, stanchev, merlinboii, shaflow2, 0xCiphky |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-munchables
- **GitHub**: https://github.com/code-423n4/2024-07-munchables-findings/issues/42
- **Contest**: https://code4rena.com/reports/2024-07-munchables

### Keywords for Search

`vulnerability`

