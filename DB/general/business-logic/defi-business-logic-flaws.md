---
# Core Classification
protocol: generic
chain: everychain
category: logic
vulnerability_type: business_logic_flaw

# Attack Vector Details
attack_type: logical_error
affected_component: state_transitions

# Technical Primitives
primitives:
  - state_machine
  - validation_logic
  - calculation_logic
  - token_accounting
  - health_factor
  - exchange_rate
  - share_calculation
  - burn_mechanism
  - mint_mechanism
  - reward_distribution

# Impact Classification
severity: critical
impact: fund_loss
exploitability: 0.7
financial_impact: critical

# Context Tags
tags:
  - defi
  - lending
  - dex
  - yield
  - staking
  - real_exploit
  - business_logic

# Version Info
language: solidity
version: ">=0.6.0"

source: DeFiHackLabs
---

## DeFi Business Logic Flaw Vulnerabilities

### Overview

Business logic flaws are the most prevalent vulnerability class in DeFi, encompassing errors in protocol state machine design, calculation logic, validation sequences, and token handling mechanisms. These vulnerabilities arise when smart contract logic deviates from intended economic or operational behavior, allowing attackers to extract value through legitimate function calls executed in unexpected sequences or with malicious parameters.

**Key Statistics from DeFiHackLabs:**
- **100+ documented incidents** (2022-2025)
- **Total losses exceeding $500M USD**
- **Major incidents:** Euler Finance ($200M), Nomad Bridge ($152M), HedgeyFinance ($48M), Level Finance ($1M)

---

### Vulnerability Description

#### Root Cause Categories

Business logic flaws stem from multiple root causes:

1. **Incorrect State Transitions** - Protocol state machine allows invalid state sequences
2. **Missing Validation on Critical Operations** - Insufficient checks before state-changing operations
3. **Incorrect Calculation/Accounting** - Flawed arithmetic in share/token/reward calculations
4. **Improper Token Handling** - Incorrect burn, mint, or transfer logic
5. **Insolvency/Health Factor Check Bypasses** - Checks performed at wrong time or with wrong parameters
6. **Share/Exchange Rate Manipulation** - Exploitable donation or inflation attacks
7. **Protocol-Specific Logic Errors** - Unique flaws in protocol design

---

## Category 1: Incorrect State Transitions

### Description
Protocol allows state changes in an unexpected order, bypassing security invariants.

### Attack Scenario
1. Attacker identifies function call sequences not anticipated by developers
2. Executes operations in an order that violates implicit protocol invariants
3. Achieves state that enables value extraction

### Vulnerable Pattern Examples

**Example 1: Euler Finance (2023-03, $200M)** [CRITICAL]
```solidity
// ❌ VULNERABLE: donateToReserves allows self-liquidation setup
// The protocol allowed:
// 1. deposit() -> receive eTokens
// 2. mint() -> borrow 10x, receive eTokens and dTokens
// 3. repay() -> partial debt repayment
// 4. mint() again -> more leverage
// 5. donateToReserves() -> reduce collateral below debt
// 6. liquidate() own account -> profit from liquidation bonus

function donateToReserves(uint subAccountId, uint amount) external {
    // @audit No check if this creates underwater position
    // @audit Allows setting up self-liquidation for profit
    (uint poolSize, uint origBalance) = getPoolSizes(underlying);
    
    // Donation reduces collateral without reducing debt
    balanceOf[account] -= amount;
    reserves += amount;
}

function liquidate(address violator, address underlying, ...) external {
    // @audit Attacker can liquidate their own underwater position
    // @audit Receives liquidation bonus on assets they donated
    checkLiquidation(liquidator, violator, underlying, collateral);
    // Transfer collateral to liquidator with discount
}
```

**Example 2: Level Finance (2023-05, $1M)** [HIGH]
```solidity
// ❌ VULNERABLE: Claim function lacks proper epoch/timing checks
function claimReward(address _to, uint256 _amount) external {
    // @audit Missing: Check if reward period has ended
    // @audit Missing: Check if user has already claimed this epoch
    // @audit Missing: Rate limiting on claims
    require(rewardBalance >= _amount, "Insufficient rewards");
    
    // Attacker can claim multiple times in same epoch
    rewardBalance -= _amount;
    token.transfer(_to, _amount);
}
```

**Example 3: Platypus Finance (2023-02, $8.5M)** [HIGH]
```solidity
// ❌ VULNERABLE: Borrow allowed even when position insolvent
function borrow(uint256 amount) external {
    // @audit Check happens AFTER state changes, not before
    _mint(msg.sender, amount);
    
    // Solvency checked after funds already minted
    // Attacker can exploit by manipulating check conditions
    require(isSolvent(msg.sender), "Insolvent");
}
```

### Real-World Incidents

| Protocol | Date | Loss | Pattern |
|----------|------|------|---------|
| Euler Finance | 2023-03 | $200M | donate + self-liquidation |
| Level Finance | 2023-05 | $1M | Multi-claim in same epoch |
| Platypus | 2023-02 | $8.5M | Emergency withdraw flaw |
| Platypus | 2023-07 | $51K | Second exploit same pattern |
| Platypus | 2023-10 | $2M | Third incident |

### Secure Implementation

```solidity
// ✅ SECURE: State machine with explicit transitions
enum State { INACTIVE, DEPOSITED, BORROWED, LIQUIDATABLE }

mapping(address => State) public accountState;

function donateToReserves(uint amount) external {
    require(accountState[msg.sender] != State.BORROWED, "Cannot donate while borrowed");
    
    // Check position remains healthy after donation
    uint newCollateral = collateral[msg.sender] - amount;
    uint debt = debts[msg.sender];
    require(newCollateral * LTV >= debt * PRECISION, "Would create insolvent position");
    
    _executeDonation(amount);
}

function liquidate(address violator) external {
    require(msg.sender != violator, "Cannot self-liquidate");
    require(isLiquidatable(violator), "Position not liquidatable");
    _executeLiquidation(violator);
}
```

---

## Category 2: Missing Validation on Critical Operations

### Description
Critical state-changing functions lack sufficient input validation, parameter checks, or access control.

### Attack Scenario
1. Attacker identifies function with weak or missing validation
2. Supplies malicious or edge-case parameters
3. Achieves unexpected state change or value extraction

### Vulnerable Pattern Examples

**Example 1: HedgeyFinance (2024-04, $48M)** [CRITICAL]
```solidity
// ❌ VULNERABLE: No validation on claim parameters
function claimTokens(
    address token,
    uint256 amount,
    bytes32[] calldata proof
) external {
    // @audit Missing: Verify proof corresponds to msg.sender
    // @audit Missing: Check if already claimed
    // @audit Missing: Validate amount against merkle root
    
    IERC20(token).transfer(msg.sender, amount);
    emit TokensClaimed(msg.sender, amount);
}
```

**Example 2: Nomad Bridge (2022-08, $152M)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Accepts uninitialized/zero merkle root as valid
function process(bytes memory _message) external {
    bytes32 _messageHash = keccak256(_message);
    
    // @audit acceptableRoot was set to 0x0 during upgrade
    // @audit 0x0 was treated as valid, allowing any message
    require(acceptableRoot(messages[_messageHash]), "Invalid root");
    
    _process(_message);
}

function acceptableRoot(bytes32 _root) public view returns (bool) {
    // @audit Returns true for 0x0 root after misconfigured upgrade
    return confirmAt[_root] != 0 || _root == bytes32(0);
}
```

**Example 3: IPC Token (2025-01, $590K)** [HIGH]
```solidity
// ❌ VULNERABLE: Burns from wrong pair in transfer
function _transfer(address from, address to, uint256 amount) internal {
    // @audit Incorrectly identifies burn target
    // @audit Burns from unintended liquidity pair
    if (shouldBurn(from, to)) {
        // Bug: burns from wrong pair, draining liquidity
        _burn(incorrectPair, burnAmount);
    }
    
    super._transfer(from, to, amount);
}
```

### Real-World Incidents

| Protocol | Date | Loss | Missing Validation |
|----------|------|------|-------------------|
| HedgeyFinance | 2024-04 | $48M | Claim proof validation |
| Nomad Bridge | 2022-08 | $152M | Merkle root validation |
| IPC Token | 2025-01 | $590K | Burn target validation |
| Reaper Farm | 2022-08 | $1.7M | Access control on withdraw |
| Hexotic | 2025-08 | $500 | Input validation |

### Secure Implementation

```solidity
// ✅ SECURE: Comprehensive validation
function claimTokens(
    address token,
    uint256 amount,
    bytes32[] calldata proof
) external nonReentrant {
    // Validate not already claimed
    require(!claimed[msg.sender][token], "Already claimed");
    
    // Validate proof corresponds to caller
    bytes32 leaf = keccak256(abi.encodePacked(msg.sender, token, amount));
    require(MerkleProof.verify(proof, merkleRoot, leaf), "Invalid proof");
    
    // Validate amount within bounds
    require(amount > 0 && amount <= maxClaimAmount, "Invalid amount");
    
    // Mark as claimed before transfer (CEI pattern)
    claimed[msg.sender][token] = true;
    
    // Execute transfer
    IERC20(token).safeTransfer(msg.sender, amount);
    
    emit TokensClaimed(msg.sender, token, amount);
}
```

---

## Category 3: Incorrect Calculation/Accounting

### Description
Mathematical errors in share calculations, reward distributions, fee computations, or token accounting.

### Attack Scenario
1. Attacker identifies calculation flaw (rounding, overflow, precision loss)
2. Exploits the flaw through specific parameter selection
3. Extracts more value than entitled to

### Vulnerable Pattern Examples

**Example 1: FPC Token (2025-07, $4.7M)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Incorrect fee calculation
function _transfer(address from, address to, uint256 amount) internal {
    uint256 fee = amount * feePercent / 100;
    uint256 netAmount = amount - fee;
    
    // @audit Fee calculation doesn't account for edge cases
    // @audit Rounding errors accumulate on repeated transfers
    // @audit Fee can be bypassed with specific amounts
    
    balances[from] -= amount;
    balances[to] += netAmount;
    balances[feeReceiver] += fee;
}
```

**Example 2: SEAMAN Token (2022-11, $7K)** [MEDIUM]
```solidity
// ❌ VULNERABLE: Reflection token with flawed accounting
function _getReflectionRate() internal view returns (uint256) {
    // @audit Rate calculation can be manipulated
    // @audit Division by excluded balance can cause issues
    uint256 rSupply = _rTotal;
    uint256 tSupply = _tTotal;
    
    for (uint256 i = 0; i < _excluded.length; i++) {
        // @audit Doesn't handle edge case of all supply excluded
        rSupply -= _rOwned[_excluded[i]];
        tSupply -= _tOwned[_excluded[i]];
    }
    
    return rSupply / tSupply;
}
```

**Example 3: ElasticSwap (2022-12, $845K)** [HIGH]
```solidity
// ❌ VULNERABLE: Rebasing token handling flaw
function swap(uint256 amountIn) external {
    // @audit Doesn't account for elastic supply changes
    // @audit LP accounting assumes static balances
    
    uint256 amountOut = getAmountOut(amountIn);
    
    // Transfer without considering rebase
    tokenIn.transferFrom(msg.sender, address(this), amountIn);
    tokenOut.transfer(msg.sender, amountOut);
    
    // @audit Reserves become desynced from actual balances
    _updateReserves();
}
```

### Real-World Incidents

| Protocol | Date | Loss | Calculation Error |
|----------|------|------|-------------------|
| FPC Token | 2025-07 | $4.7M | Fee calculation |
| Tradeonorion | 2024-05 | $645K | Accounting flaw |
| SEAMAN | 2022-11 | $7K | Reflection rate |
| ElasticSwap | 2022-12 | $845K | Rebase handling |
| SDAO | 2022-11 | $13K | Reward calculation |

### Secure Implementation

```solidity
// ✅ SECURE: Precise calculation with checks
function _transfer(address from, address to, uint256 amount) internal {
    require(amount > 0, "Zero amount");
    require(balances[from] >= amount, "Insufficient balance");
    
    // Calculate fee with precision handling
    uint256 fee = (amount * feePercent) / PRECISION;
    uint256 netAmount = amount - fee;
    
    // Ensure no rounding errors cause inconsistency
    require(fee + netAmount == amount, "Calculation error");
    
    // Update balances atomically
    balances[from] -= amount;
    balances[to] += netAmount;
    
    if (fee > 0) {
        balances[feeReceiver] += fee;
        emit FeeCollected(from, fee);
    }
    
    emit Transfer(from, to, netAmount);
}
```

---

## Category 4: Improper Token Handling (Burn/Mint/Transfer)

### Description
Flawed implementation of token burn, mint, or transfer mechanisms that can be exploited.

### Attack Scenario
1. Attacker identifies flaw in burn/mint/transfer logic
2. Exploits to either create tokens from nothing or destroy others' tokens
3. Profits from resulting supply/price manipulation

### Vulnerable Pattern Examples

**Example 1: WXC Token (2025-08, 37.5 WBNB)** [HIGH]
```solidity
// ❌ VULNERABLE: Incorrect burn mechanism in transfer
function _transfer(address from, address to, uint256 amount) internal {
    if (to == uniswapPair) {
        // @audit Burns from pair instead of sender
        // @audit Attacker can drain pair liquidity
        uint256 burnAmount = amount * burnRate / 100;
        _burn(uniswapPair, burnAmount);
    }
    
    super._transfer(from, to, amount);
}
```

**Example 2: WETC Token (2025-07, $101K)** [HIGH]
```solidity
// ❌ VULNERABLE: Burn logic burns wrong address
function transfer(address to, uint256 amount) external returns (bool) {
    // @audit Burn target calculation is flawed
    address burnTarget = _getBurnTarget();
    
    // @audit Burns from pair/protocol instead of sender
    if (shouldBurn()) {
        _burn(burnTarget, calculateBurn(amount));
    }
    
    return _transfer(msg.sender, to, amount);
}
```

**Example 3: NORMIE Token (2024-05, $490K)** [HIGH]
```solidity
// ❌ VULNERABLE: Deflationary mechanism exploitable
function _beforeTokenTransfer(address from, address to, uint256 amount) internal {
    // @audit Tax/burn applies inconsistently
    // @audit Can be exploited with specific transfer sequences
    if (isTaxed[from] || isTaxed[to]) {
        uint256 tax = amount * taxRate / 100;
        // @audit Tax collected but not properly accounted
        super._transfer(from, taxWallet, tax);
    }
}
```

### Real-World Incidents

| Protocol | Date | Loss | Token Handling Issue |
|----------|------|------|---------------------|
| WXC Token | 2025-08 | 37.5 WBNB | Wrong burn target |
| WETC Token | 2025-07 | $101K | Incorrect burn logic |
| NORMIE | 2024-05 | $490K | Deflationary exploit |
| LPC | 2022-07 | $45K | Self-transfer balance double |
| SSS Token | 2024-03 | $4.8M | Self-transfer exploit |

### Secure Implementation

```solidity
// ✅ SECURE: Proper burn mechanism
function _transfer(address from, address to, uint256 amount) internal {
    require(from != address(0), "Transfer from zero");
    require(to != address(0), "Transfer to zero");
    require(balanceOf[from] >= amount, "Insufficient balance");
    
    uint256 burnAmount = 0;
    if (shouldApplyBurn(from, to)) {
        burnAmount = (amount * burnRate) / PRECISION;
        // Burn from sender, not from any other address
        _burn(from, burnAmount);
    }
    
    uint256 transferAmount = amount - burnAmount;
    
    balanceOf[from] -= amount;
    balanceOf[to] += transferAmount;
    
    emit Transfer(from, to, transferAmount);
    if (burnAmount > 0) {
        emit Transfer(from, address(0), burnAmount);
    }
}

function _burn(address account, uint256 amount) internal {
    require(account != address(0), "Burn from zero address");
    require(balanceOf[account] >= amount, "Burn exceeds balance");
    
    balanceOf[account] -= amount;
    totalSupply -= amount;
    
    emit Transfer(account, address(0), amount);
}
```

---

## Category 5: Insolvency/Health Factor Check Bypasses

### Description
Lending protocols fail to properly enforce solvency constraints, allowing underwater positions or check timing issues.

### Attack Scenario
1. Attacker identifies when/how solvency checks can be bypassed
2. Creates position that passes checks but is actually insolvent
3. Extracts value before or instead of being liquidated

### Vulnerable Pattern Examples

**Example 1: SharwaFinance (2025-10, $146K)** [HIGH]
```solidity
// ❌ VULNERABLE: Post-insolvency check instead of pre-check
function borrow(uint256 amount) external {
    // @audit Check happens AFTER funds transferred
    _transferTokens(msg.sender, amount);
    
    // @audit Too late - attacker already has funds
    require(isHealthy(msg.sender), "Position unhealthy");
}
```

**Example 2: MIMSpell3/Abracadabra (2025-10, $3.5M combined)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Insolvency check bypassed through donation
function repay(uint256 amount) external {
    // @audit Partial repay allowed even when insolvent
    debts[msg.sender] -= amount;
    
    // @audit No check if position is still valid
    // @audit Attacker can set up liquidation arbitrage
}

function liquidate(address user) external {
    // @audit Check can be manipulated through donation
    require(!isHealthy(user), "Cannot liquidate");
    
    // @audit Attacker profits from self-liquidation
    _executeLiquidation(user);
}
```

**Example 3: BlueberryProtocol (2024-02, $1.4M)** [HIGH]
```solidity
// ❌ VULNERABLE: Health check uses stale price
function withdraw(uint256 amount) external {
    // @audit Uses cached price, not current
    uint256 healthFactor = calculateHealth(msg.sender, cachedPrice);
    
    require(healthFactor > MIN_HEALTH, "Unhealthy");
    
    // @audit By the time withdrawal happens, price may have changed
    _executeWithdraw(msg.sender, amount);
}
```

### Real-World Incidents

| Protocol | Date | Loss | Bypass Method |
|----------|------|------|---------------|
| SharwaFinance | 2025-10 | $146K | Post-insolvency check |
| MIMSpell3 | 2025-10 | $1.7M | Insolvency check bypass |
| Abracadabra | 2025-10 | $1.8M | Logic flaw |
| BlueberryProtocol | 2024-02 | $1.4M | Stale health check |
| Unilend | 2025-01 | 60 stETH | Health factor bypass |

### Secure Implementation

```solidity
// ✅ SECURE: Pre-check with atomic state updates
function borrow(uint256 amount) external nonReentrant {
    // Pre-check: Will position be healthy after borrow?
    uint256 newDebt = debts[msg.sender] + amount;
    uint256 collateralValue = getCollateralValue(msg.sender);
    
    require(
        collateralValue * LTV_PRECISION >= newDebt * requiredLTV,
        "Would create unhealthy position"
    );
    
    // Update state
    debts[msg.sender] = newDebt;
    totalBorrowed += amount;
    
    // Post-check: Verify invariant still holds
    require(isHealthy(msg.sender), "Position unhealthy");
    
    // Transfer only after all checks pass
    _transferTokens(msg.sender, amount);
    
    emit Borrowed(msg.sender, amount, newDebt);
}

function isHealthy(address user) public view returns (bool) {
    // Always use fresh price
    uint256 currentPrice = oracle.getLatestPrice();
    uint256 collateralValue = (collateral[user] * currentPrice) / PRECISION;
    uint256 debtValue = debts[user];
    
    if (debtValue == 0) return true;
    
    return (collateralValue * PRECISION) / debtValue >= MIN_HEALTH_FACTOR;
}
```

---

## Category 6: Share/Exchange Rate Manipulation (Donation/Inflation Attacks)

### Description
Exploiting share price calculation through donations or first-depositor advantages.

### Attack Scenario
1. Attacker deposits minimal amount to become first depositor
2. Donates large amount to inflate share price
3. Subsequent depositors receive fewer shares due to inflated price
4. Attacker profits from the manipulation

### Vulnerable Pattern Examples

**Example 1: BaoCommunity (2023-07, $46K)** [HIGH]
```solidity
// ❌ VULNERABLE: Classic vault inflation
function deposit(uint256 assets) external returns (uint256 shares) {
    // @audit First depositor can manipulate share price
    uint256 totalAssets = asset.balanceOf(address(this));
    uint256 totalShares = totalSupply();
    
    if (totalShares == 0) {
        shares = assets;  // @audit 1:1 on first deposit
    } else {
        // @audit Donation before second deposit inflates this
        shares = (assets * totalShares) / totalAssets;
    }
    
    // @audit With inflated totalAssets, shares rounds to 0
    _mint(msg.sender, shares);
}
```

**Example 2: Raft_fi (2023-11, $3.2M)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Donation + rounding in collateral calculation
function borrow(uint256 amount) external {
    // @audit Exchange rate manipulable through donation
    uint256 shares = convertToShares(amount);
    
    // @audit Rounding errors compound the issue
    // @audit Attacker can extract more than deposited
    _mint(msg.sender, shares);
}
```

### Real-World Incidents

| Protocol | Date | Loss | Attack Vector |
|----------|------|------|---------------|
| BaoCommunity | 2023-07 | $46K | Donation inflation |
| Raft_fi | 2023-11 | $3.2M | Donation + rounding |
| HundredFinance | 2023-04 | $7M | CompoundV2 inflation |
| WiseLending | 2023-10 | $260K | Donate + rounding |
| MahaLend | 2023-11 | $20K | Inflation attack |

### Secure Implementation

```solidity
// ✅ SECURE: Protected against inflation attacks
uint256 public constant MINIMUM_SHARES = 1000;

function deposit(uint256 assets) external returns (uint256 shares) {
    require(assets > 0, "Zero deposit");
    
    uint256 totalAssets = _totalAssets();
    uint256 totalShares = totalSupply();
    
    if (totalShares == 0) {
        // Mint minimum shares to dead address on first deposit
        shares = assets;
        require(shares > MINIMUM_SHARES, "Initial deposit too small");
        
        // Dead shares prevent inflation attack
        _mint(address(0xdead), MINIMUM_SHARES);
        shares -= MINIMUM_SHARES;
    } else {
        shares = (assets * totalShares) / totalAssets;
        // Ensure meaningful share amount
        require(shares > 0, "Shares round to zero");
    }
    
    asset.safeTransferFrom(msg.sender, address(this), assets);
    _mint(msg.sender, shares);
    
    emit Deposit(msg.sender, assets, shares);
}

function _totalAssets() internal view returns (uint256) {
    // Use tracked balance, not actual balance
    // Prevents donation manipulation
    return trackedBalance;
}
```

---

## Category 7: Protocol-Specific Logic Errors

### Description
Unique vulnerabilities arising from specific protocol designs, often combining multiple issues.

### Attack Scenario
Protocol-specific scenarios vary widely but typically involve exploiting unique protocol mechanics.

### Vulnerable Pattern Examples

**Example 1: Pawnfi (2023-06, $820K)** [HIGH]
```solidity
// ❌ VULNERABLE: NFT collateral valuation flaw
function borrowAgainstNFT(uint256 tokenId, uint256 amount) external {
    // @audit NFT valuation can be manipulated
    // @audit Same NFT can be used multiple times
    uint256 nftValue = getNFTValue(tokenId);
    
    require(amount <= nftValue * LTV / 100, "Exceeds LTV");
    
    // @audit Missing: Check if NFT already collateralized
    collateralized[tokenId] = true;
    _borrow(msg.sender, amount);
}
```

**Example 2: FloorProtocol (2023-12, $1.6M)** [HIGH]
```solidity
// ❌ VULNERABLE: NFT fractionalization flaw
function redeemFragments(uint256 fragmentAmount) external {
    // @audit Redemption logic allows gaming
    // @audit Can redeem more value than fragments worth
    
    uint256 nftValue = calculateRedemptionValue(fragmentAmount);
    
    // @audit Missing slippage/time checks
    _transferNFT(msg.sender, selectedNFT);
    _burn(msg.sender, fragmentAmount);
}
```

**Example 3: Palmswap (2023-07, $900K)** [HIGH]
```solidity
// ❌ VULNERABLE: Perpetual position manipulation
function updatePosition(uint256 positionId, int256 sizeDelta) external {
    Position storage pos = positions[positionId];
    
    // @audit Size update doesn't properly validate against collateral
    // @audit Can create overleveraged position
    pos.size += sizeDelta;
    
    // @audit Margin check uses stale funding rate
    require(isPositionHealthy(positionId), "Unhealthy");
}
```

### Real-World Incidents

| Protocol | Date | Loss | Protocol Type | Issue |
|----------|------|------|---------------|-------|
| Pawnfi | 2023-06 | $820K | NFT Lending | Collateral reuse |
| FloorProtocol | 2023-12 | $1.6M | NFT Fractionalization | Redemption flaw |
| Palmswap | 2023-07 | $900K | Perpetuals | Position manipulation |
| SiloFinance | 2023-04 | Rescued | Lending | Interest calculation |
| OpenLeverage | 2023-10 | $8K | Margin Trading | Settlement flaw |

---

## Detection Patterns

### Code Patterns to Look For

```
- Functions that change state before validation
- Missing reentrancy guards on state-changing functions
- Exchange rate / share calculations without minimum bounds
- Burn/mint functions affecting wrong addresses
- Health/solvency checks that use cached values
- Claim functions without proof validation
- Self-referential operations (self-liquidation, self-transfer)
- Donation patterns that affect share prices
```

### Audit Checklist

- [ ] Are all state changes validated BEFORE execution?
- [ ] Is there protection against first-depositor/inflation attacks?
- [ ] Are burn/mint targets always the correct addresses?
- [ ] Do health checks use current (not cached) prices?
- [ ] Are claim functions protected against double-claiming?
- [ ] Is self-liquidation or self-interaction properly restricted?
- [ ] Are share calculations protected against rounding exploitation?
- [ ] Do transfer functions handle self-transfers correctly?
- [ ] Are all external call results validated?
- [ ] Are protocol invariants maintained across all state transitions?

---

## Prevention Guidelines

### Development Best Practices

1. **Check-Effects-Interactions Pattern**: Always validate, then update state, then interact
2. **Minimum Share Reserves**: Implement dead shares to prevent inflation attacks
3. **Pre-Condition Validation**: Check if operation will result in valid state BEFORE executing
4. **Invariant Assertions**: Add require statements asserting protocol invariants
5. **Fresh Price Oracles**: Always use current prices for health/solvency calculations
6. **Self-Operation Restrictions**: Explicitly prevent self-liquidation, self-referential exploits
7. **Tracked vs Actual Balances**: Use internal accounting, not `balanceOf(address(this))`

### Testing Requirements

- Unit tests for edge cases (zero amounts, max amounts, first deposit)
- Invariant/fuzz testing for state machine transitions
- Integration tests simulating attack sequences
- Flash loan attack simulations
- Self-interaction attack tests
- Inflation/donation attack scenarios

---

## Complete Incident Reference (2022-2025)

### 2025 Incidents

| Date | Protocol | Loss | Type |
|------|----------|------|------|
| 2025-10-20 | SharwaFinance | $146K | Post insolvency check |
| 2025-10-04 | Abracadabra | $1.8M | Logic flaw |
| 2025-10-04 | MIMSpell3 | $1.7M | Insolvency bypass |
| 2025-08-31 | Hexotic | $500 | Input validation |
| 2025-08-13 | Grizzifi | $61K | Logic flaw |
| 2025-08-12 | Bebop | $21K | Arbitrary input |
| 2025-08-11 | WXC | 37.5 WBNB | Wrong burn target |
| 2025-07-20 | Stepp2p | $43K | Logic flaw |
| 2025-07-17 | WETC | $101K | Burn logic flaw |
| 2025-07-16 | VDS | $13K | Logic flaw |
| 2025-07-05 | RANT | $204K | Logic flaw |
| 2025-07-02 | FPC | $4.7M | Logic flaw |
| 2025-06-12 | AAVEBoost | $14.8K | Logic flaw |
| 2025-05-26 | YDT | $41K | Logic flaw |
| 2025-04-08 | Laundromat | $1.5K | Logic flaw |
| 2025-03-07 | UNI | $14K | Logic flaw |
| 2025-02-11 | FourMeme | $186K | Logic flaw |
| 2025-01-14 | IdolsNFT | 97 stETH | Logic flaw |
| 2025-01-13 | Mosca2 | $37.6K | Logic flaw |
| 2025-01-12 | Unilend | 60 stETH | Logic flaw |
| 2025-01-10 | JPulsepot | $21.5K | Logic flaw |
| 2025-01-07 | IPC | $590K | Wrong burn pairs |
| 2025-01-06 | Mosca | $19K | Logic flaw |

### 2024 Incidents

| Date | Protocol | Loss | Type |
|------|----------|------|------|
| 2024-12-18 | SlurpyCoin | $3K | Logic flaw |
| 2024-12-16 | BTC24H | $85.7K | Logic flaw |
| 2024-12-14 | JHY | $11K | Logic flaw |
| 2024-12-10 | LABUBU | $12K | Logic flaw |
| 2024-11-24 | Proxy_b7e1 | $8.5K | Logic flaw |
| 2024-11-17 | MFT | $33.7K | Logic flaw |
| 2024-11-07 | ChiSale | $16.3K | Logic flaw |
| 2024-11-05 | RPP | $14.1K | Logic flaw |
| 2024-09-20 | DOGGO | $7K | Logic flaw |
| 2024-09-15 | WXETA | $110K | Logic flaw |
| 2024-09-13 | OTSeaStaking | $26K | Logic flaw |
| 2024-09-02 | Pythia | 21 ETH | Logic flaw |
| 2024-08-20 | Coco | 280 BNB | Logic flaw |
| 2024-08-12 | iVest | 338 WBNB | Logic flaw |
| 2024-07-11 | SBT | $56K | Logic flaw |
| 2024-06-28 | Will | $52K | Logic flaw |
| 2024-06-27 | APEMAGA | 9 ETH | Logic flaw |
| 2024-06-18 | INcufi | $59K | Logic flaw |
| 2024-06-17 | Dyson_money | 52 BNB | Logic flaw |
| 2024-06-16 | WIFCOIN_ETH | 3.4 ETH | Logic flaw |
| 2024-06-16 | Crb2 | $15K | Logic flaw |
| 2024-06-11 | JokInTheBox | 9.2 ETH | Logic flaw |
| 2024-06-08 | YYStoken | $28K | Logic flaw |
| 2024-06-06 | SteamSwap | $91K | Logic flaw |
| 2024-06-06 | MineSTM | $13.8K | Logic flaw |
| 2024-06-04 | NCD | $6.4K | Logic flaw |
| 2024-05-31 | Liquiditytokens | $200K | Logic flaw |
| 2024-05-28 | Tradeonorion | $645K | Logic flaw |
| 2024-05-28 | EXcommunity | 33 BNB | Logic flaw |
| 2024-05-26 | NORMIE | $490K | Logic flaw |
| 2024-05-12 | TGC | $32K | Logic flaw |
| 2024-04-30 | Yield | $181K | Logic flaw |
| 2024-04-19 | HedgeyFinance | $48M | Logic flaw |
| 2024-04-16 | SATX | 50 BNB | Logic flaw |
| 2024-04-16 | MARS | >$100K | Bad reflection |
| 2024-04-15 | GFA | $14K | Logic flaw |
| 2024-04-14 | Hackathon | $20K | Logic flaw |
| 2024-04-09 | UPS | $28K | Logic flaw |
| 2024-04-02 | HoppyFrogERC | 0.3 ETH | Logic flaw |
| 2024-04-01 | ATM | $182K | Logic flaw |
| 2024-04-01 | OpenLeverage | $234K | Logic flaw |
| 2024-03-28 | LavaLending | $340K | Logic flaw |
| 2024-03-14 | MO | $413K | Logic flaw |
| 2024-03-13 | IT | $13K | Logic flaw |
| 2024-03-12 | BBT | 5.06 ETH | Logic flaw |
| 2024-03-09 | Juice | 54 ETH | Logic flaw |
| 2024-03-07 | GHT | $57K | Logic flaw |
| 2024-03-06 | TGBS | $150K | Logic flaw |
| 2024-02-23 | BlueberryProtocol | $1.4M | Logic flaw |
| 2024-01-30 | XSIJ | $51K | Logic flaw |
| 2024-01-02 | MIC | $500K | Logic flaw |

### 2023 Incidents

| Date | Protocol | Loss | Type |
|------|----------|------|------|
| 2023-12-22 | PineProtocol | $90K | Logic flaw |
| 2023-12-17 | FloorProtocol | $1.6M | Logic flaw |
| 2023-12-16 | KEST | $2.3K | Logic flaw |
| 2023-12-13 | HYPR | $200K | Logic flaw |
| 2023-12-07 | HNet | 2.4 WBNB | Logic flaw |
| 2023-12-05 | BEARNDAO | $769K | Logic flaw |
| 2023-12-01 | UnverifiedContr | $500K | Logic flaw |
| 2023-11-25 | TheNFTV2 | $19K | Logic flaw |
| 2023-11-17 | ShibaToken | $31K | Logic flaw |
| 2023-11-16 | WECO | $18K | Logic flaw |
| 2023-11-15 | XAI | Unclear | Logic flaw |
| 2023-11-07 | RBalancer | 17 ETH | Logic flaw |
| 2023-11-01 | SwampFinance | Unclear | Logic flaw |
| 2023-10-28 | AstridProtocol | 127 ETH | Logic flaw |
| 2023-10-22 | OpenLeverage | $8K | Logic flaw |
| 2023-10-12 | Platypus | $2M | Logic flaw |
| 2023-10-08 | ZS | $14K | Logic flaw |
| 2023-10-05 | DePayRouter | $827 | Logic flaw |
| 2023-09-09 | BFCToken | $38K | Logic flaw |
| 2023-09-08 | APIG | $169K | Logic flaw |
| 2023-09-02 | DAppSocial | $16K | Logic flaw |
| 2023-08-21 | EHIVE | $15K | Logic flaw |
| 2023-07-24 | Palmswap | $900K | Logic flaw |
| 2023-07-21 | SUT | $8K | Logic flaw |
| 2023-07-20 | Utopia | $119K | Logic flaw |
| 2023-07-20 | FFIST | $110K | Logic flaw |
| 2023-07-18 | APEDAO | $7K | Logic flaw |
| 2023-07-12 | Platypus | $51K | Logic flaw |
| 2023-07-12 | WGPT | $80K | Logic flaw |
| 2023-07-04 | BaoCommunity | $46K | Donation/inflation |
| 2023-06-27 | UnverifiedContr_9ad32 | $6K | Logic flaw |
| 2023-06-27 | STRAC | 12 ETH | Logic flaw |
| 2023-06-23 | SHIDO | 997 WBNB | Logic flaw |
| 2023-06-17 | Pawnfi | $820K | Logic flaw |
| 2023-05-23 | LFI Token | $36K | Logic flaw |
| 2023-05-13 | Bitpaidio | $30K | Logic flaw |
| 2023-05-11 | SellToken01 | $95K | Logic flaw |
| 2023-05-02 | Level | $1M | Logic flaw |
| 2023-04-27 | Silo finance | Rescued | Logic flaw |
| 2023-04-24 | Axioma | 21 WBNB | Logic flaw |
| 2023-03-25 | DBW | $24K | Logic flaw |
| 2023-03-13 | EulerFinance | $200M | Logic flaw |
| 2023-02-22 | DYNA | $21K | Logic flaw |
| 2023-02-17 | Starlink | $12K | Logic flaw |
| 2023-02-17 | Platypusdefi | $8.5M | Logic flaw |
| 2023-01-18 | QTNToken | 2 ETH | Logic flaw |
| 2023-01-18 | UPSToken | 22 ETH | Logic flaw |
| 2023-01-10 | BRA | $224K | Logic flaw |
| 2023-01-03 | GDS | $180K | Logic flaw |

### 2022 Incidents

| Date | Protocol | Loss | Type |
|------|----------|------|------|
| 2022-12-13 | ElasticSwap | $845K | Logic flaw |
| 2022-11-29 | SEAMAN | $7K | Logic flaw |
| 2022-11-21 | SDAO | $13K | Logic flaw |
| 2022-11-05 | BDEX | 16 WBNB | Logic flaw |
| 2022-08-04 | EtnProduct | $3K | Logic flaw |
| 2022-08-02 | Nomad Bridge | $152M | Logic flaw |
| 2022-08-01 | Reaper Farm | $1.7M | Logic flaw |
| 2022-07-25 | LPC | $45K | Logic flaw |
| 2022-03-09 | Fantasm Finance | $2.6M | Mint logic |

---

## Keywords for Search

`business logic flaw`, `logic error`, `state machine`, `incorrect calculation`, `improper validation`, `missing check`, `insolvency bypass`, `health factor`, `share manipulation`, `exchange rate`, `donation attack`, `inflation attack`, `vault exploit`, `self-liquidation`, `burn mechanism`, `mint flaw`, `reward calculation`, `accounting error`, `state transition`, `CEI pattern`, `check-effects-interactions`, `protocol invariant`, `first depositor`, `rounding error`, `token burn`, `token mint`, `claim vulnerability`, `double claim`, `epoch manipulation`

---

## Related Vulnerabilities

- [DB/general/vault-inflation-attack/vault-inflation-attack.md](../vault-inflation-attack/vault-inflation-attack.md)
- [DB/general/rounding-precision-loss/rounding-precision-loss.md](../rounding-precision-loss/rounding-precision-loss.md)
- [DB/general/reentrancy/reentrancy.md](../reentrancy/reentrancy.md)
- [DB/general/missing-validations/MISSING_VALIDATION_TEMPLATE.md](../missing-validations/MISSING_VALIDATION_TEMPLATE.md)
- [DB/tokens/erc4626/ERC4626_VAULT_VULNERABILITIES.md](../../tokens/erc4626/ERC4626_VAULT_VULNERABILITIES.md)
