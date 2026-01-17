---
# Core Classification
protocol: Eco Inc
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46244
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/f4ef1cd6-860e-4f58-82de-09751baea324
source_link: https://cdn.cantina.xyz/reports/cantina_eco_december2024.pdf
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
finders_count: 3
finders:
  - 0xRajeev
  - 0xWeiss
  - phaze
---

## Vulnerability Title

Missing event emit for solverWhitelist initialization 

### Overview

See description below for full details.

### Original Finding Content

## Context

**File:** Inbox.sol#L54  
**Description:** When emitting events, state updates need to be tracked from the first initialization. The goal is to reach the initial state if you would look back at all the logs from a specific event. In this case, `solverWhitelist` is not tracked properly by emitting its corresponding event:

```solidity
constructor(address _owner, bool _isSolvingPublic, address[] memory _solvers) Ownable(_owner) {
    isSolvingPublic = _isSolvingPublic;
    for (uint256 i = 0; i < _solvers.length; i++) {
        solverWhitelist[_solvers[i]] = true;
    }
}
```

Given that there exists a specific event `SolverWhitelistChanged` to track its storage updates as used in `changeSolverWhitelist()`:

```solidity
function changeSolverWhitelist(address _solver, bool _canSolve) public onlyOwner {
    solverWhitelist[_solver] = _canSolve;
    emit SolverWhitelistChanged(_solver, _canSolve);
}
```

## Recommendation

Consider tracking the updates to each whitelisted solver accordingly:

```solidity
constructor(address _owner, bool _isSolvingPublic, address[] memory _solvers) Ownable(_owner) {
    isSolvingPublic = _isSolvingPublic;
    for (uint256 i = 0; i < _solvers.length; i++) {
        solverWhitelist[_solvers[i]] = true;
        emit SolverWhitelistChanged(_solvers[i], true);
    }
}
```

**Eco:** Fixed in PR 119.  
**Cantina Managed:** Reviewed that PR 119 resolves the issue as recommended.

## 4 Appendix

### 4.1 Proof Security Improvements

1. **Limit Parameters:** Add a reasonable upper bound to prevent arbitrary storage slot targeting:

```solidity
function proveWorldStateBedrock(
    uint256 chainId,
    bytes calldata rlpEncodedBlockData,
    bytes32 l2WorldStateRoot,
    bytes32 l2MessagePasserStateRoot,
    uint256 l2OutputIndex,
    bytes[] calldata l1StorageProof,
    bytes calldata rlpEncodedOutputOracleData,
    bytes[] calldata l1AccountProof,
    bytes32 l1WorldStateRoot
) public virtual {
    if (l2OutputIndex > 2**64) revert OutputIndexTooHigh();
    // ... rest of function
}
```

2. **Minimize User-Provided Proof Parameters:** Derive values internally rather than accepting untrusted input. When using user input SOLELY for additional validation, clearly name the variables as such. These should not be used to directly set state when they can also be derived:

```solidity
- bytes32 l1WorldStateRoot,
+ bytes32 expectedL1WorldStateRoot,
// ...
+ bytes32 provenl1WorldStateRoot = derivedL1WorldStateRoot();
+ require(provenl1WorldStateRoot == expectedL1WorldStateRoot, "Root mismatch");
```

3. **Separate Proof Logic:** Split the Cannon proof verification into distinct stages. E.g., the first part of the cannon proof in `_faultDisputeGameFromFactory` uses `disputeGameFactoryProofData` in order to calculate `rootClaim`, which is only ever used in the second part in `faultDisputeGameIsResolved`.

4. **Improve Variable Naming Consistency:** Use clear and consistent naming conventions for all proof-related variables:

```solidity
function proveWorldStateBedrock(
    - uint256 chainId,
    + uint256 l2ChainId,
    - bytes calldata rlpEncodedBlockData,
    + bytes calldata l2RlpBlockData,
    bytes32 l2WorldStateRoot,
    - bytes32 messagePasserStateRoot,
    + bytes32 l2MessagePasserStateRoot,
    uint256 l2OutputIndex,
    - bytes[] calldata l1StorageProof,
    + bytes[] calldata l1OutputOracleStorageProof,
    - bytes calldata rlpEncodedOutputOracleData,
    + bytes calldata rlpOutputOracleAccountData,
    - bytes32 l1AccountProof,
    + bytes32 l1OutputOracleAccountProof,
    bytes32 l1WorldStateRoot
) public {
    // ...
    - bytes memory outputOracleStateRoot
    + bytes memory outputOracleStorageRoot
}
```

The naming should:
- Clearly indicate the type of root (storage vs. state).
- Include the layer prefix (L1/L2).
- Specify the contract when applicable (MessagePasser, OutputOracle).
- Use consistent terminology across the codebase.

5. **Add Fuzz Testing:** Add property-based tests focusing on proof parameter validation:

```solidity
function testFuzz_proveWorldStateBedrock(uint256 l2OutputIndex) public {
    // Set all other parameters to fixed values
    vm.assume(l2OutputIndex != L2_OUTPUT_INDEX);
    vm.expectRevert();
    proveWorldStateBedrock(
        CHAIN_ID,
        ENCODED_BLOCK_DATA,
        L2_STATE_ROOT,
        MSG_PASSER_ROOT,
        l2OutputIndex, // Fuzzed parameter
        L1_STORAGE_PROOF,
        ENCODED_ORACLE_DATA,
        L1_ACCOUNT_PROOF,
        L1_STATE_ROOT
    );
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Eco Inc |
| Report Date | N/A |
| Finders | 0xRajeev, 0xWeiss, phaze |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_eco_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/f4ef1cd6-860e-4f58-82de-09751baea324

### Keywords for Search

`vulnerability`

