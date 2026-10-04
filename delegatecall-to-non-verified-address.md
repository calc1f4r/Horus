---
# Core Classification
protocol: Spool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56556
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-30-Spool.md
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
  - Zokyo
---

## Vulnerability Title

Delegatecall to non-verified address.

### Overview


The bug report states that in line 149 of the code, there is a function called "withdraw()" that allows users to pass any address without verification. This can potentially lead to loss of funds as the code is making a delegate call to this address. The recommendation is to verify all addresses that users can pass to functions and contracts. However, the client has responded saying that the call cannot happen if the strategy is not valid and only the vault can set user strategy shares. Additionally, if the total amount withdrawn is 0, the code will revert. After further clarification, it was concluded that validating that the strategy share is greater than zero before calling the strategy is sufficient.

### Original Finding Content

**Description**

line 149, function withdraw(). Addresses from array ‘strategies’ are not verified, thus user is
able to pass any address here. Spool is making a delegate call to this address
(SpoolStrategy.sol, line 305). This might potentially cause funds loss.

**Recommendation**:

Verify any address that a user can pass to functions, and contracts are making calls to.
Answer from client.
There is no way the call happens if the strategy is not valid. Only the vault can set the user
strategy shares. If user vault shares are 0, the call is skipped. This is nice to have require to
revert if calldata is wrong, but it cannot affect the system. Also, if total withdrawn is 0, the
code reverts.

**Post-audit**.

After clarification from the client’s side, auditors came to conclusion, that validating that
strategy share is greater than zero before calling strategy is enough.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Spool |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-30-Spool.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

