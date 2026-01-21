---
# Core Classification
protocol: Radiant Riz Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35169
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/radiant-riz-audit
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
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Shutdown Is Not Irreversible

### Overview


The Riz protocol is designed for risky assets and has a feature that allows for a shutdown to be triggered in order to redistribute remaining funds after bad debt has been socialized. However, some modules in the market are upgradeable, which could potentially change the shutdown state. To prevent this, it is suggested to prevent any shutdown markets from being upgraded. The Radiant team has acknowledged the issue and stated that if a shutdown occurs, they will need to remove admin access to all proxies in that specific Riz market, which may be a complex process. 

### Original Finding Content

The Riz protocol is meant for riskier assets and supports a feature whereby a shutdown can be triggered to then slash the positions and redistribute the remaining funds after the bad debt has been socialized. However, even though the shutdown state cannot currently be changed after it has been triggered, most of the modules in the market are upgradeable. As such, these modules might call an upgraded implementation that would de\-shutdown the state.


In order to follow the specs of being completely and irreversibly shut down, consider preventing any shutdown markets from being upgraded.


***Update:** Acknowledged, not resolved. The Radiant team stated:*



> *Noted. If a shutdown happens, we will need to burn admin access to all the proxies in that specific Riz market. Making the proxy bricked might be slightly more complicated.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Radiant Riz Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/radiant-riz-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

