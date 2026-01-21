---
# Core Classification
protocol: Level Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60882
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html
source_link: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html
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
finders_count: 4
finders:
  - Jeffrey Kam
  - Mustafa Hasan
  - Rabib Islam
  - Guillermo Escobero
---

## Vulnerability Title

No Limit on Position Size with Current Timelock Configuration Enables Unstoppable Theft of Funds From Pool

### Overview


The report discusses a potential attack on the Level Finance platform that could result in the theft of all liquidity pool funds. This could happen if the Level Finance team opens a large position and then upgrades the Pool contract, allowing them to withdraw the funds. The report suggests resolving issues with the Timelock and Pool contracts to prevent this attack.

### Original Finding Content

**Update**
Mitigated. The client's response: "Along with positions limit added above, we plan to transfer proxy admin's ownership to a 48-hours timelock whenever the audit completed." However, the transfer remains to be done.

**File(s) affected:**`Timelock.sol`, `Pool.sol`

**Description:** In LEV-9, we detailed that all LP funds can be locked in the pool for a period of time because of traders who open positions of sufficiently large size.

In LEV-8, we detailed that the `Timelock` contract has only a 12-hour delay and has the ability to upgrade the `Pool` contract, allowing for funds to be stolen by the Level Finance team.

Together, these issues form the basis for an attack that would allow the Level Finance team to lock all the LP funds and drain them through a coordinated contract upgrade.

**Exploit Scenario:**

1.   Alice deposits BTC liquidity into the senior tranche.
2.   The Level Finance team opens a long position that reserves all of the pool funds (with 30x leverage, this would only require at most approximately 3.3% of the value of the funds in the pool).
3.   The Level Finance team queues a transaction in the `Timelock` contract that is aimed at upgrading the `Pool` contract, allowing the withdrawal of the funds therein by the Level Finance team exclusively.
4.   The upgrade occurs and the funds are withdrawn by the Level Finance team.

**Recommendation:** We recommend that the issues described in LEV-9 and LEV-8 are resolved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Level Finance |
| Report Date | N/A |
| Finders | Jeffrey Kam, Mustafa Hasan, Rabib Islam, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html

### Keywords for Search

`vulnerability`

