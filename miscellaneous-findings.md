---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19463
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
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

Miscellaneous Findings

### Overview

See description below for full details.

### Original Finding Content

## Description

This section details miscellaneous findings discovered by the testing team that do not have direct security implications:

1. Although the specification (specification.md) discusses upgradability, it makes no direct mention of the ContractProxy ERC1967 proxy.

2. Minor Gas Optimizations:
   - In `BytesUtils.sol`, the `div` can be replaced with the more gas-efficient `shr` instruction (and an appropriately adjusted value), though the real-world gas savings would be minimal unless used in bulk.
   - Duplicate entries in a permissions list are allowed by `EVMScriptFactoriesRegistry.addEVMScriptFactory()`, allowing unnecessary gas costs when processing associated scripts. This is noted purely to ensure awareness. Any deduplication is likely not worth the additional gas costs, particularly as the entity proposing new factories to the DAO is likely also involved in enacting associated motions.

3. List of Typos:
   - At `RewardProgramsRegistry.sol:86`, `_gerRewardProgramIndex` should be `_getRewardProgramIndex`.
   - In `utils/evm_script.py`, the function `encode_call_script` is more appropriately named `encode_calls_script` (to reflect the `CallsScript.sol` naming).
   - At `AddRewardProgram.sol:65`, the NatSpec comment for `decodeEVMScriptCallData()` is incomplete (shown below):
     ```
/// @param _evmScriptCallData Encoded tuple : ( address _rewardProgram )
     ```
     According to the spec and code, this should be `(address _rewardProgram, string memory _title)`.
   - The `EvmScriptExecutor.sol` file should be renamed to `EVMScriptExecutor.sol` to match the capitalization of its contained contract.

4. Comment on `EasyTrackStorage` state variable ordering: Note that the current organization of state variables within `EasyTrackStorage` is unsustainable with future upgrades. Although it is more legible to organize into different sections, this will break down if more state variables are added (because these need to be added to the bottom to retain a consistent storage layout). For example, a new variable relating to “motion setting” must be put at the bottom, not in the “motion setting” section.

5. Constructor validation and sanity checks:
   - There is no validation of `trustedCaller != 0`. Consider modifying the `TrustedCaller` constructor to include this check.
   - Consider validating the `EVMScriptExecutor.constructor()` arguments `_callsScript`, `_easyTrack`, `_voting` to check that they aren’t zero or are a contract.

6. Small, Nitpick Naming Suggestions:
   - The `EVMScriptExecutor` name could be slightly misleading. Although descriptive, the name could be misunderstood to suggest it implements the AragonOS I `EVMScriptExecutor` interface, which it does not. Consider renaming it to something like `EasyTrackScriptExecutor` to help distinguish this.
   - Consider adjusting the variable names in `RewardProgramsRegistry` to highlight that the expected `TrustedCaller` account is the `EVMScriptExecutor` instance (rather than an EOA like for the other contracts). For example, renaming the `_trustedCaller` constructor parameter to `_trustedScriptExecutor` would be more descriptive for readers.
   - In `EVMScriptPermissions._getNextMethodId()`, the `uint32` methodId local variable name is confusing and clashes with the understanding that the function returns a `bytes24` methodId. Consider renaming this to something like `functionSelector`, to highlight that it is the function selector and not the whole methodId.
   - At `EVMScriptPermissions.sol:35`, the use of the `PERMISSIONS_LENGTH` constant is somewhat incorrect. While the value of 24 is correct, the code is traversing along the evmscript, not the permissions. In this case, the length (24) is meant to represent the size of an address + `bytes4 calldata_size`, not a permission consisting of address + selector. Consider using a different constant name here, that is more descriptive for the context.
   - The `EVMScriptPermissions` contract contains a lot of “magic numbers”. Consider replacing these numbers with more descriptively named constants, to better describe how calls scripts are encoded.

7. It may be desirable to add an extra `createEVMScript()` overload to `EVMScriptCreator` that allows multiple calls to different methods. That is, one with a signature like the following:
   ```
   function createEVMScript(
       address _to,
       bytes4[] _methodIds,
       bytes[] memory _evmScriptCallData
   ) internal pure returns (bytes memory _evmScript) {
   ```
   This can save needing to deploy a modified library should a later script factory wants to execute more than one different function.

## Recommendations

Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

## Resolution

This has been addressed (primarily in PR #6) as follows:

1. `96479e8` — `ContractProxy` removed (see LET-01), so no need for inclusion in the specification.
2. 
   - `1c1e140`
   - New factories with duplicate permissions entries could be rejected by the voting DAO, like it should for the addition of a malicious factory.
3. Relevant fixes in `a37531f` & `39d635d`.
4. With `EasyTrack` no longer upgradable, the `EasyTrackStorage` contract has been removed and storage ordering is no longer relevant.
5. Resolved in `4ef4b5a` & `aee9b60`.
6. 
   - Magic numbers and relevant naming suggestions resolved in `e8a0826`.
   - The naming of `EVMScriptExecutor` will be retained. It has been chosen to highlight that `EasyTrack` uses the same format as the Aragon `CallsScript`. Renaming would involve significant changes across the project with minimal, if any, benefit.
   - `RewardProgramsRegistry` now inherits `AccessControl` instead of `TrustedCaller`.
7. `0d57936` — additional `createEVMScript()` overloads allowing the creation of scripts involving multiple calls to different functions in a contract, and multiple calls to different functions in different contracts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf

### Keywords for Search

`vulnerability`

