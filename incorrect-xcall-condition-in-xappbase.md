---
# Core Classification
protocol: Omni Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53602
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma_Prime_Omni_Network_Omni_Chain_2_Security_Assessment_Report_v2_1.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma_Prime_Omni_Network_Omni_Chain_2_Security_Assessment_Report_v2_1.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Incorrect XCall Condition In XAppBase

### Overview

See description below for full details.

### Original Finding Content

## Security Audit Report

## OM2-12 msg.value Checks
### Asset: XCall Contract
**Status**: Resolved: See Resolution  
**Rating**: Informational  

**Description**  
The `require()` statement in `xcall()` checks for `msg.value`, which can be incorrect when any value is sent or reserved for app fees. The following check in `xcall()` ensures that there are enough native tokens to pay for the XCall fee:

```solidity
require(address(this).balance >= fee || msg.value >= fee, "XApp: insufficient funds");
```

Checking `msg.value >= fee` can be incorrect if any value is sent to another address before calling `xcall()`, or if the XApp contract takes its own fee in native tokens. For example, a cross-L2 ETH bridge may take its own app fee in ETH when bridging from Optimism to Arbitrum. If the user sends enough ETH to cover the XCall fee but not enough for the app fee, the XCall will still succeed, and the app fee is not applied.

This issue has an informational rating as it can be mitigated if the XApp developer is aware of this behavior and correctly checks for `msg.value >= xcallFee + appFee`.

### Recommendations  
Instead of checking for `msg.value >= fee`, allow the XApp contract to take an `amtForFee` parameter in `xcall()` and check for `amtForFee >= fee`. The XApp contract can deduct any app fees or transferred value from `msg.value` before calling `xcall()`.

### Resolution  
The Omni team has removed the `msg.value >= fee` check and has added Natspec comments to inform XApp developers of where the XCall fee is deducted from. This issue has been resolved in PR #2301.

---

## OM2-13 Return nil Both For Error And abci.ValidatorUpdate  
### Asset: halo/valsync/keeper/keeper.go  
**Status**: Resolved: See Resolution  
**Rating**: Informational  

**Description**  
The `processAttested()` function returns a nil value both for an error and for the `abci.ValidatorUpdate` on line [302] and line [316] as can be seen in the following code segment.

```go
func (k *Keeper) processAttested(ctx context.Context) ([]abci.ValidatorUpdate, error) {
    valset, ok, err := k.nextUnattestedSet(ctx)
    if err != nil {
        return nil, err
    } else if !ok {
        return nil, nil // No unattested set, so no updates.
    }
    sdkCtx := sdk.UnwrapSDKContext(ctx)
    chainID, err := netconf.ConsensusChainIDStr2Uint64(sdkCtx.ChainID())
    if err != nil {
        return nil, errors.Wrap(err, "parse chain id")
    }
    conf := xchain.ConfFinalized // TODO(corver): Move this to static netconf.
    // Check if this unattested set was attested to
    if atts, err := k.aKeeper.ListAttestationsFrom(ctx, chainID, uint32(conf), valset.GetAttestOffset(), 1); err != nil {
        return nil, errors.Wrap(err, "list attestations")
    } else if len(atts) == 0 {
        return nil, nil // No attested set, so no updates.
    }
    ...
}
```

This has been given informational severity as there is no available exploit path currently for it, but it could lead to easy coding mistakes and a potential vulnerability.

### Recommendations  
Return a custom error when there are no validator updates and handle it specifically when calling the function.

### Resolution  
This has been deemed a non-issue as:
"The processAttested function is called exclusively from the EndBlock callback. The keeper.Cosmos checks the length of ValidatorUpdates internally before processing, ensuring that it only proceeds when there are valid updates. In this case, nil, nil is a valid response for slices. Therefore, no additional action is required in this case."

---

## OM2-14 Miscellaneous General Comments  
### Asset: All contracts  
**Status**: Resolved: See Resolution  
**Rating**: Informational  

**Description**  
This section details miscellaneous findings discovered by the testing team that do not have direct security implications:

1. **Gas Optimisations**  
   **Related Asset(s)**: Quorum.sol  
   The `verify()` function declares `prev` as memory even though it is not modified in the function.

   ```solidity
   for (uint256 i = 0; i < sigs.length; i++) {
       sig = sigs[i];
       if (i > 0) {
           XTypes.SigTuple memory prev = sigs[i - 1];
           // ...
       }
       // ...
   }
   ```

   Change the declaration of `prev` from memory to calldata to save gas.

2. **Typos In Natspec**  
   **Related Asset(s)**: OmniPortalStorage.sol, XTypes.sol, IOmniPortal.sol, OmniPortal.sol  
   There are several instances in the codebase with incorrect Natspec comments:
   - (a) The comment in OmniPortalStorage on line [80] reads:
     ```solidity
     /**
      * @notice Offset of the last outbound XMsg that was sent to destChainId in shardId
      * Maps destChainId -> shardId -> offset.
     */
     mapping(uint64 => mapping(uint64 => uint64)) public inXMsgOffset;
     ```
     Replace mentions of `destChainId` with `sourceChainId`.
   
   - (b) The comment in XTypes.sol on line [45] mentions the BlockHeader struct field is `sourceChainId`, when it should be `consensusChainId`.
     ```solidity
     * @custom:field sourceChainId Chain ID of the Omni consensus chain
     ```
     Replace `sourceChainId` with `consensusChainId`.
   
   - (c) The comments at the following locations indicate that the first byte of `shardId` is the `confLevel`:
     - i. IOmniPortal.sol on line [36]
     - ii. XTypes.sol on line [15]
     - iii. OmniPortal.sol on line [135]
     Correct the comments to indicate that `confLevel` is the last byte of `shardId`.

3. **Missing Input Validation**  
   **Related Asset(s)**: Staking.sol, OmniBridgeL1.sol, OmniGasPump.sol, OmniPortal.sol  
   There are several instances in the codebase with missing input validation:
   - (a) The following functions do not have zero address checks:
     - i. `OmniBridgeL1.initialize()`: Does not check that `omni` is not the zero address.
     - ii. `OmniGasPump.withdraw()`: Does not check that `to` is not the zero address.
     - iii. `OmniGasPump.fillUp()`: Does not check that `recipient` is not the zero address.
   - (b) `Staking.delegate()` does not check that `validator` is in the allow list if it is enabled.
   - (c) `OmniPortal._setXMsgMinGasLimit()` and `_setXMsgMaxGasLimit()` do not check that `xmsgMinGasLimit <= xmsgMaxGasLimit` when the values are set. If `xmsgMinGasLimit` is accidentally set to a value greater than `xmsgMaxGasLimit`, there would be no valid range, and `xcall()` will always revert.
   Add the input validation checks to the relevant functions.

### Recommendations  
Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

### Resolution  
The Omni team has implemented fixes for the issues above in PRs #2143 and #1886.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Omni Network |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma_Prime_Omni_Network_Omni_Chain_2_Security_Assessment_Report_v2_1.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma_Prime_Omni_Network_Omni_Chain_2_Security_Assessment_Report_v2_1.pdf

### Keywords for Search

`vulnerability`

