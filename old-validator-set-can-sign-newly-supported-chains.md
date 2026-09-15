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
solodit_id: 53654
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma%20Prime%20-%20Omni%20Network%20-%20Omni%20Portal%20-%20Security%20Assessment%20Report%20-%20v2.1.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma%20Prime%20-%20Omni%20Network%20-%20Omni%20Portal%20-%20Security%20Assessment%20Report%20-%20v2.1.pdf
github_link: none

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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Old Validator Set Can Sign Newly Supported Chains

### Overview


This bug report discusses an issue in the OmniPortal contract where a new source chain can be vulnerable to a long-range validator set attack. This is because the contract allows submissions from older validator sets, which can fabricate and sign false messages. To fix this, the report recommends preventing submissions from source chains with a pre-initialized variable called `inXStreamValidatorSetId`. The issue has been resolved in two PRs (#1133 and #1212) by adding a new function to set the `inXStreamValidatorSetId` for new source chains and implementing a constant cutoff to restrict long-range attacks.

### Original Finding Content

## Description

When a new source chain is supported, the `attestationRoot` of XMsgs from that chain can be signed by an older `valSetId`. The function `xsubmit()` checks that the `valSetId` that has signed the `attestationRoot` is equal to or newer than the last `valSetId` that signed the last `attestationRoot` of an XSubmission from the same source chain:

```solidity
OmniPortal.sol
176 uint64 lastValSetId = inXStreamValidatorSetId[xsub.blockHeader.sourceChainId];
178 // check that the validator set is known and has non-zero power
require(validatorSetTotalPower[valSetId] > 0, "OmniPortal: unknown val set");
180
// check that the submission's validator set is the same as the last, or the next one
182 require(valSetId >= lastValSetId, "OmniPortal: old val set"); //@audit lastValSetId is zero for new or non-existent chains
```

However, when a new source chain is supported, the `inXStreamValidatorSetId` corresponding to this new chain would be pre-initialized to zero, allowing submissions from older validator sets to still be valid. 

This makes every existing OmniPortal vulnerable to a long-range validator set attack where an older and exited validator set colludes to fabricate and sign false `attestationRoots` and XMsgs from the newly supported source chain. Additionally, this issue also persists with chains that are not yet supported or non-existent, since `inXStreamValidatorSetId` is also zero for these chains. Due to OMP-13, it would be possible for an old validator set to forge messages from any chain.

The old validator set creates a `XSubmission` which has a non-existent `sourceChainId`. Therefore, `inXStreamValidatorSetId[xsub.blockHeader.sourceChainId]` is zero. Then the attacker adds a message with a different `sourceChainId`, say the Omni chain ID. This would allow them to make admin messages such as `addValidatorSet()`.

## Recommendations

To resolve the issue, prevent submissions from source chains where `inXStreamValidatorSetId` is zero. Since Solidity pre-initializes variables to zero, the OmniPortal contract would need to set the `inXStreamValidatorSetId` for newly supported source chains to the initial `valSetId` in the `initialize()` function. This could be achieved by adding a function similar to `addValidatorSet()` that updates the `inXStreamValidatorSetId` of a chain. This function can also be called via a broadcasted system call.

## Resolution

The issue has been resolved in PR #1133. The OmniPortal contract now has a new function `initSourceChain()` that can only be called by the `XRegistry` contract. This function sets the `inXStreamValidatorSetId` of the new `srcChainId` to `inXStreamValidatorSetId[omniChainId]`, and this latter is set to the `valSetId` during initialization. Additionally, the `xsubmit()` function now checks that `inXStreamValidatorSetId` of the source chain of the submission is greater than zero. Note that `valSetId` is not checked during initialization and it could be initialized to zero. So, we recommend adding a check to `valSetId` in the `initialize()`.

Further updates have been added in PR #1212. The additional updates require the validator set to be within a constant `XSUB_VALSET_CUTOFF` of the most recent validator set. The constant is currently set to 10, thereby restricting long-range attacks to the 10 most recent validator sets.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Omni Network |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma%20Prime%20-%20Omni%20Network%20-%20Omni%20Portal%20-%20Security%20Assessment%20Report%20-%20v2.1.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma%20Prime%20-%20Omni%20Network%20-%20Omni%20Portal%20-%20Security%20Assessment%20Report%20-%20v2.1.pdf

### Keywords for Search

`vulnerability`

