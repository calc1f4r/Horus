---
# Core Classification
protocol: generic
chain: optimism|arbitrum|taiko|scroll
category: zk_rollup_fraud_proof
vulnerability_type: dispute_game_manipulation|challenge_game_bypass|bond_slashing_error|output_root_attack|mips_vm_panic|bisection_attack

# Attack Vector Details
attack_type: fund_theft|chain_freeze|dos|incorrect_resolution|proof_bypass
affected_component: dispute_game|fault_game_factory|bisection_protocol|output_root|mips_vm|challenge_period|l2_output_oracle

# Technical Primitives
primitives:
  - FaultDisputeGame
  - DisputeGameFactory
  - OPFaultVerifier
  - bisection_protocol
  - MIPS_VM
  - output_root
  - state_root
  - challenge_period
  - bond_slashing
  - finalize_blocks
  - anchor_state
  - L2OutputOracle
  - prevStateRoot
  - assertion_protocol

# Impact Classification
severity: high
impact: chain_freeze|fund_theft|incorrect_resolution|unchallenged_invalid_output
exploitability: 0.25
financial_impact: high

# Context Tags
tags:
  - optimistic_rollup
  - fraud_proof
  - dispute_game
  - optimism
  - arbitrum_bold
  - taiko
  - fault_game
  - bisection
  - MIPS
  - output_root
  - challenge
  - bond

language: solidity
version: all
---

## References & Source Reports

### Dispute Game Manipulation

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Attacker Freezes Chain and Steals Deposits via Fake prevStateRoot | `reports/zk_rollup_findings/h-2-attacker-can-freeze-chain-and-steal-challenge-deposits-using-fake-prevstater.md` | HIGH | Sherlock |
| Challenger Misses Discrepancy Events → Malicious Executors | `reports/zk_rollup_findings/h-01-challenger-misses-discrepancy-events-allowing-executors-to-perform-maliciou.md` | HIGH | Multiple |
| opFaultVerifier Ingests Incorrectly Resolved Games | `reports/zk_rollup_findings/m-02-opfaultverifier-ingests-games-that-resolve-incorrectly.md` | MEDIUM | Sherlock |
| Malicious Challenger Bricks finalizeTimestamp | `reports/zk_rollup_findings/m-5-malicious-challenger-can-brick-finalizetimestamp-of-unfinalized-batches.md` | MEDIUM | Sherlock |
| MIPS VM Panic Leads to Unchallengeable Output Root | `reports/zk_rollup_findings/m-5-panic-in-mips-vm-could-lead-to-unchallengeable-l2-output-root-claim.md` | MEDIUM | Sherlock |
| Fault Game Factory DoS via Malicious L2 Block Hash | `reports/zk_rollup_findings/m-2-fault-game-factory-can-be-manipulated-to-dos-game-type-using-malicious-l2blo.md` | MEDIUM | Sherlock |

### State Root and Batch Challenge Issues

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Batches During Ongoing Challenge Avoid Being Challenged | `reports/zk_rollup_findings/m-4-batches-committed-during-an-on-going-challenge-can-avoid-being-challenged.md` | MEDIUM | Multiple |
| inChallenge Incorrectly Set to False in revertBatch | `reports/zk_rollup_findings/m-11-in-the-revertbatch-function-inchallenge-is-set-to-false-incorrectly-causing.md` | MEDIUM | Multiple |
| Initial State Root Cannot Be Challenged | `reports/zk_rollup_findings/m03-initial-state-root-cannot-be-challenged.md` | MEDIUM | Multiple |
| Pre-State Root + TX Not Unique Transition Identifier | `reports/zk_rollup_findings/m02-pre-state-root-and-transaction-may-not-uniquely-identify-transitions.md` | MEDIUM | Multiple |
| Adversary Can Make Honest Parties Unable to Retrieve Assertion Stakes | `reports/zk_rollup_findings/h-01-adversary-can-make-honest-parties-unable-to-retrieve-their-assertion-stakes.md` | HIGH | Multiple |
| Bond Burned for Correct and Ultimate Outcome | `reports/zk_rollup_findings/h-02-validity-and-contests-bond-ca-be-incorrectly-burned-for-the-correct-and-ult.md` | HIGH | Multiple |
| Chain Operator DoS Entire Cluster During Upgrade Block | `reports/zk_rollup_findings/chain-operator-can-dos-entire-cluster-during-upgrade-block-potentially-stealing-.md` | HIGH | Multiple |

---

## Vulnerability Title

**Fraud Proof and Dispute Game Vulnerabilities — State Root Manipulation, Bond Theft, and Challenge Bypass**

### Overview

Optimistic rollups rely on fraud proof games to detect and penalize incorrect state transitions. Vulnerabilities in dispute game systems allow attackers to freeze chains (by posting fake state roots that cannot be challenged), steal honest challengers' bonds, make incorrectly resolved games acceptable to the L1 verifier, or prevent legitimate finalization of batches. These bugs undermine the core security model of optimistic rollups.

---

### Vulnerability Description

#### Root Cause

1. **Event monitoring gaps**: Challengers rely on on-chain events to detect fraudulent claims. If key events are not emitted or emitted incorrectly, challengers miss malicious executions.
2. **Bisection implementation flaws**: The bisection bisection game may accept state transitions from an arbitrary `prevStateRoot` that the prover controls, allowing invalid roots to pass.
3. **OPFaultVerifier accepting wrong resolutions**: Verifier contracts that accept game outcomes without checking the game resolved correctly allow tampered dispute outcomes to become canonical.
4. **MIPS VM panic**: If a step in the fault proof MIPS VM causes a panic (instead of reverting), the instruction at that step cannot be disputed in the on-chain VM.
5. **Bond accounting errors**: Bonds for correct/honest assertions may be incorrectly slashed due to off-by-one errors or incorrect state tracking.

---

### Pattern 1: Attacker Freezes Chain via Fake prevStateRoot

**Frequency**: 2/431 reports | **Validation**: Strong (Sherlock - HIGH)

#### Attack Scenario

1. Attacker monitors the rollup for opportunities to submit a new batch with a crafted `prevStateRoot`
2. The `prevStateRoot` references a state that does not actually exist in the chain history
3. Honest challengers cannot construct a valid fault proof against a transition from a non-existent state
4. The batch cannot be challenged successfully → it gets finalized with an incorrect state
5. Attacker steals all challenge deposits from honest parties who tried to dispute it

**Example 1: Fake prevStateRoot Freezes Chain** [HIGH]
```solidity
// ❌ VULNERABLE: Rollup contract doesn't validate prevStateRoot exists in history
contract RollupChain {
    mapping(bytes32 => bool) public knownStateRoots;
    
    function commitBatch(
        bytes32 prevStateRoot,
        bytes32 newStateRoot,
        bytes calldata batchData
    ) external {
        // BUG: No check that prevStateRoot is a known valid state root!
        // Attacker provides arbitrary prevStateRoot → no valid dispute possible
        // Honest challengers cannot prove a transition from this fake root is wrong
        
        batches.push(Batch({
            prevStateRoot: prevStateRoot, // UNCHECKED
            newStateRoot: newStateRoot,
            timestamp: block.timestamp
        }));
    }
}
```

**Fix:**
```solidity
// ✅ SECURE: Enforce prevStateRoot is from the canonical chain
function commitBatch(
    bytes32 prevStateRoot,
    bytes32 newStateRoot,
    bytes calldata batchData
) external {
    // Validate prevStateRoot is the last finalized/committed state root
    require(prevStateRoot == latestCommittedStateRoot, "Invalid prevStateRoot");
    // OR validate it exists in the acknowledged state root set
    require(knownStateRoots[prevStateRoot], "Unknown prevStateRoot");
    batches.push(...);
}
```

---

### Pattern 2: Challenger Misses Discrepancy Events → Malicious Execution

**Frequency**: 1/431 reports | **Validation**: Strong (HIGH)

#### Root Cause

The challenger (fraud proof monitor) relies on on-chain events to detect discrepancies between proposed state transitions and the actual L2 computation. If the event emission logic has a bug (e.g., events only emitted on certain code paths, not all execution paths), the challenger never sees the discrepancy and the malicious state transition is not challenged.

**Example 2: Missing Event Emission on Malicious Execution Path** [HIGH]
```solidity
// ❌ VULNERABLE: Discrepancy event only emitted for one execution type
contract FraudDetector {
    event DiscrepancyDetected(bytes32 indexed claimedRoot, bytes32 indexed computedRoot);
    
    function verifyExecution(
        bytes32 claimedStateRoot,
        ExecutionType execType,
        bytes calldata input
    ) external {
        bytes32 computed = _execute(execType, input);
        if (execType == ExecutionType.STANDARD) {
            if (computed != claimedStateRoot) {
                emit DiscrepancyDetected(claimedStateRoot, computed); // Only for STANDARD
            }
        } else {
            // BUG: No event emitted for other execution types!
            // Challenger's monitor never sees the discrepancy
            _updateState(claimedStateRoot); // Malicious state accepted silently
        }
    }
}
```

---

### Pattern 3: opFaultVerifier Ingests Games That Resolve Incorrectly

**Frequency**: 1/431 reports | **Validation**: Strong (Sherlock - Optimism)

#### Root Cause

The `OPFaultVerifier` (or similar finalization contract) reads the outcome of a `FaultDisputeGame` to determine if a proposed output root should be accepted. If it doesn't verify that the game resolved to the CORRECT winner (e.g., only checks that a game exists, not that it resolved in favor of the defender), an attacker can manipulate the game outcome and have an invalid output root accepted.

**Example 3: FaultVerifier Accepts Any Resolved Game** [MEDIUM]
```solidity
// ❌ VULNERABLE: OPFaultVerifier checks game existence but not winning party
contract OPFaultVerifier {
    IDisputeGameFactory public factory;
    
    function checkWithdrawal(
        bytes32 outputRoot,
        IDisputeGame game
    ) external view returns (bool) {
        // Check game was created by the factory
        require(factory.games(outputRoot) == address(game), "Invalid game");
        // Check game is resolved
        require(game.status() == GameStatus.RESOLVED, "Game not resolved");
        
        // BUG: Never checks if game was WON by DEFENDER (correct output)
        // Attacker wins as challenger → output root should be INVALID
        // But this contract still accepts it!
        return true;
    }
}
```

**Fix:**
```solidity
// ✅ SECURE: Check game was resolved in favor of the correct party
function checkWithdrawal(
    bytes32 outputRoot,
    IDisputeGame game
) external view returns (bool) {
    require(factory.games(outputRoot) == address(game), "Invalid game");
    require(game.status() == GameStatus.RESOLVED, "Game not resolved");
    // CRITICAL: Check the game resolved in favor of the DEFENDER (output root is valid)
    require(game.winningParty() == Party.DEFENDER, "Output root was disputed and lost");
    return true;
}
```

---

### Pattern 4: MIPS VM Panic Causes Unchallengeable Output Root

**Frequency**: 1/431 reports | **Validation**: Moderate (Optimism - Sherlock)

#### Root Cause

The optimistic rollup's fault proof uses an on-chain MIPS VM to simulate a single disputed instruction. If executing that instruction in the MIPS VM causes a Solidity `panic` (e.g., array out-of-bounds, division by zero in the VM implementation), the transaction reverts entirely — the on-chain step cannot be performed. Since no one can execute this step on-chain, the entire output root claim becomes unchallengeable.

**Example 4: MIPS Step Causes Unrecoverable Panic** [MEDIUM]
```solidity
// ❌ VULNERABLE: MIPS VM can panic on certain opcode inputs
contract MIPSVM {
    function step(
        bytes calldata stateData,
        bytes calldata proof
    ) external returns (bytes32 postState) {
        MIPSState memory state = abi.decode(stateData, (MIPSState));
        
        // Certain opcodes can cause array access panics
        uint256 regIdx = state.instruction & 0x1F; // 5-bit register index
        // BUG: if regIdx > 31 (can happen due to instruction format bug)
        // → array out of bounds panic → entire call reverts
        uint256 regValue = state.registers[regIdx]; // PANIC if regIdx >= 32
        // Challenge cannot be completed if this reverts
    }
}
```

**Fix:**
```solidity
// ✅ SECURE: Validate all array indices before access; return error state instead of panicking
function step(...) external returns (bytes32 postState) {
    MIPSState memory state = abi.decode(stateData, (MIPSState));
    uint256 regIdx = state.instruction & 0x1F;
    require(regIdx < 32, "Invalid register index"); // Explicit bound check
    uint256 regValue = state.registers[regIdx];     // Safe access
    // ...
}
```

---

### Pattern 5: Bond Slashed for Correct/Honest Assertion

**Frequency**: 2/431 reports | **Validation**: Strong

#### Root Cause

In assertion-based fraud proof systems (e.g., Arbitrum BOLD), each participant puts up a bond that can be slashed if their assertion is proven wrong. If the bond slashing logic has an error (e.g., incorrectly determines the "ultimate outcome" or uses stale state during a multi-round protocol), an honest validator's bond may be slashed even though their assertion was correct.

**Example 5: Bond Slashed for Correct Assertion** [HIGH]
```solidity
// ❌ VULNERABLE: Bond slashing uses stale game state during challenge rounds
contract ArbitrumBoldChallenge {
    function slash(address party) external {
        // BUG: party.lastClaimedRoot is checked, but this can be the 
        // ORIGINAL claim (now proved correct) rather than the most recent dispute
        // In multi-round bisection, the protocol uses stale state
        if (party.lastClaimedRoot != finalizedRoot) {
            // Incorrectly slashes honest party whose original claim was correct
            _slashBond(party);
        }
    }
}
```

---

### Pattern 6: Batches Committed During Challenge Avoid Being Challenged

**Frequency**: 1/431 reports | **Validation**: Moderate

#### Root Cause

Some rollup implementations use an `inChallenge` flag to prevent commitment of new batches while a challenge is ongoing. However, if new batches CAN be committed during a challenge, those batches are not subject to challenge (the challenge window has elapsed or the challenger can't challenge while the original challenge is ongoing). Attacker submits invalid batches during the challenge window.

**Example 6: Bypassing Challenge Window via Parallel Submission** [MEDIUM]
```solidity
// ❌ VULNERABLE: inChallenge only blocks future challenges, not new commitments
contract Rollup {
    bool public inChallenge;
    
    function commitBatch(bytes calldata batchData) external {
        // Missing: require(!inChallenge) check here
        // Attacker can commit new invalid batches while old challenge is ongoing
        _commitBatch(batchData);
    }
    
    function challengeBatch(uint256 batchId) external {
        require(!inChallenge, "Challenge already ongoing");
        inChallenge = true;
        // Challenge only covers the ONE batch — new batches sneak through
    }
}
```

---

### Impact Analysis

#### Technical Impact
- Invalid state roots finalized on L1 after challenge period
- Honest challengers lose their bonds despite being correct
- Chain halted (frozen) when unchallenged invalid state prevents progression
- MIPS VM panics create permanently unchallengeable dispute game positions

#### Business Impact  
- User funds stolen via fraudulent L2→L1 withdrawals from invalid state roots
- Loss of honest validator collateral (bonds) due to protocol bugs
- L2 chain becomes effectively unusable when frozen by fake state roots
- Trust in optimistic rollup security undermined

---

### Secure Implementation

```solidity
// ✅ DISPUTE GAME SECURITY CHECKLIST:
// 1. Validate prevStateRoot is canonical before accepting batch commitment
// 2. Check dispute games resolved for the CORRECT party (defender wins = output valid)
// 3. All on-chain VM (MIPS, etc.) steps must be panic-safe — validate inputs
// 4. Implement inChallenge guard on batch commitment, not just on new challenges
// 5. Emit DiscrepancyDetected events on ALL execution paths, not just one branch
// 6. Bond slashing logic must reference the CURRENT (not stale) assertion state

// Key invariants to test:
// - ∀ honest assertions, bond is NOT slashed
// - ∀ invalid output roots, they CANNOT be finalized if challenged correctly
// - MIPS/RISCV step execution is panic-safe for all valid instruction encodings
```

---

### Detection Patterns

```
1. commitBatch() without require(!inChallenge) check
2. FaultVerifier.checkWithdrawal() not checking game.winningParty() == Party.DEFENDER
3. MIPS VM step() using array[index] without index bounds check
4. Event emission inside if/else where one branch doesn't emit the discrepancy event
5. prevStateRoot in commitBatch() not validated against canonical state root set
6. Bond slashing logic using stale state variables (not updated during multi-round bisection)
```

### Keywords for Search

`dispute game manipulation`, `fraud proof challenge bypass`, `output root manipulation`, `FaultDisputeGame`, `MIPS VM panic unchallengeable`, `bisection protocol attack`, `bond slashing correct assertion`, `opFaultVerifier wrong resolution`, `prevStateRoot fake`, `chain freeze fraud proof`, `challenge period bypass`, `inChallenge flag missing`, `Optimism fault proof`, `Arbitrum BOLD`, `assertion protocol`, `L2OutputOracle`, `challenger misses event`, `dispute game finalization bug`
