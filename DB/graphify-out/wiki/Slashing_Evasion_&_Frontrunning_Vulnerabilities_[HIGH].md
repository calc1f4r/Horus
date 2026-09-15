# Slashing Evasion & Frontrunning Vulnerabilities [HIGH]

> God node · 127 connections · `DB/cosmos/app-chain/slashing/slashing-evasion-frontrunning.md`

## Connections by Relation

### affects_component
- [[slashing_logic]] `EXTRACTED`
- [[withdrawal_queue]] `EXTRACTED`
- [[cooldown_mechanism]] `EXTRACTED`

### contextual_report
- [[reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md]] `INFERRED`
- [[reports/cosmos_cometbft_findings/elected-tss-nodes-can-act-without-any-deposit.md]] `INFERRED`
- [[reports/cosmos_cometbft_findings/h-02-users-who-queue-withdrawal-before-a-slashing-event-disadvantage-users-who-q.md]] `INFERRED`
- [[reports/cosmos_cometbft_findings/gas-price-spikes-cause-the-selected-operator-to-be-vulnerable-to-front-running-a.md]] `INFERRED`
- [[reports/cosmos_cometbft_findings/h-06-gas-price-spikes-cause-the-selected-operator-to-be-vulnerable-to-frontrunni.md]] `INFERRED`

### has_graph_hint
- [[missing frontrun protection]] `INFERRED`
- [[missing timing guard]] `INFERRED`
- [[withdrawal delay bypass]] `INFERRED`

### has_root_cause_family
- [[missing_timing_guard]] `EXTRACTED`

### mentions_keyword
- [[beaconChainETHStrategy]] `INFERRED`
- [[decreaseStakeLockupDuration]] `INFERRED`
- [[pendingWithdrawals]] `INFERRED`

### related_variant
- [[Description]] `INFERRED`
- [[6. Slashing Queued Excluded]] `INFERRED`
- [[5. Deposit Queue Processing Errors]] `INFERRED`
- [[Description]] `INFERRED`
- [[Keywords]] `INFERRED`
- [[3. Slashing Delegation Bypass]] `INFERRED`
- [[1. Slashing Frontrun Exit]] `INFERRED`
- [[1. Validation Zero Check Missing [HIGH]]] `INFERRED`
- [[2. Slashing Cooldown Exploit]] `INFERRED`
- [[8. Funds Missing Slippage]] `INFERRED`
- [[5. Slashing Pending Operations]] `INFERRED`
- [[8. Slashing Mechanism Abuse]] `INFERRED`
- [[4. Slashing Reward Interaction]] `INFERRED`
- [[Severity]] `INFERRED`
- [[4. Slashing Insufficient Deposit]] `INFERRED`
- [[7. Slashing Unregistered Operator]] `INFERRED`
- [[Data Validation [HIGH]]] `INFERRED`
- [[Keywords]] `INFERRED`
- [[5. Slashing External Block]] `INFERRED`
- [[1. Slashing Amount Incorrect [HIGH]]] `INFERRED`

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*