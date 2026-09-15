---
# Core Classification
protocol: Mozaic Archimedes
chain: everychain
category: dos
vulnerability_type: dos

# Attack Vector Details
attack_type: dos
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18994
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-23-Mozaic Archimedes.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - dos

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-H-1 An attacker can drain Mozaic Vaults by manipulating the LP price

### Overview


This bug report is about an economic attack that can be used to bypass counting of LP tokens across all chains. The attack takes advantage of the fact that LP tokens are LayerZero OFT tokens which can be bridged. The attacker can wait for the Controller to initiate snapshotting, bridge a large amount of tokens with a miniscule gas fee, and then finish bridging-in with a valid gas amount. This would cause the Controller to order Vaults to settle, at which point the attacker converts their LP tokens at an artificially high price. Another way to exploit this flaw is to count LP tokens multiple times, by quickly transporting them to additional chains just before those chains are snapshotted.

Mozaic's response to this bug is to disable LP token bridging altogether. This is a configuration-level fix and users are encouraged to confirm the tokens are not linked via bridges at runtime.

### Original Finding Content

**Description:**
The controller is tasked with synchronizing LP token price across all chains. It implements a 
lifecycle. An admin initiates the snapshot phase, where Controller requests all Vaults to report 
the total stable ($) value and LP token supply. Once all reports are in, admin calls the settle 
function which dispatches the aggregated value and supply to all vaults. At this point, vaults 
process all deposits and withdrawals requested up to the last snapshot, using the universal 
value/supply ratio. 
The described pipeline falls victim to an economic attack, stemming from the fact that LP 
tokens are LayerZero OFT tokens which can be bridged. An attacker can use this property to 
bypass counting of their LP tokens across all chains. When the controller would receive a
report with correct stable value and artificially low LP supply, it would cause queued LP 
withdrawals to receive incorrectly high dollar value.
To make vaults miscalculate, attacker can wait for Controller to initiate snapshotting. At that 
moment, they can start bridging a large amount of tokens. They may specify custom LayerZero 
adapter params to pay a miniscule gas fee, which will guarantee that the bridge-in transaction 
will fail due to out-of-gas. At this point, they simply wait until all chains have been
snapshotted, and then finish bridging-in with a valid gas amount. Finally, Controller will order 
vaults to settle, at which point the attacker converts their LP tokens at an artificially high price.
Another clever way to exploit this flaw is to count LP tokens multiple times, by quickly 
transporting them to additional chains just before those chains are snapshotted. This way, the 
LP tokens would be diluted and the attacker can get a disproportionate amount of LP tokens 
for their stables.

**Recommended Mitigation:**
The easy but limiting solution is to reduce complexity and disable LP token bridging across 
networks. The other option is to increase complexity and track incoming/outgoing bridge 
requests in the LP token contract. When snapshotting, cross reference the requested 
snapshot time with the bridging history. 

**Team response:**
Fixed.

**Mitigation Review:**
Mozaic's response is to disable LP token bridging altogether. As this is a configuration-level 
fix, users are encouraged to confirm the tokens are not linked via bridges at runtime.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Trust Security |
| Protocol | Mozaic Archimedes |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-23-Mozaic Archimedes.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`DOS`

