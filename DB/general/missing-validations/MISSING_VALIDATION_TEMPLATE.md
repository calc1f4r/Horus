---
# Core Classification
protocol: generic
chain: everychain
category: input_validation
vulnerability_type: missing_validation

# Attack Vector Details
attack_type: logical_error
affected_component: validation_logic

# Technical Primitives
primitives:
  - input_validation
  - parameter_checking
  - bounds_enforcement
  - state_verification

# Impact Classification
severity: medium  # Range: low|medium|high|critical
impact: varies    # fund_loss, dos, manipulation, state_corruption
exploitability: 0.7
financial_impact: medium

# Context Tags
tags:
  - missing_validation
  - input_sanitization
  - parameter_bounds
  - zero_address
  - state_check

# Version Info
language: solidity
version: all
---

## References
- [Pattern Source]: reports/missing_validations_findings/

---

# MISSING VALIDATION VULNERABILITY TEMPLATE

## Overview

Missing validation vulnerabilities occur when smart contracts fail to properly validate inputs, parameters, state conditions, or relationships before executing critical operations. These are among the most common vulnerability types, representing ~30-40% of all audit findings.

**Root Cause Statement**: This vulnerability exists because [UNTRUSTED INPUT/PARAMETER] in [COMPONENT] is not validated for [CONDITION] before [OPERATION], leading to [IMPACT].

---

## VULNERABILITY PATTERN CATEGORIES

### 1. ADDRESS VALIDATION PATTERNS

#### 1.1 Zero Address Checks

**Where to Look:**
- Constructor parameters
- Initializer functions
- Setter functions (setAdmin, setFeeCollector, setTreasury)
- Token transfer recipients
- Approval targets
- Delegation targets

**Pattern Description:** Functions accept address parameters without verifying they are not `address(0)`.

**Vulnerable Code Pattern:**
```solidity
// ❌ VULNERABLE: No zero address check
function setFeeCollector(address _feeCollector) external onlyOwner {
    feeCollector = _feeCollector; // Can be set to address(0)
}

function initialize(address _admin, address _token) external {
    admin = _admin;     // No validation
    token = _token;     // No validation
}
```

**Secure Implementation:**
```solidity
// ✅ SECURE: Zero address validation
function setFeeCollector(address _feeCollector) external onlyOwner {
    require(_feeCollector != address(0), "Zero address");
    emit FeeCollectorUpdated(feeCollector, _feeCollector);
    feeCollector = _feeCollector;
}

function initialize(address _admin, address _token) external {
    require(_admin != address(0), "Admin zero");
    require(_token != address(0), "Token zero");
    admin = _admin;
    token = _token;
}
```

**Impact:** 
- Permanent loss of admin access
- Funds sent to burn address
- Non-functional fee collection
- Broken governance

**Severity:** LOW to HIGH (depending on the role)

---

#### 1.2 Contract Existence Checks

**Where to Look:**
- Before delegatecall operations
- Before low-level call() operations
- When interacting with user-provided addresses
- When calling interfaces on dynamic addresses

**Pattern Description:** Code assumes an address contains contract code without verification.

**Vulnerable Code Pattern:**
```solidity
// ❌ VULNERABLE: No contract check before delegatecall
function executeOnAdapter(address adapter, bytes calldata data) external {
    (bool success,) = adapter.delegatecall(data); // No extcodesize check
    require(success);
}

// ❌ VULNERABLE: No check if target is a contract
function callExternal(address target, bytes calldata data) external {
    (bool success,) = target.call(data); // Silent success if EOA
}
```

**Secure Implementation:**
```solidity
// ✅ SECURE: Contract existence check
function executeOnAdapter(address adapter, bytes calldata data) external {
    require(adapter.code.length > 0, "Not a contract");
    (bool success,) = adapter.delegatecall(data);
    require(success);
}

// Using OpenZeppelin
import "@openzeppelin/contracts/utils/Address.sol";
function callExternal(address target, bytes calldata data) external {
    require(Address.isContract(target), "Not a contract");
    Address.functionCall(target, data);
}
```

**Impact:** Silent failures, unexpected behavior, delegatecall to EOA

**Severity:** MEDIUM to HIGH

---

### 2. NUMERIC BOUNDS VALIDATION PATTERNS

#### 2.1 Missing Upper/Lower Bounds

**Where to Look:**
- Fee percentage setters
- Interest rate configurations
- Slippage parameters
- Duration/time configurations
- Utilization ratio calculations
- Leverage/ratio parameters

**Pattern Description:** Numeric parameters lack minimum or maximum value constraints.

**Vulnerable Code Pattern:**
```solidity
// ❌ VULNERABLE: Fee can exceed 100%
function setFee(uint256 _fee) external onlyOwner {
    fee = _fee; // No upper bound, can be > 10000 (100%)
}

// ❌ VULNERABLE: Duration can be zero
function setVestingDuration(uint256 _duration) external {
    vestingDuration = _duration; // Can be 0, breaking vesting logic
}

// ❌ VULNERABLE: Utilization can exceed 100%
function withdraw(uint256 amount) external {
    totalSupply -= amount; 
    // Utilization = totalBorrowed / totalSupply can now exceed 100%
}
```

**Secure Implementation:**
```solidity
// ✅ SECURE: Bounded fee
uint256 public constant MAX_FEE = 1000; // 10%
function setFee(uint256 _fee) external onlyOwner {
    require(_fee <= MAX_FEE, "Fee exceeds max");
    emit FeeUpdated(fee, _fee);
    fee = _fee;
}

// ✅ SECURE: Bounded duration
uint256 public constant MIN_DURATION = 1 days;
uint256 public constant MAX_DURATION = 4 * 365 days;
function setVestingDuration(uint256 _duration) external {
    require(_duration >= MIN_DURATION, "Duration too short");
    require(_duration <= MAX_DURATION, "Duration too long");
    vestingDuration = _duration;
}

// ✅ SECURE: Utilization check
function withdraw(uint256 amount) external {
    uint256 newSupply = totalSupply - amount;
    require(newSupply == 0 || (totalBorrowed * 1e18 / newSupply) <= maxUtilization, 
        "Utilization exceeds max");
    totalSupply = newSupply;
}
```

**Impact:** 
- Unbounded interest rates causing overflow
- Division by zero
- DOS through excessive fees
- Market instability

**Severity:** MEDIUM to CRITICAL

---

#### 2.2 Array Length & Index Validation

**Where to Look:**
- Batch operations (batchTransfer, multiCall)
- Paired array operations (addresses[] with amounts[])
- Dynamic array access
- Loop boundaries

**Pattern Description:** Array operations without proper length or index validation.

**Vulnerable Code Pattern:**
```solidity
// ❌ VULNERABLE: No length check, division by zero possible
function distributeRewards(address[] calldata recipients) external {
    uint256 share = totalRewards / recipients.length; // Division by zero if empty
    for (uint i = 0; i < recipients.length; i++) {
        _transfer(recipients[i], share);
    }
}

// ❌ VULNERABLE: Mismatched array lengths
function batchTransfer(address[] calldata to, uint256[] calldata amounts) external {
    for (uint i = 0; i < to.length; i++) {
        _transfer(to[i], amounts[i]); // Out of bounds if amounts shorter
    }
}

// ❌ VULNERABLE: Unbounded array can cause DOS
function processAll(uint256[] calldata data) external {
    for (uint i = 0; i < data.length; i++) { // Can exceed gas limit
        _process(data[i]);
    }
}
```

**Secure Implementation:**
```solidity
// ✅ SECURE: Length validation
function distributeRewards(address[] calldata recipients) external {
    require(recipients.length > 0, "Empty recipients");
    uint256 share = totalRewards / recipients.length;
    for (uint i = 0; i < recipients.length; i++) {
        require(recipients[i] != address(0), "Zero recipient");
        _transfer(recipients[i], share);
    }
}

// ✅ SECURE: Matched lengths
function batchTransfer(address[] calldata to, uint256[] calldata amounts) external {
    require(to.length == amounts.length, "Length mismatch");
    require(to.length > 0 && to.length <= MAX_BATCH_SIZE, "Invalid length");
    for (uint i = 0; i < to.length; i++) {
        _transfer(to[i], amounts[i]);
    }
}
```

**Impact:** Division by zero, out-of-bounds access, gas DOS

**Severity:** LOW to HIGH

---

### 3. PARAMETER RELATIONSHIP VALIDATION PATTERNS

#### 3.1 Time/Duration Relationships

**Where to Look:**
- Vesting schedules (startTime, endTime, cliffDuration)
- Auction parameters (startTime, endTime, duration)
- Lock periods (lockStart, unlockTime)
- Deadline parameters

**Pattern Description:** Related time parameters not validated for logical consistency.

**Vulnerable Code Pattern:**
```solidity
// ❌ VULNERABLE: No relationship validation
function createVesting(
    uint256 startTime,
    uint256 endTime,
    uint256 cliffDuration
) external {
    // Missing: endTime > startTime
    // Missing: cliffDuration < (endTime - startTime)
    // Missing: startTime >= block.timestamp (or intentionally in past?)
    vestingSchedule = VestingSchedule(startTime, endTime, cliffDuration);
}

// ❌ VULNERABLE: End time can be in the past
function setAuction(uint256 endTime) external {
    auctionEndTime = endTime; // No check against block.timestamp
}
```

**Secure Implementation:**
```solidity
// ✅ SECURE: Full relationship validation
function createVesting(
    uint256 startTime,
    uint256 endTime,
    uint256 cliffDuration
) external {
    require(startTime >= block.timestamp, "Start in past");
    require(endTime > startTime, "End before start");
    require(cliffDuration <= endTime - startTime, "Cliff exceeds duration");
    require(endTime - startTime >= MIN_VESTING_DURATION, "Duration too short");
    require(endTime - startTime <= MAX_VESTING_DURATION, "Duration too long");
    
    vestingSchedule = VestingSchedule(startTime, endTime, cliffDuration);
}
```

**Impact:** Broken vesting logic, impossible claims, locked funds

**Severity:** MEDIUM to HIGH

---

#### 3.2 Token/Amount Relationship Validation

**Where to Look:**
- Pool creation (token0, token1)
- Trading pairs
- Multi-token operations
- Supply/allocation sums

**Pattern Description:** Related token or amount parameters not validated for consistency.

**Vulnerable Code Pattern:**
```solidity
// ❌ VULNERABLE: Same token for both sides
function createPair(address tokenA, address tokenB) external {
    // Missing: tokenA != tokenB
    pairs[pairId] = Pair(tokenA, tokenB);
}

// ❌ VULNERABLE: Allocations don't match total
function setCategories(Category[] calldata categories, uint256 totalSupply) external {
    // Missing: sum of category supplies == totalSupply
    for (uint i = 0; i < categories.length; i++) {
        categorySupply[i] = categories[i].supply;
    }
    maxSupply = totalSupply;
}
```

**Secure Implementation:**
```solidity
// ✅ SECURE: Token relationship check
function createPair(address tokenA, address tokenB) external {
    require(tokenA != tokenB, "Identical tokens");
    require(tokenA != address(0) && tokenB != address(0), "Zero address");
    (address token0, address token1) = tokenA < tokenB 
        ? (tokenA, tokenB) 
        : (tokenB, tokenA);
    require(getPair[token0][token1] == address(0), "Pair exists");
    pairs[pairId] = Pair(token0, token1);
}

// ✅ SECURE: Supply sum validation
function setCategories(Category[] calldata categories, uint256 totalSupply) external {
    uint256 sum = 0;
    for (uint i = 0; i < categories.length; i++) {
        sum += categories[i].supply;
        categorySupply[i] = categories[i].supply;
    }
    require(sum >= totalSupply, "Insufficient category supply");
    maxSupply = totalSupply;
}
```

**Impact:** Invalid pairs, stuck funds, broken minting

**Severity:** MEDIUM to HIGH

---

### 4. STATE CONSISTENCY VALIDATION PATTERNS

#### 4.1 Duplicate Prevention

**Where to Look:**
- Adding items to lists (validators, tokens, strategies)
- Registration functions
- Pool/pair creation
- Role assignments

**Pattern Description:** Missing checks to prevent duplicate entries.

**Vulnerable Code Pattern:**
```solidity
// ❌ VULNERABLE: Can add same validator twice
function addValidator(address validator) external onlyOwner {
    validators.push(validator); // No duplicate check
}

// ❌ VULNERABLE: Can register same token multiple times
function registerToken(address token) external {
    registeredTokens.push(token); // No existence check
    isRegistered[token] = true;
}
```

**Secure Implementation:**
```solidity
// ✅ SECURE: Duplicate prevention
mapping(address => bool) public isValidator;

function addValidator(address validator) external onlyOwner {
    require(validator != address(0), "Zero address");
    require(!isValidator[validator], "Already validator");
    
    validators.push(validator);
    isValidator[validator] = true;
    emit ValidatorAdded(validator);
}

function removeValidator(address validator) external onlyOwner {
    require(isValidator[validator], "Not validator");
    isValidator[validator] = false;
    // Remove from array logic...
    emit ValidatorRemoved(validator);
}
```

**Impact:** Double counting, inflated totals, broken invariants

**Severity:** LOW to MEDIUM

---

#### 4.2 State Transition Validation

**Where to Look:**
- Claim functions (claimed snapshots, epochs)
- Withdrawal functions
- State machine transitions
- Order/request processing

**Pattern Description:** Missing validation of current state before state changes.

**Vulnerable Code Pattern:**
```solidity
// ❌ VULNERABLE: Can claim same snapshot multiple times
function claimRewards(uint256 snapshotId) external {
    uint256 amount = calculateRewards(snapshotId);
    lastClaimedSnapshot[msg.sender] = snapshotId; // Bug: if snapshotId=0, resets!
    _transfer(msg.sender, amount);
}

// ❌ VULNERABLE: No check if already processed
function processWithdrawal(uint256 requestId) external {
    WithdrawalRequest storage request = requests[requestId];
    // Missing: require(!request.processed)
    request.processed = true;
    _transfer(request.user, request.amount);
}
```

**Secure Implementation:**
```solidity
// ✅ SECURE: Proper state tracking
function claimRewards(uint256 snapshotId) external {
    require(snapshotId > 0, "Invalid snapshot");
    require(snapshotId > lastClaimedSnapshot[msg.sender], "Already claimed");
    require(snapshotId <= currentSnapshot, "Future snapshot");
    
    uint256 amount = calculateRewards(snapshotId);
    lastClaimedSnapshot[msg.sender] = snapshotId;
    _transfer(msg.sender, amount);
    
    emit RewardsClaimed(msg.sender, snapshotId, amount);
}

// ✅ SECURE: Process state check
function processWithdrawal(uint256 requestId) external {
    WithdrawalRequest storage request = requests[requestId];
    require(request.user != address(0), "Request not found");
    require(!request.processed, "Already processed");
    require(block.timestamp >= request.unlockTime, "Still locked");
    
    request.processed = true;
    _transfer(request.user, request.amount);
}
```

**Impact:** Double claims, double spending, broken accounting

**Severity:** HIGH to CRITICAL

---

### 5. SIGNATURE & NONCE VALIDATION PATTERNS

#### 5.1 Nonce Validation

**Where to Look:**
- Meta-transaction handlers
- Permit functions
- Off-chain signed messages
- Multi-sig operations

**Pattern Description:** Missing or improper nonce validation allowing replay attacks.

**Vulnerable Code Pattern:**
```solidity
// ❌ VULNERABLE: Nonce not validated before use
function executeWithSignature(
    bytes memory signature,
    TxData calldata txData
) external {
    bytes32 digest = hashTx(txData); // txData includes nonce
    address signer = ECDSA.recover(digest, signature);
    require(isAuthorized[signer], "Unauthorized");
    
    // Bug: nonce in txData not checked against stored nonce!
    nonceOf[txData.user]++; // Just increments without checking
    
    _execute(txData);
}
```

**Secure Implementation:**
```solidity
// ✅ SECURE: Proper nonce validation
function executeWithSignature(
    bytes memory signature,
    TxData calldata txData
) external {
    // Validate nonce BEFORE signature verification
    require(txData.nonce == nonceOf[txData.user], "Invalid nonce");
    
    bytes32 digest = hashTx(txData);
    address signer = ECDSA.recover(digest, signature);
    require(isAuthorized[signer], "Unauthorized");
    
    nonceOf[txData.user]++;
    _execute(txData);
}
```

**Impact:** Transaction replay attacks, duplicate operations

**Severity:** HIGH to CRITICAL

---

### 6. ORACLE & EXTERNAL DATA VALIDATION PATTERNS

**Where to Look:**
- Chainlink price feed integrations
- Any external oracle calls
- Cross-chain message handlers
- API response handlers

**Pattern Description:** Missing validation of external data freshness and sanity.

**Vulnerable Code Pattern:**
```solidity
// ❌ VULNERABLE: No staleness or sanity checks
function getPrice() external view returns (uint256) {
    (, int256 price,,,) = priceFeed.latestRoundData();
    return uint256(price); // No checks!
}
```

**Secure Implementation:**
```solidity
// ✅ SECURE: Full oracle validation
function getPrice() external view returns (uint256) {
    (
        uint80 roundId,
        int256 price,
        ,
        uint256 updatedAt,
        uint80 answeredInRound
    ) = priceFeed.latestRoundData();
    
    require(price > 0, "Invalid price");
    require(updatedAt > 0, "Round not complete");
    require(answeredInRound >= roundId, "Stale price");
    require(block.timestamp - updatedAt <= MAX_STALENESS, "Price too old");
    require(uint256(price) <= MAX_PRICE, "Price exceeds max");
    require(uint256(price) >= MIN_PRICE, "Price below min");
    
    return uint256(price);
}
```

**Impact:** Using stale/manipulated prices, incorrect liquidations

**Severity:** HIGH to CRITICAL

---

## DETECTION PATTERNS (FOR AUDITORS)

### Grep/Regex Patterns

```bash
# Find missing zero address checks in setters
rg "function set\w+\(address" --type solidity

# Find constructors without address validation
rg "constructor\s*\([^)]*address" --type solidity

# Find functions that accept arrays without length checks
rg "function \w+\([^)]*\[\]" --type solidity

# Find unchecked low-level calls
rg "\.call\(|\.delegatecall\(" --type solidity

# Find oracle calls without validation
rg "latestRoundData|getPrice|latestAnswer" --type solidity
```

### Semgrep Rules

```yaml
rules:
  - id: missing-zero-address-check
    patterns:
      - pattern: |
          function $FUNC(address $ADDR, ...) {
            ...
            $STATE = $ADDR;
            ...
          }
      - pattern-not: |
          require($ADDR != address(0), ...);
    message: "Missing zero address validation"
    severity: WARNING

  - id: missing-array-length-check
    patterns:
      - pattern: |
          function $FUNC($TYPE[] $ARR, ...) {
            ...
            for (...; $I < $ARR.length; ...) { ... }
            ...
          }
      - pattern-not: |
          require($ARR.length > 0, ...);
    message: "Missing array length validation"
    severity: WARNING
```

---

## AUDIT CHECKLIST

### Constructor/Initializer
- [ ] All address parameters checked for `!= address(0)`
- [ ] All numeric parameters have reasonable bounds
- [ ] Array parameters have length limits
- [ ] Time parameters are logically consistent
- [ ] Sum/total validations for allocations

### Setter Functions
- [ ] New value != current value (prevent event spam)
- [ ] New value within acceptable bounds
- [ ] Address values != address(0)
- [ ] Emit events after successful change

### User-Facing Functions
- [ ] Input amounts > 0 (when required)
- [ ] Input amounts <= available balance
- [ ] Recipient != address(0)
- [ ] Deadline not expired
- [ ] Slippage within acceptable limits

### Batch/Array Operations
- [ ] Arrays not empty (when required)
- [ ] Paired arrays have equal lengths
- [ ] No duplicate entries
- [ ] Gas-safe maximum lengths

### State Transitions
- [ ] Valid current state before transition
- [ ] No double-processing (claimed, executed, etc.)
- [ ] Proper nonce/ID validation

### External Integrations
- [ ] Oracle data staleness checks
- [ ] Oracle data sanity bounds
- [ ] Contract existence checks before calls
- [ ] Return value validation

---

## KEYWORDS FOR SEARCH

**Primary Terms:** missing validation, input validation, parameter check, bounds check, zero address, null check, sanity check, require statement

**Validation Types:** address validation, numeric bounds, array length, duplicate check, state check, nonce validation, staleness check, existence check

**Impact Terms:** stuck funds, double claim, replay attack, division by zero, overflow, underflow, DOS, state corruption

**Code Patterns:** require, assert, revert, if check, validation, sanitize, verify, ensure

**Function Locations:** constructor, initialize, setter, admin function, user function, batch operation, claim, withdraw, transfer
