---
# Core Classification
protocol: Taiko
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36020
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/taiko/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/taiko/review.pdf
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

protocol_categories:
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Security Council Is Owner Of TaikoTimelockController Proxy Allowing Upgrades

### Overview

See description below for full details.

### Original Finding Content

## Description

According to the deploy scripts, the owner of the `TaikoTimelockController` contract will be the security council. The `TaikoTimelockController` is an upgradable proxy, which can be upgraded instantly by the owner. Therefore, it is possible for the security council to upgrade the timelock controller without any governance voting or delays. 

The `TaikoTimelockController` could be upgraded, through the proxy, to a contract without any delays and ignores voting from the `TaikoGovernor` contract. The issue is important since `TaikoTimelockController` is the owner of most other contracts in the system, such as `TaikoL1`. Setting a malicious contract as the controller would allow making arbitrary changes to the protocol and draining all funds in the bridge.

## Recommendations

It is recommended to have the `TaikoTimelockController` own itself. This enforces at least the minimum delay required to elapse before a proxy upgrade.

## Resolution

The development team have opted not to fix this issue. Instead, the initial owner will be the security council. After a period of time when the development team is happy with the security maturity of the protocol, they may transfer ownership to the `TaikoTimelockController`.

## TKO-26 Miscellaneous General Comments

- **Asset**: All contracts  
- **Status**: Resolved: See Resolution  
- **Rating**: Informational  

This section details miscellaneous findings discovered by the testing team that do not have direct security implications:

1. **Reachable assert Statement**  
   - **Related Asset(s)**: `L1/verifiers/PseZkVerifier.sol`  
   There is an assert statement on line `[75]` of `PseZkVerifier.sol` which can be reached if an invalid proof is supplied. The following assert will be triggered when a prover supplies a `pointProof` and `blobUsed = false`. While it is not the happy path and the transaction should revert for this case, it is desirable to revert with an error message. This will reduce the gas cost for users and provide an explanation as to why.
   ```solidity
   assert(zkProof.pointProof.length == 0);
   ```
   Consider changing the assert statement to a revert with an error message.

2. **Events Declared But Never Used**  
   - **Related Asset(s)**: `bridge/Bridge.sol`  
   The events `SignalSent` and `DestChainEnabled` are declared but never used. If not needed, remove the unused events.

3. **Optimistic Proofs Denoted By Default Address**  
   - **Related Asset(s)**: `L1/libs/LibProving.sol`  
   The verifier address for optimistic proofs is denoted by `address(0)` which is also the default returned by values not set in Solidity. This could lead to bypassing proofs if future verifiers are not set up correctly such as not being set in the `AddressManager`, such mistakes might be difficult to notice at first due to the fact the system will misinterpret the missing verifier entry as an optimistic proof and the call to `proveBlock()` would succeed. The proving system should first check for an optimistic proof, then if one is not found it can revert should `resolver.resolve()` return the zero address.

4. **Typos**  
   - **Related Asset(s)**: `contracts/*`  
   Typos were noticed in some file, these should be corrected for clarity:
     - Line `[198]` of `LibProposing.sol`: "alghouth" should be "although".
     - Line `[245]` of `LibProposing.sol`: "shall choose use extra" should be "should choose to use extra".
     - Line `[47]` of `SgxVerifier.sol`: "timstamp" should be "timestamp".
     - Line `[16]` of `L1/hooks/AssignmentHook.sol`: "variﬁcation" should be "veriﬁcation".
   Review noted areas and make alterations as seen fit.

5. **LibRLPReader Can Only Parse Lists Shorter 32 Elements**  
   - **Related Asset(s)**: `thirdparty/LibRLPReader.sol`  
   `LibRLPReader.sol` can only parse lists smaller than `MAX_LIST_LENGTH` which is currently set to 32. `LibRLPReader.sol` is used to parse MPT proofs; as such, if a proof is longer than 32 nodes it will not be able to be verified. This would require a very large MPT, however (impossible considering gas limits), and is thus very unlikely. Consider removing or increasing `MAX_LIST_LENGTH`.

6. **Unnecessary Functions in Some Contracts**  
   - **Related Asset(s)**: `signal/SignalService.sol & common/AddressManager.sol`  
   The `SignalService` contract inherits from `AuthorizableContract` and this latter inherits from `EssentialContract` which also inherits from `OwnerUUPSUpgradable`. So, the contract `SignalService` has the functions `pause()` and `unpause()` which are not necessary as the modifiers `whenPaused` and `whenNotPaused` are never used in `SignalService`.  
   The contract `AddressManager` inherits from `OwnerUUPSUpgradable`, so `AddressManager` has the `pause()` and `unpause()` functions which are not necessary as the modifier `whenNotPaused` is never used in `AddressManager`. Change the design of inheritance so that the contracts don’t have unnecessary functions. This would also avoid extra bytecodes and save deployment costs.

7. **sendEther() With Zero Amount**  
   - **Related Asset(s)**: `bridge/Bridge.sol & tokenVaults/ERCxxxVault.sol`  
   In the function `Bridge.processMessage()`, it is possible that the call `refundTo.sendEther(refundAmount)` on line `221` is made with `refundAmount == 0`. For each `receiveToken()` function of the different `ERCxxx` vaults, the call `_to.sendEther(msg.value)` is made without checking the `msg.value`, which could be 0. To avoid unnecessary external calls and potentially save gas, consider checking that the amount argument used in `sendEther()` is greater than 0.

8. **Duplicate Comment**  
   - **Related Asset(s)**: `thirdparty/LibMerkleTrie.sol`  
   `_getSharedNibbleLength()` has a duplicated NatSpec comment. Remove the duplicate comment to improve readability.

9. **Missing Comments**  
   - **Related Asset(s)**: `thirdparty/LibBytesUtils.sol`, `thirdparty/LibUint512Math.sol & thirdparty/LibRLPReader.sol`  
   Some functions have functionality or edge cases that are undocumented and may be unexpected:
     - `LibUint512Math.add()` does not revert when an overflow occurs.
     - `LibBytesUtils.toBytes32()` will align to the left if the input is smaller than 32 bytes. For example: input `0xff` will return `0xff00...00`.
     - `LibRLPReader.readBytes32()` will align to the right for an input smaller than 32 bytes.
     - `LibRLPReader.readAddress()` will return `address(0)` on any input with a length of 1, regardless of the input's value.
   It is recommended to mention these edge cases in comments to avoid future issues.

10. **High Mainnet Gas May Lead To Degraded Network Performance**  
    - **Related Asset(s)**: `L1/*`  
    As Taiko settles on the Ethereum Mainnet and does so in a decentralized manner, it is sensitive to gas price fluctuations. ETH deposits, for example, are only processed once a new block is proposed. Therefore, if Layer 1 gas becomes very expensive, depositing could become impossible as proposers cease to publish `proposeBlock()` transactions due to it not being profitable. This can be further exacerbated by the max deposit queue size of 1024 deposits, meaning that if this cap is reached, all further attempts to queue a deposit will revert. Likewise, other actions such as proving or verifying blocks may also become too expensive gas-wise for third-party actors to run, leading to degraded performance for users transacting on Taiko.  
    Inform users of Taiko limitations and best practices during times of high Layer-1 congestion. Determine if it is worthwhile for the Taiko team to run their own proposer & prover set that can maintain the network performance at a loss during high congestion periods.

11. **Comments Link To Broken URLs**  
    - **Related Asset(s)**: `thirdparty/*`  
    Some files have comments that contain broken links, such as `LibBytesUtils.sol` linking to the optimism repository which no longer works. It is recommended to replace these broken links with the updated version, e.g., the optimism-legacy repository.

12. **Confusing Comments Or Variable Names**  
    - **Related Asset(s)**: `L1/gov/TaikoGovernor.sol`, `L1/tiers/TaikoA6TierProvider.sol & L1/provers/Guardians.sol`  
    Some variables or comments are misleading and could be made clearer, such as:
      - On line `[86]` of `TaikoGovernor.sol`, the comment refers to "proposer"; however, as Taiko also uses this term to mean block proposers, it is advised to clearly state the votes make a voter become a vote proposer for the governance system, not a block proposer.
      - Each tier in `TaikoA6TierProvider.sol` has its own `maxBlocksToVerify` field which is used when verifying after proving a block. This is not used when proposing blocks, which use the tier agnostic `config.maxBlocksToVerifyPerProposal`. The tier field should have its name made clearer such as `maxBlocksToVerifyPerProof` to emphasize this.
      - `Guardians.setGuardians()` makes use of arrays called `guardians` and `_guardians`. Having these arrays with the same type increases the likelihood of errors in future alterations. It is advised to differentiate the arrays by more than one character, such as renaming `_guardians` to `newGuardians`.  
    Review noted areas and delete redundant code to save on deployment costs if deemed worthwhile.

13. **Redundant Code**  
    - **Related Asset(s)**: `L1/*`  
    Some lines of code are redundant and can be deleted. For example:
      - Lines `[85-87]` of `LibVerifying.sol` contain inequalities where we have `x < 0` for an unsigned integer `x` which will never return true. Likewise, `config.ethDepositMaxFee >= type(uint96).max` from line `[89]` is redundant in light of the stronger condition included on line `[90]`: `config.ethDepositMaxFee >= type(uint96).max / config.ethDepositMaxCountPerBlock`.
      - For `TaikoGovernor.sol` and `TaikoTimelockController.sol`, only parent contracts in proxies need the storage `_gap` variable; in these contracts, it serves no purpose.
      - In `Guardians.sol` line `[46]` contains `_minGuardians == 0` which is redundant; the second check covers this because line `[42]` ensures `guardians.length >= 5`, hence `_minGuardians < _guardians.length / 2` is equal or stronger than `_minGuardians < 2`.
      - In `LibProving.sol` on line `[170]`, the condition `proof.tier < meta.minTier` is redundant as the condition that comes directly after it coupled with the check on line `[164]` ensures this condition is already matched.  
    Review noted areas and delete redundant code to save on deployment costs if deemed worthwhile.

14. **No Cap For Amount Of ETH Deposits**  
    - **Related Asset(s)**: `L1/libs/LibVerifying.sol`  
    A stronger condition is suggested for `ethDepositMaxCountPerBlock` in `isConfigValid()` as currently it has no cap and cannot be changed once set without moving to new proxy logic. If the value is set too high, it would be possible for all ETH deposits into Taiko to become halted as if the deposit queue grew to such a size where any block proposing reverted. Furthermore, as deposits are processed as part of the block proposal call, it would also freeze any future block proposals for Taiko until the proxy migrated to a new implementation. Consider adding an upper bound check to `ethDepositMaxCountPerBlock` in `isConfigValid()`. Alternatively, verify the config values have been set correctly after deployment.

15. **Total Supply Of TKO Token Difficult To Determine**  
    - **Related Asset(s)**: `L1/TaikoL1.sol`, `L1/libs/LibVerifying.sol & L1/libs/LibProving.sol`  
    In the Taiko system, TKO bonds are taken for various actions and stored in the `TaikoL1.sol` contract. If the prover performs an action incorrectly, they can lose their TKO bond, some of which is burnt. This burning occurs simply by leaving the TKO balance unallocated in the `TaikoL1.sol` contract.  
    This mechanism makes it difficult for third-party organizations to determine the true liquid total supply of TKO as the `TaikoL1.sol` contract both holds tokens awaiting return to provers and those considered burnt and out of the token supply. Furthermore, leaving burnt tokens in an upgradable contract is not advisable for security reasons; it is possible a future vulnerability allows a user to then drain these burnt tokens, which would cause large ecosystem issues once sold.  
    Either burnt TKO tokens should be sent to a recognizable burn address such as `address(0)` or a record of the total burnt tokens should be maintained and used to prevent these burnt tokens from being transferred again.

16. **Errors Missing From File**  
    - **Related Asset(s)**: `L1/libs/LibProposing.sol`  
    On line `[38]` it states “Warning: Any errors defined here must also be defined in `TaikoErrors.sol`.”; however, the errors `L1_TXLIST_OFFSET` and `L1_TXLIST_SIZE` are not included in `TaikoErrors.sol`. Ensure all errors included in `LibProposing.sol` are present in `TaikoErrors.sol`. Note that there are two unused errors, `L1_TXLIST_OFFSET_SIZE` and `L1_TXLIST_TOO_LARGE` in `TaikoErrors.sol`.

17. **Unused Errors**  
    - **Related Asset(s)**: `L1/TaikoErrors.sol`  
    The following errors are not used and can be safely removed:
    - `L1_INSUFFICIENT_TOKEN`
    - `L1_INVALID_ADDRESS`
    - `L1_INVALID_AMOUNT`
    - `L1_TXLIST_OFFSET_SIZE`
    - `L1_TXLIST_TOO_LARGE`

18. **Unused Events**  
    - **Related Asset(s)**: `L1/TaikoEvents.sol`  
    The following events are not used and can be safely removed:
    - `TokenDeposited`
    - `TokenWithdrawn`
    - `TokenCredited`
    - `TokenDebited`

19. **Reachable Overflow**  
    - **Related Asset(s)**: `L1/hooks/AssignmentHook.sol`  
    It is possible to cause an overflow on line `[95]` of `AssignmentHook.sol`. The overflow occurs if `input.tip` is set to a value just below `2256`. The solidity compiler will have built-in overflow checking for this case and thus, when triggered, the transaction will revert.
    ```solidity
    uint256 refund;
    if (assignment.feeToken == address(0)) {
        if (msg.value < proverFee + input.tip) { //@audit proverFee + input.tip can overflow 
            revert HOOK_ASSIGNMENT_INSUFFICIENT_FEE();
        }
    }
    ```
    Consider setting a maximum bound on `input.tip`.

20. **Inaccuracy In Comment About Required Check**  
    - **Related Asset(s)**: `L1/libs/LibProving.sol`  
    The comment in the following code snippet is not correct. The check `blk.metaHash != keccak256(abi.encode(meta))` is necessary to ensure the supplied parameters for `proveBlock()` match those generated in `proposeBlock()`. Without this check, a malicious prover could change a range of fields such as `meta.isBlobUsed`.
    ```solidity
    // Check the integrity of the block data. It's worth noting that in 
    // theory, this check may be skipped, but it's included for added 
    // caution.
    if (blk.blockId != meta.id || blk.metaHash != keccak256(abi.encode(meta))) {
        revert L1_BLOCK_MISMATCH();
    }
    ```
    Remove the sentence about skipping the check.

21. **Provers May Contest Their Own Proof**  
    - **Related Asset(s)**: `L1/libs/LibProving.sol`  
    It is possible for a prover to contest their own state transition. The malicious user would lose a portion of their bond depending on which root ends up being correct. Thus, it is not an economically viable attack. Consider preventing the prover from contesting their own transition.

## Recommendations

Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

## Resolution

The development team have addressed issues where appropriate in PRs #15600 and #15605.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Taiko |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/taiko/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/taiko/review.pdf

### Keywords for Search

`vulnerability`

