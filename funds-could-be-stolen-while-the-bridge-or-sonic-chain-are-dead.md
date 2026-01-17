---
# Core Classification
protocol: Sonic Gateway
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59005
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/sonic-gateway/fbb78575-2a22-4f4b-813f-340eb6296185/index.html
source_link: https://certificate.quantstamp.com/full/sonic-gateway/fbb78575-2a22-4f4b-813f-340eb6296185/index.html
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
finders_count: 3
finders:
  - Julio Aguilar
  - Mustafa Hasan
  - Jonathan Mevs
---

## Vulnerability Title

Funds Could Be Stolen While the Bridge or Sonic Chain Are Dead

### Overview


A bug has been reported in the `ExitAdministrator.sol` file, where the admin access can be compromised and potentially allow someone to steal all the funds from the bridge. This is because the `ExitAdministrator` contract does not perform any validations or track withdrawals, but instead relies on the `TokenDeposit` contract. The client has marked this bug as "fixed" and suggests removing the `ExitAdministrator` contract and relying solely on the `DirectExitAdministrator` for managing fund withdrawals and validations.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `5dcf7016b6644d5e8f48eb32201fd6ba4e058a80`. The client provided the following explanation:

> Admin access replaced by updating the ExitAdministrator by validators update.

**File(s) affected:**`ExitAdministrator.sol`

**Description:** The `DirectExitAdministrator` contract validates the user’s proof of minted balance on Sonic and tracks users who have withdrawn their funds from the bridge. In contrast, the `ExitAdministrator` neither performs these validations nor tracks withdrawals. It merely calls the `TokenDeposit` contract, which trusts the `ExitAdministrator` without further verification. If the admin of the `ExitAdministrator` is compromised, the `IMPLEMENTATION_ROLE` could be granted to another address, potentially allowing them to steal all the funds from the bridge.

Furthermore, the additional modularity provided by the `ExitAdministrator` seems redundant. Since it does not offer any meaningful functionality or validation and directly interacts with the `TokenDeposit` contract, its responsibilities can be handled by the `DirectExitAdministrator` after verifying the user’s proof.

**Recommendation:** We recommend removing the `ExitAdministrator` contract and relying solely on the `DirectExitAdministrator` to manage fund withdrawals and validations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Sonic Gateway |
| Report Date | N/A |
| Finders | Julio Aguilar, Mustafa Hasan, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/sonic-gateway/fbb78575-2a22-4f4b-813f-340eb6296185/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/sonic-gateway/fbb78575-2a22-4f4b-813f-340eb6296185/index.html

### Keywords for Search

`vulnerability`

