# Cosmos/CometBFT Appchain Vulnerability Database

## Overview

This database contains synthesized vulnerability patterns from 847 security audit findings related to Cosmos SDK, CometBFT, and appchain security. The entries are organized by category and optimized for vector search.

## Database Structure

### app-chain/abci-lifecycle/
- **unmetered-lifecycle-dos.md** - Unmetered ABCI lifecycle execution DoS
  - Unbounded iteration in BeginBlock/EndBlock without gas metering
  - Geometric unbonding amplification (multi-denom delegation attacks)
  - Hook failure propagation causing chain halt
  - Silent error handling leading to state corruption
  - Non-determinism in FinalizeBlock via RPC calls
  - Real-world: MilkyWay, MANTRA Chain, Allora, Skip Block-SDK, Story

### app-chain/consensus/
- **abci-vote-extensions.md** - Vote extension validation vulnerabilities in ABCI++
  - Malicious vote extensions
  - Missing validation in PrepareProposal/ProcessProposal
  - Real-world: Initia, Allora, Berachain

### app-chain/gas-metering/
- **evm-gas-handling.md** - EVM gas metering bypass vulnerabilities
  - Missing intrinsic gas charges (EIP-2930)
  - Infinite gas meters in BeginBlock/EndBlocker
  - Stack overflow gas bypass
  - Real-world: Initia MiniEVM, ZetaChain, Nibiru

### app-chain/ibc/
- **ibc-middleware-vulnerabilities.md** - IBC middleware authentication issues
  - Missing sender/channel authentication in OnRecvPacket
  - Wrong version return in handshake
  - Non-deterministic JSON unmarshalling (ASA-2025-004)
  - Real-world: Initia, Allora, SEDA, Elys

### app-chain/staking-delegation/
- **staking-state-management.md** - Staking state management issues
  - Silent error handling in EndBlocker
  - UnbondingTime parameter changes breaking queues
  - EVM-Cosmos state desync in precompiles
  - Real-world: Allora, Andromeda, Cosmos LSM, ZetaChain

- **slashing-evasion-bypass.md** - Slashing evasion and bypass vulnerabilities
  - Frontrunning slash with withdrawal/exit
  - Checkpoint protection blocking slash execution
  - Withdrawal delay bypass via pre-request
  - Cooldown activation during protocol pause
  - Governance timing attacks (lockup < voting period)
  - Gas griefing denial of slashing
  - Real-world: Telcoin, Celo, Audius, Increment, Rio Network, Ethos, Mantle

- **epoch-snapshot-timing-manipulation.md** - Epoch/snapshot timing and reward manipulation
  - Future epoch cache manipulation for reward inflation
  - Same-block supply snapshot desynchronization
  - Unlimited validator registration without stake locking
  - Double-counting unclaimed/delayed rewards
  - Orphaned rewards capture by first staker
  - Snapshot blocking via same-block validator creation
  - Checkpoint protection bypass for slashing avoidance
  - Real-world: Suzaku Core, Cabal, Karak, Casimir, Elixir, Zivoe, Celo, Ajna

### app-chain/governance/
- **governance-voting-manipulation.md** - Governance voting and parameter manipulation
  - Quorum lowering via delegation manipulation
  - DAO vote bypass via stale poll re-triggering
  - Commission rate manipulation trapping delegators
  - Voting power snapshot timing attacks
  - Real-world: FrankenDAO, Ethereum Credit Guild, Tortuga

### app-chain/hooks-callbacks/
- **malicious-hook-callback-dos.md** - Hook/callback denial of service vulnerabilities
  - TokenFactory BeforeSendHook with invalid address causing chain halt
  - Rogue plugin overflow preventing removal and freezing staking
  - External hook state dependencies blocking operations
  - BeginBlocker panic via reward distribution hook failures
  - Real-world: MANTRA Chain, Telcoin, Radiant Capital, Toki Bridge

### app-chain/module-accounting/
- **cross-module-fund-accounting.md** - Cross-module fund transfer and token supply accounting
  - Incorrect coin iteration (processing entire sdk.Coins instead of sdk.Coin)
  - Non-atomic operations with temporary contexts (mint before EVM call)
  - Missing withdrawal address configuration freezing rewards
  - Duplicate accounting entries inflating tracked balances
  - Silent error handling in SendCoinsFromModuleToAccount
  - Real-world: Initia MiniEVM, ZetaChain, Andromeda, stNXM, Allora, MilkyWay

### app-chain/precompiles/
- **evm-precompile-vulnerabilities.md** - EVM precompile security issues
  - DELEGATECALL allowing fund theft (msg.value reuse)
  - Dirty EVM state not committed before Cosmos operations
  - Panic on empty calldata
  - Real-world: Monad, ZetaChain, Nibiru

### app-chain/message-handling/
- **message-registration-vulnerabilities.md** - Message registration issues
  - Missing message registration in RegisterCodec/RegisterInterfaces
  - Amino name mismatch breaking signing
  - Deprecated GetSigners usage
  - Message type confusion (Cosmos SDK message disguised as EVM tx)
  - Real-world: Ethos, Initia, ZetaChain

### app-chain/state-management/
- **evm-cosmos-state-sync.md** - EVM-Cosmos state synchronization
  - Dirty state not committed before Cosmos operations
  - Nonce desync between EVM and Cosmos
  - Cache context mismanagement
  - Reward claiming gaps
  - Real-world: Initia MiniEVM, ZetaChain

### unique/
- **chain-halt-dos-vectors.md** - Chain halt DoS attack vectors
  - Unmetered linear iteration in BeginBlock/EndBlocker
  - Division by zero in governance modules
  - Negative amount validation failures
  - Non-determinism in consensus code
  - Real-world: MilkyWay, Allora, Cosmos SDK (ASA-2025-003)

## Categories Covered

1. **Consensus** - ABCI++, vote extensions, PrepareProposal, ProcessProposal
2. **Gas Metering** - EVM gas handling, intrinsic gas, infinite meters
3. **IBC** - Middleware authentication, packet handling, channel handshake
4. **Staking/Delegation** - State management, unbonding, slashing, epoch timing
5. **Hooks/Callbacks** - TokenFactory hooks, plugin callbacks, BeforeSendHook DoS
6. **Precompiles** - EVM precompile security, DELEGATECALL, state isolation
7. **Message Handling** - Codec registration, signing, type confusion
8. **State Management** - EVM-Cosmos sync, nonces, cache contexts
9. **Module Accounting** - Cross-module fund transfers, token supply, atomicity, CacheContext
10. **ABCI Lifecycle** - BeginBlock/EndBlock DoS, hook failures, non-determinism
11. **Unique/DoS** - Chain halt vectors, non-determinism

## Usage

Each entry contains:
- YAML frontmatter with metadata for search
- References to source audit reports
- Root cause analysis
- Impact analysis (technical and business)
- Audit checklist
- Real-world examples with severity ratings
- Keywords for vector search

## Source Reports

All entries are synthesized from audit reports in `reports/cosmos_cometbft_findings/` (847 findings from Sherlock, Code4rena, OtterSec, Pashov, and other audit firms).

