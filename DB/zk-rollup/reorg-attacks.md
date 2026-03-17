---
# Core Classification
protocol: generic
chain: ethereum|l2_rollup
category: reorg_attack
vulnerability_type: reorg_frontrun|factory_reorg|create_address_collision|lp_fund_theft|deployment_griefing

# Attack Vector Details
attack_type: fund_theft|frontrun|address_collision|impersonation|deployment_hijack
affected_component: factory_contract|create2_deployment|liquidity_pool|questFactory|deployment_addresses

# Technical Primitives
primitives:
  - CREATE
  - CREATE2
  - CREATE3
  - block_reorg
  - factory_pattern
  - nonce_dependency
  - deterministic_address
  - msg_sender_address
  - initialize_pattern
  - liquidity_pool_deployment
  - deployment_frontrun
  - questFactory
  - proxyFactory

# Impact Classification
severity: high
impact: fund_theft|deployment_hijack|lp_theft|griefing
exploitability: 0.2
financial_impact: high

# Context Tags
tags:
  - reorg_attack
  - CREATE2
  - factory
  - deployment
  - frontrun
  - liquidity_pool
  - questFactory
  - nonce
  - block_reorg
  - Ethereum
  - mainnet_reorg
  - address_collision

language: solidity
version: all

# Pattern Identity (Required)
root_cause_family: logic_error
pattern_key: logic_error | factory_contract | reorg_frontrun

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - CREATE
  - CREATE2
  - CREATE3
  - addLiquidity
  - block.number
  - block.timestamp
  - block_reorg
  - createPool
  - createPoolAndAddLiquidity
  - createQuest
  - deploy
  - deployProxy
  - deployment_frontrun
  - deposit
  - deterministic_address
  - factory_pattern
  - initialize_pattern
  - liquidity_pool_deployment
  - msg.sender
  - msg_sender_address
---

## References & Source Reports

### Factory Reorg Attacks

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| questFactory Is Suspicious of Reorg Attack | `reports/zk_rollup_findings/m-01-questfactory-is-suspicious-of-the-reorg-attack.md` | MEDIUM | Sherlock |
| Many create Methods Suspicious of Reorg Attack | `reports/zk_rollup_findings/m-04-many-create-methods-are-suspicious-of-the-reorg-attack.md` | MEDIUM | Sherlock |
| factory.create Is Vulnerable to Reorg Attacks | `reports/zk_rollup_findings/m-08-factorycreate-is-vulnerable-to-reorg-attacks.md` | MEDIUM | Sherlock |
| create Methods Suspicious of Reorg Attack | `reports/zk_rollup_findings/m-09-create-methods-are-suspicious-of-reorg-attack.md` | MEDIUM | Multiple |
| Re-org Attack in Factory | `reports/zk_rollup_findings/m-14-re-org-attack-in-factory.md` | MEDIUM | Sherlock |
| Use of CREATE Method Is Suspicious of Reorg Attack | `reports/zk_rollup_findings/use-of-create-method-is-suspicious-of-reorg-attack.md` | MEDIUM | Multiple |

### Liquidity Pool Reorg Attack

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Stealing Liquidity Pool Funds with Reorg | `reports/zk_rollup_findings/stealing-liquidity-pool-fund-with-reorg.md` | HIGH | Multiple |

---

## Vulnerability Title

**Block Reorg Attacks on Factory Contracts and Liquidity Pools — Address Collision Leading to Fund Theft and Deployment Hijacking**

### Overview

Block reorganizations (reorgs) on Ethereum and L2 chains are short-lived events where a competing chain branch temporarily becomes canonical. During a reorg, transactions from the discarded branch are replayed in a different order. Factory contracts that deploy child contracts using `CREATE` (nonce-dependent address) or `CREATE2` (salt-dependent address) are vulnerable: attackers can predict the deployment address, front-run the initialization of the newly deployed contract, and steal funds deposited immediately after deployment.

---



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of logic_error"
- Pattern key: `logic_error | factory_contract | reorg_frontrun`
- Interaction scope: `single_contract`
- Primary affected component(s): `factory_contract|create2_deployment|liquidity_pool|questFactory|deployment_addresses`
- High-signal code keywords: `CREATE`, `CREATE2`, `CREATE3`, `addLiquidity`, `block.number`, `block.timestamp`, `block_reorg`, `createPool`
- Typical sink / impact: `fund_theft|deployment_hijack|lp_theft|griefing`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `LiquidityFactory.function -> ProxyFactory.function -> QuestFactory.function`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: State variable updated after external interaction instead of before (CEI violation)
- Signal 2: Withdrawal path produces different accounting than deposit path for same principal
- Signal 3: Reward accrual continues during paused/emergency state
- Signal 4: Edge case in state machine transition allows invalid state

#### False Positive Guards

- Not this bug when: Standard security patterns (access control, reentrancy guards, input validation) are in place
- Safe if: Protocol behavior matches documented specification
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

1. **CREATE-based address predictability**: `CREATE` produces an address based on `keccak256(deployer_address, nonce)`. If a factory's nonce is predictable (or the factory call is replayed from a reorg), an attacker can compute the future address before it's initialized.  
2. **CREATE2 reuse**: `CREATE2` produces an address from `keccak256(0xFF, deployer, salt, initcodeHash)`. If the salt is predictable (e.g., token addresses, block number), an attacker computes the same address and front-runs the legitimate deployer's initialization.
3. **Unprotected two-step deploy+initialize**: Many factory patterns deploy a proxy (step 1) and initialize it with funding in a separate transaction (step 2). During a reorg, the initialization transaction lands on the attacker-deployed contract at the same address.

The classic attack flow:
```
1. Victim tx: factory.create(salt=X) → deploys contract at address A, sends ETH
2. Reorg happens — Victim's tx is removed from canonical chain
3. Attacker broadcasts: factory.create(salt=X) → same address A, different owner
4. Victim's original tx gets re-included → funds sent to address A (now attacker-owned)
5. Attacker withdraws funds from A
```

---

### Pattern 1: questFactory Reorg Attack

**Frequency**: 5/431 reports | **Validation**: Strong (multiple firms - MEDIUM/HIGH)

#### Attack Description

`questFactory.createQuest(...)` deploys a new Quest contract at a deterministic address (using CREATE or CREATE2 with predictable parameters). Users send rewards to the quest address immediately after creation. During a reorg:
1. Attacker sees the factory call in the mempool
2. Reorg causes the factory's nonce to reset
3. Attacker calls `createQuest` first with same parameters → controls the deployed Quest
4. Victim's reward deposit lands in the attacker-controlled Quest

**Example 1: Nonce-Based CREATE Reorg Vulnerability** [MEDIUM]
```solidity
// ❌ VULNERABLE: Factory uses CREATE (nonce-based address) for Quest deployment
contract QuestFactory {
    Quest[] public quests;
    
    function createQuest(
        address rewardToken,
        uint256 endTime,
        uint256 totalParticipants
    ) external returns (address questAddress) {
        // BUG: CREATE produces address based on this factory's nonce
        // After reorg, nonce is the same → same deployment address
        // Attacker can call createQuest first to deploy their own Quest at this address
        Quest quest = new Quest(rewardToken, endTime, totalParticipants, msg.sender);
        questAddress = address(quest);
        quests.push(quest);
        
        // User sends rewards AFTER this call completes
        // But in a reorg, "quest" could be attacker-owned at questAddress
    }
}
```

**Fix:**
```solidity
// ✅ SECURE: Include msg.sender and block-specific data in CREATE2 salt
function createQuest(
    address rewardToken,
    uint256 endTime,
    uint256 totalParticipants,
    bytes32 salt
) external returns (address questAddress) {
    // Include msg.sender in salt so attacker cannot preempt victim's deployment
    bytes32 uniqueSalt = keccak256(abi.encode(msg.sender, salt, block.chainid));
    questAddress = address(new Quest{salt: uniqueSalt}(
        rewardToken, endTime, totalParticipants, msg.sender
    ));
    // Also: do NOT accept external deposits separately — initialize in same tx
}
```

---

### Pattern 2: Stealing Liquidity Pool Funds via Reorg

**Frequency**: 1/431 reports | **Validation**: Strong (HIGH)

#### Attack Description

When a new liquidity pool is deployed (e.g., via Uniswap-style factory), a "first depositor" must provide initial liquidity. If the pool's address is predictable and the initial deposit transaction is separate from the pool creation, a reorg allows an attacker to:

1. Deploy a malicious pool contract at the same predicted address
2. Receive the victim's initial liquidity deposit
3. Drain the pool via the attacker-controlled pool logic

**Example 2: LP Fund Theft via Reorg** [HIGH]
```solidity
// ❌ VULNERABLE: Pool deployed in one tx, funded in another
contract LiquidityFactory {
    function createPool(
        address tokenA,
        address tokenB,
        uint24 fee
    ) external returns (address pool) {
        // CREATE2 with predictable salt
        bytes32 salt = keccak256(abi.encode(tokenA, tokenB, fee));
        pool = address(new UniswapV3Pool{salt: salt}());
        // Pool deployed but NOT initialized with liquidity yet
    }
}

// Victim's workflow (vulnerable):
// Tx 1: factory.createPool(USDC, ETH, 3000) → pool at 0xABCD...
// Tx 2: pool.addLiquidity(USDC, ETH, 1_000_000e6) → sends $1M
// 
// Reorg between Tx 1 and Tx 2:
// Attacker deploys malicious contract at 0xABCD...
// Victim's Tx 2 sends $1M to the malicious contract
```

**Fix:**
```solidity
// ✅ SECURE: Deploy and fund in the same atomic transaction
function createPoolAndAddLiquidity(
    address tokenA,
    address tokenB,
    uint24 fee,
    uint256 liquidity
) external {
    bytes32 salt = keccak256(abi.encode(msg.sender, tokenA, tokenB, fee));
    address pool = address(new LiquidityPool{salt: salt}());
    // Initialize and fund atomically
    ILiquidityPool(pool).initialize(tokenA, tokenB, fee);
    ILiquidityPool(pool).addLiquidity(liquidity);
    // No gap between deployment and funding
}
```

---

### Pattern 3: General Factory.create Reorg (Multiple Protocols)

**Frequency**: 5/431 reports | **Validation**: Strong (multiple Sherlock/audit reports - MEDIUM)

#### Root Cause

Any factory that:  
(a) deploys a contract with a nonce-predictable or salt-predictable address, AND  
(b) relies on users sending funds to the predicted address in a subsequent transaction

...is vulnerable to the reorg pattern. This appears consistently across multiple unrelated protocol audits.

**Example 3: Generic Factory CREATE Reorg** [MEDIUM]
```solidity
// ❌ VULNERABLE: Canonical pattern seen in 5+ reports
contract ProxyFactory {
    uint256 public deployCount;
    
    function deployProxy(
        address implementation,
        bytes calldata initData
    ) external returns (address proxy) {
        // CREATE → address = hash(factory, deployCount)
        // deployCount increments each call
        // After reorg, deployCount resets → same address reachable by attacker
        proxy = address(new TransparentProxy(implementation));
        deployCount++;
        
        // Users call: proxy.initialize(initData) separately — VULNERABLE
    }
}
```

**Secure Patterns:**

| Approach | How It Helps |
|----------|-------------|
| Include `msg.sender` in CREATE2 salt | Attacker cannot predict victim's deployment address |
| Atomic deploy+initialize+fund | No gap between deployment and initialization |
| Ownership check in `initialize` | Reject initialization if `msg.sender != expectedDeployer` |
| Minimum deposit delay (e.g., N blocks) | Outlasts typical reorg depth (99% of reorgs < 2 blocks) |
| Add unique entropy: `block.prevrandao`, `tx.origin`, `block.timestamp` | Non-replayable parameters in salt |

---

### Pattern 4: CREATE vs CREATE2 Reorg Risk Comparison

**Frequency**: Observed across all 7 reorg-related reports | **Validation**: Strong

| `CREATE` | `CREATE2` |
|----------|-----------|
| Address = `keccak256(factory, nonce)` | Address = `keccak256(0xFF, factory, salt, initcodeHash)` |
| Vulnerable when factory nonce is predictable or replayable | Vulnerable when salt is predictable (token addresses, sequential counter) |
| Reorg resets nonce → same address | Reorg allows attacker to front-run with same salt |
| Riskier: all factory nonces are replayable after reorg | Safer: salt can include `msg.sender` to be attacker-resistant |

**High-Risk Salt Patterns:**
```solidity
// ❌ BAD salts (predictable, reorg-vulnerable):
bytes32 salt = keccak256(abi.encode(tokenA, tokenB));    // No deployer
bytes32 salt = bytes32(deployCount++);                     // Sequential integer
bytes32 salt = keccak256(abi.encode(block.number));        // Reorg-replayable
bytes32 salt = keccak256(abi.encode(questId++));           // Sequential ID

// ✅ GOOD salts (include deployer identity):
bytes32 salt = keccak256(abi.encode(msg.sender, tokenA, tokenB, block.chainid));
bytes32 salt = keccak256(abi.encode(msg.sender, userProvidedSalt));
bytes32 salt = keccak256(abi.encode(tx.origin, block.prevrandao, questId)); // Non-replayable
```

---

### Impact Analysis

#### Technical Impact
- Factory child contracts deployed to predictable addresses can be hijacked during reorgs
- All user funds deposited to hijacked contracts are stolen
- Protocol's operational security depends on chain reorganization not occurring for 2+ blocks

#### Business Impact
- Fund theft from initial LP deposits (HIGH) — $50K to $10M depending on protocol TVL
- Quest reward theft — all reward tokens deposited to hijacked contracts
- Protocol reputation damage from "known" but unmitigated reorg attack vector

---

### Secure Implementation

```solidity
// ✅ GOLD STANDARD: Reorg-safe factory pattern
contract SafeFactory {
    // 1. Include msg.sender in salt
    function deploy(bytes32 userSalt) external returns (address) {
        bytes32 salt = keccak256(abi.encode(msg.sender, userSalt));
        address deployed = address(new ChildContract{salt: salt}(msg.sender));
        
        // 2. Initialize in same transaction (no gap)
        ChildContract(deployed).initialize(msg.sender);
        
        // 3. If funding is needed, do it here atomically
        if (msg.value > 0) {
            ChildContract(deployed).fund{value: msg.value}();
        }
        
        return deployed;
    }
}
```

---

### Detection Patterns

```
1. factory.create() or new Contract() without msg.sender in salt
2. Two-step pattern: deploy in tx1, initialize/fund in tx2 (different function calls)
3. Salt derived from: block.number, sequential counter, or token addresses alone
4. addLiquidity() / depositRewards() called on address predicted from factory params
5. Factory using CREATE (not CREATE2) — nonce-based addressing is always vulnerable
6. Proxies deployed via ProxyFactory with salt = keccak256(tokenA, tokenB) only
```

### Keywords for Search

`reorg attack factory`, `block reorganization deployment`, `CREATE2 reorg front-run`, `factory nonce reorg`, `questFactory reorg`, `deployment address hijack`, `predictable contract address`, `liquidity pool reorg theft`, `ProxyFactory reorg`, `salt without msg.sender`, `create method reorg`, `fund theft L1 reorg`, `contract deployment replay`, `two-step deploy initialize reorg`, `address collision reorg`

### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`CREATE`, `CREATE2`, `CREATE3`, `Ethereum`, `addLiquidity`, `address_collision`, `block.number`, `block.timestamp`, `block_reorg`, `createPool`, `createPoolAndAddLiquidity`, `createQuest`, `deploy`, `deployProxy`, `deployment`, `deployment_frontrun`, `deposit`, `deterministic_address`, `factory`, `factory_pattern`, `frontrun`, `initialize_pattern`, `liquidity_pool`, `liquidity_pool_deployment`, `mainnet_reorg`, `msg.sender`, `msg_sender_address`, `nonce`, `nonce_dependency`, `proxyFactory`, `questFactory`, `reorg_attack`, `reorg_frontrun|factory_reorg|create_address_collision|lp_fund_theft|deployment_griefing`
