---
# Core Classification
protocol: Lido Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62195
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-07-lido-finance
source_link: https://code4rena.com/reports/2025-07-lido-finance
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
finders_count: 0
finders:
---

## Vulnerability Title

[L-02] Mid-Season Merkle Root Update Invalidates Previously Valid Proofs

### Overview

See description below for full details.

### Original Finding Content


Type: Operational / Design Limitation

### Summary

In the `VettedGate` referral reward system, the on-chain contract stores a single active `merkleRoot` and verifies claims with respect to that root. If the root is updated mid-season — even without removing a legitimate referrer from the set — all proofs generated against the previous root become invalid and cannot be used to claim rewards.

This behavior is inherent to Merkle proof verification: proofs are root-specific, so any root change (due to leaf removal, addition, or re-ordering) requires distributing new proofs to all eligible participants.

While this is not a security bug, it introduces an operational dependency: off-chain systems must re-issue updated proofs to all still-eligible referrers whenever the root changes.

### Description

During a referral season, administrators may call:

in [VettedGate.sol# L291-297](https://github.com/code-423n4/2025-07-lido-finance/blob/main/src/VettedGate.sol# L291-L297):
```

vettedGate.setTreeParams(newRoot, newCid);
```

to replace the current Merkle root and CID. This may happen to ban malicious addresses or add new reward addresses. However:

* The contract does not store historical roots. and [`claimReferrerBondCurve`](https://github.com/code-423n4/2025-07-lido-finance/blob/main/src/VettedGate.sol# L265) always calls [`verifyProof`](https://github.com/code-423n4/2025-07-lido-finance/blob/main/src/VettedGate.sol# L330) against the current root.
* Because Merkle proofs are tied to a specific root, any proof generated for a previous root will become invalid after an update, even if the address remains in the new tree.

Example sequence:

1. Season starts, tree = `[NodeOperator, Stranger, AnotherNodeOperator]`.
2. Stranger reaches referral threshold.
3. Admin updates root mid-season to `[Stranger, NodeOperator]` to ban `AnotherNodeOperator`.
4. Stranger tries to claim with old proof (built for index=1 in old tree) → `InvalidProof` revert.
5. Stranger must obtain new proof (index=0 in new tree) to succeed.

This matches expected Merkle mechanics but can surprise operators if not accounted for.

### PoC

This PoC was implemented directly in the existing `VettedGateReferralProgramTest` suite, not `PoC.t.sol`, due to the low severity and straightforward nature of the issue.
```

function test_proofBreaksAfterRootUpdate_whenIndexShifts() public {
    _addReferrals();
    bytes32[] memory oldProof = merkleTree.getProof(1); // stranger's original index is 1

    MerkleTree newTree = new MerkleTree();
    newTree.pushLeaf(abi.encode(stranger)); // index now 0
    newTree.pushLeaf(abi.encode(anotherNodeOperator));
    bytes32 newRoot = newTree.root();

    vm.startPrank(admin);
    vettedGate.grantRole(vettedGate.SET_TREE_ROLE(), admin);
    vettedGate.setTreeParams(newRoot, "cid");
    vm.stopPrank();

    NodeOperatorManagementProperties memory no;
    no.rewardAddress = stranger;
    CSMMock(csm).mock_setNodeOperatorManagementProperties(no);

    // Old proof fails
    vm.expectRevert(IVettedGate.InvalidProof.selector);
    vm.prank(stranger);
    vettedGate.claimReferrerBondCurve(0, oldProof);

    // New proof works
    bytes32[] memory newProof = newTree.getProof(0);
    vm.prank(stranger);
    vettedGate.claimReferrerBondCurve(0, newProof);
}
```

Test Output:
```

Ran 1 test for test/VettedGate.t.sol:VettedGateReferralProgramTest
[PASS] test_proofBreaksAfterRootUpdate_whenIndexShifts() (gas: 1228763)
Suite result: ok. 1 passed; 0 failed; 0 skipped; finished in 69.27ms (4.04ms CPU time)
```

### Impact

* Operational: Every root change forces all still-eligible participants to obtain a new proof before claiming.
* Timing risk: If root updates occur between reaching threshold and claiming, legitimate claims can fail until new proofs are distributed.
* User experience: Users unaware of the root update may face unexpected `InvalidProof` errors.

### Recommendations

1. Document this behavior in the admin/operator playbook so off-chain systems automatically re-generate and distribute proofs upon root update.
   or
2. Consider keyed Merkle tree or index-stable design (e.g., sparse Merkle tree with address-based leaves) to minimize proof regeneration cost, though root changes will still invalidate old proofs.
   or
3. Optionally store previous root(s) temporarily and accept them for a grace period to reduce operational friction.
   or
4. A stricter on-chain safeguard could block `setTreeParams` when `isReferralProgramSeasonActive == true`, preventing mid-season root updates entirely — but this would significantly restrict operational flexibility (e.g., urgent malicious address removal) and may not be desirable in practice.

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Lido Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2025-07-lido-finance
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2025-07-lido-finance

### Keywords for Search

`vulnerability`

