---
# Core Classification
protocol: Pyth Data Association Entropy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37873
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-01-pyth-entropy-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-01-pyth-entropy-securityreview.pdf
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
finders_count: 2
finders:
  - Tjaden Hess
  - Elvis Skoždopolj
---

## Vulnerability Title

Lack of contract existence check on low-level call

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: High

## Type: Data Validation

### Target: Executor.sol

## Description

The Executor contract uses a low-level call on arbitrary receivers but does not implement a contract existence check. If the call receiver is set to an incorrect address, such as an externally owned account (EOA), the call will succeed and could cause the protocol team to incorrectly assume that the attempted action has been performed.

The Executor contract is intended to execute messages that were previously transmitted and verified using the Wormhole cross-chain bridge in order to perform governance-approved actions on the receiver chain. This is done by calling the `execute` function with the appropriate encoded message, as shown in Figure 2.1.

```solidity
function execute (
    bytes memory encodedVm
) public returns (bytes memory response) {
    IWormhole.VM memory vm = verifyGovernanceVM(encodedVm);
    GovernanceInstruction memory gi = parseGovernanceInstruction(vm.payload);
    
    if (gi.targetChainId != chainId && gi.targetChainId != 0)
        revert ExecutorErrors.InvalidGovernanceTarget();
    if (
        gi.action != ExecutorAction.Execute ||
        gi.executorAddress != address(this)
    ) revert ExecutorErrors.DeserializationError();
    
    bool success;
    (success, response) = address(gi.callAddress).call(gi.callData);
    
    // Check if the call was successful or not.
    if (!success) {
        // If there is return data, the delegate call reverted with a reason or a
        // custom error, which we bubble up.
        if (response.length > 0) {
            // The first word of response is the length, so when we call revert we
            // add 1 word (32 bytes) to give the pointer to the beginning of the revert data 
            // and pass the size as the second argument.
            assembly {
                let returndata_size := mload(response)
                revert(add(32, response), returndata_size)
            }
        } else {
            revert ExecutorErrors.ExecutionReverted();
        }
    }
}
```
*Figure 2.1: The `execute` function of Executor.sol*

However, if the `gi.callAddress` parameter is mistakenly set to an EOA, the call will always succeed. Because the call to `execute` does not revert, the protocol team may assume that important actions have been performed, even though no action has been executed.

## Exploit Scenario

Alice, a Pyth team member, submits a cross-chain message through Wormhole to execute a time-sensitive transaction but inputs the wrong `gi.callAddress`. She calls `execute` with the message data, which passes because the call is made to an EOA. Alice believes the intended transaction was successful and only realizes her mistake after it is too late to resubmit the correct message.

## Recommendations

- **Short term:** Implement a contract existence check before the low-level call to ensure that the call reverts if the receiver is an EOA.

- **Long term:** Carefully review the Solidity documentation, especially the “Warnings” section about using low-level call operations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Pyth Data Association Entropy |
| Report Date | N/A |
| Finders | Tjaden Hess, Elvis Skoždopolj |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-01-pyth-entropy-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-01-pyth-entropy-securityreview.pdf

### Keywords for Search

`vulnerability`

