---
# Core Classification
protocol: Superposition
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45238
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-10-superposition
source_link: https://code4rena.com/reports/2024-10-superposition
github_link: https://github.com/code-423n4/2024-10-superposition-findings/issues/19

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
  - DadeKuma
---

## Vulnerability Title

[M-01] It's still not possible to set pool's protocol fees

### Overview


This bug report discusses an issue where the admin is unable to set a pool's protocol fee due to a missing function. The previous attempt to fix the issue was unsuccessful and the root cause has been identified as the function not being implemented. As a result, the original problem persists and protocol fees cannot be set. The recommended solution is to add a new function to the code. The assessed type of this issue is Access Control. There is some disagreement among the team about the severity of the issue, but it is ultimately classified as a Medium risk.

### Original Finding Content


The admin can't set a pool's protocol fee because the function has not been implemented.

### Proof of Concept

The previous issue, [M-12](<https://github.com/code-423n4/2024-08-superposition-findings/issues/8>), wasn't fixed properly.

The root cause is that the admin has no way to call `set_fee_protocol_C_B_D_3_E_C_35` through Seawater, as the function wasn't implemented.

As a result, the original issue persists because protocol fees cannot be set.

### Recommended Mitigation Steps

Consider adding the following function to `SeaWaterAMM.sol`:

```solidity
    function setFeeProtocolCBD3EC35(address /* pool */, uint8 /* feeProtocol0 */, uint8 /* feeProtocol1 */) external {
        directDelegate(_getExecutorAdmin());
    }
```

### Assessed type

Access Control

**[af-afk (Superposition) commented](https://github.com/code-423n4/2024-10-superposition-findings/issues/19#issuecomment-2489996735):**
 > 0xsomeone - It's possible to call this function since the signature resolves it to the admin facet in the fallback.

**[0xsomeone (judge) commented](https://github.com/code-423n4/2024-10-superposition-findings/issues/19#issuecomment-2489784329):**
 > Per discussions in [#8](https://github.com/code-423n4/2024-08-superposition-findings/issues/8) this is a valid, albeit, Medium risk issue.

**[af-afk (Superposition) commented](https://github.com/code-423n4/2024-10-superposition-findings/issues/19#issuecomment-2548775895):**
> We felt this was technically inaccurate given that the function signature corresponded to the right fallback, triggering the correct dispatch, but we opted to fix this in principal with the similar issues. We weren't responsive at the time to affect the ruling.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Superposition |
| Report Date | N/A |
| Finders | DadeKuma |

### Source Links

- **Source**: https://code4rena.com/reports/2024-10-superposition
- **GitHub**: https://github.com/code-423n4/2024-10-superposition-findings/issues/19
- **Contest**: https://code4rena.com/reports/2024-10-superposition

### Keywords for Search

`vulnerability`

