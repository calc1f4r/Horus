---
# Core Classification
protocol: Olympusdao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18687
audit_firm: ZachObront
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-06-23-OlympusDAO.md
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

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zach Obront
---

## Vulnerability Title

[H-02] If AMO becomes primary depositor of Silo, user can force withdrawals to get inflated interest rates

### Overview


This bug report discusses an issue related to the SiloAMO, which is a protocol used to calculate interest rates for borrowers. The issue is that a user can manipulate the AMO to withdraw funds, leading to a critically overutilized supply and dramatically increased interest rates. This can be done by depositing a large amount of OHM, which causes the AMO to withdraw all of its funds, followed by the user withdrawing a portion of the funds. This sequence of events can be repeated daily, and if not fixed, can make the market unusable for regular users.

The recommended fix is to follow any of the recommended fixes for H-01, which is the inverse of this issue. The bug has been fixed as recommended in the commit 4bce45602daa4ee49b1ef52acf6f88021d1390d7.

### Original Finding Content

This issue is the inverse of [H-01], where the SiloAMO can be forced to deposit additional funds, decreasing rates for borrowers until 1 day later when `update()` can be called again.

In this case, we can imagine a situation where the SiloAMO becomes the primary depositor in the market. This is likely, as there is no reason to believe the market equilibrium for depositing OHM will align with the `uopt` and the interest rate at a near-optimal value calculated using `ki`. AMOs allow the rates determined by the protocol to become the market rates, whether or not the market agrees with these rates.

In the event that the majority of the deposited OHM is from the AMO, a user can manipulate the AMO to withdraw their funds, leading to a critically overutilized supply and dramatically increased interest rates.

A user who is a depositor of OHM in the pool could do this to benefit from the increased interest rates.

As a simple example of what this might look like:

- There is 100,000 OHM in the pool, close to all of which comes from the AMO
- Given the 50% optimal utilization rate, this means that 50,000 is borrowed
- A user deposits 100,000 OHM to the system
- The next block, they call `update()`, which causes the AMO to withdraw all its funds to maintain equilibrium
- The user then withdraws 50,000 OHM, leading to a utilization rate of 100% and massive interest rates

The `update()` function cannot be called again, and the market will need to wait for other users to jump in and fund deposits, or else regular borrowers of OHM will dramatically overpay for their borrows.

This sequence of events could be repeated daily, or even alternated with #155, making the market unusable for regular users.

**Recommendation**

Following any of the recommended fixes for H-01 will solve this issue as well.

**Review**

Fixed as recommended in [4bce45602daa4ee49b1ef52acf6f88021d1390d7](https://github.com/OlympusDAO/bophades/commit/4bce45602daa4ee49b1ef52acf6f88021d1390d7).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ZachObront |
| Protocol | Olympusdao |
| Report Date | N/A |
| Finders | Zach Obront |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-06-23-OlympusDAO.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

