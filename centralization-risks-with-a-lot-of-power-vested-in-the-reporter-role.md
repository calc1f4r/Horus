---
# Core Classification
protocol: Casimir
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35009
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
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
finders_count: 2
finders:
  - Hans
  - 0kage
---

## Vulnerability Title

Centralization risks with a lot of power vested in the `Reporter` role

### Overview


The current design of the Casimir protocol has a potential issue where a single address, known as the `Reporter`, is responsible for many important operations. This puts the protocol at risk of centralization, which could lead to issues such as compromised private keys, rogue administrators, and human or automation errors. To mitigate these risks, it is recommended to continuously monitor off-chain processes and automate `Reporter` operations through a multi-sig system. In the long term, the protocol should aim for decentralization. The Casimir team has acknowledged this issue and plans to implement a solution in the future.

### Original Finding Content

**Description:** In the current design, the `Reporter`, a protocol-controlled address, is responsible for executing a number of mission-critical operations. Only `Reporter` operations include starting & finalizing a report, selecting & replacing operators, syncing/activating/withdrawing and depositing validators, verifying & claiming rewards from EigenLayer, etc. Also noteworthy is the fact that the timing and sequence of these operations are crucial for the proper functioning of the Casimir protocol.

**Impact:** With so many operations controlled by a single address, a significant part of which are initiated off-chain, the protocol is exposed to all the risks associated with centralization. Some of the known risks include:

- Compromised/lost private keys that control the `Reporter` address
- Rogue admin
- Network downtime
- Human/Automation errors associated with the execution of multiple operations

**Recommended Mitigation:** While we understand that the protocol in the launch phase wants to retain control over mission-critical parameters, we strongly recommend implementing the following even at the launch phase:

- Continuous monitoring of off-chain processes
- Reporter automation via a multi-sig

In the long term, the protocol should consider a clear path towards decentralization.

**Casimir:**
Acknowledged. We plan to implement the expected EigenLayer checkpoint upgrade that significantly reduces the intervention of the reporter while syncing validator balances.

**Cyfrin:** Acknowledged.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Casimir |
| Report Date | N/A |
| Finders | Hans, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

