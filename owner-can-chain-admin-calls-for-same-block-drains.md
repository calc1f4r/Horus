---
# Core Classification
protocol: Sherpa
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63837
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Immeas
  - MrPotatoMagic
---

## Vulnerability Title

Owner can chain admin calls for same-block drains

### Overview


This bug report addresses a vulnerability in the Sherpa protocol's admin controls. These controls allow the owner to make privileged calls across the vault and wrapper in a single transaction, giving them immediate and unrestricted access to funds. The impact of this bug is that the owner (or a compromised key) can redirect custody and move funds without giving users any warning or reaction time. To mitigate this issue, the report recommends adding a delay to certain functions, making certain variables immutable, and using a timelock with a user-protective delay. The report also mentions that the team has implemented a pseudo-immutable solution for the `stableWrapper` and `keeper` variables. The report concludes by stating that the bug has been fixed in a recent commit.

### Original Finding Content

**Description:** The protocol’s admin controls let the owner chain privileged calls across the vault and wrapper in a single transaction:

* **Vault path:** Call `SherpaVault::setStableWrapper` to switch which token is protected from rescue. Then immediately call `SherpaVault::rescueTokens` to withdraw any balance of the old wrapper from the vault.
* **Wrapper operator path:** Call `SherpaUSD::setOperator`, then (as operator) use `SherpaUSD::transferAsset` to move USDC out of the wrapper.
* **Wrapper keeper path:** Call `SherpaUSD::setKeeper`, then use `SherpaUSD::depositToVault` to pull USDC from users who left approvals, mint SherpaUSD to the keeper, and extract value via the `transferAsset` path above.

All of these are owner-only and have no built-in delay, so they can be executed together in the same block.

**Impact:** Even though the code comments stress limiting owner power, the owner (or a compromised key) can immediately redirect custody and move funds with no user warning or reaction time. This creates a trust gap between stated intent and actual authority.

**Recommended Mitigation:** * Add a delay (at least one withdrawal epoch) to `SherpaVault.setStableWrapper`, `SherpaVault.rescueTokens`, `SherpaUSD.setOperator`, `SherpaUSD.setKeeper`, and consider delaying `SherpaUSD.transferAsset`.
* Make `SherpaVault.stableWrapper`, `SherpaUSD.keeper` immutable.
* Use a timelock (e.g., OpenZeppelin [`TimelockController`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/governance/TimelockController.sol)) with a user-protective delay so people can withdraw or reduce approvals before changes take effect.

**Sherpa:**
> Vault path: Call SherpaVault::setStableWrapper to switch which token is protected from rescue. Then immediately call SherpaVault::rescueTokens to withdraw any balance of the old wrapper from the vault.
> Wrapper keeper path: Call SherpaUSD::setKeeper, then use SherpaUSD::depositToVault to pull USDC from users who left approvals, mint SherpaUSD to the keeper, and extract value via the transferAsset path above.

We're implementing a pseudo-immutable `stableWrapper` and `keeper` - both will be set once during deployment and cannot be changed after system initialization. This eliminates both attack surfaces while maintaining the deployment flexibility needed to solve the chicken-and-egg deployment problem: vault constructor requires wrapper address, but we can't deploy wrapper until vault exists. We solve this by deploying vault with a temporary wrapper address, then calling `setStableWrapper()` once to set the real wrapper and lock it permanently.

> Wrapper operator path: Call SherpaUSD::setOperator, then (as operator) use SherpaUSD::transferAsset to move USDC out of the wrapper.

Timelocks / delays on `setOperator` and related admin functions would be ineffective given our vault's trust model and architecture. The operator already has manual custody of strategy funds (transferred to fund manager for on and off-chain strategy delegation) and can pause the system at will, meaning any timelock delay could be circumvented by simply pausing withdrawals during the timelock window. The operator must remain changeable for operational flexibility (personnel changes, key rotation) so we cant make it immutable like we did with `keeper` and `setStableWrapper`. The owner role is a 2-of-3 multisig that controls operator selection, so centralization is lessened there as best as we can.

Fixed in commit [`15e2706`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/commit/15e270673d42e02f1e3a08bcba6d1ac61f14010d)

**Cyfrin:** Verified. Both `stableWrapper` and `keeper` now locked after initial assignment which will effectively make them immutable. Operator concern acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Sherpa |
| Report Date | N/A |
| Finders | Immeas, MrPotatoMagic |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

