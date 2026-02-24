---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42506
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-03-biconomy
source_link: https://code4rena.com/reports/2022-03-biconomy
github_link: https://github.com/code-423n4/2022-03-biconomy-findings/issues/137

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

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-02] A `pauser` can brick the contracts

### Overview


This bug report is about a problem with the Pausable contract found in the code for Biconomy. The issue was discovered by multiple users and can be triggered by a malicious or compromised 'pauser' who can freeze all funds by calling 'pause()' and 'renouncePauser()'. The recommended solution is to either remove 'renouncePauser()' or require the contract to not be in the 'paused' mode when 'renouncePauser()' is called. However, there are concerns about changing the 'onlyPauser' modifier to 'onlyOwner' as it could have negative consequences if the owner account is compromised. The decision on how to address this issue is up to the developers.

### Original Finding Content

_Submitted by WatchPug, also found by JMukesh, peritoflores, and whilom_

[Pausable.sol#L65-L68](https://github.com/code-423n4/2022-03-biconomy/blob/db8a1fdddd02e8cc209a4c73ffbb3de210e4a81a/contracts/security/Pausable.sol#L65-L68)<br>

```solidity
    function renouncePauser() external virtual onlyPauser {
        emit PauserChanged(_pauser, address(0));
        _pauser = address(0);
    }
```

A malicious or compromised `pauser` can call `pause()` and `renouncePauser()` to brick the contract and all the funds can be frozen.

### Proof of Concept

Given:

*   Alice (EOA) is the `pauser` of the contract.

1.  Alice calls `pause()` ;
2.  Alice calls `renouncePauser()`;

As a result, most of the contract's methods are now unavailable, and this cannot be reversed even by the `owner`.

### Recommended Mitigation Steps

Consider removing `renouncePauser()`, or requiring the contract not in `paused` mode when `renouncePauser()`.

**[ankurdubey521 (Biconomy) confirmed and commented](https://github.com/code-423n4/2022-03-biconomy-findings/issues/137#issuecomment-1083350829):**
 > Yeah, `changePauser` needs to have an `onlyOwner` modifier instead of `onlyPauser`.
 >
 > [HP-25: C4 Audit Fixes, Dynamic Fee Changes bcnmy/hyphen-contract#42](https://github.com/bcnmy/hyphen-contract/pull/42)

**[pauliax (judge) commented](https://github.com/code-423n4/2022-03-biconomy-findings/issues/137#issuecomment-1095044957):**
 > A valid concern, however, the proposed solution has drawbacks too. If you change from onlyPauser to onlyOwner here, a compromise of the owner account will have devastating consequences while with the current implementation the pauser can still pause the contracts independently of an owner. So this is a double-edged sword, it is up to you to decide which way is more acceptable.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-biconomy
- **GitHub**: https://github.com/code-423n4/2022-03-biconomy-findings/issues/137
- **Contest**: https://code4rena.com/reports/2022-03-biconomy

### Keywords for Search

`vulnerability`

