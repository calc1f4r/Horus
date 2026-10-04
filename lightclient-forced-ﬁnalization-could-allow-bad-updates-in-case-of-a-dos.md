---
# Core Classification
protocol: Succinct Labs Telepathy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21289
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-succinct-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-succinct-securityreview.pdf
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
finders_count: 3
finders:
  - Joe Doyle
  - Marc Ilunga
  - Tjaden Hess
---

## Vulnerability Title

LightClient forced ﬁnalization could allow bad updates in case of a DoS

### Overview


This bug report is about a data validation issue in the LightClient.sol contract. In periods of delayed finality, the LightClient may finalize block headers with few validators participating. If the Telepathy provers were targeted by a denial-of-service (DoS) attack, this condition could be triggered and used by a malicious validator to take control of the LightClient and finalize malicious block headers. This is because the LightClient contract typically considers a block header to be finalized if it is associated with a proof that more than two-thirds of sync committee participants have signed the header.

Exploit Scenario: Alice, a malicious ETH2.0 validator, controls about 5% of the total validator stake, split across many public keys. She waits for a sync committee period, includes at least 10 of her public keys, then launches a DoS against the active Telepathy provers. Alice creates a forged beacon block with a new sync committee containing only her own public keys, then uses her 10 active committee keys to sign the block. She calls LightClient.rotate with this forged block and waits until the sync committee period ends, finally calling LightClient.force to gain control over all future light client updates.

Recommendations: Short term, consider removing the LightClient.force function, extending the waiting period before updates may be forced, or introducing a privileged role to mediate forced updates. Long term, explicitly document expected liveness behavior and associated safety tradeoffs.

### Original Finding Content

## Security Assessment Report

## Difficulty: High

### Type: Data Validation

### Target: contracts/src/lightclient/LightClient.sol

### Description
Under periods of delayed finality, the LightClient may finalize block headers with few validators participating. If the Telepathy provers were targeted by a denial-of-service (DoS) attack, this condition could be triggered and used by a malicious validator to take control of the LightClient and finalize malicious block headers.

The LightClient contract typically considers a block header to be finalized if it is associated with a proof that more than two-thirds of sync committee participants have signed the header. Typically, the sync committee for the next period is determined from a finalized block in the current period. However, in the case that the end of the sync committee period is reached before any block containing a sync committee update is finalized, a user may call the `LightClient.force` function to apply the update with the most signatures, even if that update has less than a majority of signatures. A forced update may have as few as 10 participating signers, as determined by the constant `MIN_SYNC_COMMITTEE_PARTICIPANTS`.

```solidity
/// @notice In the case there is no finalization for a sync committee rotation, this
///         method is used to apply the rotate update with the most signatures throughout
///         the period.
/// @param period The period for which we are trying to apply the best rotate update for.
function force(uint256 period) external {
    LightClientRotate memory update = bestUpdates[period];
    uint256 nextPeriod = period + 1;
    if (update.step.finalizedHeaderRoot == 0) {
        revert("Best update was never initialized");
    } else if (syncCommitteePoseidons[nextPeriod] != 0) {
        revert("Sync committee for next period already initialized.");
    } else if (getSyncCommitteePeriod(getCurrentSlot()) < nextPeriod) {
        revert("Must wait for current sync committee period to end.");
    }
    setSyncCommitteePoseidon(nextPeriod, update.syncCommitteePoseidon);
}
```

*Figure 8.1: telepathy/contracts/src/lightclient/LightClient.sol#123–139*

## Exploit Scenario
Alice, a malicious ETH2.0 validator, controls about 5% of the total validator stake, split across many public keys. She waits for a sync committee period, includes at least 10 of her public keys, then launches a DoS against the active Telepathy provers, using an attack such as that described in `TOB-SUCCINCT-1` or an attack against the offchain prover/relayer client itself. Alice creates a forged beacon block with a new sync committee containing only her own public keys, then uses her 10 active committee keys to sign the block. She calls `LightClient.rotate` with this forged block and waits until the sync committee period ends, finally calling `LightClient.force` to gain control over all future light client updates.

### Recommendations
- **Short term**: Consider removing the `LightClient.force` function, extending the waiting period before updates may be forced, or introducing a privileged role to mediate forced updates.
- **Long term**: Explicitly document expected liveness behavior and associated safety trade-offs.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Succinct Labs Telepathy |
| Report Date | N/A |
| Finders | Joe Doyle, Marc Ilunga, Tjaden Hess |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-succinct-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-succinct-securityreview.pdf

### Keywords for Search

`vulnerability`

