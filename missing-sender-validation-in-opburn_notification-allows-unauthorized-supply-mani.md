---
# Core Classification
protocol: XDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61876
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/xdao/2670863d-2e1c-42e6-a15c-5572dd4fef85/index.html
source_link: https://certificate.quantstamp.com/full/xdao/2670863d-2e1c-42e6-a15c-5572dd4fef85/index.html
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
  - István Böhm
  - Andy Lin
  - Cameron Biniamow
---

## Vulnerability Title

Missing Sender Validation in `op::burn_notification` Allows Unauthorized Supply Manipulation

### Overview


The bug report discusses an issue that was found and fixed in a specific file called `contracts/master.fc`. The problem was in a function called `master.recv_internal()` where a certain branch called `op::burn_notification` was not properly checking if the sender's address matched the designated jetton master address. This means that an attacker could send a fake `burn_notification` and change the total supply of the token without going through the proper governance or burn mechanisms. The report also provides a scenario for how this exploit could be carried out. To fix this, the team recommends adding a check at the beginning of the `op::burn_notification` handler to ensure that only the legitimate jetton master can initiate a supply burn. 

### Original Finding Content

**Update**
The team fixed the issue as recommended. Addressed in: `288fd7183366ece8ce26693df60379bb22535fcc`.

**File(s) affected:**`contracts/master.fc`

**Description:** In `master.recv_internal()`, the `op::burn_notification` branch updates `data::total_supply` without verifying that `sender_address` matches `data::jetton_master_address`. An attacker can send a spoofed `burn_notification` to arbitrarily change the total supply, bypassing the intended governance or burn mechanisms.

**Exploit Scenario:**

1.   An attacker crafts an internal message with `op::burn_notification` and a chosen `new_supply`.
2.   The message is sent to the contract from any address.
3.   The contract updates `data::total_supply` to the attacker’s value, undermining token economics and governance.

**Recommendation:** At the start of the `op::burn_notification` handler, add `throw_unless(error::invalid_sender, equal_slices(sender_address, data::jetton_master_address))` to ensure only the legitimate jetton master can signal a supply burn.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | XDAO |
| Report Date | N/A |
| Finders | István Böhm, Andy Lin, Cameron Biniamow |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/xdao/2670863d-2e1c-42e6-a15c-5572dd4fef85/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/xdao/2670863d-2e1c-42e6-a15c-5572dd4fef85/index.html

### Keywords for Search

`vulnerability`

