---
# Core Classification
protocol: Remora Pledge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61203
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Dacian
  - Stalin
---

## Vulnerability Title

Minting new PropertyTokens close to the end of the distribution period will dilute rewards for holders who were holding for the full period

### Overview

See description below for full details.

### Original Finding Content

**Description:** Holder's balanceHistory is updated each time a transfer of tokens occurs (mint or burn too). The [accounting saves the holders' balance during a certain index](https://github.com/remora-projects/remora-smart-contracts/blob/main/contracts/RWAToken/DividendManager.sol#L533-L540), which is used to determine the payout earned from the distributed amount of stablecoin for the index.

```solidity
    function _updateHolders(address from, address to) internal {
        ...
            } else {
                // else update status data and create new entry
                tHolderStatus.mostRecentEntry = payoutIndex;
//@audit => saves the holder balance for the current payout, regardless of how much time is left for the distribution to end
                $._balanceHistory[to][payoutIndex] = TokenBalanceChange({
                    isValid: true,
                    tokenBalance: toBalance
                });
            }
        }

```

New mintings of PropertyTokens mean that the same amount of payout distributed for all holders will give less payout to each PropertyToken. The problem is that new mintings that occur close to the end of the distribution period will dilute payouts for holders who have held their PropertyTokens for the full period.

**Impact:** Holders who have held their PropertyTokens for the full distribution period will get their rewards diluted by new PropertyTokens that get minted close to the end of the period.

**Recommended Mitigation:** On the [mint()](https://github.com/remora-projects/remora-smart-contracts/blob/main/contracts/RWAToken/RemoraToken.sol#L268-L270) calculate how much time has passed on the current distribution period, and if a certain threshold (maybe 75-80%) has passed, don't allow new mintings until the next distribution period.

**Remora:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Remora Pledge |
| Report Date | N/A |
| Finders | Dacian, Stalin |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

