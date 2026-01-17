---
# Core Classification
protocol: Olas
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30030
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-12-autonolas
source_link: https://code4rena.com/reports/2023-12-autonolas
github_link: https://github.com/code-423n4/2023-12-autonolas-findings/issues/377

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
finders_count: 1
finders:
  - hash
---

## Vulnerability Title

[M-04] Possible DOS when withdrawing liquidity from Solana Lockbox

### Overview


This bug report discusses a possible denial-of-service (DOS) vulnerability in the process of withdrawing liquidity from a Lockbox. The report includes a proof of concept, which shows that the accounts required for the transaction can change and cause the transaction to fail. This could potentially allow attackers to steal fees by frequently withdrawing before other users. To prevent this, it is recommended to redesign the lockbox to continuously increase liquidity in a single position instead of adding new positions. The vulnerability has been confirmed by a team member.

### Original Finding Content


Possible DOS when withdrawing liquidity from Lockbox.

### Proof of Concept

When withdrawing it is required to pass all the associated accounts in the [transaction](https://solanacookbook.com/core-concepts/transactions.html#deep-dive). But among these (position,pdaPositionAccount and positionMint) are dependent on the current modifiable-state of the account ie. if another withdrawal occurs, the required accounts to be passed to the function call might change resulting in a revert.

<https://github.com/code-423n4/2023-12-autonolas/blob/2a095eb1f8359be349d23af67089795fb0be4ed1/lockbox-solana/solidity/liquidity_lockbox.sol#L194-L214>

```solidity
    @mutableAccount(pool)
    @account(tokenProgramId)
    @mutableAccount(position)
    @mutableAccount(userBridgedTokenAccount)
    @mutableAccount(pdaBridgedTokenAccount)
    @mutableAccount(userWallet)
    @mutableAccount(bridgedTokenMint)
    @mutableAccount(pdaPositionAccount)
    @mutableAccount(userTokenAccountA)
    @mutableAccount(userTokenAccountB)
    @mutableAccount(tokenVaultA)
    @mutableAccount(tokenVaultB)
    @mutableAccount(tickArrayLower)
    @mutableAccount(tickArrayUpper)
    @mutableAccount(positionMint)
    @signer(sig)
    function withdraw(uint64 amount) external {
        address positionAddress = positionAccounts[firstAvailablePositionAccountIndex];
        if (positionAddress != tx.accounts.position.key) {
            revert("Wrong liquidity token account");
        }
```

The DOS for a withdrawal can be caused by another user withdrawing before the user's transaction. Due to the possibility to steal fees, attackers would be motivated to frequently call the withdraw method making such a scenario likely.

### Recommended Mitigation Steps

To mitigate this it would require a redesign on how the lockbox accepts liquidity. Instead of adding new positions, the lockbox can keep its liquidity in a single position continuously increasing its liquidity for deposits.

**[mariapiamo (Olas) confirmed](https://github.com/code-423n4/2023-12-autonolas-findings/issues/377#issuecomment-1892552759)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Olas |
| Report Date | N/A |
| Finders | hash |

### Source Links

- **Source**: https://code4rena.com/reports/2023-12-autonolas
- **GitHub**: https://github.com/code-423n4/2023-12-autonolas-findings/issues/377
- **Contest**: https://code4rena.com/reports/2023-12-autonolas

### Keywords for Search

`vulnerability`

