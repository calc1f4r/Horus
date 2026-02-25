---
# Core Classification
protocol: generic
chain: zksync|optimism|arbitrum|scroll
category: zk_rollup_gas_accounting
vulnerability_type: gas_theft|fee_manipulation|gas_dos|incorrect_fee_calculation|underpriced_sequencer|gas_bypass

# Attack Vector Details
attack_type: fund_theft|resource_dos|fee_bypass|underpayment
affected_component: gas_tracking|pubdata_gas|l1_l2_gas|bootloader|fee_model|bytecode_compression|batch_fees|paymaster

# Technical Primitives
primitives:
  - pubdata_cost
  - bootloader_gas
  - commitScalar
  - spentOnPubdata
  - gasleft_tracking
  - batch_fees_multiplier
  - bytecode_compression
  - L1_gas_price
  - operator_gas_steal
  - free_variables
  - gas_per_pubdata_byte
  - L2_gas_limit
  - baseFeePerGas
  - validateAndPayForPaymaster

# Impact Classification
severity: high
impact: fund_theft|resource_dos|underpayment|fee_bypass
exploitability: 0.4
financial_impact: high

# Context Tags
tags:
  - gas_accounting
  - pubdata
  - bootloader
  - fee_manipulation
  - zksync
  - sequencer
  - operator
  - bytecode_compression
  - batch_fees
  - l1_gas_cost
  - DoS
  - paymaster

language: solidity|yul
version: all
---

## References & Source Reports

### Gas Calculation Errors

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Gas Calculation Uses Unchecked Free Variables | `reports/zk_rollup_findings/gas-calculation-frequently-uses-unchecked-free-variables.md` | HIGH | Multiple |
| Invalid Gas Accounting | `reports/zk_rollup_findings/invalid-gas-accounting.md` | HIGH | Multiple |
| Gas Tracking Introduces Resource Consumption DoS | `reports/zk_rollup_findings/gas-tracking-introduces-resource-consumption-related-dos.md` | HIGH | Multiple |
| Incorrect commitScalar Underpays Sequencer | `reports/zk_rollup_findings/h-3-sequencer-will-be-underpaid-because-of-incorrect-commitscalar.md` | HIGH | Spearbit (zkSync) |
| Lack of Fee Limits for v3 Transactions | `reports/zk_rollup_findings/lack-of-fee-limits-for-v3-transactions-fixed.md` | HIGH | Multiple |

### Fee Theft and Manipulation

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Operator Steals All Gas for L1→L2 Transactions | `reports/zk_rollup_findings/m-14-operator-can-steal-all-gas-provided-by-any-user-for-l1l2-transactions.md` | MEDIUM | Spearbit (zkSync) |
| Paymaster Refunds spentOnPubdata to User | `reports/zk_rollup_findings/h-01-paymaster-will-refund-spentonpubdata-to-user-instead-of-burning-it.md` | HIGH | Spearbit (zkSync) |
| Burning User Gas in sendCompressedBytecode | `reports/zk_rollup_findings/m-08-burning-of-the-user-gas-in-the-sendcompressedbytecode-function.md` | MEDIUM | Spearbit (zkSync) |
| Potential Gas Manipulation via Bytecode Compression | `reports/zk_rollup_findings/m-22-potential-gas-manipulation-via-bytecode-compression.md` | MEDIUM | Spearbit (zkSync) |
| Batch Fees Multiplier Cap Bypassed | `reports/zk_rollup_findings/batch-fees-multiplier-cap-bypassed-with-multiple-calls.md` | MEDIUM | Multiple |
| Compress Right After Convert Can Bypass Completeness Checks | `reports/zk_rollup_findings/h-5-compress-right-after-convert-can-bypass-completeness-checks.md` | HIGH | Multiple |

---

## Vulnerability Title

**Gas Accounting Vulnerabilities — Operator Fee Theft, Pubdata Cost Errors, Batch Fee Bypass, and Gas DoS**

### Overview

ZK rollup gas accounting involves multiple layers: L2 transaction gas, pubdata costs (cost of posting state diffs to L1), compression rebates, and sequencer fee reimbursement. Bugs in any layer allow operators to steal user gas, let users avoid paying pubdata costs, cause undercompensation of the sequencer for L1 data costs, or enable denial-of-service via resource exhaustion in gas tracking.

---

### Vulnerability Description

#### Root Cause

1. **Pubdata gas not burned**: If `spentOnPubdata` (the gas consumed by L1 pubdata costs) is refunded to users or paymasters instead of being burned, the protocol subsidizes L1 costs from treasury funds.
2. **Operator gas steal via L1→L2 tx**: The operator can set gas parameters on L1→L2 transactions to capture user-provided gas as profit rather than applying it to execution.
3. **Unchecked free variables in gas computation**: When compiling circuits or computing gas costs, some variables are "free" (unconstrained by the proof) and an operator can set them arbitrarily to manipulate reported gas consumption.
4. **Incorrect commitScalar**: When computing the L1 data cost of a batch commitment, using a wrong `commitScalar` formula causes persistent underpayment to the sequencer. 
5. **Batch fee multiplier cap bypass**: A per-call multiplier cap is meant to prevent batch fees from escalating too fast, but making multiple calls in one transaction resets the counter, allowing bypass.

---

### Pattern 1: Paymaster Refunds spentOnPubdata Instead of Burning

**Frequency**: 1/431 reports | **Validation**: Strong (zkSync - Spearbit - HIGH)

#### Root Cause

In ZKSync, `spentOnPubdata` represents the gas consumed by posting state diffs to L1 (pubdata). This cost must be **burned** (not returned), because the protocol uses it to pay L1 validators. If the paymaster flow refunds this amount to the user, the protocol is effectively subsidizing L1 costs, draining the protocol treasury.

**Example 1: spentOnPubdata Refunded Instead of Burned** [HIGH]
```solidity
// ❌ VULNERABLE: Bootloader refunds full gas including pubdata cost
// In the bootloader (ZKSync), validateAndPayForPaymaster is called first,
// then at the end of transaction execution, refund is computed as:
uint256 refund = gasLimit - gasUsed - spentOnPubdata;
// BUG: refund should NOT include spentOnPubdata to the user/paymaster
// The pubdata gas must be burned (sent to L1 treasury), never refunded

// If refunded:
// → Operator absorbs the pubdata cost from their own treasury
// → User receives back what should have been burned for L1 data posting
```

**Fix:**
```solidity
// ✅ SECURE: Burn spentOnPubdata; only refund pure L2 gas not consumed
uint256 l2GasRefund = gasLimit - gasUsedForComputation; // Only L2 computation gas
uint256 pubdataToburn = spentOnPubdata;                 // Must be burned separately
_burnGas(pubdataToBurn);                                // Send to L1 operator, NOT user
_refundGas(l2GasRefund, recipient);                     // Only L2 gas portion
```

---

### Pattern 2: Operator Steals All Gas Provided for L1→L2 Transactions

**Frequency**: 1/431 reports | **Validation**: Strong (zkSync - Spearbit - MEDIUM)

#### Root Cause

When a user sends an L1→L2 transaction, they specify `gasLimit` and `gasPerPubdataByte`. The operator (sequencer) reads these values from the L1 call. If the operator can set these values for their own L1→L2 txs (or influence them), they can set `gasLimit` high but `gasPerPubdataByteLimit` to 0, allowing the bootloader to apply the full `gasLimit` budget without actually spending any of it on computation — pocketing the difference.

**Example 2: Operator Manipulates L1→L2 Transaction Gas Parameters** [MEDIUM]
```solidity
// ❌ VULNERABLE: L1 contract trusts operator-provided gas parameters
contract MailboxFacet {
    function requestL2Transaction(
        address _contractL2,
        uint256 _l2Value,
        bytes calldata _calldata,
        uint256 _l2GasLimit,        // operator can manipulate
        uint256 _l2GasPerPubdataByteLimit, // operator sets this to 0
        bytes[] calldata _factoryDeps,
        address _refundRecipient
    ) external payable returns (bytes32 canonicalTxHash) {
        // BUG: No minimum check on _l2GasPerPubdataByteLimit
        // Operator sets _l2GasPerPubdataByteLimit = 0
        // _l2GasLimit = 1_000_000 (user pays for this)
        // Result: All gas applied to operator's account, none to computation
    }
}
```

**Fix:**
```solidity
// ✅ SECURE: Enforce minimum gasPerPubdataByteLimit
function requestL2Transaction(...) external payable {
    require(
        _l2GasPerPubdataByteLimit >= REQUIRED_L2_GAS_PRICE_PER_PUBDATA,
        "Gas price per pubdata too low"
    );
    // ... standard processing
}
```

---

### Pattern 3: Gas Calculation Uses Unchecked Free Variables

**Frequency**: 1/431 reports | **Validation**: Strong (HIGH)

#### Root Cause

In STARK/ZK proof systems compiled from high-level languages, some intermediate variables in gas calculations may not be constrained by the proof (they are "free" or "witness" values). If the prover/operator can set these values arbitrarily without the verifier checking them, they can report any gas cost they choose — either undercharging (to avoid fees) or overcharging (to steal from users).

**Example 3: Unconstrained Gas Witness Variables** [HIGH]
```
// ❌ VULNERABLE pattern (abstract, applies to AIR/PIL circuits):
// Gas = freeVar * gasPerOp + baseCost
// If freeVar is not constrained by any polynomial identity, 
// the prover can set freeVar=0 to pay zero gas for expensive operations

// In Solidity terms (analogous to unchecked return value):
function executeOp(uint256 opcode) external returns (uint256 gasConsumed) {
    // BUG: gasConsumed is returned from a subcall that is not verified
    // User-controlled "gasConsumed" value, not actually measured
    (bool ok, bytes memory result) = gasMeasurer.measure(opcode);
    gasConsumed = abi.decode(result, (uint256)); // Unverified return value
    _chargeGas(gasConsumed); // Charges based on unverified amount
}
```

---

### Pattern 4: Burning User Gas in sendCompressedBytecode

**Frequency**: 1/431 reports | **Validation**: Strong (zkSync - Spearbit - MEDIUM)

#### Root Cause

When a new contract is deployed on ZKSync Era, the bytecode may need to be compressed and sent to L1 as part of pubdata. The `sendCompressedBytecode()` system function adds pubdata costs. If this function is called from within a normal transaction, the pubdata cost gets attributed to the USER's gas budget rather than being handled as a separate contract-funding cost. This can unexpectedly drain the user's gas.

**Example 4: User's Gas Budget Consumed by Compression** [MEDIUM]
```solidity
// ❌ VULNERABLE: sendCompressedBytecode() called in user-funded transaction context
// When ContractDeployer.create() is called:
// 1. User provides gasLimit
// 2. During deployment, sendCompressedBytecode is called
// 3. sendCompressedBytecode charges pubdata cost AGAINST user's gasLimit
// 4. User's transactions run out of gas unexpectedly
// 5. Transaction reverts, but user already burned gas on compression attempt

// Specific impact: Users deploying contracts with large bytecode
// find their gasLimit insufficient despite appearing to have enough
```

---

### Pattern 5: Incorrect commitScalar Underpays Sequencer

**Frequency**: 1/431 reports | **Validation**: Strong (zkSync - Spearbit - HIGH)

#### Root Cause

When computing how much the protocol should reimburse the sequencer for posting batch commitments to L1, a `commitScalar` constant is used (representing the approximate L1 gas cost per batch commitment). An incorrectly calibrated `commitScalar` (too low) results in the sequencer being permanently underpaid for L1 data posting costs, causing economic unsustainability.

**Example 5: Wrong commitScalar Constant** [HIGH]
```solidity
// ❌ VULNERABLE: commitScalar is miscalculated — too low
contract Bootloader {
    // This constant should represent the L1 gas cost of batch commitment calldata
    // BUG: The constant does not account for all fixed calldata overhead per batch
    // (e.g., missing: 4-byte function selector, ABI encoding overhead, struct padding)
    uint256 constant COMMIT_OVERHEAD_GAS = 0; // Ignores all fixed L1 overhead
    
    function calculateBatchFee(uint256 pubdataBytes) internal pure returns (uint256) {
        // Missing: COMMIT_OVERHEAD_GAS contribution
        return pubdataBytes * L1_GAS_PER_PUBDATA_BYTE; // No fixed overhead
    }
}
```

**Fix:**
```solidity
// ✅ SECURE: commitScalar includes all L1 calldata overhead
uint256 constant COMMIT_OVERHEAD_GAS = 2_297; // Measured from L1 tx traces
uint256 constant PROVE_OVERHEAD_GAS  = 1_100;

function calculateBatchFee(uint256 pubdataBytes) internal pure returns (uint256) {
    return COMMIT_OVERHEAD_GAS + (pubdataBytes * L1_GAS_PER_PUBDATA_BYTE);
}
```

---

### Pattern 6: Batch Fees Multiplier Cap Bypassed with Multiple Calls

**Frequency**: 1/431 reports | **Validation**: Moderate (MEDIUM)

#### Root Cause

A batch fee multiplier is used to limit fee escalation. A per-call cap prevents the multiplier from being raised beyond a threshold in a single call. However, if the cap is applied per-call (not per-block or per-epoch), an attacker can make multiple calls in rapid succession — each within the per-call limit — to raise the multiplier far above the intended maximum.

**Example 6: Multiplier Cap Reset Per-Call** [MEDIUM]
```solidity
// ❌ VULNERABLE: Cap enforced per-call, compounding across multiple calls
contract BatchFeeManager {
    uint256 public feeMultiplier;
    uint256 constant MAX_PER_CALL_INCREASE = 1_000; // Max 1000 units per call
    
    function updateFeeMultiplier(uint256 newMultiplier) external {
        // Only checks per-call delta
        require(
            newMultiplier <= feeMultiplier + MAX_PER_CALL_INCREASE,
            "Increase too large"
        );
        feeMultiplier = newMultiplier;
        // BUG: Call again 100 times → multiplier raised by 100_000 total
    }
}
```

**Fix:**
```solidity
// ✅ SECURE: Apply cap relative to a reference point that resets periodically (per block/epoch)
mapping(uint256 => uint256) public blockBaseMultiplier; // multiplier at start of block

function updateFeeMultiplier(uint256 newMultiplier) external {
    uint256 base = blockBaseMultiplier[block.number];
    if (base == 0) base = feeMultiplier;
    require(newMultiplier <= base + MAX_PER_BLOCK_INCREASE, "Block cap exceeded");
    feeMultiplier = newMultiplier;
}
```

---

### Pattern 7: Bytecode Compression Bypass Completeness Checks

**Frequency**: 1/431 reports | **Validation**: Strong (HIGH)

#### Root Cause

Bytecode compression in ZKSync involves two steps: `convert` (encode dictionary) and `compress` (apply encoding). The completeness check ensures all original bytecode chunks appeared in the dictionary. If `compress` is called immediately after `convert` within the same call (before completeness check runs), the check is bypassed — allowing malformed or incomplete compression to be committed to L1.

**Example 7: Compression Completeness Check Bypass** [HIGH]
```solidity
// ❌ VULNERABLE: Compress called in same transaction as convert, skipping completeness
interface ICompressor {
    function publishCompressedBytecode(
        bytes calldata _bytecode,
        bytes calldata _rawCompressedData
    ) external returns (bytes32);
}

// Attacker calls in one tx:
// 1. convert(_bytecode) → sets up dictionary state
// 2. compress(_bytecode, partialData) → completeness check expects convert to be "finalized"
//    but since we're in the SAME call context, the invariant is violated
// Result: Incomplete/crafted compressed bytecode accepted by the system
```

---

### Impact Analysis

#### Technical Impact
- Sequencer/operator receives less than their L1 cost for data posting → unsustainable economics
- User gas budget consumed by compression operations not attributed to them
- Fee multiplier caps defeated → transaction fees spike beyond protocol parameters
- Proof system gas variables unconstrained → arbitrary gas reporting from malicious provers

#### Business Impact
- User fund loss via gas theft (operator steals L1→L2 tx gas budget)
- pubdata refund to users instead of burning → treasury drain
- Long-term sequencer underpayment leads to operator exit
- Bytecode compression bypass corrupts state diff integrity

---

### Detection Patterns

```
1. Bootloader paymaster flow refunding pubdata cost (spentOnPubdata) to user
2. requestL2Transaction() missing minimum _l2GasPerPubdataByteLimit check
3. Gas computed from unchecked return values of subcalls (unverified witness)
4. commitScalar/commitOverhead constant = 0 or obviously lower than actual L1 calldata cost
5. Fee multiplier cap checked as delta-per-call, not delta-per-block
6. compress() callable in same transaction as convert() without completeness barrier
7. sendCompressedBytecode() attributing costs to user gas rather than system gas
```

### Keywords for Search

`pubdata gas accounting`, `spentOnPubdata refund`, `operator gas steal L1 L2`, `commitScalar underpayment`, `batch fee multiplier cap bypass`, `bytecode compression completeness bypass`, `bootloader gas theft`, `ZKSync gas accounting`, `L2 pubdata cost`, `gas per pubdata byte`, `unchecked gas variable`, `paymaster gas manipulation`, `sequencer underpaid`, `free variable gas circuit`, `sendCompressedBytecode gas burn`, `batch overhead constant`, `fee model attack`
