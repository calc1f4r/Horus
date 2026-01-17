---
# Core Classification
protocol: AZTEC
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16739
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/aztec.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/aztec.pdf
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
finders_count: 6
finders:
  - James Miller
  - Ben Perez
  - Paul Kehrer
  - Alan Cao
  - Will Song
---

## Vulnerability Title

Replay attack and revocation inversion on conﬁdentialApprove

### Overview


A bug was discovered in the NoteRegistryManager.sol smart contract, which is used to allow third parties to spend notes on the note owner's behalf. The confidentialApprove method is used to verify that the signature giving (or revoking) permission to spend is valid and was signed by the owner. However, when verifying the signature, the _status (indicating giving or revoking of permission) is not actually tied to the signature. This means that the same signature used to revoke permission can be used to restore permission, and there is no mechanism in place to detect the resubmission of previously used signatures.

This bug can be exploited to wrongfully give or revoke permissions. For example, if an owner decides to revoke permission that was previously given to a third party, that party can resubmit either the original signature giving permission or the latest signature revoking permission (where they switch the permission back to true) and wrongfully reinstate their permission to spend notes. Additionally, another malicious party (who is neither the owner nor third party) can revoke any permission given to third parties.

In the short term, the confidentialApprove method should be updated to tie the _status value into the signature used to give/revoke permission to spend. This will also require updating signer/index.js in aztec.js to tie this value into the signature (presently, the _status value is always set to true). Additionally, state should be maintained to prevent the replay of previous signatures. In the long term, the signature scheme should be adjusted so it is not detachable in this way, in order to prevent similar replay attacks in the future.

### Original Finding Content

## Data Validation Report

## Target
NoteRegistryManager.sol

## Difficulty
Hard

## Description
The `confidentialApprove` method is used to allow third parties to spend notes on the note owner’s behalf. In the `confidentialApprove` method, there is a call to `validateSignature`, which verifies that the signature giving (or revoking) permission to spend is valid and was signed by the owner. However, when verifying the signature, the `_status` (indicating giving or revoking of permission) is not actually tied to the signature (see figure 13.1), so the same signature used to revoke permission can be used to restore permission. This problem is compounded because there is no mechanism in place to detect the resubmission of previously used signatures.

> **Figure 13.1:** The `confidentialApprove` method in `ZKAssetBase.sol`. The `_status` value is not included in the `_hashStruct` used to verify the signature.

## Exploit Scenario
This can be exploited to wrongfully give or revoke permissions. Say an owner decides to revoke permission that was previously given to a third party. That party can resubmit either the original signature giving permission or the latest signature revoking permission (where they switch the permission back to true) and wrongfully reinstate their permission to spend notes.

Further, another malicious party (who is neither the owner nor third party) can revoke any permission given to third parties. If an owner submits a signature giving permission to a third party, this malicious party can easily resubmit this signature and switch the `_status` to `false`. Again, since `_status` is not tied to the signature, they will accept this malicious submission.

## Recommendation
Short term, update `confidentialApprove` to tie the `_status` value into the signature used to give/revoke permission to spend. In order for valid signatures to work, this will also require updating `signer/index.js` in `aztec.js` to tie this value into the signature (presently, the `_status` value is always set to `true`; see Figure 13.2). In addition, we recommend maintaining state to prevent the replay of previous signatures.

> **Figure 13.2:** The `signNoteForConfidentialApprove` method in `signer/index.js`. The `status` value is always set to `true`.

Long term, adjust the signature scheme so it is not detachable in this way, in order to prevent similar replay attacks in the future.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | AZTEC |
| Report Date | N/A |
| Finders | James Miller, Ben Perez, Paul Kehrer, Alan Cao, Will Song, David Pokora |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/aztec.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/aztec.pdf

### Keywords for Search

`vulnerability`

