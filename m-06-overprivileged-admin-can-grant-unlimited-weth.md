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
solodit_id: 25231
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-canto
source_link: https://code4rena.com/reports/2022-06-canto
github_link: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/241

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

[M-06] Overprivileged admin can grant unlimited WETH

### Overview


A bug was discovered in the Comptroller smart contract of the lending-market project. If the admin key gets compromised, the attacker can use the `_grantComp()` function to immediately drain all the assets from the contract to their address without any timelock, amount boundaries, or address limitations. The team Watchpug previously reported this issue and the team Canto acknowledged it, but felt that changing the core functionality of compound would be too costly. The judge then decreased the severity of the issue to Medium. 

To mitigate this issue, the team should consider implementing a timelock for the `_grantComp()` function, a hard-coded recipient to prevent funds from being sent to any address, and a limit to the amount that can be granted.

### Original Finding Content

_Submitted by hake_

<https://github.com/Plex-Engineer/lending-market/blob/755424c1f9ab3f9f0408443e6606f94e4f08a990/contracts/Comptroller.sol#L1376><br>

Admin can `_grantComp()` to any address using any amount and drain the contract.

### Proof of Concept

If admin key gets compromised there is no timelock, no amount boundaries and no address limitations to prevent the assets to be drained immediately to the attacker's address.

### Recommended Mitigation Steps

There is a few suggestions that could help mitigate this issue:<br>
Implement timelock for `_grantComp()`<br>
Implement hard coded recipient so funds cannot be arbitrarily sent to any address.<br>
Implement a limit to the amount that can be granted.<br>

Here is a reference to a past submission where this issue has been made by team Watchpug: <https://github.com/code-423n4/2022-01-insure-findings/issues/271>

**[nivasan1 (Canto) acknowledged and commented](https://github.com/code-423n4/2022-06-canto-findings/issues/241#issuecomment-1163850385):**
 > We acknowledge that this is an issue, however we feel that changing the core functionality of compound would be too costly.

**[Alex the Entreprenerd (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-06-canto-findings/issues/241#issuecomment-1211287073):**
 > The warden has shown how the Admin could sweep the reward token(in this case WETH) to any address, at any time, for an amount equal to all tokens available to the Comptroller.
> 
> Because this is contingent on admin privilege, I think Medium Severity to be more appropriate.



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

- **Source**: https://code4rena.com/reports/2022-06-canto
- **GitHub**: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/241
- **Contest**: https://code4rena.com/reports/2022-06-canto

### Keywords for Search

`vulnerability`

