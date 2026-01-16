---
# Core Classification
protocol: Lukso Lsp Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18974
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-04-13-LUKSO LSP audit.md
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
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-H-1 Reentrancy protection can likely be bypassed

### Overview


A bug was discovered in the KeyManager of a contract, which allows an attacker to reenter the contract through a third-party contract with REENTRANCY_PERMISSION. This bug could potentially be chained several times, leading to a vulnerable code that assumes such flows to be impossible. The recommended mitigation was to return the flag to the original value before reentry, rather than always setting it to false. The team applied a different fix, which left the reentrancyStatus on when the current call is not the initial call to the KeyManager.

### Original Finding Content

**Description:**
The KeyManager offers reentrancy protection for interactions with the associated account. 
Through the LSP20 callbacks or through the `execute()` calls, it will call `_nonReentrantBefore()`
before execution, and `_nonReentrantAfter()` post-execution. The latter will always reset the 
flag signaling entry.
```solidity
    function _nonReentrantAfter() internal virtual {
    // By storing the original value once again, a refund is triggered 
             (see // https://eips.ethereum.org/EIPS/eip-2200)
        _reentrancyStatus = false;
     }
```
An attacker can abuse it to reenter provided that there exists some third-party contract with 
REENTRANCY_PERMISSION that performs some interaction with the contract. The attacker 
would trigger the third-party code path, which will clear the reentrancy status, and enable 
attacker to reenter. This could potentially be chained several times. Breaking the reentrancy 
assumption would make code that assumes such flows to be impossible to now be vulnerable.

**Recommended Mitigation:**
In `_nonReentrantAfter()`, the flag should be returned to the original value before reentry, 
rather than always setting it to false.

**Team response:**
Applied a fix different than recommendation.

**Mitigiation review:**
All code paths will now leave the **_reentrancyStatus** on when the current call is not the initial 
call to the KeyManager.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Lukso Lsp Audit |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-04-13-LUKSO LSP audit.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

