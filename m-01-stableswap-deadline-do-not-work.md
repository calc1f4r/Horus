---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25324
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-canto-v2
source_link: https://code4rena.com/reports/2022-06-canto-v2
github_link: https://github.com/code-423n4/2022-06-NewBlockchain-v2-findings/issues/90

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
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-01] Stableswap - Deadline do not work

### Overview


A bug has been identified in the Plex Engineer lending-market-v2 codebase. The `ensure` modifier has been commented out, meaning that the deadline function will not work when passing orders. This breaks the functionality of the program. The bug was acknowledged by nivasan1 (Canto) and commented on by Alex the Entreprenerd (judge). Alex noted that this lack of deadline means that a miner may be able to deny a transaction from being mined until it incurs the maximum amount of slippage, which is not ideal. As a result, Alex agreed with the severity of the bug being rated as medium.

### Original Finding Content

_Submitted by Picodes, also found by cccz, Funen, ladboy233, Soosh, and zzzitron_

<https://github.com/Plex-Engineer/lending-market-v2/blob/ea5840de72eab58bec837bb51986ac73712fcfde/contracts/Stableswap/BaseV1-periphery.sol#L86><br>

The `ensure` modifier is commented, so deadlines will not work when passing orders, breaking this functionality.

**[nivasan1 (Canto) acknowledged](https://github.com/code-423n4/2022-06-canto-v2-findings/issues/90)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-06-canto-v2-findings/issues/90#issuecomment-1214244667):**
 > The warden has shown how, due to a comment, the modifier `deadline` doesn't work.
> 
> Because Front-running is a key aspect of AMM design, `deadline` is a useful tool to ensure that your tx cannot be "saved for later".
> 
> Due to the removal of the check, it may be more profitable for a miner to deny the transaction from being mined until the transaction incurs the maximum amount of slippage.
> 
> The lack of deadline means that the tx can be withheld indefinitely at the advantage of the miner.
> 
> For those reasons I agree with Medium Severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-canto-v2
- **GitHub**: https://github.com/code-423n4/2022-06-NewBlockchain-v2-findings/issues/90
- **Contest**: https://code4rena.com/reports/2022-06-canto-v2

### Keywords for Search

`vulnerability`

