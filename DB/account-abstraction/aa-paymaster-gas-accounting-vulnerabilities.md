---
# Core Classification
protocol: generic
chain: everychain
category: account_abstraction
vulnerability_type: gas_accounting_error

# Attack Vector Details
attack_type: logical_error
affected_component: paymaster_gas_validation

# Technical Primitives
primitives:
  - paymaster
  - validatePaymasterUserOp
  - postOp
  - prefund
  - verificationGasLimit
  - preVerificationGas
  - callGasLimit
  - handleOp
  - stake
  - reputation
  - ERC-4337
  - EntryPoint

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.65
financial_impact: high

# Context Tags
tags:
  - account-abstraction
  - ERC-4337
  - paymaster
  - gas-accounting
  - stake
  - fee-bypass
  - smart-wallet
  - bundler

language: solidity
version: ">=0.8.0"
---

## References

| Tag | Report Path |
|-----|-------------|
| [GAS-1] | `reports/account_abstraction_findings/h01-incorrect-prefund-calculation-core.md` |
| [GAS-2] | `reports/account_abstraction_findings/h02-duplicate-validation-gas-accounting-core.md` |
| [GAS-3] | `reports/account_abstraction_findings/h03-paymasters-can-spend-locked-stake-core.md` |
| [GAS-4] | `reports/account_abstraction_findings/h05-incorrect-gas-price-core.md` |
| [GAS-5] | `reports/account_abstraction_findings/h-05-paymaster-eth-can-be-drained-with-malicious-sender.md` |
| [GAS-6] | `reports/account_abstraction_findings/invalid-gas-accounting.md` |
| [GAS-7] | `reports/account_abstraction_findings/fee-bypass-in-paymaster-implementation.md` |
| [GAS-8] | `reports/account_abstraction_findings/operations-can-throttle-paymasters-core.md` |
| [GAS-9] | `reports/account_abstraction_findings/m02-separate-stake-and-prepayment-core.md` |
| [GAS-10] | `reports/account_abstraction_findings/paymaster-may-incur-losses-due-to-penalties-for-unused-gas.md` |
| [GAS-11] | `reports/account_abstraction_findings/verifyingsigner-has-no-authority-over-paymaster-related-gas-limits.md` |
| [GAS-12] | `reports/account_abstraction_findings/permissions-can-drain-approvals-given-to-certain-paymasters.md` |
| [GAS-13] | `reports/account_abstraction_findings/postop-reverts-can-lead-to-uncompleted-repayment-of-paymaster-and-stuck-funds.md` |
| [GAS-14] | `reports/account_abstraction_findings/h-03-users-can-escape-paying-for-the-tx-gas.md` |
| [GAS-15] | `reports/account_abstraction_findings/insufficient-charge-of-user-operation-execution-fees.md` |
| [GAS-16] | `reports/account_abstraction_findings/m-13-improper-tokengasprice-design-can-overcharge-user-and-undercharge-paymaster.md` |
| [GAS-17] | `reports/account_abstraction_findings/m-04-the-_postop-function-in-gastank-is-not-handling-gas-penalty-for-unused-gas.md` |
| [GAS-18] | `reports/account_abstraction_findings/h-01-paymaster-will-refund-spentonpubdata-to-user.md` |
| [GAS-19] | `reports/account_abstraction_findings/h-06-feerefundtokengaspricefactor-is-not-included-in-signed-transaction-data-all.md` |
| [GAS-20] | `reports/account_abstraction_findings/attacker-might-repeatedly-use-selfrevokesigner-to-steal-gas-refunds.md` |
| [GAS-21] | `reports/account_abstraction_findings/the-sponsorpaymaster-owner-should-be-restricted-to-withdraw.md` |
| [GAS-22] | `reports/account_abstraction_findings/erc-4337-call-to-_payprefund-may-lead-to-the-validator-stake-being-split.md` |

## Vulnerability Title

**AA Paymaster & Gas Accounting Vulnerabilities — Incorrect Prefund, Duplicate Accounting, Stake Bypass, Fee Escape**

### Overview

ERC-4337 paymaster and gas accounting logic is a rich source of bugs: inverted conditions, duplicate gas measurements, stake bypass tricks, and fee escape paths allow attackers to drain paymasters, execute transactions for free, exhaust bundler-paid gas, or permanently throttle honest paymasters. These findings span EIP-4337 core (OpenZeppelin audit) and dozens of production paymaster integrations.

### AA Paymaster Gas Accounting — Prefund Errors, Duplicate Snapshots, Stake Bypass, and Fee Escape

#### Root Cause

Gas accounting in ERC-4337 is a multi-phase process (validation → execution → postOp) with several hand-off points where gas values can be measured incorrectly:

1. **Inverted `verificationGasLimit` multiplier** — The spec requires ops WITHOUT a paymaster to multiply `verificationGasLimit` by 3 (single validation pass is more expensive). An inverted condition applies the multiplier to paymasterd ops instead.
2. **Duplicate `preGas` snapshot** — In `handleOp`, the same `preGas` variable is reused for both the pre-execution snapshot and the pre-postOp snapshot, zeroing the postOp gas charge.
3. **Paymaster == wallet stake bypass** — If paymaster address equals the account, its `deposit()` call uses locked stake, bypassing the reputation throttle system.
4. **Malicious sender drains paymaster** — `validatePaymasterUserOp` may trust sender-supplied parameters (token amounts, rate) without independent verification.
5. **postOp reverts causing under-refund** — When `postOp` reverts after successful execution, gas already consumed is not reclaimed, leaving paymaster with incorrectly updated balances.
6. **Unsigned fee factors** — `feeRefundTokenGasPriceFactor`, `tokenGasPrice`, and similar multipliers that determine how much a user is charged in the paymaster's token are not included in the signed data, allowing a malicious relayer/bundler to manipulate the effective fee.

#### Attack Scenario

**Scenario A — Inverted prefund multiplier [GAS-1] (OpenZeppelin EIP-4337 audit, HIGH):**
1. An op WITHOUT a paymaster submits `verificationGasLimit = G`.
2. Buggy contract applies `G * 3` multiplier ONLY to ops WITH a paymaster (inverted condition).
3. Non-paymaster ops receive no reserve multiplier → under-funded → EntryPoint reverts or attacker pays less gas than expected.

**Scenario B — Duplicate gas accounting [GAS-2] (OpenZeppelin, HIGH):**
1. `handleOp` records `preGas = gasleft()` before validation phase.
2. `preGas` value is reused (not re-snapshotted) before postOp phase.
3. `gasCost(postOp) = preGas - gasleft()` resolves to a near-zero or negative value.
4. Paymaster is not charged for postOp gas → protocol accumulates a shortfall.

**Scenario C — Paymaster stake bypass [GAS-3] (OpenZeppelin, HIGH):**
1. Attacker deploys contract where `paymaster == smartAccount`.
2. `deposit(paymaster, amount)` internally calls `paymaster.addStake()` using locked stake balance.
3. Bypasses the throttle mechanism — the paymaster's reputation is not decremented, so throttling never triggers.

**Scenario D — Malicious sender drains paymaster [GAS-5] (HIGH):**
1. Attacker crafts a userOp with a manipulated `paymasterAndData` field (e.g., inflated token refund amount).
2. Paymaster's `validatePaymasterUserOp` trusts the sender-supplied value without checking against an oracle.
3. Paymaster approves the op and later pays out more than the actual gas cost.

**Scenario E — Gas escape [GAS-14] (HIGH):**
1. User crafts an op whose calldata causes execution to revert in a specific way.
2. The gas-charging path is skipped due to a conditional logic bug.
3. User's op executes (or partially executes) without paying for gas.

**Scenario F — Unsigned fee factor manipulation [GAS-19] (HIGH):**
1. Paymaster operator signs `{token, gasPrice, validUntil, validAfter}` but NOT `feeRefundTokenGasPriceFactor`.
2. Malicious bundler submits the op with a much higher `feeRefundTokenGasPriceFactor`.
3. User is severely overcharged; excess token fees go to the relayer or are lost.

#### Vulnerable Pattern Examples

**Example 1: Inverted verificationGas multiplier** [HIGH] — Source: [GAS-1]
```solidity
// ❌ VULNERABLE: Applies 3x multiplier to ops WITH paymaster — opposite of spec
// Ops WITHOUT paymaster are under-funded

function _validatePrepayment(uint256 opIndex, UserOperation calldata op, ...) {
    uint256 requiredPreFund;
    if (op.paymaster != address(0)) {
        // Applies to paymaster ops — WRONG, should be non-paymaster ops
        requiredPreFund = op.callGasLimit * 3 * op.maxFeePerGas
            + op.verificationGasLimit * 3 * op.maxFeePerGas; // ← inverted
    } else {
        requiredPreFund = (op.callGasLimit + op.verificationGasLimit) * op.maxFeePerGas;
        // ← Missing 3x multiplier here
    }
}
```

**Example 2: Same preGas snapshot used twice** [HIGH] — Source: [GAS-2]
```solidity
// ❌ VULNERABLE: preGas reused from before-validation for before-postOp measurement
// postOp gas cost calculates to ≈ 0

function handleOp(UserOperation calldata op, address payable beneficiary) internal {
    uint256 preGas = gasleft();  // ← snapshot before validation

    // ... validation + execution phases ...

    // postOp phase — preGas NOT re-snapshotted here
    IPaymaster(paymaster).postOp(mode, context, preGas - gasleft());
    // ← preGas is the SAME value from before validation, not before postOp
    //   gasleft() here is much smaller → preGas - gasleft() ≈ total gas, not postOp gas
}
```

**Example 3: Paymaster == sender stake bypass** [HIGH] — Source: [GAS-3]
```solidity
// ❌ VULNERABLE: When paymaster == sender, deposit call uses locked stake
// Bypasses ERC-4337 reputation throttle

function _handlePostOp(..., address paymaster, address sender, ...) internal {
    if (paymaster == sender) {
        // Stake and deposit from same account — reputation system cannot throttle
        IStakeManager(entryPoint).depositTo{value: prefundAfterGas}(paymaster);
        // ← should come from unlocked deposit, not stake
    }
}
```

**Example 4: Unsigned gas price factor** [HIGH] — Source: [GAS-19]
```solidity
// ❌ VULNERABLE: feeRefundTokenGasPriceFactor not included in the signed struct
// Bundler can inflate it to overcharge users

struct PaymasterData {
    address token;
    uint256 gasPrice;       // signed
    uint48  validUntil;     // signed
    uint48  validAfter;     // signed
    // feeRefundTokenGasPriceFactor is NOT in this struct → not signed
}

function validatePaymasterUserOp(UserOperation calldata op, ...) {
    (PaymasterData memory data, bytes calldata sig) = abi.decode(op.paymasterAndData[20:], ...);
    uint256 multiplier = abi.decode(op.paymasterAndData[OFFSET:], (uint256)); // ← NOT verified!
    _validateSignature(data, sig);
    uint256 charge = gasUsed * data.gasPrice * multiplier; // ← multiplier unverified
}
```

**Example 5: postOp revert leaves paymaster with wrong balance** [MEDIUM] — Source: [GAS-13]
```solidity
// ❌ VULNERABLE: When postOp reverts, execution result is considered complete
// but paymaster balance update from execution phase is not reversed

function _executeUserOp(uint256 opIndex, UserOperation calldata op, ...) internal {
    try this._innerHandleOp(op, opInfo, context) returns (uint256 actualGasCost) {
        collected = actualGasCost;
    } catch {
        // postOp reverted — but execution already debited paymaster
        // no reversal of debit → paymaster loses funds
        collected = 0;
    }
    // _compensate(beneficiary, collected) called regardless
}
```

**Example 6: User escapes paying gas** [HIGH] — Source: [GAS-14]
```solidity
// ❌ VULNERABLE: Gas charge path has a reachable bypass branch

function _handlePostOp(
    IPaymaster.PostOpMode mode,
    bytes calldata context,
    uint256 actualGasCost,
    address paymaster
) private {
    if (mode == IPaymaster.PostOpMode.opSucceeded) {
        // Normal charge path
        _debitPaymasterDeposit(paymaster, actualGasCost);
    } else if (mode == IPaymaster.PostOpMode.opReverted) {
        // ← Revert path might not charge if opReverted handling is skipped
        // Bug: actualGasCost is 0 when execution reverts early in a specific path
        _debitPaymasterDeposit(paymaster, actualGasCost); // actualGasCost == 0 → no charge
    }
}
```

### Impact Analysis

#### Technical Impact
- EntryPoint core arithmetic bugs (GAS-1, GAS-2) break the gas invariant — bundlers accumulate losses silently
- Paymaster reputation throttle bypassed (GAS-3) → malicious actors can submit unlimited ops
- Unsigned multipliers → relayer can arbitrarily inflate token fees (GAS-19)
- postOp revert mismatch → paymaster permanently loses funds without users being re-charged

#### Business Impact
- Bundler profitability eroded by under-charged ops (GAS-1, GAS-2, GAS-14)
- Paymaster ETH drained by malicious senders crafting favorable `paymasterAndData` (GAS-5)
- Paymaster stake split across sub-deposits may never reach throttle threshold (GAS-22)
- Over-charging users damages UX and erodes adoption (GAS-16)

#### Affected Scenarios
- Incorrect prefund: Common in custom EntryPoint forks (2/22 reports are core EntryPoint bugs)
- Gas escape: Medium severity, requires careful execution path analysis (3/22 reports)
- Unsigned fee factor: Affects token-denominated paymasters (3/22 reports)
- postOp issues: Cross-cutting (4/22 reports)
- Stake bypass: Requires paymaster == sender setup (1/22 reports, HIGH)

### Secure Implementation

**Fix 1: Correct verificationGas multiplier placement**
```solidity
// ✅ SECURE: Apply 3x multiplier to ops WITHOUT paymaster (single validation overhead)

function _getRequiredPrefund(UserOperation calldata op) internal pure returns (uint256) {
    uint256 mul = op.paymaster != address(0) ? 1 : 3; // ← correct branch
    return (op.callGasLimit + op.verificationGasLimit * mul + op.preVerificationGas)
        * op.maxFeePerGas;
}
```

**Fix 2: Re-snapshot gas before postOp phase**
```solidity
// ✅ SECURE: Always snapshot gasleft() immediately before calling postOp

function handleOp(UserOperation calldata op, address payable beneficiary) internal {
    // validation phase
    _validatePrepayment(op);

    // execution phase
    uint256 preExecGas = gasleft();
    _executeUserOp(op);
    uint256 actualExecGasCost = (preExecGas - gasleft()) * actualGasPrice;

    // postOp phase — NEW snapshot
    uint256 prePostOpGas = gasleft(); // ← dedicated snapshot
    IPaymaster(op.paymaster).postOp(mode, context, actualExecGasCost);
    uint256 postOpGasCost = (prePostOpGas - gasleft()) * actualGasPrice;
}
```

**Fix 3: Include all fee-determining parameters in signed paymaster data**
```solidity
// ✅ SECURE: Sign every parameter that affects how much the user/paymaster pays

struct PaymasterData {
    address token;
    uint256 gasPrice;
    uint256 feeRefundTokenGasPriceFactor; // ← now signed
    uint48  validUntil;
    uint48  validAfter;
}

bytes32 constant PAYMASTER_DATA_TYPEHASH = keccak256(
    "PaymasterData(address token,uint256 gasPrice,uint256 feeRefundTokenGasPriceFactor,"
    "uint48 validUntil,uint48 validAfter)"
);

function validatePaymasterUserOp(UserOperation calldata op, ...) {
    PaymasterData memory data = _decodePaymasterData(op);
    bytes32 hash = _hashTypedData(keccak256(abi.encode(PAYMASTER_DATA_TYPEHASH, data)));
    require(ECDSA.recover(hash, sig) == verifyingSigner, "InvalidSig");
    // Now multiplier is verified against signer intent
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- if (op.paymaster != address(0)) { verificationGasLimit * 3 } — inverted multiplier
- uint256 preGas = gasleft() used both before validation and reused before postOp
- paymaster == sender (or paymaster == account) followed by depositTo without stake check
- paymasterAndData decoded field used in fee calculation but NOT included in the signed bytes
- postOp call inside try/catch where catch branch sets collected = 0
- _validatePaymasterUserOp trusting user-supplied rate/amount without oracle verification
- feeRefundTokenGasPriceFactor, tokenGasPrice, gasMultiplier decoded from calldata but not in signed struct
```

#### Audit Checklist
- [ ] Does prefund calculation apply `verificationGasLimit * 3` to the correct branch (no-paymaster)?
- [ ] Is `gasleft()` re-snapshotted immediately before the `postOp` call?
- [ ] Are ALL parameters that affect the user's fee included in the signed paymaster data?
- [ ] Is `validatePaymasterUserOp` independent of any sender-supplied numerical parameters?
- [ ] Does `postOp` revert handling correctly reverse or account for already-charged amounts?
- [ ] Are paymaster stake and deposit managed from separate balances?
- [ ] Is there any path where `actualGasCost` can be zero while the op succeeded?
- [ ] Can a user submit ops that bypass gas charging via crafted calldata reverts?

### Real-World Examples

#### Known Exploits from Audit Reports
- **EIP-4337 EntryPoint (OpenZeppelin)** — Inverted `verificationGasLimit * 3` multiplier [GAS-1] — HIGH
- **EIP-4337 EntryPoint (OpenZeppelin)** — Duplicate `preGas` snapshot in `handleOp` [GAS-2] — HIGH
- **EIP-4337 EntryPoint (OpenZeppelin)** — Paymasters spend locked stake [GAS-3] — HIGH
- **EIP-4337 EntryPoint (OpenZeppelin)** — Incorrect gas price formula [GAS-4] — HIGH
- **Custom paymaster (Shieldify)** — Malicious sender drains paymaster ETH [GAS-5] — HIGH
- **ZkSync paymaster (zkSync/Cyfrin)** — `spentOnPubdata` refunded to user instead of operator [GAS-18] — HIGH
- **Token paymaster (multiple)** — `feeRefundTokenGasPriceFactor` unsigned [GAS-19] — HIGH
- **GasTank paymaster (Code4rena)** — postOp gas penalty not handled [GAS-17] — MEDIUM
- **Modular account paymaster (Quantstamp)** — postOp revert leaves paymaster under-refunded [GAS-13] — MEDIUM

### Prevention Guidelines

#### Development Best Practices
1. **Follow the EIP-4337 gas calculation spec exactly** — re-read §6 (EntryPoint execution) for every gas snapshot point.
2. **Sign every numerical parameter in `paymasterAndData`** — if a value is decoded from the bytes and used in fee calculation, it must be in the signed struct.
3. **Use `gasleft()` snapshots immediately before each phase** — do NOT cache `gasleft()` across phase boundaries.
4. **Separate deposit and stake balances explicitly** — never allow a `depositTo` call to draw from locked stake.
5. **Test `postOp` revert paths** — ensure the accounting invariant holds even when `postOp` reverts.
6. **Rate-limit or oracle-verify all user-supplied parameters** to `validatePaymasterUserOp`.

#### Testing Requirements
- Unit test: `handleOps` with no-paymaster op → verify 3x reserve multiplication
- Unit test: injection of artificially high `feeRefundTokenGasPriceFactor` → must revert
- Unit test: `postOp` that reverts → verify paymaster balance deducted correctly
- Fuzz: vary `preVerificationGas` / `callGasLimit` → bundler must never lose more than intended overhead
- Integration test: paymaster == sender account → stake must remain untouched

### Keywords for Search

`paymaster gas accounting`, `prefund calculation`, `verificationGasLimit multiplier`, `duplicate gas snapshot`, `preGas reuse`, `paymaster stake bypass`, `validatePaymasterUserOp`, `postOp revert`, `fee bypass paymaster`, `unsigned gas price factor`, `feeRefundTokenGasPriceFactor`, `tokenGasPrice unsigned`, `gas escape ERC-4337`, `bundler gas loss`, `paymaster drain`, `malicious sender paymaster`, `handleOp gas`, `ERC-4337 gas bug`, `operations throttle paymaster`, `reputation bypass`, `separate stake prepayment`, `spentOnPubdata refund`, `paymaster overcharge`, `paymaster undercharge`

### Related Vulnerabilities

- `DB/account-abstraction/aa-signature-replay-attacks.md` — signature validation issues in validateUserOp
- `DB/account-abstraction/aa-session-key-permission-abuse.md` — session key draining paymaster approvals
- `DB/general/calculation/` — general arithmetic and fee calculation bugs

---
