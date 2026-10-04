---
# Core Classification
protocol: The Graph Timeline Aggregation Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32996
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/thegraph-timeline-aggregation-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Front-Running redeem Can Prevent Indexers From Receiving Rewards for Allocations

### Overview


The `redeem` function in `Escrow.sol` allows Indexers to receive query rewards by submitting a signed Receipt Aggregate Voucher (RAV) and `allocationIDProof`. However, anyone with knowledge of a valid `signedRAV` and `allocationIDProof` can call `redeem` and receive the rewards, regardless of whether they are the rightful owner. This is because the function only checks the validity of the contents and signature, but not the caller's identity. This can lead to an attacker front-running an Indexer's transaction and receiving the rewards instead. The proposed solution is to use the Indexer's address from the `allocationID` to prevent this issue. The bug has been fixed in a recent update.

### Original Finding Content

The [`redeem`](https://github.com/semiotic-ai/timeline-aggregation-protocol-contracts/blob/d8795c747d44da90f7717b3db9a08698e64a9b2f/src/Escrow.sol#L366) function in `Escrow.sol` enables Indexers to receive query rewards by submitting a signed Receipt Aggregate Voucher (RAV) and `allocationIDProof`. However, anyone who knows the contents of a valid `signedRAV` and `allocationIDProof` can call `redeem` regardless of whether the proof and signed RAV belong to them. This is because `redeem` only checks that the contents and signature of the passed-in `signedRAV` and `allocationIDProof` are valid, but does not check that the caller is the originator of the signatures and calldata. Additionally, the function uses the caller to [determine the amount of GRT](https://github.com/semiotic-ai/timeline-aggregation-protocol-contracts/blob/d8795c747d44da90f7717b3db9a08698e64a9b2f/src/Escrow.sol#L377-L384) that will be sent as the query reward to the `Staking` contract.


Consequently, a malicious user who knows a valid `signedRAV` and `allocationIDProof` can call `redeem`, which, if the user does not have a GRT balance in the `Escrow` contract, will result in zero GRT being rewarded for an `allocationID`. This also prevents future calls to `redeem` that correspond to the same `allocationID` as the ID will have been [marked as used](https://github.com/semiotic-ai/timeline-aggregation-protocol-contracts/blob/d8795c747d44da90f7717b3db9a08698e64a9b2f/src/AllocationIDTracker.sol#L65) in the `AllocationIDTracker` as part of the [`redeem` function's logic](https://github.com/semiotic-ai/timeline-aggregation-protocol-contracts/blob/d8795c747d44da90f7717b3db9a08698e64a9b2f/src/Escrow.sol#L390-L394). This effectively prevents an Indexer from being rewarded for a given `allocationID`. The following example outlines a proposed attack against an Indexer:


1. An Indexer calls `redeem` with their `signedRAV` and `allocationIDProof` on the Ethereum Mainnet.
2. A malicious user sees the proposed transaction in the public mempool, creates a duplicate transaction using the now public information, and pays to front-run the Indexer's transaction.
3. The malicious user's call to redeem happens first, and because they do not have any GRT balance in the `Escrow` contract, zero GRT will be awarded to the `allocationID` via the [collect](https://github.com/semiotic-ai/timeline-aggregation-protocol-contracts/blob/d8795c747d44da90f7717b3db9a08698e64a9b2f/src/Escrow.sol#L395) call. Note that both `redeem` and `collect` (in `Staking.sol`) will pass even though zero GRT is awarded to an Indexer. Additionally, this uses the `allocationID` in the `AllocationIDTracker` contract.
4. The Indexer's redeem call happens and fails because `useAllocationID` will now revert.


Consider deriving the Indexer address to pull GRT from via the `getAllocation` function in the Staking contract instead of using the `msg.sender` as the expected address in the `redeem` function. This prevents the wrong address' `EscrowAccount` 's GRT balance from being used and always ensures that regardless of who calls `redeem`, the correct address will be used when moving GRT to the `Staking` contract.


***Update:** Resolved in [pull request #58.](https://github.com/semiotic-ai/timeline-aggregation-protocol-contracts/pull/58) The Graph's core developers stated:*



> *Thank you for finding and highlighting this critical issue. We have investigated it further and discussed a few solutions. To prevent possible front-running attacks and allow the vesting contracts to redeem, we decided to proceed with the suggested solution to use the Indexer indicated in the allocation as the receiver (i.e., obtaining the receiver address from the staking contract using `allocationID`). The associated issue can be found [here](https://github.com/semiotic-ai/timeline-aggregation-protocol-contracts/issues/31).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | The Graph Timeline Aggregation Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/thegraph-timeline-aggregation-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

