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
solodit_id: 62194
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

[L-01] Batch Operation Fully Reverts on Invalid Ejection Entry

### Overview

See description below for full details.

### Original Finding Content


Type: Logic Error / Design Flaw

### Summary

The `processBadPerformanceProof` function in the `CSStrikes` contract, which handles batch ejections for validators with excessive strikes, will revert the entire transaction if any single validator in the batch does not meet the required strike threshold for ejection. This “all-or-nothing” behavior is caused by a hard `revert` within the internal `_ejectByStrikes` function when it encounters an invalid entry.

Consequently, all other valid ejections within the same batch are also rolled back, preventing their timely processing. This design introduces operational inefficiency, as the entire batch must be filtered off-chain and resubmitted, potentially delaying necessary enforcement actions against poorly performing validators.

### Description

In Lido’s Community Staking Module, when processing batch validator ejections for excessive strikes, the entire batch operation will revert if any single entry in the batch fails a required precondition. This means no state changes or side effects are committed, even for entries that satisfy all requirements.

Concretely, in `CSStrikes.processBadPerformanceProof`, a list of validator keys is processed for potential ejection. For each entry, the function calls the internal `_ejectByStrikes` method, which calculates the total strikes and checks them against the configured threshold. If any entry in the batch has `strikes < threshold`, `_ejectByStrikes` reverts with `NotEnoughStrikesToEject()`. Due to EVM atomicity, this causes the entire transaction to revert, undoing all previous state changes and external calls, including for those entries that otherwise qualified for ejection.

in [`CSStrikes# L243-L245`](https://github.com/code-423n4/2025-07-lido-finance/blob/main/src/CSStrikes.sol# L243-L245):
```

if (strikes < threshold) {
    revert NotEnoughStrikesToEject();
}
```

While enforcing the threshold check on-chain is reasonable to ensure protocol-level consistency and security, reverting the entire transaction due to a single invalid entry is unnecessarily restrictive. This design can prevent the timely processing of valid entries within the batch and introduce operational friction.

### PoC

This PoC was implemented directly in the existing `CSStrikesProofTest` suite, not `PoC.t.sol`, due to the low severity and straightforward nature of the issue.

The scenario is:

* A user (or automation) submits a batch proof for ejection:

  + `[Key1 (sufficient strikes), Key2 (sufficient strikes), Key3 (insufficient strikes)]`
* `processBadPerformanceProof` begins processing.
* On reaching Key3, the function reverts, causing the entire transaction to revert.
* No validator is ejected, no penalties are recorded, and the operation must be retried offchain with a filtered list.

  
```

  function test_processBadPerformanceProof_RevertWhen_OneOfManyHasNotEnoughStrikes()
  public
  {
  // 1. Setup test environment and manual Merkle tree.
  // Set the strikes threshold for ejection to 50.
  uint256 STRIKES_THRESHOLD = 50;
  module.PARAMETERS_REGISTRY().setStrikesParams(0, 6, STRIKES_THRESHOLD);

  // Manually create leaves for success/failure scenarios.
  // Successful entry 1 (strikes > 50)
  (bytes memory pubkey0, ) = keysSignatures(1, 0);
  uint256[] memory strikesData0 = UintArr(60); // total strikes: 60
  leaves.push(Leaf(ICSStrikes.KeyStrikes({ nodeOperatorId: 0, keyIndex: 0, data: strikesData0 }), pubkey0));

  // Successful entry 2 (strikes > 50)
  (bytes memory pubkey1, ) = keysSignatures(1, 1);
  uint256[] memory strikesData1 = UintArr(70); // total strikes: 70
  leaves.push(Leaf(ICSStrikes.KeyStrikes({ nodeOperatorId: 1, keyIndex: 0, data: strikesData1 }), pubkey1));

  // Failing entry (strikes < 50)
  (bytes memory pubkey2, ) = keysSignatures(1, 2);
  uint256[] memory strikesData2 = UintArr(40); // total strikes: 40
  leaves.push(Leaf(ICSStrikes.KeyStrikes({ nodeOperatorId: 2, keyIndex: 0, data: strikesData2 }), pubkey2));

  // Build the Merkle tree with the constructed leaves.
  tree.pushLeaf(abi.encode(0, pubkey0, strikesData0));
  tree.pushLeaf(abi.encode(1, pubkey1, strikesData1));
  tree.pushLeaf(abi.encode(2, pubkey2, strikesData2));

  // Submit the Merkle root to the contract.
  bytes32 root = tree.root();
  vm.prank(oracle);
  strikes.processOracleReport(root, someCIDv0());

  // 2. Prepare proof data and mocking.
  uint256[] memory indicies = UintArr(0, 1, 2);
  ICSStrikes.KeyStrikes[] memory keyStrikesList = new ICSStrikes.KeyStrikes[](indicies.length);
  for(uint256 i = 0; i < indicies.length; ++i) {
      keyStrikesList[i] = leaves[i].keyStrikes;
  }

  (bytes32[] memory proof, bool[] memory proofFlags) = tree.getMultiProof(indicies);

  // Mock getSigningKeys calls for all entries in the loop.
  for (uint256 i = 0; i < indicies.length; i++) {
      Leaf memory leaf = leaves[indicies[i]];
      vm.mockCall(
          address(module),
          abi.encodeWithSelector(
              ICSModule.getSigningKeys.selector,
              leaf.keyStrikes.nodeOperatorId,
              leaf.keyStrikes.keyIndex,
              1
          ),
          abi.encode(leaf.pubkey)
      );
  }

  // 3. Expect revert and call the function.
  // The proof is valid, so the revert will occur inside _ejectByStrikes due to threshold failure.
  vm.expectRevert(ICSStrikes.NotEnoughStrikesToEject.selector);

  this.processBadPerformanceProof{ value: keyStrikesList.length }(
      keyStrikesList,
      proof,
      proofFlags,
      address(0)
  );

  // Because the revert happens, even the entries that should have succeeded do not have their state updated.
  }
  
```

The following log shows that `EjectorMock::ejectBadPerformer` is successfully called for the first two entries in the batch (with sufficient strikes), but the transaction ultimately reverts on the third entry (`NotEnoughStrikesToEject()`), rolling back all prior state changes as expected.
```

Ran 1 test for test/CSStrikes.t.sol:CSStrikesProofTest
[PASS] test_processBadPerformanceProof_RevertWhen_OneOfManyHasNotEnoughStrikes() (gas: 880667)
...
│   │   ├─ [285] EjectorMock::ejectBadPerformer{value: 1}(0, 0, CSStrikesProofTest: [...])
│   │   │   └─ ← [Stop]
│   │   ├─ [583] ExitPenaltiesMock::processStrikesReport(0, ...)
│   │   │   └─ ← [Stop]
│   │   ├─ [285] EjectorMock::ejectBadPerformer{value: 1}(1, 0, CSStrikesProofTest: [...])
│   │   │   └─ ← [Stop]
│   │   ├─ [583] ExitPenaltiesMock::processStrikesReport(1, ...)
│   │   │   └─ ← [Stop]
│   │   └─ ← [Revert] NotEnoughStrikesToEject()
│   └─ ← [Revert] NotEnoughStrikesToEject()
└─ ← [Stop]
Suite result: ok. 1 passed; 0 failed; 0 skipped; finished in 12.50ms (1.93ms CPU time)
```

### Impact

* This can lead to unnecessary delays in enforcement, particularly when large batches are submitted, as the entire batch must be retried after removing the invalid entry.
* When reporting large batches of poor-performing validators, a single invalid entry can cause unnecessary transaction failures and delay enforcement across the protocol.

### Recommendations

To improve operational efficiency, the contract should be updated to process all valid entries within a batch and simply skip any invalid ones, emitting an event for each skipped entry. This ensures that valid reports are handled without delay, and skipped entries can still be tracked off-chain.
```

if (strikes >= threshold) {
    ejector.ejectBadPerformer{ value: value }(
        keyStrikes.nodeOperatorId,
        keyStrikes.keyIndex,
        refundRecipient
    );
    EXIT_PENALTIES.processStrikesReport(keyStrikes.nodeOperatorId, pubkey);
} else {
	// emit event
}
```

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

