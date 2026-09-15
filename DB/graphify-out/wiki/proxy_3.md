# proxy 3

> 24 nodes · cohesion 0.34

## Key Concepts

- **1. Fake Token Reward Harvesting Callback Reentrancy [CRITICAL]** (29 connections) — `DB/general/reentrancy/defihacklabs-reentrancy-2024-patterns.md`
- **2. Empty Market Phantom Collateral Attack [CRITICAL]** (29 connections) — `DB/general/reentrancy/defihacklabs-reentrancy-2024-patterns.md`
- **3. ERC-3156 Flash Loan Callback Re-deposit Loop [CRITICAL]** (29 connections) — `DB/general/reentrancy/defihacklabs-reentrancy-2024-patterns.md`
- **4. Strategy Callback Reentrancy via Attacker-Controlled Hook [CRITICAL]** (29 connections) — `DB/general/reentrancy/defihacklabs-reentrancy-2024-patterns.md`
- **Agent role can drain CollateralPool via fake reward-claim return value** (29 connections) — `DB/unique/l1-misc/flare/fassets-collateral-pool-unverified-reward-claim.md`
- **collateral_accounting** (10 connections) — `DB/general/reentrancy/defihacklabs-reentrancy-2024-patterns.md`
- **cross function reentrancy** (10 connections) — `DB/general/reentrancy/defihacklabs-reentrancy-2024-patterns.md`
- **flash_loan_callback** (8 connections) — `DB/general/reentrancy/defihacklabs-reentrancy-2024-patterns.md`
- **reward_harvest** (8 connections) — `DB/general/reentrancy/defihacklabs-reentrancy-2024-patterns.md`
- **strategy_callback** (8 connections) — `DB/general/reentrancy/defihacklabs-reentrancy-2024-patterns.md`
- **DB/general/reentrancy/defihacklabs-reentrancy-2024-patterns.md** (4 connections) — `DB/general/reentrancy/defihacklabs-reentrancy-2024-patterns.md`
- **on flash loan** (4 connections) — `DB/general/reentrancy/defihacklabs-reentrancy-2024-patterns.md`
- **agent controlled claim target** (2 connections) — `DB/unique/l1-misc/flare/fassets-collateral-pool-unverified-reward-claim.md`
- **collateral pool reward claim** (2 connections) — `DB/unique/l1-misc/flare/fassets-collateral-pool-unverified-reward-claim.md`
- **erc flash loan callback deposit loop** (2 connections) — `DB/general/reentrancy/defihacklabs-reentrancy-2024-patterns.md`
- **external call return value** (2 connections) — `DB/unique/l1-misc/flare/fassets-collateral-pool-unverified-reward-claim.md`
- **fake token reward harvesting callback reentrancy** (2 connections) — `DB/general/reentrancy/defihacklabs-reentrancy-2024-patterns.md`
- **missing balance delta check** (2 connections) — `DB/unique/l1-misc/flare/fassets-collateral-pool-unverified-reward-claim.md`
- **pool share redemption** (2 connections) — `DB/unique/l1-misc/flare/fassets-collateral-pool-unverified-reward-claim.md`
- **privileged agent role** (2 connections) — `DB/unique/l1-misc/flare/fassets-collateral-pool-unverified-reward-claim.md`
- **total collateral accounting** (2 connections) — `DB/unique/l1-misc/flare/fassets-collateral-pool-unverified-reward-claim.md`
- **unverified claim return** (2 connections) — `DB/unique/l1-misc/flare/fassets-collateral-pool-unverified-reward-claim.md`
- **reports/flare-l1_findings/45893-sc-high-agent-role-can-stolen-nat-token-from-protocol-users.md** (2 connections) — `DB/unique/l1-misc/flare/fassets-collateral-pool-unverified-reward-claim.md`
- **DB/unique/l1-misc/flare/fassets-collateral-pool-unverified-reward-claim.md** (1 connections) — `DB/unique/l1-misc/flare/fassets-collateral-pool-unverified-reward-claim.md`

## Relationships

- [defi 4](defi_4.md) (8 shared connections)
- [bridge](bridge.md) (5 shared connections)
- [proxy 4](proxy_4.md) (4 shared connections)

## Source Files

- `DB/general/reentrancy/defihacklabs-reentrancy-2024-patterns.md`
- `DB/unique/l1-misc/flare/fassets-collateral-pool-unverified-reward-claim.md`

## Audit Trail

- EXTRACTED: 47 (43%)
- INFERRED: 63 (57%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*