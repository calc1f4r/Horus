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
solodit_id: 6139
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-vetoken-finance-contest
source_link: https://code4rena.com/reports/2022-05-vetoken
github_link: https://github.com/code-423n4/2022-05-vetoken-findings/issues/233

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
  - shenwilly
---

## Vulnerability Title

[M-18] Governance can arbitrarily burn VeToken from any address

### Overview


This bug report is about the governance token VeToken.sol, which has a risky burn function that allows governance to burn any amount of VeToken from any address. This is a security risk as it could be exploited by malicious or compromised governance, resulting in users losing their tokens. The recommended mitigation step is to either remove the function or modify the burn function so that only the sender can burn the token.

### Original Finding Content

_Submitted by shenwilly_

Governance can burn any amount of `VeToken` from any address.

Unlike `VE3Token` which is minted when users deposit veAsset and burned when users withdraw, the `burn` function in the governance token `VeToken.sol` is unnecessary and open up the risk of malicious/compromised governance burning user's token.

### Recommended Mitigation Steps

Consider removing the function, or modify the burn function so it only allows `msg.sender` to burn the token:

    function burn(uint256 _amount) external {
        _burn(msg.sender, _amount);
    }

**[solvetony (veToken Finance) acknowledged and commented](https://github.com/code-423n4/2022-05-vetoken-findings/issues/233#issuecomment-1156744206):**
 > We might update readme on that case.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-05-vetoken-findings/issues/233#issuecomment-1193449708):**
 > The warden has shown how the operator, which may be the DAO or a privileged Multisig, can burn any tokens.
> 
> While the functionality is part of the system for VE3Token as the system uses it to track underlying ownership, burning of balances from arbitrary addresses is a dangerous form of admin privilege.
> 
> I'd recommend deleting the burn function.



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
| Finders | shenwilly |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-vetoken
- **GitHub**: https://github.com/code-423n4/2022-05-vetoken-findings/issues/233
- **Contest**: https://code4rena.com/contests/2022-05-vetoken-finance-contest

### Keywords for Search

`vulnerability`

