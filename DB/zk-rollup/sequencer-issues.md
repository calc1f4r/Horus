---
# Core Classification
protocol: generic
chain: arbitrum|optimism|base|zksync|scroll|linea
category: zk_rollup_sequencer
vulnerability_type: sequencer_downtime_dos|sequencer_censorship|sequencer_centralization|l2_timestamp_manipulation|sequencer_underpayment

# Attack Vector Details
attack_type: denial_of_service|economic_exploit|censorship|front_running
affected_component: sequencer|l2_block_proposer|forced_inclusion|batch_submission|forced_transactions

# Technical Primitives
primitives:
  - sequencer_downtime
  - forced_inclusion
  - l2_block_timestamp
  - batch_submission
  - sequencer_uptime_feed
  - grace_period
  - finalize_blocks
  - commit_scalar
  - l1_fee
  - forced_transaction_queue
  - censorship_resistance
  - block_proposer

# Impact Classification
severity: high
impact: dos|censorship|fund_loss|unfair_liquidation|economic_loss
exploitability: 0.40
financial_impact: high

# Context Tags
tags:
  - zk_rollup
  - optimistic_rollup
  - sequencer
  - arbitrum
  - optimism
  - zksync
  - taiko
  - l2
  - forced_inclusion
  - sequencer_downtime
  - censorship

language: solidity
version: all
---

## References & Source Reports

### Protocol Functions Breaking During Sequencer Downtime

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Access-Controlled Functions Fail During Sequencer Downtime | `reports/zk_rollup_findings/access-controlled-functions-cannot-be-called-when-l2-sequencers-are-down.md` | MEDIUM | Multiple |
| Redemptions Blocked During Sequencer Downtime | `reports/zk_rollup_findings/redemptions-are-blocked-when-l2-sequencers-are-down.md` | MEDIUM | Multiple |
| Options Expire During L2 Sequencer Downtime | `reports/zk_rollup_findings/m-4-loss-of-option-token-from-teller-and-reward-from-otlm-if-l2-sequencer-goes-d.md` | MEDIUM | Sherlock |
| Arbitrum Sequencer Downtime Prevents Epoch Transitions | `reports/zk_rollup_findings/m-11-arbitrum-sequencer-downtime-lasting-before-and-beyond-epoch-expiry-prevents.md` | MEDIUM | Sherlock |
| User Unfairly Liquidated After L2 Sequencer Grace Period | `reports/zk_rollup_findings/user-might-be-unfairly-liquidated-after-l2-sequencer-grace-period.md` | MEDIUM | Multiple |
| Dutch Auctions Execute at Bad Prices During Sequencer Down | `reports/zk_rollup_findings/m-3-no-check-for-sequencer-uptime-can-lead-to-dutch-auctions-executing-at-bad-pr.md` | MEDIUM | Multiple |

### Sequencer Centralization and Censorship

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Linea Censors Users to Lock ETH on L2 | `reports/zk_rollup_findings/linea-can-permanently-lock-user-eth-on-l2-by-censoring-user-transactions-through.md` | MEDIUM | Spearbit |
| No Mechanism to Flag Sequencer Fraud | `reports/zk_rollup_findings/no-mechanism-to-flag-sequencer-fraud.md` | HIGH | Multiple |
| Front-Running finalizeBlocks in Decentralized Sequencer | `reports/zk_rollup_findings/front-running-finalizeblocks-when-sequencers-are-decentralized.md` | HIGH | Multiple |
| Lack of Validator Penalties Enables Censorship | `reports/zk_rollup_findings/lack-of-validator-penalties-enables-risk-free-economic-censorship-and-liveness-a.md` | MEDIUM | Multiple |

### Sequencer Economic Issues

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Sequencer Underpaid Due to Incorrect commitScalar | `reports/zk_rollup_findings/h-3-sequencer-will-be-underpaid-because-of-incorrect-commitscalar.md` | HIGH | Sherlock |
| Aggregator Rewards Averaged Across Forced Batches | `reports/zk_rollup_findings/aggregator-rewards-are-averaged-across-forced-batches-rollups.md` | MEDIUM | Multiple |
| Keepers Suffer Losses From L1 Rollup Cost Miscalculation | `reports/zk_rollup_findings/h-6-keepers-will-suffer-significant-losses-due-to-miss-compensation-for-l1-rollu.md` | HIGH | Sherlock |
| Broken Block Time Assumptions Affect AMM Epoch Duration | `reports/zk_rollup_findings/broken-block-time-assumptions-affect-am-amm-epoch-duration-and-can-dos-rebalanci.md` | MEDIUM | Multiple |
| L2 Proposer Can Bias Difficulty | `reports/zk_rollup_findings/l2-proposer-can-signiﬁcantly-bias-diﬃculty.md` | MEDIUM | Multiple |
| Enforced Transactions Signed Off-Chain Likely to Fail | `reports/zk_rollup_findings/enforced-transactions-signed-off-chain-are-likely-to-fail.md` | MEDIUM | Multiple |

---

## Vulnerability Title

**L2 Sequencer Downtime and Centralization Vulnerabilities — Protocol DoS, Censorship, and Economic Exploitation**

### Overview

L2 sequencers are the central operators that order transactions and submit batches to L1. Their downtime or malicious behavior causes cascading failures: DeFi protocols relying on time-sensitive operations (liquidations, options expiry, epoch transitions, Dutch auctions) malfunction; access-controlled functions become unreachable; and economic incentives are misaligned when fee calculations are incorrect. These vulnerabilities are distinct from—and broader than—oracle staleness issues.

---

### Vulnerability Description

#### Root Cause

1. **Downtime blindness**: Protocols assume L2 is always live and use `block.timestamp` without checking if the sequencer is operational
2. **No grace period logic**: After sequencer restart, there is no buffer period before time-sensitive operations resume, causing unfair liquidations on stale prices
3. **Censorship via sequencer role**: A malicious sequencer can exclude specific addresses from having their transactions processed
4. **Incorrect fee parameters**: `commitScalar` and L1 gas cost estimations hard-coded incorrectly cause systematic under/overpayment
5. **Block time assumptions**: Protocols assume 1 block = 2 seconds (L1 cadence) on L2 where block times are different

---

### Pattern 1: Access-Controlled Functions Fail During Sequencer Downtime

**Frequency**: 3/431 reports | **Validation**: Strong

#### Attack Scenario

1. Protocol has time-sensitive functions (e.g., debt repayment, collateral deposit, emergency pause)
2. These functions require calling a smart contract on L2
3. L2 sequencer goes down for 4-24 hours
4. Users cannot submit transactions; time-based deadlines pass
5. When sequencer restarts, users find they've been liquidated, positions have expired, or actions are irreversible

**Example 1: Emergency Functions Blocked by Sequencer Downtime** [MEDIUM]
```solidity
// ❌ VULNERABLE: emergencyRepay() can only be called on L2
// If L2 sequencer is down, users cannot save their position from liquidation
contract LendingPool {
    function emergencyRepay(uint256 amount) external {
        // Requires Arbitrum sequencer to be live to include this transaction
        // No forced-inclusion fallback mechanism
        repay(msg.sender, amount);
    }
    
    function liquidate(address user) external {
        // Health factor calculated using timestamps — if user couldn't repay
        // due to sequencer downtime, they're still liquidated
        require(getHealthFactor(user) < 1e18, "Not liquidatable");
        _liquidate(user);
    }
}
```

**Fix:**
```solidity
// ✅ SECURE: Add sequencer uptime check before enforcing deadlines
import {AggregatorV3Interface} from "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract LendingPool {
    AggregatorV3Interface public sequencerUptimeFeed;
    uint256 constant GRACE_PERIOD = 3600; // 1 hour after restart
    
    modifier whenSequencerUp() {
        (, int256 answer, uint256 startedAt, ,) = sequencerUptimeFeed.latestRoundData();
        require(answer == 0, "Sequencer down");
        require(block.timestamp - startedAt > GRACE_PERIOD, "Grace period active");
        _;
    }
    
    function liquidate(address user) external whenSequencerUp {
        require(getHealthFactor(user) < 1e18, "Not liquidatable");
        _liquidate(user);
    }
}
```

---

### Pattern 2: Dutch Auctions and Options Expire at Bad Prices During Downtime

**Frequency**: 4/431 reports | **Validation**: Strong (Sherlock multiple contests)

#### Attack Scenario

1. Protocol runs Dutch auctions (price decreases linearly over time) or time-limited options
2. L2 sequencer goes down during an active auction/option period
3. When sequencer comes back online, auction start price was high but `block.timestamp` is now much later
4. The Dutch auction has "progressed" through many price steps without any actual time passing on L2
5. Traders snipe the auction at a deeply discounted price, or options expire worthless without user ability to exercise

**Example 2: Dutch Auction Stale Price Exploitation** [MEDIUM]
```solidity
// ❌ VULNERABLE: Dutch auction price depends on block.timestamp
// During sequencer downtime, no transactions are processed
// When sequencer restarts, block.timestamp has advanced but price has crashed
contract DutchAuction {
    uint256 public startTime;
    uint256 public startPrice;
    uint256 public priceDecayRate; // price per second decay
    
    function getCurrentPrice() public view returns (uint256) {
        // BUG: if sequencer was down, elapsed time includes downtime
        // Price is now much lower than it should be
        uint256 elapsed = block.timestamp - startTime;
        return startPrice > elapsed * priceDecayRate 
            ? startPrice - elapsed * priceDecayRate 
            : 0;
    }
    
    function buy() external {
        // No sequencer uptime check — attacker buys at bottom price
        uint256 price = getCurrentPrice();
        _executePurchase(msg.sender, price);
    }
}
```

**Fix:**
```solidity
// ✅ SECURE: Check sequencer is up (and has been up for grace period) before auctions
function buy() external {
    _checkSequencerUptime(); // Revert if sequencer was recently offline
    uint256 price = getCurrentPrice();
    _executePurchase(msg.sender, price);
}
```

---

### Pattern 3: Linea / Sequencer Censorship Locking User Funds

**Frequency**: 2/431 reports | **Validation**: Strong (Linea - Spearbit)

#### Root Cause

On some L2 chains (e.g., early Linea), the sequencer has a `denylist` or role-based exclusion mechanism. A malicious or compromised sequencer operator can add a user's address to the denylist, preventing their transactions from being included. If the L2→L1 withdrawal mechanism also flows through the sequencer, the user cannot exit and their ETH is permanently locked on L2.

**Example 3: Censorship-Based Lock of L2 Funds** [MEDIUM]
```solidity
// ❌ VULNERABLE: Linea L2MessageService allows sequencer to denylist users
// A denylisted address cannot submit L2→L1 messages (withdrawals)
contract L2MessageService {
    mapping(address => bool) public denylisted; // Sequencer-controlled
    
    function submitL2ToL1Message(bytes calldata message) external {
        require(!denylisted[msg.sender], "Address denylisted");
        // Withdrawal is processed... 
        // But denylisted users can NEVER withdraw to L1
    }
}
```

**Fix:**
```solidity
// ✅ SECURE: Uncensorable withdrawal path — users can always force-exit to L1
// Implement L1-based forced withdrawal that bypasses sequencer
contract L1MessageService {
    // Users can submit forced withdrawals directly on L1, bypassing L2 sequencer
    function forceWithdraw(
        address recipient,
        uint256 amount,
        bytes32[] calldata proof
    ) external {
        // Verify user's L2 balance via state proof; no L2 sequencer involvement
        require(_verifyL2Balance(recipient, amount, proof), "Invalid proof");
        _sendEth(recipient, amount);
    }
}
```

---

### Pattern 4: Sequencer Underpaid Due to Incorrect commitScalar

**Frequency**: 2/431 reports | **Validation**: Strong (Sherlock)

#### Root Cause

ZK rollup sequencers (or keepers who submit proofs) are compensated for L1 gas costs via a `commitScalar` parameter encoded in transaction fee calculations. If `commitScalar` is set incorrectly (too low), every submitted batch underpays the sequencer for L1 data publishing costs, leading to sustained economic losses.

**Example 4: Incorrect commitScalar Undercompensates Sequencer** [HIGH]
```solidity
// ❌ VULNERABLE: commitScalar uses wrong L1 gas cost estimate
// Actual calldata cost: 16 gas per non-zero byte, 4 gas per zero byte
// commitScalar is set using old EIP-2028 values without blob consideration

contract FeeCalculator {
    uint256 public commitScalar = 652; // WRONG: should account for EIP-4844 blobs
    
    function calculateL2Fee(uint256 l2GasLimit, uint256 l2GasPrice, uint256 pubdataBytes) 
        public view returns (uint256) 
    {
        uint256 l1GasCost = pubdataBytes * commitScalar; // Underestimates real cost
        return l2GasLimit * l2GasPrice + l1GasCost;
        // Sequencer pays more for L1 than they receive → sustained losses
    }
}
```

**Fix:**
```solidity
// ✅ SECURE: Set commitScalar based on current L1 gas parameters and blob pricing
// commitScalar should be updated dynamically or verified on deployment 
// to accurately reflect L1 data costs (EIP-4844 blob gas)
uint256 public commitScalar; // Must be set correctly at deployment + updatable
```

---

### Pattern 5: Front-Running finalizeBlocks in Decentralized Sequencer Mode

**Frequency**: 1/431 reports | **Validation**: Strong

#### Root Cause

In decentralized sequencer systems where multiple proposers can submit `finalizeBlocks`, the ordering of finalization transactions can be manipulated. A malicious actor can observe a `finalizeBlocks` call in the mempool and front-run it with their own finalization, potentially stealing proposer rewards or preventing honest finalizers from being compensated.

**Example 5: finalizeBlocks Front-Running** [HIGH]
```solidity
// ❌ VULNERABLE: Anyone can call finalizeBlocks for a batch
// Attacker sees honest proposer's finalizeBlocks tx in mempool
// Copies the proof and front-runs with higher gas
contract ZkRollup {
    function finalizeBlocks(
        bytes calldata proof,
        uint256[] calldata publicInputs
    ) external {
        require(verifier.verify(proof, publicInputs), "Invalid proof");
        // Reward goes to msg.sender — attacker steals reward
        _payReward(msg.sender);
    }
}
```

**Fix:**
```solidity
// ✅ SECURE: Commit-reveal or permissioned submission prevents front-running
// Only the designated proposer for a given batch can finalize it
function finalizeBlocks(
    bytes calldata proof,
    uint256[] calldata publicInputs
) external {
    address expectedProposer = batchProposer[currentBatch];
    require(msg.sender == expectedProposer || 
            block.timestamp > proposerDeadline[currentBatch], // fallback after timeout
            "Not authorized proposer");
    require(verifier.verify(proof, publicInputs), "Invalid proof");
    _payReward(msg.sender);
}
```

---

### Impact Analysis

#### Technical Impact
- Time-sensitive DeFi functions (liquidations, auctions, options, epoch transitions) malfunction during downtime
- Access control functions unreachable when sequencer is offline
- Protocols based on L2 `block.timestamp` advance during downtime without user awareness

#### Business Impact
- Mass unfair liquidations when sequencer restarts with stale oracle prices
- Options/vault strategies expire worthless without user ability to act
- Keepers and sequencers suffer economic losses from fee miscalculation
- Users permanently locked out of funds on chains with censorship mechanisms

#### Affected Scenarios
- Any L2 DeFi protocol (lending, options, perpetuals, auctions) on Arbitrum, Optimism, zkSync etc.
- Protocols with epoch-based reward calculations
- Chains where the sequencer has role-based transaction exclusion capabilities

---

### Secure Implementation

```solidity
// ✅ COMPLETE SEQUENCER DOWNTIME GUARD
// Reference: reports/zk_rollup_findings/user-might-be-unfairly-liquidated-after-l2-sequencer-grace-period.md
contract SequencerAwareProtocol {
    AggregatorV3Interface internal l2SequencerFeed;
    uint256 public constant GRACE_PERIOD = 3600; // 1 hour
    
    function isSequencerUp() public view returns (bool, uint256) {
        (, int256 answer, uint256 startedAt, ,) = l2SequencerFeed.latestRoundData();
        // answer == 0 means sequencer is UP
        if (answer != 0) return (false, 0);
        uint256 timeSinceRestart = block.timestamp - startedAt;
        return (timeSinceRestart > GRACE_PERIOD, timeSinceRestart);
    }
    
    modifier requiresSequencerUp() {
        (bool isUp,) = isSequencerUp();
        require(isUp, "Sequencer down or in grace period");
        _;
    }
    
    // Apply to ALL time-sensitive functions:
    function liquidate(address user) external requiresSequencerUp { ... }
    function executeDutchAuction() external requiresSequencerUp { ... }
    function settleOptions() external requiresSequencerUp { ... }
}
```

---

### Detection Patterns

```
1. Contracts on Arbitrum/Optimism/zkSync with liquidate(), auction(), settleOptions() missing sequencer check
2. block.timestamp used in deadline calculations without sequencerUptimeFeed validation
3. Functions protected only by require(block.timestamp > deadline) — doesn't account for sequencer downtime
4. DeFi protocols that pause emergency repay/deposit during L2 downtime
5. Fee calculation contracts with hardcoded gas scalar values (commitScalar, l1BaseFeeScalar)
6. Epoch-based protocols that advance epoch boundaries using block.number on L2
```

### Keywords for Search

`L2 sequencer downtime`, `Arbitrum sequencer offline`, `Optimism sequencer down`, `sequencer uptime feed`, `grace period sequencer`, `unfair liquidation after restart`, `Dutch auction sequencer`, `options expire sequencer`, `epoch transition blocked`, `sequencer censorship`, `L2 forced inclusion`, `sequencer underpaid`, `commitScalar incorrect`, `finalize blocks front-run`, `block timestamp L2`, `sequencer blacklist`, `sequencer denylist`, `forced transaction queue`, `L2 liveness`, `sequencer centralization risk`
