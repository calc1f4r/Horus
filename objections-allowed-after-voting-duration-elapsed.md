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
solodit_id: 19460
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

Objections Allowed After Voting Duration Elapsed

### Overview

See description below for full details.

### Original Finding Content

## Description
LDO holders can submit a “late” objection to a motion, where its duration has already elapsed (provided the motion has not yet been enacted and deleted). This may introduce some risk of front-running abuse, where a malicious whale slightly wastes the enacting account’s gas by waiting for the `enactMotion()` transaction to be released before front-running an objection sufficient to reach the threshold.

## Recommendations
Consider requiring that `objectToMotion()` can only succeed for open motions whose voting duration has yet to elapse (the opposite of the check in `enactMotion()` at line [104]).

## Resolution
The Lido team has acknowledged the issue and deemed there to be sufficient risk mitigation without code changes. Any exploit would require the attacker to control a similar amount of LDO as for LET-02, and also pay higher gas fees to reliably front-run the enacting account. If abused, the Lido DAO can increase the objections threshold such that the attack becomes increasingly economically infeasible (if it were not already).

The Lido team also points out that the existing functionality is useful in scenarios where the motion can no longer be enacted successfully (e.g. due to some conflicting state change). Here, the smaller threshold of LDO holders can clean up (delete) the outstanding motion without resorting to an expensive Aragon DAO vote. The testing team also notes that the gas costs alone expended to continually execute this attack would likely greatly outweigh any impact on the entity enacting motions (not to mention the large LDO prerequisite).

## LET-06 EVMScriptPermissions Gas Efficiency Considerations
**Asset contracts/EVMScriptFactoriesRegistry.sol & contracts/libraries/EVMScriptPermissions.sol**  
**Status:** Closed: See Resolution  
**Rating:** Informational  

## Description
The current implementation of factory permissions introduces efficiency and complexity tradeoffs that may be undesirable, depending on the usual number of scripts associated with each factory, and the expected number of calls in associated scripts. Each EVMScript Factory registered with the EasyTrack system has an associated set of permissions restricting which contract functions (“methods”) may be called in their scripts. These are represented in the form of a series of (bytes20 address, bytes4 function_selector) tuples, concatenated into a bytes value.

Note that, for the purposes of EasyTrack, an EVMScript is simply a series of external contract calls. The current implementation is most problematic with regards to gas efficiency when a factory has a large permissions set, associated scripts involve many calls, and the associated motions are enacted regularly.

Consider the following points regarding the current implementation:
1. Permissions lookup via `_hasPermission()` occurs in O(n) time and gas (where n = number of permissions associated with that factory).
2. To validate a script containing m calls via `canExecuteEVMScript()` will take O(n × m) time and gas.
3. The entire set of permissions is always loaded from storage, even if the relevant permission is the first one in the list.

The current implementation appears to prioritize storage space efficiency, which is most pronounced when the permission set contains only one permission tuple (the entire bytes value can be packed into a single storage slot), or many tuples (it is only for values with 4 or more tuples that the space packing becomes more efficient than the more simply encoded `bytes24[]`).

The current implementation may be often reasonable, as storage access costs can usually heavily outweigh other execution costs. However, ensure these other scenarios are considered:

### A large permission set and large script:
For a large script with distinct calls, we can expect that the entire permission set would need to be loaded from storage (so we can assume all permissions are available via `bytes memory` or `bytes24[] memory`). If gas efficiency were a significant concern, an implementation could improve lookup from O(n) by relying on ordering of permissions to perform a binary search in O(log n). However, because Solidity includes no “builtin” memory collections with better than O(n) lookup, this would involve more complicated and potentially error-prone logic that would be less efficient for small permissions sets.

### A large permission set and a small script:
(Or also a larger script containing only repeated calls to the same method.) Loading the entire permissions set into memory can dominate in this case, particularly if regularly executed. A more efficient implementation here could involve mappings such that only a single `SLOAD` is involved (e.g. `address => bytes` instead of the tuple, with the bytes containing concatenated `bytes4` function selectors).

### Permission sets usually containing 2-3 tuples and not often used:
Here, gas is less of a concern, and it may be worth considering a more gas expensive but simple solution that avoids the technical complexity and risk potential associated with the low level assembly needed to handle the permissions decoding.

## Recommendations
Ensure that the comments are understood and acknowledged, and consider implementing any relevant suggestions as appropriate for the expected use-case. Also take into account the costs associated with needing to deploy an updated implementation if this use-case changes drastically.

## Resolution
The Lido team has acknowledged this and confirmed that the tradeoffs described were carefully considered for the current `EVMScriptPermissions` implementation, which is intentionally designed to minimize gas use for the current factory implementations. Each of these initial factories only requires a single permission entry, and the resulting EVMScripts only contain a small number of function calls. Should the frequently executed scripts change such that the existing library implementation is inefficient, it can be updated (replaced) as needed.

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

