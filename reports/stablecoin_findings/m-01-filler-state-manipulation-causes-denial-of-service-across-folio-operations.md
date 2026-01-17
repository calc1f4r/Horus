---
# Core Classification
protocol: Reserve_2025-06-02
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58224
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Reserve-security-review_2025-06-02.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
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

[M-01] Filler state manipulation causes denial-of-service across Folio operations

### Overview


The report describes a bug in the `Folio` protocol that may cause a denial-of-service (DoS) attack. This bug is caused by the `sync()` modifier, which can be exploited to manipulate internal token balances and prevent certain functions from executing properly. This can affect crucial operations such as `mint()`, `redeem()`, and fee distribution functions, as well as parameter updates. The attack can be executed by front-running target transactions and deploying a contract that calls `Folio.createTrustedFill()` followed by `filler.rescueToken()`. To prevent this, the report suggests implementing access control, restricting the `rescueToken()` function, or adding a check to disallow the function from being called during block initialization. 

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

As the `sync()` modifier, which reverts if `swapActive()` returns `true`, is used in many crucial functions in `Folio` and also the `FolioDAOFeeRegistry`, this can be exploited to cause a DoS on protocol operations including:

1. `mint()` and `redeem()` functions, blocking users from entering or exiting positions.
2. Auction functions, preventing the protocol from executing trades.
3. Fee distribution functions, disrupt the protocol's economic model.
4. Parameter updates: `removeFromBasket()` and `FolioDAOFeeRegistry()` folio's fee setting functions.

By performing the frontruning attack to thoes operations with `{Folio.createTrustedFiller(); filler.rescueToken();}`

The attack can be executed by front-running target transactions with a sequence of:

1. Deploy a contract that calls `Folio.createTrustedFill()` followed by `filler.rescueToken()`, which manipulates internal token balances.
2. This causes `swapActive()` to return `true`, preventing the filler from being closed and causing any subsequent `sync()`

## Recommendation

Possible options:

- Restrict `rescueToken()` to be `internal` and callable only through `closeFiller()`.
- Add access control to restrict the `rescueToken()`.
- Restrict `rescueToken()` to be callable only when `swapActive()` is `false`. This could ensure that fillers cannot be locked into a fake active state indefinitely and avoid protocol-wide denial-of-service scenarios.
- Add a check to disallow rescueToken from being called during block in which the contract was initialized (block.number == blockInitialized).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Reserve_2025-06-02 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Reserve-security-review_2025-06-02.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

