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
solodit_id: 18689
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

[H-04] AMO model opens up OHM treasury to increased risk

### Overview


The bug report is about the risk associated with connecting the OHM `MINTR` with an external contract in an automated way. The SiloAMO is using the externally set `uopt` value as an input that directly feeds to `MINTR` to determine new OHM deployed to the market. This could lead to an exploit where a hacker could tap into the `MINTR` contract to steal additional OHM. In addition, conditions could encourage the market to shift in a way that the AMO doesn't allow. To prevent this, the recommendation is to impose bounds on the `update()` function to only operate when `uopt` is between `ulow` and `ucrit`. In the event that the utilization rate falls outside of these bounds, a manual call to `deposit()` or `withdraw()` will need to be made by the Olympus team to restart the AMO. This will ensure that the AMO will not be exploitable in any extreme market conditions.

### Original Finding Content

While H-01 and H-02 describe specific ways that users might manipulate the AMO for their own gain, there is a more general risk associated with connecting the OHM `MINTR` with an external contract in an automated way.

In essence, what the SiloAMO is doing is using the externally set `uopt` value as an input that directly feeds to `MINTR` to determine new OHM deployed to the market.

The `uopt` value is determined by the Silo Finance team and not by the market. Markets are expected to function because users are self interested and weighing information, and the balance of users on both sides leads to rates, liquidity, and risks that these individuals deem appropriate. Blunting the market's judgment with automation is a risky proposition.

As an example of how this could cause a problem, imagine there is an exploit on Silo Finance that allows OHM to be drained. Instead of simply stealing what is in the Silo, the AMO provides the hacker with a tap directly into the `MINTR` contract to steal additional OHM.

Similar risks exist in less extreme situations, where conditions might encourage the market to shift in a way that the AMO doesn't allow. For example, in the event of an XAI depeg, all XAI depositors would want to maximize borrows against their assets. This would usually max out the borrows of OHM in the Silo, but the direct tap into the `MINTR` would provide exit liquidity for more XAI holders.

**Recommendation**

Similar to H-01 and H-02, there are a number of possible solutions, but my preferred solution is to impose bounds on the `update()` function to only operate when `uopt` is between `ulow` and `ucrit`.

In the event that the utilization rate falls outside of these bounds, a manual call to `deposit()` or `withdraw()` will need to be made by the Olympus team to restart the AMO.

This effectively ensures that, in any extreme market conditions, the AMO will turn off and not be exploitable.

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

