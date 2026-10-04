---
# Core Classification
protocol: Sapien - 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62027
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/sapien-2/9f938662-5bf7-4dc3-8774-3e7a12204cc3/index.html
source_link: https://certificate.quantstamp.com/full/sapien-2/9f938662-5bf7-4dc3-8774-3e7a12204cc3/index.html
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
finders_count: 3
finders:
  - Paul Clemson
  - Julio Aguilar
  - Tim Sigl
---

## Vulnerability Title

QA Penalty Can Be Avoided by Unstaking Before Penalty Processing

### Overview


The client has reported a bug in the SapienVault and SapienQA files. The bug allows users to instantly withdraw their tokens without waiting for the two day cooldown period, by using the `earlyUnstake()` function and paying a 20 percent penalty. This allows users to avoid larger QA penalties, which defeats the purpose of the cooldown period. The client recommends enforcing a cooldown period on all unstaking actions to prevent users from avoiding QA penalties. The bug has been fixed and the issue is now closed.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `737af6c63b0eae0af9c80425eb8a27afffd14ad8`, `cf36a2fac54e84904c51f8d419c04e215c7b35da` and `24e56c21d8cabbaf5b6236080265d629361e182e`.

**File(s) affected:**`SapienVault.sol`, `SapienQA.sol`

**Description:** Typical unstaking within the protocol requires a two day cooldown period to pass before unstaking can be completed. The intention of this is to allow a sufficient window for any QA penalties to be applied before the user can unstake their tokens. However, in the case of the `earlyUnstake()` function, users are able to instantly withdraw their funds by paying a 20 percent penalty. In cases where a user is expecting to be slashed a value greater than 20 percent they can call the `earlyUnstake()` function to immediately withdraw their tokens and avoid the impending larger QA penalty.

**Recommendation:** Consider enforcing a cooldown period on all unstaking actions to ensure that QA penalties cannot be avoided.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Sapien - 2 |
| Report Date | N/A |
| Finders | Paul Clemson, Julio Aguilar, Tim Sigl |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/sapien-2/9f938662-5bf7-4dc3-8774-3e7a12204cc3/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/sapien-2/9f938662-5bf7-4dc3-8774-3e7a12204cc3/index.html

### Keywords for Search

`vulnerability`

