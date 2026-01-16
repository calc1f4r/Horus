---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: consensus
vulnerability_type: vote_extension_manipulation

# Attack Vector Details
attack_type: data_manipulation
affected_component: abci_vote_extensions

# Technical Primitives
primitives:
  - vote_extensions
  - validator_voting_power
  - proposer_selection
  - prepareproposal
  - processproposal
  - round_validation

# Impact Classification
severity: high
impact: consensus_manipulation
exploitability: 0.6
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - cometbft
  - abci
  - consensus
  - vote_extensions
  - validator
  
language: go
version: cosmos-sdk-v0.50+
---

## References
- [vote-extension-risks.md](../../../reports/cosmos_cometbft_findings/vote-extension-risks.md)
- [incorrect-injected-vote-extensions-validation.md](../../../reports/cosmos_cometbft_findings/incorrect-injected-vote-extensions-validation.md)
- [mismatch-between-cometbft-and-application-views.md](../../../reports/cosmos_cometbft_findings/mismatch-between-cometbft-and-application-views.md)

## Vulnerability Title

**Vote Extension Validation Bypass via Proposer-Injected Data Manipulation**

### Overview

CometBFT's ABCI++ vote extensions allow validators to attach arbitrary data to their votes during consensus. However, improper validation of vote extensions in `PrepareProposal` and `ProcessProposal` handlers enables malicious proposers to manipulate voting power calculations, inject historical round data, or cause consensus failures by exploiting the trust placed in proposer-injected data.

### Vulnerability Description

#### Root Cause

The `ValidateVoteExtensions` function relies on data injected by the proposer (`extCommit.Votes`), which can be manipulated to:
1. Misrepresent the total voting power (`totalVP`) by selectively including/excluding votes
2. Inject past round values in `CanonicalVoteExtension` construction
3. Create mismatches between CometBFT's view of validators and the application's view

The fundamental issue is that proposers have the ability to inject any vote set, including potentially malicious ones, and the calculated `totalVP` may not accurately represent the true total voting power of the network.

#### Attack Scenario

1. **Setup**: A malicious validator becomes the block proposer
2. **Manipulation**: The proposer crafts vote extensions containing:
   - Only their own votes to distort total voting power
   - Past round values to selectively include advantageous extensions
   - Altered voting power values to skew calculations
3. **Impact**: 
   - Incorrect consensus decisions leading to invalid blocks accepted
   - State machine may reject valid blocks
   - Potential chain halt if required voting power cannot be reached

#### Vulnerable Pattern Examples

**Example 1: Unvalidated Total Voting Power Calculation** [Approx Severity: HIGH]
```go
// ❌ VULNERABLE: totalVP calculated from proposer-injected votes
func ValidateVoteExtensions(
    ctx sdk.Context,
    valStore ValidatorStore,
    currentHeight int64,
    chainID string,
    extCommit abci.ExtendedCommitInfo,
) error {
    var totalVP int64
    var sumVP int64
    
    // Proposer can inject any votes they want
    for _, vote := range extCommit.Votes {
        totalVP += vote.Validator.Power  // No validation against actual validator set
        // ...
    }
    // totalVP may not represent true network voting power
}
```

**Example 2: Mismatch Between CometBFT and Application Views** [Approx Severity: MEDIUM]
```go
// ❌ VULNERABLE: Using current height data with previous height vote extensions
func (k *Keeper) voteweightedMedian(ctx sdk.Context, extCommit abci.ExtendedCommitInfo) error {
    // Vote extensions are from previous height
    for _, vote := range extCommit.Votes {
        // But voteWeight and totalBondedTokens are from current height
        voteWeight := k.GetCurrentVotingPower(vote.Validator.Address)
        // This creates a data mismatch leading to inaccurate calculations
    }
}
```

**Example 3: Past Round Injection** [Approx Severity: HIGH]
```go
// ❌ VULNERABLE: Using proposer-injected round value
func ValidateVoteExtensions(..., extCommit abci.ExtendedCommitInfo) error {
    // extCommit.Round is controlled by proposer
    cve := CanonicalVoteExtension{
        Round: extCommit.Round,  // Could be a past round value
        // ...
    }
    // Validators may incorrectly validate extensions from historical rounds
}
```

### Impact Analysis

#### Technical Impact
- Consensus decisions based on manipulated voting power
- State machine accepting invalid blocks or rejecting valid ones
- Potential for chain halts when voting power requirements not met
- Non-deterministic behavior across validators

#### Business Impact
- Complete chain halt leading to service unavailability
- Loss of trust in network consensus mechanism
- Financial losses from inability to process transactions
- Potential for double-spend if consensus is compromised

#### Affected Scenarios
- Oracle price aggregation using vote extensions
- Cross-chain message validation via vote extensions
- Any application relying on vote extension data for critical decisions
- Networks with asymmetric validator power distribution

### Secure Implementation

**Fix 1: Validate Against Actual Validator Set**
```go
// ✅ SECURE: Calculate totalVP from actual validator set, not injected data
func ValidateVoteExtensions(
    ctx sdk.Context,
    valStore ValidatorStore,
    currentHeight int64,
    chainID string,
    extCommit abci.ExtendedCommitInfo,
) error {
    // Get actual total voting power from validator store
    actualTotalVP := valStore.TotalBondedTokens(ctx)
    
    var sumVP int64
    for _, vote := range extCommit.Votes {
        // Validate each vote against actual validator
        val, found := valStore.GetValidatorByConsAddr(ctx, vote.Validator.Address)
        if foundryup
git init
forge install OpenZeppelin/openzeppelin-contracts 1inch/token-plugins=1inch/token-plugins@d71d6500e954315871bf9da070a6d9d95ac65015 1inch/solidity-utils=1inch/solidity-utils 1inch/farming=1inch/farming@da9c87962272fdcfcee79be14eb13b27387a677e mangrovedao/mangrove-core morpho-org/morpho-blue foundry-rs/forge-std nomad-xyz/ExcessivelySafeCall 

forge build --skip=Skip --sizes
forge test
 {
            continue // Skip unknown validators
        }
        // Use actual voting power, not injected value
        actualPower := val.GetConsensusPower()
        if vote.Validator.Power != actualPower {
            return errors.New("voting power mismatch")
        }
        sumVP += actualPower
    }
    
    // Check against actual total, not manipulated total
    if sumVP*3 <= actualTotalVP*2 {
        return errors.New("insufficient voting power")
    }
    return nil
}
```

**Fix 2: Validate Round Values**
```go
// ✅ SECURE: Validate round is not from a past height
func ValidateVoteExtensions(
    ctx sdk.Context,
    extCommit abci.ExtendedCommitInfo,
    expectedRound int32,
) error {
    // Ensure round matches expected current round
    if extCommit.Round != expectedRound {
        return fmt.Errorf("invalid round: got %d, expected %d", extCommit.Round, expectedRound)
    }
    // Continue with validation...
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `for _, vote := range extCommit.Votes` without validating against actual validator set
- Pattern 2: Using `vote.Validator.Power` directly without cross-referencing validator store
- Pattern 3: Using `extCommit.Round` without validation against current consensus round
- Pattern 4: Vote extension handlers that don't check `VoteExtensionsEnableHeight`
```

#### Audit Checklist
- [ ] Vote extension handlers validate voting power against actual validator set
- [ ] Round values in vote extensions are validated
- [ ] Total voting power is calculated from trusted source, not injected data
- [ ] Height mismatches between vote extensions and current state are handled
- [ ] Vote extensions are only processed after `VoteExtensionsEnableHeight`

### Real-World Examples

| Protocol | Audit Firm | Severity | Issue |
|----------|------------|----------|-------|
| Cosmos SDK | OtterSec | HIGH | ValidateVoteExtensions relies on proposer-injected data |
| Ethos Cosmos | OtterSec | HIGH | Incorrect injected vote extensions validation |
| Skip Slinky Oracle | OtterSec | MEDIUM | Mismatch between CometBFT and application views |

### Keywords for Search

`vote_extensions, ValidateVoteExtensions, ExtendedCommitInfo, PrepareProposal, ProcessProposal, voting_power, totalVP, proposer_manipulation, consensus, CometBFT, ABCI++, validator_set, round_injection`
