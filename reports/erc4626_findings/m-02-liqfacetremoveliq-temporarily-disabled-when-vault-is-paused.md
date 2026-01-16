---
# Core Classification
protocol: Burve_2025-01-29
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55216
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Burve-security-review_2025-01-29.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] `LiqFacet::removeLiq` temporarily disabled when vault is paused

### Overview


This bug report discusses an issue with the `LiqFacet` function where users are unable to remove liquidity due to a lack of consideration for paused vaults. The function currently attempts to withdraw from all vaults where a token is in the closure, but if one of these vaults is paused, the entire withdrawal process is blocked. The recommendation is to implement a mechanism that skips paused vaults and allows for withdrawals from the remaining active vaults to ensure a smooth liquidity removal process. 

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

In `LiqFacet`, when users add liquidity, they deposit a single token into a specific vault:

```solidity
    function addLiq(
        address recipient,
        uint16 _closureId,
        address token,
        uint128 amount
    ) external nonReentrant returns (uint256 shares) {
```

However, when removing liquidity, the function attempts to withdraw from all vaults where the token is in the closure:

```solidity
        for (uint8 i = 0; i < n; ++i) {
            VertexId v = newVertexId(i);
            VaultPointer memory vPtr = VaultLib.get(v);
            uint128 bal = vPtr.balance(cid, false);
            if (bal == 0) continue;
            // If there are tokens, we withdraw.
            uint256 withdraw = FullMath.mulX256(percentX256, bal, false);
            vPtr.withdraw(cid, withdraw);
            vPtr.commit();
            address token = tokenReg.tokens[i];
            TransferHelper.safeTransfer(token, recipient, withdraw);
        }
```

The issue arises when one of these vaults is paused. Since the function does not account for paused vaults, the entire withdrawal process is blocked, preventing users from removing liquidity.

## Recommendations

Implement a mechanism to skip paused vaults and allow withdrawals from the remaining active vaults to ensure a smooth liquidity removal.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Burve_2025-01-29 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Burve-security-review_2025-01-29.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

