---
# Core Classification
protocol: avalanche
chain: avalanche
category: bridge
vulnerability_type: missing_validation

# Pattern Identity
root_cause_family: missing_validation
pattern_key: missing_dedup_and_fee_check | bridge_receipt_queue | retryReceipt | relayer_griefing

# Interaction Scope
interaction_scope: cross_chain
involved_contracts:
  - TeleporterMessenger / Avalanche-Ethereum bridge receipts
  - Relayer (off-chain)
  - submitCreateBridgeToken token deployment path
path_keys:
  - missing_dedup_and_fee_check | retryReceipt() | TeleporterMessenger->Relayer
  - missing_fee_check | submitCreateBridgeToken() | TokenHome->TokenRemote
  - unbounded_queue_growth | sendMessage() | subnet->subnet_message_flow

# Attack Vector Details
attack_type: resource_exhaustion
affected_component: bridge_receipt_queue

# Technical Primitives
primitives:
  - receipt_queue
  - retryReceipt
  - deduplication
  - fee_caps (MaxFeeCap / MinerTip)
  - zero_address_check
  - relayer_incentives
  - warp_signature_aggregation

# Grep / Hunt-Card Seeds
code_keywords:
  - retryReceipt
  - submitCreateBridgeToken
  - MaxFeeCap
  - MinerTip
  - receiptsQueue
  - redeemMessage
  - WarpMessage
  - validatorSignatures

# Impact Classification
severity: medium
impact: dos
exploitability: 0.6
financial_impact: medium

# Context Tags
tags:
  - l1
  - bridge
  - relayer
  - subnet
  - warp_messaging
  - dos

# Version Info
language: solidity
version: "2023 bridge contracts; avalanchego node 2025 assessment"
---

## References & Source Reports

> Reference files verified to exist under `reports/other-l1_findings/`. Content basis noted per row.

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [AVAX1] | reports/other-l1_findings/avalanchego-graft-subnet-evm-docs-audits-bridge-smart-contracts-least-authority-july-7th-2023-pdf.md | MEDIUM-HIGH | Least Authority | Least Authority final report, 7 July 2023 (issue list verified from report ToC) |
| [AVAX2] | reports/other-l1_findings/publications-reviews-2025-08-ava-labs-avalanchego-securityreview-pdf.md | HIGH | Trail of Bits | ToB public assessment, 8 Aug 2025, 39 pp. (metadata + DoS classification verified; findings text not extracted — PDF is word-per-line garbled) |
| [AVAX3] | reports/other-l1_findings/avalanchego-graft-subnet-evm-docs-audits-avalanche-warp-messaging-openzeppelin-november-16th-2023-pdf.md | LOW | OpenZeppelin | OZ warp-messaging review, 16 Nov 2023 (index-verified only: validator-signature / subnet messaging issues, resolved) |

## Avalanche Bridge & Node Validation Gaps (Receipt Queue, Fee Caps, Warp Signatures)

### Overview

Across Avalanche's audited bridge stack, the recurring pattern is **missing secondary validation on message/receipt lifecycle and fee math**: unbalanced two-chain activity grows an unbounded receipt queue that destroys relayer incentives ([AVAX1] Issue A), duplicate receipts can be re-enqueued through `retryReceipt` ([AVAX1] Issue B), `MinerTip` is excluded from the `MaxFeeCap` computation ([AVAX1] Issue D), and a zero-address check is missing on the token-creation path ([AVAX1] Issue C). A 2025 Trail of Bits assessment of the AvalancheGo node itself carries a high-severity, denial-of-service classification ([AVAX2]).

#### Agent Quick View

- Root cause statement: "This vulnerability exists because bridge receipt handling lacks deduplication and queue-bounds enforcement, fee-cap math omits a fee component, and address/parameter checks are missing on deployment paths."
- Pattern key: `missing_dedup_and_fee_check | bridge_receipt_queue | retryReceipt | relayer_griefing`
- Interaction scope: `cross_chain`
- Primary affected component(s): `bridge receipt queue, relayer economics, token deployment path, warp message validation`
- Contracts / modules involved: `TeleporterMessenger-style receipts, Relayer, submitCreateBridgeToken, WarpMessage verification (node)`
- Path keys: `missing_dedup_and_fee_check | retryReceipt() | TeleporterMessenger->Relayer` · `missing_fee_check | submitCreateBridgeToken() | TokenHome->TokenRemote`
- High-signal code keywords: `retryReceipt, submitCreateBridgeToken, MaxFeeCap, MinerTip, receiptsQueue, WarpMessage, validatorSignatures`
- Typical sink / impact: `relayer DoS / griefing, stuck cross-chain messages, mispriced fees, misdirected tokens`
- Validation strength: `moderate` (bridge issue list verified verbatim from [AVAX1] ToC; [AVAX2] verified at metadata level only; [AVAX3] index-verified)

#### Contract / Boundary Map

- Entry surface(s): `sendMessage()`, `retryReceipt()`, `submitCreateBridgeToken()`, warp message submission to subnet validators
- Contract hop(s): `SourceSubnet dApp -> TeleporterMessenger -> Relayer -> DestinationSubnet TeleporterMessenger -> dApp`
- Trust boundary crossed: `cross-chain message / relayer (off-chain actor) / warp BLS aggregate signature`
- Shared state or sync assumption: `receipt queue on each chain must mirror delivered messages; fee caps must cover total fee (base + miner tip)`

#### Valid Bug Signals

- Signal 1: A receipt that was already delivered/executed can be re-enqueued (no `delivered` / nonce-consumed guard on the retry path).
- Signal 2: Message flow between two chains is attacker-influenceable (one-direction flooding) AND queue growth has no cap or economic backpressure → relayer exits, messages stall.
- Signal 3: Fee-cap math compares against `BaseFee` alone while execution can pay `MinerTip`, so estimated cap < actual required fee → reverts or stuck relayer txs.
- Signal 4: Token/bridge deployment accepts a zero address for recipient or token implementation without revert.

#### False Positive Guards

- Not this bug when: the retry path already checks `receipt.delivered` or consumes a nonce before re-enqueueing.
- Not this bug when: the queue is intentionally unbounded but relayer payment scales with queue age (incentive preserved by design).
- Safe if: fee cap is computed as `BaseFee + MaxPriorityFee` (EIP-1559 total) and the zero-address check reverts.
- Requires attacker control of: message volume between the two chains (cheap spam), or a warp message with spoofed/insufficient validator signature weight.
- [AVAX3] warp-messaging issues were reported resolved by OpenZeppelin — do not re-report without re-verifying the current signature-quorum code.

### Vulnerability Description

#### Root Cause

1. **Receipt lifecycle dedup missing** ([AVAX1] Issue B): `retryReceipt` re-enqueues receipts without proving the prior attempt is still outstanding, so duplicates accumulate.
2. **No queue bound / incentive coupling** ([AVAX1] Issue A): unbalanced activity between the two chains grows the outstanding-receipt queue faster than relayer rewards, collapsing the relayer business case — a liveness failure, not theft.
3. **Incomplete fee formula** ([AVAX1] Issue D): `MaxFeeCap` calculation omits `MinerTip`, so cap-checks undercount the true execution fee.
4. **Missing parameter validation** ([AVAX1] Issue C): zero-address check absent on the bridge-token creation flow (`submitCreateBridgeToken` is the audited surface).
5. **Node-level DoS surface** ([AVAX2]): the AvalancheGo node assessment is classified high / denial-of-service at the report level (content basis unassessed here).

#### Attack Scenario / Path Variants

**Path A: Receipt-queue griefing via unbalanced flow**
Path key: `missing_dedup_and_fee_check | retryReceipt() | TeleporterMessenger->Relayer`
Entry surface: `sendMessage()` on the cheaper side of the bridge pair
Contracts touched: `Source messenger -> Relayer -> Destination messenger`
Boundary crossed: `cross-chain message + off-chain relayer`
1. Attacker sends a flood of one-directional messages (the cheap direction).
2. Outstanding receipts accumulate; each needs relayer gas to deliver.
3. Duplicate re-enqueue via `retryReceipt` multiplies queue entries.
4. Relayer reward per receipt falls below cost → relayer stops → legitimate messages stall (DoS).

**Path B: Mispriced fee cap on token creation**
Path key: `missing_fee_check | submitCreateBridgeToken() | TokenHome->TokenRemote`
Entry surface: `submitCreateBridgeToken()` / delivery tx
Contracts touched: `TokenHome -> TokenRemote -> new bridge token`
Boundary crossed: `cross-chain deployment`
1. User/relayer computes allowed fee from `MaxFeeCap` that excludes `MinerTip`.
2. Actual delivery cost exceeds the cap.
3. Delivery reverts or relayer eats the difference.
4. Combined with the missing zero-address check ([AVAX1] Issue C), a bad parameter can brick the token route.

**Path C: Node-level DoS (AvalancheGo)**
Path key: `node_dos | p2p/consensus message handling | avalanchego internals`
Entry surface: AvalancheGo network/consensus message processing ([AVAX2], detail unassessed)
1. Malformed or resource-heavy peer messages reach processing.
2. Missing bounds/validation → CPU/memory exhaustion.
3. Validator degraded → liveness impact on subnet. Treat as a hunt lead, not a verified path.

#### Vulnerable Pattern Examples

> Reconstructed from the audited issue descriptions in [AVAX1]; identifiers preserved from the report.

**Example 1: Duplicate re-enqueue in retryReceipt** [Approx Vulnerability : MEDIUM]
```solidity
// ❌ VULNERABLE: receipt re-enqueued without checking outstanding status ([AVAX1] Issue B)
function retryReceipt(bytes32 messageHash) external {
    Receipt storage r = receipts[messageHash];
    // no check that r.delivered == false / not already in queue
    receiptsQueue.enqueue(messageHash);        // duplicates possible
    emit RetryReceipt(messageHash);
}
```

**Example 2: Fee cap that ignores MinerTip** [Approx Vulnerability : LOW-MEDIUM]
```solidity
// ❌ VULNERABLE: MaxFeeCap omits MinerTip ([AVAX1] Issue D)
function requiredFeeCap() public view returns (uint256) {
    return block.basefee;                      // miner tip not covered
}
```

**Example 3: Missing zero-address check on token creation** [Approx Vulnerability : LOW]
```solidity
// ❌ VULNERABLE: no zero-address validation ([AVAX1] Issue C, submitCreateBridgeToken surface)
function submitCreateBridgeToken(address token, address recipient) external {
    createBridgeTokenRequests[token] = recipient;  // recipient == address(0) accepted
}
```

### Impact Analysis

#### Technical Impact
- Unbounded receipt queue → relayer economics inverted → cross-chain liveness failure
- Duplicate receipts → double relayer payouts or double delivery attempts, state divergence between chains
- Underestimated fee caps → reverted deliveries, stuck messages, relayer fund drain
- Zero-address acceptance → bricked token route / burned deployment

#### Business Impact
- Bridge outage risk on Avalanche subnets; user fund access delays (not direct theft)
- [AVAX2] shows the node itself carries high-sev DoS exposure — reputational/liveness risk for subnet operators

#### Affected Scenarios
- Cheap-direction message spam between a low-fee subnet and mainnet
- Fee spikes (MinerTip matters most under congestion)
- Warp-messaging integrations that trust signature quorums without re-checking [AVAX3] fixes

### Secure Implementation

**Fix 1: Bounded, deduplicated receipt queue with total-fee cap**
```solidity
// ✅ SECURE: dedup guard, queue bound, and EIP-1559-total fee cap
function retryReceipt(bytes32 messageHash) external {
    Receipt storage r = receipts[messageHash];
    require(!r.delivered && !r.enqueued, "already handled");
    require(receiptsQueue.length() < MAX_QUEUE, "queue full");   // [AVAX1] Issue A
    r.enqueued = true;
    receiptsQueue.enqueue(messageHash);
}

function requiredFeeCap() public view returns (uint256) {
    return block.basefee + block.priorityFee + RELAYER_MARGIN;   // [AVAX1] Issue D fix
}

function submitCreateBridgeToken(address token, address recipient) external {
    require(token != address(0) && recipient != address(0), "zero address"); // Issue C fix
    createBridgeTokenRequests[token] = recipient;
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- retryReceipt
- submitCreateBridgeToken
- MaxFeeCap
- MinerTip
- receiptsQueue
- validatorSignatures
- WarpMessage
```

#### Code Patterns to Look For
```
- enqueue without delivered/enqueued flag check
- fee comparisons against basefee only
- address parameters used without zero-check in deployment paths
- queue length never compared to a bound
```

#### Audit Checklist
- [ ] Can a delivered receipt be re-enqueued through any retry path?
- [ ] Does the fee cap formula include priority/miner tip and margin?
- [ ] Is there an explicit queue bound or backpressure tied to relayer rewards?
- [ ] Are all address params on token-creation paths zero-checked?
- [ ] For warp messaging: is validator signature weight re-validated against current quorum?

### Real-World Examples

#### Known Exploits
- None cited in the audited reports for these issues (liveness/griefing class).

#### Related CVEs/Reports
- [AVAX1] Least Authority, Avalanche–Ethereum bridge smart contracts, 7 July 2023 (Issues A–D)
- [AVAX2] Trail of Bits, AvalancheGo Security Assessment, 8 Aug 2025 (high / DoS)
- [AVAX3] OpenZeppelin, Avalanche Warp Messaging review, 16 Nov 2023 (resolved)

### Keywords for Search

`avalanche`, `avalanchego`, `subnet`, `teleporter`, `bridge receipts`, `retryReceipt`, `relayer incentive`, `queue growth`, `duplicate receipt`, `MaxFeeCap`, `MinerTip`, `fee cap`, `zero address check`, `warp messaging`, `validator signatures`, `BLS aggregate`, `cross-chain liveness`, `griefing`

### Related Vulnerabilities

- DB/unique/l1-misc/polygon-bor-heimdall-validation.md (same receipt/queue liveness class on Polygon)
- DB/bridge/ entries on message replay and relayer economics
