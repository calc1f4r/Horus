---
# Core Classification
protocol: BakerFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49655
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-12-bakerfi-invitational
source_link: https://code4rena.com/reports/2024-12-bakerfi-invitational
github_link: https://code4rena.com/audits/2024-12-bakerfi-invitational/submissions/F-27

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
finders_count: 3
finders:
  - 0xlemon
  - MrPotatoMagic
---

## Vulnerability Title

[M-09] Non-whitelisted recipient can receive shares

### Overview


This bug report is about a vulnerability in the BakerFi protocol. The issue is that the protocol does not check if the recipient of the vault shares is whitelisted, meaning that non-whitelisted users can receive shares and then withdraw them through the VaultRouter. This bypasses the whitelist and could potentially lead to unauthorized access to shares. To mitigate this issue, the protocol has been updated to check if the recipient is whitelisted. The mitigation has been confirmed and full details can be found in the reports from shaflow2 and 0xlemon. 

### Original Finding Content



<https://github.com/code-423n4/2024-12-bakerfi/blob/main/contracts/core/VaultBase.sol# L237-L271>

### Summary

The recipient of the vault shares isn’t checked to be in the whitelist. This means that a non-whitelisted user can receive shares and then withdraw/redeem them throught the `VaultRouter`.

### Vulnerability Details

If we look at `VaultBase` deposit/mint/withdraw/redeem functions have a `onlyWhiteListed` modifier that means they can only be called by someone who is within the `_enabledAccounts`. However the protocol doesn’t check if the `receiver` is included in that whitelist. This allows non-whitelisted people to receive shares and they can later easily withdraw them through the `VaultRouter`.

### Impact

Bypass of the whitelist

### Recommended mitigation steps

Check if the `receiver` of the vault shares is whitelisted

**chefkenji (BakerFi) confirmed**

**[BakerFi mitigated](https://github.com/code-423n4/2025-01-bakerfi-mitigation?tab=readme-ov-file# findings-being-mitigated):**

> [PR-26](https://github.com/baker-fi/bakerfi-contracts/pull/26)

**Status:** Mitigation confirmed. Full details in reports from [shaflow2](https://code4rena.com/evaluate/2025-01-bakerfi-mitigation-review/findings/S-19) and [0xlemon](https://code4rena.com/evaluate/2025-01-bakerfi-mitigation-review/findings/S-23).

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BakerFi |
| Report Date | N/A |
| Finders | 0xlemon, MrPotatoMagic |

### Source Links

- **Source**: https://code4rena.com/reports/2024-12-bakerfi-invitational
- **GitHub**: https://code4rena.com/audits/2024-12-bakerfi-invitational/submissions/F-27
- **Contest**: https://code4rena.com/reports/2024-12-bakerfi-invitational

### Keywords for Search

`vulnerability`

