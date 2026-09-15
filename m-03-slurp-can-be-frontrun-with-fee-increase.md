---
# Core Classification
protocol: Tribe
chain: everychain
category: economic
vulnerability_type: front-running

# Attack Vector Details
attack_type: front-running
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1548
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-tribe-turbo-contest
source_link: https://code4rena.com/reports/2022-02-tribe-turbo
github_link: https://github.com/code-423n4/2022-02-tribe-turbo-findings/issues/29

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
  - front-running

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cmichel
  - gzeon
---

## Vulnerability Title

[M-03] Slurp can be frontrun with fee increase

### Overview


This bug report outlines a vulnerability in the "TurboSafe.slurp" function of the "2022-02-tribe-turbo" code repository found on GitHub. This function fetches the current fee from the "clerk()", which can be changed. This allows for a situation where a "clerk" can frontrun the transaction, increasing the fee and stealing the vault yield that should go to the user. The report recommends that the mechanic of the "master" being able to call "slurp" at any time needs to be addressed first in order to provide better user protection and mitigation.

### Original Finding Content

_Submitted by cmichel, also found by gzeon_

The `TurboSafe.slurp` function fetches the current fee from the `clerk()`.
This fee can be changed.
The `slurp` transaction can be frontrun with a fee increase (specifically targeted for the vault or the asset) by the clerk and steal the vault yield that should go to the user.

Maybe the user would not want to `slurp` at the new fee rate and would rather wait as they expect the fees to decrease again in the future.
Or they would rather create a new vault if the default fees are lower.

### Recommended Mitigation Steps

Right now there's no good protection against this as the master can call `slurp` at any time.
(They could even increase the fees to 100%, slurp, reset the fees.)
This mechanic would need to be addressed first if mitigation and better user protection are desired.

**[Joeysantoro (Tribe Turbo) disputed and commented](https://github.com/code-423n4/2022-02-tribe-turbo-findings/issues/29#issuecomment-1050202638):**
 > Slurping is public, and fee increases will be behind governance timelocks. Users are sufficiently protected. Any more complete solution to this would dramatically increase the computational complexity of the architecture.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-02-tribe-turbo-findings/issues/29#issuecomment-1066146290):**
 > I have to agree with the Warden here that this type of Admin Privilege is present in the system and can be used to raise fees up to 100%.
> 
> I believe protocol users could get stronger security guarantees by having a MAX_FEE hardcoded variable to ensure fees can never go above a certain threshold.
> 
> I recommend the sponsor to publicly disclose this potential risk to protocol users, and given that I believe that the timelock will provide a good base security guarantee to which I'd recommend adding a MAX_FEE.
> 
> Because the finding is contingent on malicious governance I believe medium severity to be appropriate.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tribe |
| Report Date | N/A |
| Finders | cmichel, gzeon |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-tribe-turbo
- **GitHub**: https://github.com/code-423n4/2022-02-tribe-turbo-findings/issues/29
- **Contest**: https://code4rena.com/contests/2022-02-tribe-turbo-contest

### Keywords for Search

`Front-Running`

