---
# Core Classification
protocol: veToken Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6141
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-vetoken-finance-contest
source_link: https://code4rena.com/reports/2022-05-vetoken
github_link: https://github.com/code-423n4/2022-05-vetoken-findings/issues/50

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

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Picodes
---

## Vulnerability Title

[M-20] Contracts should be robust to upgrades of underlying gauges and eventually changes of the underlying tokens

### Overview


This bug report is about the vulnerability of veAsset projects to changes in underlying LP tokens and interfaces. If changes occur, the system could become blocked or frozen. This has already happened a few weeks ago, and the veToken team would have to take painful shutdown steps to rescue the funds. 

In order to mitigate this vulnerability, either the VoterProxy needs to be upgradable, or intermediate contracts between the staker and the gauge need to be added and upgraded to preserve the logic. These steps should be taken to ensure that the system remains robust to changes in underlying LP tokens and interfaces.

### Original Finding Content

_Submitted by Picodes_

For some veAsset project (for example Angle’s [gauges](https://github.com/AngleProtocol/angle-core/blob/main/contracts/staking/LiquidityGaugeV4UpgradedToken.vy), gauge contracts are upgradable, so interfaces and underlying LP tokens are subject to change, blocking and freezing the system. Note that this is not hypothetic as it happened a few weeks ago: see this [snapshot vote](https://snapshot.org/#/anglegovernance.eth/proposal/0x1adb0a958220b3dcb54d2cb426ca19110486a598a41a75b3b37c51bfbd299513). Therefore, the system should be robust to a change in the pair gauge / token.

Note that is doable in the current setup for the veToken team to rescue the funds in such case, hence it is only a medium issue.
You’d have to do as follow: a painful shutdown of the `Booster` (which would lead to an horrible situation where you’d have to preserve backwards compatibility for LPs to save their funds in the new Booster), an operator change in `VoterProxy` to be able to call `execute`.

### Recommended Mitigation Steps

To deal with upgradeable contracts, either the `VoterProxy` needs to be upgradable to deal with any situation that may arise, either you need to add upgradeable “intermediate” contracts between the `staker` and the gauge that could be changed to preserve the logic.

**[jetbrain10 (veToken Finance) confirmed and commented](https://github.com/code-423n4/2022-05-vetoken-findings/issues/50#issuecomment-1156647119):**
 > Same as answer [#49](https://github.com/code-423n4/2022-05-vetoken-findings/issues/49)  for angle Voter Proxy, will make it upgrade able and make all future VoterProxy can be upgrade able as well if veAsset project agrees.  

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-05-vetoken-findings/issues/50#issuecomment-1194878444):**
 > The warden has shown how, due to integrating with underlying upgradeable contracts, the Sponsors Contracts could get bricked or forced into a shutdown.
> 
> I believe the finding to be equivalent to showing how the system could end up being attached to a bad gauge, and the warden has shown historical proof that this has happened and could happen again.
> 
> For those reasons, as well as the Sponsor Confirming, I believe the finding to be valid and of Medium Severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | veToken Finance |
| Report Date | N/A |
| Finders | Picodes |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-vetoken
- **GitHub**: https://github.com/code-423n4/2022-05-vetoken-findings/issues/50
- **Contest**: https://code4rena.com/contests/2022-05-vetoken-finance-contest

### Keywords for Search

`vulnerability`

