---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53563
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
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

Unsafe Casting In OperatorSetLib.decode()

### Overview

See description below for full details.

### Original Finding Content

## Description

The function `decode()` will take a 32-byte `_key` as input and decode it to a 20-byte avs address and a 3-byte id. The remaining bytes are unused and may be arbitrarily set.

## OperatorSetLib.sol::decode()

```solidity
function decode(
    bytes32 _key
) internal pure returns (OperatorSet memory) {
    /// forgefmt: disable-next-item
    return OperatorSet({
        avs: address(uint160(uint256(_key) >> 96)),
        id: uint32(uint256(_key) & type(uint96).max) // @audit lossy casting here if the key has bits 136-192 set
    });
}
```

This issue is rated as informational severity as each occurrence of `decode()` occurs on keys which have been encoded by `OperatorSetLib`. Therefore, it is not possible to call `decode()` with a `_key` that has bits 136 to 192 set.

## Recommendations

- Consider performing safe casting and revert if `uint96(uint256(_key)) >= (1 << 32)`.
- Furthermore, the `& type(uint96).max` condition is not necessary when casting a `uint256` to `uint32` as any values larger than `2^32` will be truncated. Consider removing the unnecessary code.

## Resolution

The EigenLayer team has acknowledged this issue and has chosen to not implement a fix as there is no known attack vector.

## EGSL-19 Miscellaneous General Comments

**Asset:** All contracts  
**Status:** Closed: See Resolution  
**Rating:** Informational  

## Description

This section details miscellaneous findings discovered by the testing team that do not have direct security implications:

1. **Redundant Event Emission**  
   **Related Asset(s):** AllocationManager.sol  
   The `createOperatorSets()` function allows duplicate strategies within `params[i].strategies` when adding to operator sets. While the `EnumerableSet` library prevents actual duplicate entries in storage, there is potential to trigger redundant `StrategyAddedToOperatorSet` events despite no state change.
   
   ```solidity
   AllocationManager.sol::createOperatorSets()
   bytes32 operatorSetKey = operatorSet.key();
   for (uint256 j = 0; j < params[i].strategies.length; j++) {
       _operatorSetStrategies[operatorSetKey].add(address(params[i].strategies[j]));
       emit StrategyAddedToOperatorSet(operatorSet, params[i].strategies[j]);
   }
   ```
   Wrap the `add()` line in a `require()` statement to ensure there are no duplicate strategies, or check that the `params[i].strategies` array is sorted and that consecutive elements are not identical.

2. **Gas Optimisation**  
   **Related Asset(s):** DelegationManager.sol  
   In the `_undelegate()` function, consider declaring the relevant arrays outside of the for loop to save gas.

   ```solidity
   DelegationManager.sol::_undelegate()
   for (uint256 i = 0; i < strategies.length; i++) {
       IStrategy[] memory singleStrategy = new IStrategy[](1);
       uint256[] memory singleDepositShares = new uint256[](1);
       uint256[] memory singleSlashingFactor = new uint256[](1);
       // ...
   }
   ```

3. **Missing Return Value Check In _removeSharesAndQueueWithdrawal()**  
   **Related Asset(s):** DelegationManager.sol  
   `_removeSharesAndQueueWithdrawal()` does not verify that the withdrawal root is not already in the set. While withdrawalRoot overlaps should not occur due to the uniqueness of the nonce field, explicitly checking the return value improves code clarity and maintainability.
   
   ```solidity
   DelegationManager.sol::_removeSharesAndQueueWithdrawal()
   uint256 nonce = cumulativeWithdrawalsQueued[staker];
   cumulativeWithdrawalsQueued[staker]++;
   Withdrawal memory withdrawal = Withdrawal({
       staker: staker,
       delegatedTo: operator,
       withdrawer: staker,
       nonce: nonce,
       startBlock: uint32(block.number),
       strategies: strategies,
       scaledShares: scaledShares
   });
   bytes32 withdrawalRoot = calculateWithdrawalRoot(withdrawal);
   pendingWithdrawals[withdrawalRoot] = true;
   queuedWithdrawals[withdrawalRoot] = withdrawal;
   // @audit wrap this in a require statement to ensure the withdrawal root
   // is not already in the set
   _stakerQueuedWithdrawalRoots[staker].add(withdrawalRoot);
   emit SlashingWithdrawalQueued(withdrawalRoot, withdrawal, withdrawableShares);
   return withdrawalRoot;
   ```
   Consider checking the returned value is true.

4. **Inconsistent NatSpec Documentation On Whole Gwei Requirements**  
   **Related Asset(s):** EigenPodManager.sol, EigenPod.sol  
   The NatSpec for `EigenPodManager.withdrawSharesAsTokens()` states that shares must be a whole Gwei amount to avoid reverting. Similarly, `EigenPod.withdrawRestakedBeaconChainETH()` specifies that `amountWei` must also be a whole Gwei amount to prevent reverts. This requirement is no longer enforced after the slashing upgrade. Consider updating the NatSpec comments to remove the requirement for whole Gwei amounts and clarify that any sub-Gwei values are rounded off.

5. **modifyAllocations() Allows Empty params Array**  
   **Related Asset(s):** AllocationManager.sol  
   The function `modifyAllocations()` allows the function parameter `params` to be of length zero. When this is the case no allocations are modified. Consider adding a check to ensure `params.length > 0`.

## Recommendations

Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

## Resolution

The EigenLayer team has acknowledged the issues above.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf

### Keywords for Search

`vulnerability`

