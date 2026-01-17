---
# Core Classification
protocol: Nayms 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60787
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/nayms-2/ae3ff4fd-fac2-4f52-b8eb-d570d730d6a6/index.html
source_link: https://certificate.quantstamp.com/full/nayms-2/ae3ff4fd-fac2-4f52-b8eb-d570d730d6a6/index.html
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - Jonathan Mevs
  - Andy Lin
  - Roman Rohleder
  - Jeffrey Kam
  - Martinet Lee
---

## Vulnerability Title

Entities Write Policies at a Collateralized Ratio

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation: This is by design, we want this to be doable.

**Description:** Capital Providers in the system should be aware that the amount of insurance policies that can be written by an Entity is based on a collateralized amount, meaning in theory, Entities can write more insurance policies than they may actually have funds to pay the claim for. We include this finding as a note to Capital Providers that insufficient liquidity is technically possible on chain for an Entity. However, off-chain, there are a number of steps done by Nayms to mitigate the risk of insufficient liquidity.

Entities are assigned a `maxCapacity` for the insurance amount they can write by the SysAdmin on creation which is validated when updated. Additionally, the whitepaper mentions that Segregated Accounts must have capital in line with Bermuda's solvency capital requirement framework. The whitepaper also mentions that the Nayms Discretionary Fund (NDF) can be used as a non-guaranteed, discretionary backstop to the SAC, although the NDF will be governed by the Nayms Token which is not yet implemented in the current system.

**Recommendation:** Ensure that Capital Providers are aware of this.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Nayms 2 |
| Report Date | N/A |
| Finders | Jonathan Mevs, Andy Lin, Roman Rohleder, Jeffrey Kam, Martinet Lee, Valerian Callens |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/nayms-2/ae3ff4fd-fac2-4f52-b8eb-d570d730d6a6/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/nayms-2/ae3ff4fd-fac2-4f52-b8eb-d570d730d6a6/index.html

### Keywords for Search

`vulnerability`

