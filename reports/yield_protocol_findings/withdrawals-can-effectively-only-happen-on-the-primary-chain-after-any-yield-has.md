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
solodit_id: 63838
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

Withdrawals can effectively only happen on the primary chain after any yield has accrued

### Overview


This bug report discusses an issue that occurs when trying to withdraw funds from a system called SherpaVault. The problem arises when a user withdraws funds from a secondary chain, causing the system to become corrupted. This is due to a function called `SherpaVault::adjustAccountingSupply` which is used to adjust the balance of funds. The recommended solution is to split the approval mode and introduce explicit asset-only rebalancing. This bug has been fixed in a recent update.

### Original Finding Content

**Description:** During round rolls, yield is only realized on the primary chain in `SherpaVault::_adjustBalanceAndEmit`. This leaves the system in a problematic state if withdrawals happens on another chain.

Imagine the scenario: there's 500 + 500 deposits of SherpaUSD on chain A and B, A being primary. 100 SherpaUSD is added as yield on A. The balance is 500 + 600, global total 1100 giving a share price of 1.1.
Alice, who has half the total shares decides do withdraw on chain B, giving her 550 SherpaUSD (USDC). Since this isn't available on chain B, the protocol needs to rebalance 50 SherpaUSD from A to B.

They do this by calling `SherpaUSD::ownerBurn(50)` on chain A followed by `SherpaUSD::ownerMint(50)` on chain B. This will store 50 in both `approvedTotalStakedAdjustment` and `approvedAccountingAdjustment` on both chains. The latter one being the issue.

Once `SherpaVault::adjustTotalStaked` is called by the operator, the rebalance of SherpaUSD is done, and Alice can effectively withdraw. However, there's no way to clear the state in `approvedAccountingAdjustment` as no shares were ever moved. If `SherpaVault::adjustAccountingSupply` is called, it will corrupt the `accountingSupply` as no shares were ever moved. So the states of `approvedAccountingAdjustment` are effectively permanently corrupted as `consumeAccountingApproval` can only be cleared from the vault.

In addition to this, if `SherpaVault::adjustAccountingSupply` was called on chain A, `accountingSupply` would be decremented and the `accountingSupply` subtraction in function `_unstake()` would underflow on chain A, hence bricking funds.


**Impact:** Withdrawals can only safely happen on the primary chain as soon as any yield is accrued. If yield is withdraw from the secondary chain that will corrupt either `SherpaUSD.approvedAccountingAdjustment` or `SherpaVault.accountingSupply` on both chains.

**Recommended Mitigation:** Consider split approval modes. Introduce explicit asset-only rebalancing (set `approvedTotalStakedAdjustment` without setting `approvedAccountingAdjustment`) and a share-sync mode (set both).

**Sherpa:** Fixed in commit [`34f2092`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/commit/34f2092f8f882005304c8f1a2ad311ed91d9161a)

**Cyfrin:** Verified. Calls to rebalance assets only were added.

\clearpage

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

