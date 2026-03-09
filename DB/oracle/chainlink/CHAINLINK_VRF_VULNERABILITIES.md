---
# Core Classification (Required)
protocol: generic
chain: everychain
category: randomness
vulnerability_type: chainlink_vrf_integration

# Attack Vector Details (Required)
attack_type: randomness_manipulation|economic_exploit|dos
affected_component: vrf|randomness|callback

# Oracle-Specific Fields
oracle_provider: chainlink
oracle_attack_vector: vrf_manipulation|re_roll|subscription_drain|callback_revert|deprecation

# Technical Primitives (Required)
primitives:
  - VRF
  - VRFConsumerBaseV2
  - requestRandomWords
  - fulfillRandomWords
  - subscription
  - confirmations
  - keyHash
  - callbackGasLimit
  - requestId
  - randomWords

# Impact Classification (Required)
severity: high
impact: manipulation|fund_loss|dos|unfair_outcomes
exploitability: 0.60
financial_impact: high

# Context Tags
tags:
  - defi
  - gaming
  - lottery
  - nft
  - randomness
  - external_dependency

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### VRF Re-Roll / Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Miners can re-roll VRF | `reports/chainlink_findings/h-02-miners-can-re-roll-the-vrf-output-to-game-the-protocol.md` | HIGH | Code4rena |
| Predictable randomness | `reports/chainlink_findings/h-01-predictable-randomness-in-activity-outcomes.md` | HIGH | Multiple |

### VRF Subscription Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Subscription may be drained | `reports/chainlink_findings/h-01-funds-in-subscription-may-be-drained.md` | HIGH | Pashov |
| Users drain VRF subscription | `reports/chainlink_findings/users-can-start-the-same-quest-multiple-times-draining-the-chainlink-vrf-subscri.md` | MEDIUM | Multiple |

### VRF Callback Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| fulfillRandomWords could revert | `reports/chainlink_findings/m-4-fulfillrandomwords-could-revert-under-certain-circumstances.md` | MEDIUM | Sherlock |
| fulfillRandomWords must not revert | `reports/chainlink_findings/n-11-fulfillrandomwords-must-not-revert.md` | LOW | Multiple |

### VRF Deprecation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| VRF V1 deprecated | `reports/chainlink_findings/02-chainlinks-vrf-v1-is-deprecated.md` | LOW | Code4rena |

### External Links
- [Chainlink VRF Documentation](https://docs.chain.link/vrf)
- [VRF Security Considerations](https://docs.chain.link/vrf/v2/security)
- [VRF Best Practices](https://docs.chain.link/vrf/v2/best-practices)

---

# Chainlink VRF Integration Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Chainlink VRF Security Audits**

---

## Table of Contents

1. [VRF Re-Roll / Manipulation Attacks](#1-vrf-re-roll--manipulation-attacks)
2. [Subscription Drain Vulnerabilities](#2-subscription-drain-vulnerabilities)
3. [Callback Revert Issues](#3-callback-revert-issues)
4. [VRF Version Deprecation](#4-vrf-version-deprecation)
5. [Weak Randomness Sources](#5-weak-randomness-sources)
6. [Request Configuration Issues](#6-request-configuration-issues)

---

## 1. VRF Re-Roll / Manipulation Attacks

### Overview

Miners and block producers can potentially manipulate VRF outcomes by choosing whether to include or exclude certain transactions, or by reorganizing the chain to get a different VRF output.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/h-02-miners-can-re-roll-the-vrf-output-to-game-the-protocol.md`
> - `reports/chainlink_findings/c-01-polygon-chain-reorgs-will-often-change-game-results.md`

### Vulnerability Description

#### Root Cause

When VRF request and fulfillment happen in quick succession without sufficient block confirmations, miners can reorganize the chain to produce different randomness outcomes.

#### Attack Scenario

1. Protocol requests VRF randomness
2. Miner/validator sees the VRF fulfillment transaction in mempool
3. If outcome is unfavorable, miner reorganizes chain
4. New chain has different blockhash → different VRF output
5. Miner repeats until favorable outcome

### Vulnerable Pattern Examples

**Example 1: Insufficient Block Confirmations** [HIGH]
> 📖 Reference: `reports/chainlink_findings/h-02-miners-can-re-roll-the-vrf-output-to-game-the-protocol.md`
```solidity
// ❌ VULNERABLE: Low confirmation count allows re-org attacks
uint16 constant REQUEST_CONFIRMATIONS = 1; // Too low!

function requestRandomness() internal returns (uint256 requestId) {
    requestId = COORDINATOR.requestRandomWords(
        keyHash,
        subscriptionId,
        REQUEST_CONFIRMATIONS, // Only 1 confirmation - easily reorged
        callbackGasLimit,
        1
    );
}
```

**Example 2: Same-Block VRF Usage** [HIGH]
> 📖 Reference: Pattern observed in lottery/gaming protocols
```solidity
// ❌ VULNERABLE: Using VRF result immediately
function requestAndUse() external {
    uint256 requestId = requestRandomness();
    // Bad: Using randomness in same transaction/block context
    processResult(requestId);
}
```

### Impact Analysis

#### Technical Impact
- Randomness can be biased by block producers
- Chain reorganization changes outcomes
- Protocol's fairness guarantees violated

#### Business Impact
- Gaming/lottery protocols can be rigged
- NFT minting rarity can be manipulated
- Loss of user trust in fairness

#### Affected Scenarios
- Lotteries and prize draws
- NFT trait/rarity assignment
- Random selection mechanisms
- Gaming protocols with random outcomes

### Secure Implementation

**Fix 1: Sufficient Block Confirmations**
```solidity
// ✅ SECURE: Higher confirmation count
uint16 constant REQUEST_CONFIRMATIONS = 3; // Minimum recommended
// For high-value scenarios, use 6+ confirmations

function requestRandomness() internal returns (uint256 requestId) {
    requestId = COORDINATOR.requestRandomWords(
        keyHash,
        subscriptionId,
        REQUEST_CONFIRMATIONS,
        callbackGasLimit,
        1
    );
}
```

**Fix 2: Time-Delayed Reveal Pattern**
```solidity
// ✅ SECURE: Commit-reveal with time delay
mapping(uint256 => uint256) public requestTimestamps;
uint256 constant REVEAL_DELAY = 1 hours;

function fulfillRandomWords(uint256 requestId, uint256[] memory randomWords) 
    internal override 
{
    require(
        block.timestamp >= requestTimestamps[requestId] + REVEAL_DELAY,
        "Reveal delay not passed"
    );
    // Process randomness
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- REQUEST_CONFIRMATIONS = 1 or 2
- Immediate use of VRF results
- Missing commit-reveal pattern
- High-value outcomes without delay
```

#### Audit Checklist
- [ ] Verify REQUEST_CONFIRMATIONS >= 3 (higher for mainnet)
- [ ] Check for commit-reveal patterns in high-stakes scenarios
- [ ] Verify delay between request and result usage
- [ ] Review if protocol operates on chains with frequent reorgs

---

## 2. Subscription Drain Vulnerabilities

### Overview

VRF subscriptions hold LINK tokens to pay for randomness requests. Malicious actors can drain subscriptions by triggering excessive requests without proper rate limiting or cost validation.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/h-01-funds-in-subscription-may-be-drained.md`
> - `reports/chainlink_findings/users-can-start-the-same-quest-multiple-times-draining-the-chainlink-vrf-subscri.md`
> - `reports/chainlink_findings/craftamount-can-be-set-to-zero-draining-the-chainlink-vrf-subscription.md`

### Vulnerability Description

#### Root Cause

Missing or inadequate access controls and rate limiting on functions that trigger VRF requests. Users can spam requests at minimal cost while protocol pays LINK fees.

#### Attack Scenario

1. Attacker identifies function that triggers VRF request
2. Function lacks rate limiting or has negligible cost
3. Attacker spams requests repeatedly
4. Protocol's LINK subscription is drained
5. Legitimate VRF requests fail due to insufficient balance

### Vulnerable Pattern Examples

**Example 1: No Request Cost** [HIGH]
> 📖 Reference: `reports/chainlink_findings/h-01-funds-in-subscription-may-be-drained.md`
```solidity
// ❌ VULNERABLE: Free VRF requests
function spin(uint256 _totalSlots, uint256 _prizeCount) external {
    // Cost can be gamed to near-zero
    uint256 spinCost = (avgBasePrice * _prizeCount * 1000) / (_totalSlots * 1000);
    // If _totalSlots is huge, spinCost rounds to 0!
    
    usdcToken.transferFrom(msg.sender, address(this), spinCost);
    requestRandomness(); // Drains subscription LINK
}
```

**Example 2: Missing Rate Limiting** [MEDIUM]
> 📖 Reference: `reports/chainlink_findings/users-can-start-the-same-quest-multiple-times-draining-the-chainlink-vrf-subscri.md`
```solidity
// ❌ VULNERABLE: No limit on request frequency
function startQuest() external {
    // User can call repeatedly
    requestRandomness();
    questCount[msg.sender]++;
}
```

### Impact Analysis

#### Technical Impact
- Subscription LINK balance depleted
- DoS for all protocol VRF operations
- Legitimate users blocked from using randomness

#### Business Impact
- Protocol functionality broken
- Additional cost to refill subscription
- User experience degradation

### Secure Implementation

**Fix 1: Minimum Request Cost**
```solidity
// ✅ SECURE: Enforce minimum cost per request
uint256 constant MIN_REQUEST_COST = 1e6; // 1 USDC minimum

function spin(uint256 _totalSlots, uint256 _prizeCount) external {
    uint256 spinCost = calculateSpinCost(_totalSlots, _prizeCount);
    require(spinCost >= MIN_REQUEST_COST, "Cost too low");
    
    usdcToken.transferFrom(msg.sender, address(this), spinCost);
    requestRandomness();
}
```

**Fix 2: Rate Limiting**
```solidity
// ✅ SECURE: Rate limit VRF requests per user
mapping(address => uint256) public lastRequestTime;
uint256 constant REQUEST_COOLDOWN = 1 hours;

function requestRandomness() internal returns (uint256) {
    require(
        block.timestamp >= lastRequestTime[msg.sender] + REQUEST_COOLDOWN,
        "Request cooldown active"
    );
    lastRequestTime[msg.sender] = block.timestamp;
    
    return COORDINATOR.requestRandomWords(...);
}
```

**Fix 3: Pass LINK Cost to User**
```solidity
// ✅ SECURE: User pays for LINK cost
function requestWithPayment() external payable {
    uint256 linkCost = estimateVRFCost();
    require(msg.value >= linkCost, "Insufficient payment");
    
    // Convert ETH to LINK and fund subscription
    // Or charge equivalent in protocol tokens
    
    requestRandomness();
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- VRF request functions callable by anyone
- No minimum payment per VRF request
- Missing cooldown/rate limiting
- Division that can round to zero
```

#### Audit Checklist
- [ ] Verify minimum cost per VRF request
- [ ] Check rate limiting on request functions
- [ ] Review calculation for rounding vulnerabilities
- [ ] Confirm subscription balance monitoring

---

## 3. Callback Revert Issues

### Overview

`fulfillRandomWords` callback must NOT revert, as Chainlink won't retry failed callbacks. Reverts cause lost randomness and stuck protocol states.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/m-4-fulfillrandomwords-could-revert-under-certain-circumstances.md`
> - `reports/chainlink_findings/n-11-fulfillrandomwords-must-not-revert.md`
> - `reports/chainlink_findings/autoredemptionfulfillrequest-should-never-be-allowed-to-revert.md`

### Vulnerability Description

#### Root Cause

Complex logic, external calls, or state validations in `fulfillRandomWords` that can fail under certain conditions.

#### Attack Scenario

1. Protocol requests VRF randomness
2. Chainlink provides randomness callback
3. `fulfillRandomWords` reverts due to:
   - External call failure
   - State validation failure
   - Out of gas
4. Randomness is lost, state becomes stuck
5. Protocol may be permanently blocked

### Vulnerable Pattern Examples

**Example 1: External Calls in Callback** [MEDIUM]
> 📖 Reference: `reports/chainlink_findings/m-4-fulfillrandomwords-could-revert-under-certain-circumstances.md`
```solidity
// ❌ VULNERABLE: External call can fail
function fulfillRandomWords(
    uint256 requestId, 
    uint256[] memory randomWords
) internal override {
    address winner = selectWinner(randomWords[0]);
    
    // External call can revert!
    prizeToken.transfer(winner, prizeAmount);
}
```

**Example 2: State Validation in Callback** [MEDIUM]
> 📖 Reference: Pattern observed in multiple audits
```solidity
// ❌ VULNERABLE: State checks can fail
function fulfillRandomWords(
    uint256 requestId, 
    uint256[] memory randomWords
) internal override {
    Raffle storage raffle = raffles[requestId];
    
    // Can revert if raffle was cancelled!
    require(raffle.status == RaffleStatus.PENDING, "Invalid status");
    
    processWinner(raffle, randomWords[0]);
}
```

**Example 3: Unbounded Loop** [MEDIUM]
```solidity
// ❌ VULNERABLE: Can run out of gas
function fulfillRandomWords(
    uint256 requestId, 
    uint256[] memory randomWords
) internal override {
    // If participants array is large, this can exceed gas limit
    for (uint i = 0; i < participants.length; i++) {
        distributePrize(participants[i], randomWords[i % randomWords.length]);
    }
}
```

### Impact Analysis

#### Technical Impact
- Lost randomness that cannot be recovered
- Stuck protocol states
- Potential permanent DoS

#### Business Impact
- Users cannot complete actions waiting for randomness
- Potential fund lockup
- Protocol reputation damage

### Secure Implementation

**Fix 1: Store and Process Pattern**
```solidity
// ✅ SECURE: Store randomness, process separately
mapping(uint256 => uint256[]) public storedRandomness;

function fulfillRandomWords(
    uint256 requestId, 
    uint256[] memory randomWords
) internal override {
    // Just store - minimal logic, cannot revert
    storedRandomness[requestId] = randomWords;
    emit RandomnessReceived(requestId);
}

function processRandomness(uint256 requestId) external {
    uint256[] memory randomWords = storedRandomness[requestId];
    require(randomWords.length > 0, "No randomness");
    
    // Process with complex logic here - can be retried if fails
    processWinners(randomWords);
    
    delete storedRandomness[requestId];
}
```

**Fix 2: Try/Catch for External Calls**
```solidity
// ✅ SECURE: Handle external call failures
function fulfillRandomWords(
    uint256 requestId, 
    uint256[] memory randomWords
) internal override {
    address winner = selectWinner(randomWords[0]);
    
    // Try external call, handle failure gracefully
    try prizeToken.transfer(winner, prizeAmount) {
        emit PrizeDistributed(winner, prizeAmount);
    } catch {
        // Store for later claim instead
        pendingPrizes[winner] += prizeAmount;
        emit PrizePending(winner, prizeAmount);
    }
}
```

**Fix 3: Sufficient Gas Limit**
```solidity
// ✅ SECURE: Calculate required gas properly
uint32 constant CALLBACK_GAS_LIMIT = 500000; // Sufficient for logic

function requestRandomness() internal returns (uint256) {
    return COORDINATOR.requestRandomWords(
        keyHash,
        subscriptionId,
        confirmations,
        CALLBACK_GAS_LIMIT, // Must cover all callback operations
        numWords
    );
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- External calls in fulfillRandomWords
- require/revert statements in callback
- Unbounded loops in callback
- Complex business logic in callback
- Low callbackGasLimit
```

#### Audit Checklist
- [ ] Verify fulfillRandomWords has minimal logic
- [ ] Check no external calls that can fail
- [ ] Confirm no require/revert statements
- [ ] Verify callbackGasLimit is sufficient
- [ ] Review for unbounded iterations

---

## 4. VRF Version Deprecation

### Overview

Chainlink VRF V1 is deprecated. Projects using V1 should migrate to V2 for improved security and features.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/02-chainlinks-vrf-v1-is-deprecated.md`

### Vulnerability Description

#### Root Cause

VRF V1 has security limitations and is no longer maintained. New security patches and improvements only apply to V2.

### Vulnerable Pattern Examples

**Example 1: Using VRF V1** [LOW]
> 📖 Reference: `reports/chainlink_findings/02-chainlinks-vrf-v1-is-deprecated.md`
```solidity
// ❌ VULNERABLE: Using deprecated VRF V1
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract OldVRF is VRFConsumerBase {
    // V1 implementation - deprecated
}
```

### Secure Implementation

**Fix 1: Use VRF V2**
```solidity
// ✅ SECURE: Use VRF V2
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";

contract ModernVRF is VRFConsumerBaseV2 {
    VRFCoordinatorV2Interface COORDINATOR;
    
    constructor(address coordinator) VRFConsumerBaseV2(coordinator) {
        COORDINATOR = VRFCoordinatorV2Interface(coordinator);
    }
    
    function requestRandomWords() internal returns (uint256 requestId) {
        requestId = COORDINATOR.requestRandomWords(
            keyHash,
            subscriptionId,
            requestConfirmations,
            callbackGasLimit,
            numWords
        );
    }
    
    function fulfillRandomWords(
        uint256 requestId,
        uint256[] memory randomWords
    ) internal override {
        // Process randomness
    }
}
```

---

## 5. Weak Randomness Sources

### Overview

Some protocols use predictable or manipulable sources of randomness instead of VRF, or combine VRF with weak sources that undermine security.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/m-01-insecure-generation-of-randomness-used-for-token-determination-logic.md`
> - `reports/chainlink_findings/m-06-bad-source-of-randomness.md`
> - `reports/chainlink_findings/predictable-sources-of-randomness.md`

### Vulnerable Pattern Examples

**Example 1: Using block.timestamp** [HIGH]
```solidity
// ❌ VULNERABLE: Predictable randomness
function pseudoRandom() internal view returns (uint256) {
    return uint256(keccak256(abi.encodePacked(
        block.timestamp,  // Manipulable by miners
        block.difficulty, // Deprecated, now 0 on PoS
        msg.sender
    )));
}
```

**Example 2: Using blockhash alone** [HIGH]
```solidity
// ❌ VULNERABLE: Can be predicted/manipulated
function getRandomNumber(uint256 blockNumber) external view returns (uint256) {
    return uint256(blockhash(blockNumber)); // Predictable!
}
```

### Secure Implementation

**Fix: Use Chainlink VRF**
```solidity
// ✅ SECURE: True randomness from VRF
function fulfillRandomWords(
    uint256 requestId,
    uint256[] memory randomWords
) internal override {
    // Use VRF-provided randomness
    uint256 trueRandom = randomWords[0];
    processRandom(trueRandom);
}
```

---

## 6. Request Configuration Issues

### Overview

Improper VRF request configuration can lead to security issues, failed requests, or wasted gas.

> **📚 Source Reports for Deep Dive:**
> - `reports/chainlink_findings/l-13-requestconfirmations-below-chainlink-minimum-allowed-in-updatevrfconfig.md`

### Vulnerable Pattern Examples

**Example 1: Too Low Request Confirmations** [LOW]
```solidity
// ❌ VULNERABLE: Below Chainlink minimum (3)
uint16 constant REQUEST_CONFIRMATIONS = 1;
```

**Example 2: Insufficient Callback Gas** [MEDIUM]
```solidity
// ❌ VULNERABLE: Gas too low for callback logic
uint32 constant CALLBACK_GAS_LIMIT = 50000; // Not enough!
```

### Secure Implementation

**Fix: Proper Configuration**
```solidity
// ✅ SECURE: Proper VRF configuration
uint16 constant REQUEST_CONFIRMATIONS = 3; // Minimum recommended
uint32 constant CALLBACK_GAS_LIMIT = 500000; // Sufficient for callback
uint32 constant NUM_WORDS = 1;

function requestRandomWords() internal returns (uint256) {
    return COORDINATOR.requestRandomWords(
        keyHash,
        subscriptionId,
        REQUEST_CONFIRMATIONS,
        CALLBACK_GAS_LIMIT,
        NUM_WORDS
    );
}
```

---

## Prevention Guidelines

### Development Best Practices

1. **Use VRF V2** - Never use deprecated V1
2. **Sufficient confirmations** - Minimum 3, higher for high-value
3. **Callback safety** - fulfillRandomWords must not revert
4. **Rate limiting** - Prevent subscription drain attacks
5. **User cost recovery** - Pass VRF costs to users
6. **Gas estimation** - Ensure callbackGasLimit covers all logic

### Testing Requirements

- Test callback with various failure scenarios
- Fuzz test subscription drain vectors
- Test with insufficient gas
- Simulate chain reorganization effects

---

## Keywords for Search

`chainlink vrf`, `vrf v2`, `vrf v1`, `requestRandomWords`, `fulfillRandomWords`, `randomness`, `random`, `subscription`, `callback`, `confirmations`, `re-roll`, `miner manipulation`, `block producer`, `reorg`, `lottery`, `gaming`, `nft`, `trait`, `rarity`, `callbackGasLimit`, `keyHash`, `VRFConsumerBaseV2`, `COORDINATOR`, `subscription drain`, `rate limit`

---

## Related Vulnerabilities

- [Chainlink Price Feed Vulnerabilities](./CHAINLINK_PRICE_FEED_VULNERABILITIES.md)
- [Chainlink CCIP Vulnerabilities](./CHAINLINK_CCIP_VULNERABILITIES.md)
- [Chainlink Automation Vulnerabilities](./CHAINLINK_AUTOMATION_VULNERABILITIES.md)
