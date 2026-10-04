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
solodit_id: 59853
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/venus-protocol-vaults/9497f0a0-be2e-4214-9ade-f4f2e76b5cb2/index.html
source_link: https://certificate.quantstamp.com/full/venus-protocol-vaults/9497f0a0-be2e-4214-9ade-f4f2e76b5cb2/index.html
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Stakers in XVS Vault May Be Able to Double Their Voting Power by Re-Staking

### Overview


The client has marked a bug as "Fixed" in the `XVSVault.sol` file. The bug allows users to gain double voting power by depositing XVS into a pool with a different reward token and then re-staking in an XVS pool. This occurs because the user's voting power is only removed when the pool's reward token is XVS. The recommended solution is to change the logic in `requestWithdrawal()` so that the user's voting power is removed when the pool token is XVS.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `bad686c0ebd7c24e6f13cd7115a521c2a436bed2`.

**File(s) affected:**`XVSVault.sol`

**Description:** Users can deposit XVS into the XVS vault to get voting power. However, according to the implementation, when users request a withdrawal, their voting power is removed only when the pool's reward token is XVS. For pools having a different reward token, the user's voting power will not be removed, and therefore they can re-stake to the pool to gain double voting power with the same amount of XVS deposit.

**Exploit Scenario:**

1.   Suppose there is a pool with USDC as the reward token and XVS as the pool token.
2.   Assume that Alice has not made any deposits yet. First, Alice delegates to herself.
3.   Alice deposits 100 XVS to the pool. Since the pool token is XVS, Alice gets 100 voting power.
4.   Alice sends a withdrawal request. Since the reward token is not XVS, Alice's voting power is not removed.
5.   After the locked period passes, Alice can execute the withdrawal and re-stake into an XVS pool to get double voting power.

**Recommendation:** Consider changing the logic in `requestWithdrawal()` so that the user's voting power is removed when the pool token is XVS, rather than the reward token being XVS.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

