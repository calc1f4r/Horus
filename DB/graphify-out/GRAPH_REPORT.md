# Graph Report - /home/calc1f4r/Horus/DB  (2026-04-28)

## Corpus Check
- 213 files · ~140,903 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2139 nodes · 11969 edges · 17 communities detected
- Extraction: 57% EXTRACTED · 43% INFERRED · 0% AMBIGUOUS · INFERRED: 5087 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_cosmos|cosmos]]
- [[_COMMUNITY_defi|defi]]
- [[_COMMUNITY_general|general]]
- [[_COMMUNITY_amm|amm]]
- [[_COMMUNITY_zk-rollup|zk-rollup]]
- [[_COMMUNITY_proxy|proxy]]
- [[_COMMUNITY_access-control|access-control]]
- [[_COMMUNITY_oracle|oracle]]
- [[_COMMUNITY_bridge|bridge]]
- [[_COMMUNITY_governance|governance]]
- [[_COMMUNITY_protocol-specific|protocol-specific]]
- [[_COMMUNITY_general|general]]
- [[_COMMUNITY_token|token]]
- [[_COMMUNITY_general|general]]
- [[_COMMUNITY_general|general]]
- [[_COMMUNITY_solana|solana]]
- [[_COMMUNITY_general|general]]

## God Nodes (most connected - your core abstractions)
1. `cosmos` - 414 edges
2. `ibc` - 414 edges
3. `appchain` - 414 edges
4. `defi` - 261 edges
5. `calculation` - 261 edges
6. `vault` - 261 edges
7. `flash-loan` - 261 edges
8. `general` - 235 edges
9. `amm` - 105 edges
10. `dex` - 105 edges
11. `liquidity` - 105 edges
12. `swap` - 105 edges
13. `proxy` - 87 edges
14. `reentrancy` - 87 edges
15. `storage` - 87 edges

## Surprising Connections (you probably didn't know these)
- `1. Consensus Proposer Dos` --mentions_keyword--> `single_contract`  [INFERRED]
  DB/cosmos/app-chain/consensus/consensus-finality-vulnerabilities.md → DB/cosmos/app-chain/abci-lifecycle/abci-lifecycle-vulnerabilities.md
- `1. Evm Intrinsic Gas Missing` --mentions_keyword--> `single_contract`  [INFERRED]
  DB/cosmos/app-chain/evm/evm-gas-handling-vulnerabilities.md → DB/cosmos/app-chain/abci-lifecycle/abci-lifecycle-vulnerabilities.md
- `Keywords` --mentions_keyword--> `balanceOf`  [INFERRED]
  DB/cosmos/app-chain/fund-safety/fund-theft-vulnerabilities.md → DB/cosmos/app-chain/fund-safety/fund-locking-insolvency.md
- `1. Infra Ssrf` --mentions_keyword--> `single_contract`  [INFERRED]
  DB/cosmos/app-chain/infrastructure/security-infrastructure-vulnerabilities.md → DB/cosmos/app-chain/abci-lifecycle/abci-lifecycle-vulnerabilities.md
- `1. Liquidity Pool Manipulation` --mentions_keyword--> `single_contract`  [INFERRED]
  DB/cosmos/app-chain/liquidity/liquidity-pool-vulnerabilities.md → DB/cosmos/app-chain/abci-lifecycle/abci-lifecycle-vulnerabilities.md
- `1. Mev Staking Frontrun` --mentions_keyword--> `single_contract`  [INFERRED]
  DB/cosmos/app-chain/mev/frontrunning-mev-vulnerabilities.md → DB/cosmos/app-chain/abci-lifecycle/abci-lifecycle-vulnerabilities.md
- `4. Mev Block Stuffing` --mentions_keyword--> `safeTransferFrom`  [INFERRED]
  DB/cosmos/app-chain/mev/frontrunning-mev-vulnerabilities.md → DB/bridge/custom/defihacklabs-bridge-2022-patterns.md
- `6. Mev Priority` --mentions_keyword--> `safeTransferFrom`  [INFERRED]
  DB/cosmos/app-chain/mev/frontrunning-mev-vulnerabilities.md → DB/bridge/custom/defihacklabs-bridge-2022-patterns.md
- `Umee Security Assessment` --mentions_keyword--> `safeTransferFrom`  [INFERRED]
  DB/cosmos/app-chain/mev/frontrunning-mev-vulnerabilities.md → DB/bridge/custom/defihacklabs-bridge-2022-patterns.md
- `Data Validation` --mentions_keyword--> `safeTransferFrom`  [INFERRED]
  DB/cosmos/app-chain/mev/frontrunning-mev-vulnerabilities.md → DB/bridge/custom/defihacklabs-bridge-2022-patterns.md

## Communities

### Community 0 - "cosmos"
Cohesion: 0.02
Nodes (523): appchain, cosmos, ibc, 1. Abci Endblock Error, 2. Abci Checktx Bypass, 3. Abci Vote Extension Abuse, 4. Abci Finalize Block, Keywords (+515 more)

### Community 1 - "defi"
Cohesion: 0.03
Nodes (361): calculation, defi, flash-loan, vault, DB/general/bonding-curve/BONDING_CURVE_ACCESS_CONTROL_STATE_VULNERABILITIES.md, DB/general/bonding-curve/BONDING_CURVE_DOS_GRIEFING_VULNERABILITIES.md, DB/general/bonding-curve/BONDING_CURVE_FEE_ROUNDING_VULNERABILITIES.md, DB/general/bonding-curve/BONDING_CURVE_MATH_FORMULA_VULNERABILITIES.md (+353 more)

### Community 2 - "general"
Cohesion: 0.06
Nodes (172): general, DB/Sui-Move-specific/MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md, DB/Sui-Move-specific/MOVE_CROSS_CHAIN_BRIDGE_VULNERABILITIES.md, DB/Sui-Move-specific/MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md, DB/Sui-Move-specific/MOVE_DENIAL_OF_SERVICE_VULNERABILITIES.md, DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md, DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md, DB/Sui-Move-specific/SUI_CROSS_CHAIN_BRIDGE_VULNERABILITIES.md (+164 more)

### Community 3 - "amm"
Cohesion: 0.09
Nodes (154): 1. First Depositor / Inflation Attacks, 10. Decimal & Math Calculation Issues, 11. Liquidity Migration & Protocol Upgrade Attacks, 12. Flash Loan-Based Graduation/Threshold Manipulation, 13. Detection Patterns & Audit Checklist, 13. Imbalanced Liquidity Addition Exploitation, 14. Rebasing Token Integration Issues, 15. Impermanent Loss Protection Abuse (+146 more)

### Community 4 - "zk-rollup"
Cohesion: 0.14
Nodes (121): ERC-7579 Module System — Registry Bypass, moduleType Confusion, Hook PostCheck Skip, Fallback Flaws, AA Paymaster Gas Accounting — Prefund Errors, Duplicate Snapshots, Stake Bypass, and Fee Escape, Session Key Abuse — Spend Limit Bypass, Cross-Wallet Consumption, Permission Overwrite, PermissionId Frontrun, AA Signature Replay — Missing Binding Fields in UserOperation and Enable Mode Hashes, account-abstraction, arbitrum, batch-processing, circuit (+113 more)

### Community 5 - "proxy"
Cohesion: 0.09
Nodes (120): proxy, reentrancy, storage, upgradeable, DB/general/bridge/cross-chain-bridge-vulnerabilities.md, DB/general/diamond-proxy/DIAMOND_PROXY_VULNERABILITIES.md, DB/general/erc7702-integration/erc7702-integration-vulnerabilities.md, DB/general/proxy-vulnerabilities/PROXY_PATTERN_VULNERABILITIES.md (+112 more)

### Community 6 - "access-control"
Cohesion: 0.09
Nodes (113): access-control, input, signature, validation, DB/general/access-control/access-control-vulnerabilities.md, DB/general/access-control/defihacklabs-access-control-2021-2022-patterns.md, DB/general/access-control/defihacklabs-access-control-2023-patterns.md, DB/general/access-control/defihacklabs-access-control-2024-2025.md (+105 more)

### Community 7 - "oracle"
Cohesion: 0.07
Nodes (93): data-freshness, oracle, price-feed, 1. Oracle Stale Price, 2. Oracle Price Manipulation, 3. Oracle Dos, 4. Oracle Deviation Exploit, 5. Oracle Frontrunning (+85 more)

### Community 8 - "bridge"
Cohesion: 0.1
Nodes (90): 1. Gateway Validation Bypass, 10. Command ID Collision, 2. Source Chain & Address Spoofing, 3. Token Burn-but-Call-Fails, 4. Express Execution Front-Running, 5. ITS Token Manager Misconfiguration, 6. Gas Service Payment Issues, 7. String-Based Chain Matching (+82 more)

### Community 9 - "governance"
Cohesion: 0.11
Nodes (87): dao, governance, mev, stablecoin, voting, DB/general/dao-governance/DAO_GOVERNANCE_VULNERABILITIES.md, DB/general/dao-governance-vulnerabilities/defihacklabs-governance-attack-patterns.md, DB/general/dao-governance-vulnerabilities/governance-takeover.md (+79 more)

### Community 10 - "protocol-specific"
Cohesion: 0.06
Nodes (78): protocol-specific, unique, 1. Dos Block Production Halt, 2. Dos Consensus Halt, 3. Dos State Machine, 4. Dos Unbounded Beginblock, 5. Dos Unbounded Array, 6. Dos Panic Crash (+70 more)

### Community 11 - "general"
Cohesion: 0.21
Nodes (46): DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md, DB/Sui-Move-specific/SUI_MOVE_ACCESS_CONTROL_VALIDATION_VULNERABILITIES.md, accept_ownership, approve_operator, capability_pattern, custom_withdraw, emergency_withdraw, finalize_snapshot_update (+38 more)

### Community 12 - "token"
Cohesion: 0.23
Nodes (45): erc20, erc4626, erc721, token, DB/tokens/erc20/ERC20_TOKEN_VULNERABILITIES.md, DB/tokens/erc4626/ERC4626_VAULT_VULNERABILITIES.md, DB/tokens/erc721/ERC721_NFT_VULNERABILITIES.md, adminRecoverStuckFunds (+37 more)

### Community 13 - "general"
Cohesion: 0.22
Nodes (45): DB/Sui-Move-specific/MOVE_ACCESS_CONTROL_AUTHORIZATION_VULNERABILITIES.md, DB/Sui-Move-specific/MOVE_TOKEN_SUPPLY_INFLATION_VULNERABILITIES.md, accrue_user_pool_reward, add_wallet_by_investor, claim_with_signature_safe, deposit_liquidity, freeze_coin_store, freeze_thapt_coin_stores (+37 more)

### Community 14 - "general"
Cohesion: 0.23
Nodes (41): DB/Sui-Move-specific/SUI_MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md, DB/Sui-Move-specific/SUI_MOVE_DEFI_LOGIC_VULNERABILITIES.md, calculate_epoch_reward, calculate_rewards, calculate_share, convert_amount, get_sui_for_shares, get_sui_for_shares_round_up (+33 more)

### Community 15 - "solana"
Cohesion: 0.35
Nodes (30): anchor, solana, spl, DB/Solana-chain-specific/solana-program-security.md, DB/Solana-chain-specific/token-2022-extensions.md, account_closure, account_reallocation, init_if_needed (+22 more)

### Community 16 - "general"
Cohesion: 0.47
Nodes (20): DB/Sui-Move-specific/MOVE_STATE_MANAGEMENT_VULNERABILITIES.md, accrue_interest, borrow_global_mut, check_group_limit, copy_semantics, deposit_and_stake, dynamic_field, Move State Management & Data Integrity Vulnerabilities (+12 more)

## Knowledge Gaps
- **42 isolated node(s):** `DB/account-abstraction/aa-erc7579-module-system-enable-mode.md`, `DB/account-abstraction/aa-paymaster-gas-accounting-vulnerabilities.md`, `DB/account-abstraction/aa-session-key-permission-abuse.md`, `DB/account-abstraction/aa-signature-replay-attacks.md`, `DB/amm/concentrated-liquidity/slippage-sandwich-frontrun.md` (+37 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Vulnerable Pattern Examples` connect `defi` to `cosmos`?**
  _High betweenness centrality (0.000) - this node is a cross-community bridge._
- **What connects `DB/account-abstraction/aa-erc7579-module-system-enable-mode.md`, `DB/account-abstraction/aa-paymaster-gas-accounting-vulnerabilities.md`, `DB/account-abstraction/aa-session-key-permission-abuse.md` to the rest of the system?**
  _42 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `cosmos` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._
- **Should `defi` be split into smaller, more focused modules?**
  _Cohesion score 0.03 - nodes in this community are weakly interconnected._
- **Should `general` be split into smaller, more focused modules?**
  _Cohesion score 0.06 - nodes in this community are weakly interconnected._
- **Should `amm` be split into smaller, more focused modules?**
  _Cohesion score 0.09 - nodes in this community are weakly interconnected._
- **Should `zk-rollup` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._