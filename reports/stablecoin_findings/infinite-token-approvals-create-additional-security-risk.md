---
# Core Classification
protocol: vusd-stablecoin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61780
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html
source_link: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 1.00
financial_impact: low

# Scoring
quality_score: 5
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Paul Clemson
  - Leonardo Passos
  - Tim Sigl
---

## Vulnerability Title

Infinite Token Approvals Create Additional Security Risk

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> Minter and Redeemer doesn't hold any erc20 token. It is immediately deposited to protocol when user interact for mint. Router has approval of COMP token only not stable coins.

**Description:** The Minter contract uses infinite token approvals (`type(uint256).max`) when adding a new token to the whitelist. This occurs in the `_addToken()`function with the line `IERC20(_token).safeApprove(_cToken, type(uint256).max)`. Similarly, in the Treasury contract, infinite approvals are granted in multiple places: when adding tokens via `_addToken()` and when updating the swap manager via `_approveRouters()`. While this approach eliminates the need for subsequent approval transactions, it exposes the protocol to greater risk if any of the approved contracts (cToken contracts or routers) were to be compromised.

**Exploit Scenario:**

1.   A vulnerability is discovered in one of the cToken contracts or swap routers that have been granted infinite approval.
2.   An attacker exploits this vulnerability to drain all tokens from the Minter or Treasury contracts.
3.   Since the attacker has access to the maximum possible allowance, they can transfer all available tokens in a single transaction.
4.   The protocol loses all funds held in the affected contract, potentially causing significant financial damage.

**Recommendation:** Consider replacing infinite approvals with exact amounts needed for each transaction, particularly for critical operations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 5/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | vusd-stablecoin |
| Report Date | N/A |
| Finders | Paul Clemson, Leonardo Passos, Tim Sigl |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html

### Keywords for Search

`vulnerability`

