---
# Core Classification
protocol: Venus protocol (vaults)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59854
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/venus-protocol-vaults/9497f0a0-be2e-4214-9ade-f4f2e76b5cb2/index.html
source_link: https://certificate.quantstamp.com/full/venus-protocol-vaults/9497f0a0-be2e-4214-9ade-f4f2e76b5cb2/index.html
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
finders_count: 4
finders:
  - Shih-Hung Wang
  - Julio Aguilar
  - Roman Rohleder
  - Ibrahim Abouzied
---

## Vulnerability Title

VRT Vault Users Can Earn Additional Interests When Depositing After the Last Accrual Block

### Overview


The client has marked a bug in the VRTVault smart contract as "Fixed". The bug caused users' interest to be calculated incorrectly when they deposited funds after the last accruing block. This issue also affected existing users who made a second deposit. The recommendation is to redesign how the VRT vault keeps track of users' accrualStartBlockNumber or to only allow deposits when the last accruing block is at least the current block.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `b0a896c88bef287c6a58e1fe51aa63e8cb4f2dab`. The client provided the following explanation:

> Fixed by putting more restrictions in setLastAccruingBlock (see #25). Now admin cannot update lastAccruingBlock after it has passed.

**File(s) affected:**`VRTVault.sol`

**Description:** When a user deposits into the VRT vault and `lastAccruingBlock` is behind the current block, their `accrualStartBlockNumber` will be set to `lastAccruingBlock`. Although the user deposits at the current block, their interests are accrued starting from the `lastAccruingBlock`. They can claim those interests once the `lastAccruingBlock` has been moved forward to a more recent block.

**Exploit Scenario:**

1.   Suppose the `lastAccruingBlock` is set to 100 and the current block number is 200.
2.   A new user deposits into the vault. According to the `deposit()` function, their `accrualStartBlockNumber` is set to 100, the same value as `lastAccruingBlock`.
3.   The admin updates the `lastAccruingBlock` to 150.
4.   The user calls `claim()`. According to the calculation in `computeAccruedInterest()`, the user receives the interests between block 100 and 150 even though they did deposit any funds during that period.

This issue also exists for existing users with a non-zero deposit at the time of the second deposit. As a result, they will earn more interest for their second deposit when the `lastAccruingBlock` moves forward.

**Recommendation:** It is unclear whether the protocol should allow users to deposit after the last accruing block. If so, consider re-designing how the VRT vault keeps track of users' `accrualStartBlockNumber`. Ideally, each deposit should have its specific `accrualStartBlockNumber`.

An alternative way is to allow users to deposit only when their deposit amount is 0 or `lastAccruingBlock` is at least the current block. However, this approach limits the flexibility of the deposit functionality.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Venus protocol (vaults) |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Julio Aguilar, Roman Rohleder, Ibrahim Abouzied |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/venus-protocol-vaults/9497f0a0-be2e-4214-9ade-f4f2e76b5cb2/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/venus-protocol-vaults/9497f0a0-be2e-4214-9ade-f4f2e76b5cb2/index.html

### Keywords for Search

`vulnerability`

