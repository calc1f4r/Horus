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
solodit_id: 62656
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Easy%20Track%20(3)/README.md#1-validator-exit-status-and-valindex-not-verified
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
  - MixBytes
---

## Vulnerability Title

Validator Exit Status and `valIndex` Not Verified

### Overview

See description below for full details.

### Original Finding Content

##### Description
The `validateExitRequests` function in `SubmitExitRequestHashesUtils` verifies many aspects of an exit request—such as module and node operator ID ranges, public key length, and duplicate keys. However, it does not check whether the validator has already exited from the beacon chain or is otherwise inactive.

This creates a risk where an exit request could be redundantly submitted for a validator that has already exited, leading to wasted motion execution or unexpected behavior downstream.

There is also a missing check for the `valIndex` values in the `ExitRequestInput[]` array. Validator exit requests should be sorted in an ascending order by the `valIndex` in order to be accepted by the `ValidatorsExitBusOracle`.

##### Recommendation
We recommend adding an explicit check in `validateExitRequests` function to ensure that the validator associated with the exit request is active. We also recommend changing the check for duplicates. It is better to reduce the current check complexity by removing the logic associated with the `valPubkey` and checking instead that `valIndex` values in exit requests array are placed in a strictly ascending order - this will ensure that there are no duplicates. 

> **Client's Commentary:**
> Client: We simplified the check based on the recommendation, but skipped the proposal for validation of the validator's index and CL status. Here’s why:
> - A validator's status may change while the objection window is still open. This can cause the enactment transaction to revert on execution. The protocol assumes that validators can be requested again for exit even if the validator has already exited.
> - Providing CL proofs is expensive and complex. This significantly reduces the number of validators that can be included in a single batch request.
> - The Validator Ejector (an off-chain tool hosted by Node Operators) strictly verifies all fields in the event. If any data is invalid, it ignores the event. This mechanism protects us from unchecked data that cannot be easily verified on-chain.
>
> 
> MixBytes: We ensured the correctness of the `_exitRequests` sorting check implemented in commit `a4bbe78934bdec534c4b78871f0bdce57467eab1`, which takes into account the `moduleId`, `nodeOpId`, and `valIndex` parameters, and confirmed that this check matches the implementation in the `ValidatorsExitBusOracle._processExitRequestsList` function.


### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Easy%20Track%20(3)/README.md#1-validator-exit-status-and-valindex-not-verified
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

