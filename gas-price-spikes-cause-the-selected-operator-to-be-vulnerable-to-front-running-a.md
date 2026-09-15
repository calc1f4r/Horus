---
# Core Classification
protocol: Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52129
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/holograph/protocol
source_link: https://www.halborn.com/audits/holograph/protocol
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
  - Halborn
---

## Vulnerability Title

Gas price spikes cause the selected operator to be vulnerable to front-running and be slashed

### Overview


This bug report is about a vulnerability in the `HolographOperator` contract. The current code allows other operators to front-run and potentially slash the selected operator during gas price spikes. The report suggests adjusting the operator node software to queue transactions immediately with the specified gas price during a gas spike to prevent this vulnerability. The Holograph team has accepted this risk.

### Original Finding Content

##### Description

In the `HolographOperator`contract, gas price spikes expose the selected operator to frontrunning and slashing vulnerabilities. The current code includes:

```
require(gasPrice >= tx.gasprice, "HOLOGRAPH: gas spike detected");
// operator slashing logic
_bondedAmounts[job.operator] -= amount;
_bondedAmounts[msg.sender] += amount;
```

This mechanism aims to prevent operators from being slashed due to gas spikes. However, it allows other operators to front-run by submitting their transactions with a higher gas price, resulting in the selected operator being slashed if they delay their transaction.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:H/Y:N/R:N/S:U (7.5)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:H/Y:N/R:N/S:U)

##### Recommendation

Adjust the operator node software to queue transactions immediately with the gas price specified in `bridgeInRequestPayload` during a gas spike.

##### Remediation

**RISK ACCEPTED:** The **Holograph team** accepted the risk of this finding.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Protocol |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/holograph/protocol
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/holograph/protocol

### Keywords for Search

`vulnerability`

