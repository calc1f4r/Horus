---
# Core Classification
protocol: The Standard Smart Vault
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38337
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
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
  - Giovanni Di Siena
---

## Vulnerability Title

Yield deposits are susceptible to losses of up to 10\%

### Overview


This bug report discusses an issue related to slippage in the Smart Vault Yield Manager contract. The contract currently has a requirement that the total collateral value should not decrease by more than 90% during certain interactions. This is meant to protect users from complete loss, but it still results in a significant loss of 10% on each deposit or withdrawal. This could potentially be exploited by MEV bots on the Arbitrum network. The report recommends allowing users to pass more restrictive parameters to mitigate this issue. The bug has been fixed in the latest commit by The Standard DAO and has been verified by Cyfrin. 

### Original Finding Content

**Description:** To deal with the slippage incurred through multiple [[1](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L99), [2](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L127), [3](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L141), [4](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L151), [5](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L191), [6](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L197), [7](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L205)] intermediate DEX swaps and Gamma Vault interactions when [`SmartVaultV4::depositYield`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L299-L310) and [`SmartVaultV4::withdrawYield`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L312-L322) are called, there is a requirement that the total collateral value should not have decreased more than 90%:

```solidity
    function significantCollateralDrop(uint256 _preCollateralValue, uint256 _postCollateralValue) private pure returns (bool) {
    return _postCollateralValue < 9 * _preCollateralValue / 10;
}
```

While this design will successfully protect users against complete and immediate loss, 10% is nevertheless a significant amount to lose on each deposit/withdrawal action.

Currently, due to the existence of a centralized sequencer, MEV on Arbitrum does not exist in the typical sense; however, it is still possible to execute latency-driven strategies for predictable events such as liquidations. As such, it may still be possible for MEV bots to cause collateral yield deposits/withdrawals to return 90% of the original collateral value, putting the Smart Vault unnecessarily close to liquidation.

**Impact:** Users could lose a significant portion of collateral when depositing into and withdrawing from Gamma Vaults.

**Recommended Mitigation:** While the existing validation can remain, consider allowing the user to pass a more restrictive collateral drop percentage and more fine-grained slippage parameters for the interactions linked above.

**The Standard DAO:** Fixed by commit [`cc86606`](https://github.com/the-standard/smart-vault/commit/cc86606ef6f8c1fea84f378e7f324e648f9bcbc8).

**Cyfrin:** Verified, `SmartVaultV4::depositYield` and `SmartVaultV4::withdrawYield` now accept a user-supplied minimum collateral percentage parameter. Note that due to the re-ordering of validation in `SmartVaultV4::mint`, the `remainCollateralised()` modifier can be used for this function.

**The Standard DAO:** Fixed by commit [e89daee](https://github.com/the-standard/smart-vault/commit/e89daee950d76180a969c6f93839addd8d43b195).

**Cyfrin:** Verified, the modifier is now used for `mint()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | The Standard Smart Vault |
| Report Date | N/A |
| Finders | Immeas, Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

