---
# Core Classification
protocol: Hinkal Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60155
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/hinkal-protocol/66b9b783-8b42-4a4e-89ed-3ef2a2df5958/index.html
source_link: https://certificate.quantstamp.com/full/hinkal-protocol/66b9b783-8b42-4a4e-89ed-3ef2a2df5958/index.html
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
finders_count: 7
finders:
  - Shih-Hung Wang
  - Ibrahim Abouzied
  - Jan Gorzny
  - Martin Derka
  - Ruben Koch
---

## Vulnerability Title

Gas Griefing Attacks on the Relayers

### Overview


The client has marked the issue as "Acknowledged" and explained that it is the desired behavior for users to be able to use hooks before or after token exchanges. However, this can lead to problems with relayer fees not properly reflecting the gas usage of the transaction. This is because users can specify their own hook contracts and potentially use a large amount of gas, causing the relayer to spend more gas than they receive in fees. It is recommended that the Hinkal team limit the capabilities of user-specified hooks to reduce the risk of attacks. This could include limiting on-chain gas usage or implementing a way to charge gas fees from users. It is also suggested to add a whitelisting mechanism for addresses allowed to be used for pre and post-hook transactions. Off-chain measures may only partially mitigate this issue as the behavior of hook contracts can differ between off-chain simulation and on-chain execution. 

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> This is desired behavior - user should be free to do after/pre hooks.

**File(s) affected:**`Hinkal.sol`

**Description:** Relayer fees are calculated by a percentage of the exchanged token amount without considering the actual gas usage of the transaction. When making a `transact()` call on Hinkal, users can specify hook contracts, which `Hinkal` will call specific functions on them before or after the token exchange. A user may specify their hook contracts and spend a large amount of gas during the hook function calls, theoretically up to the block gas limit. As a result, the relayer may spend a large amount of gas executing the user's transaction but does not receive enough fees in return.

The support of user-specified hooks means external calls can be performed to arbitrary addresses for each transaction. This can result in unexpected behavior, like the aforementioned gas griefing. We advise the Hinkal team to limit such capabilities to reduce the attack surface of the protocol.

**Recommendation:** Confirm whether this is an intended or acceptable result. If not, consider limiting the on-chain gas usage or implementing a way to charge gas fees from users.

Notice that off-chain measures, e.g., estimating the gas usage off-chain, could only partially mitigate this issue since the user's hook contracts may behave differently between the off-chain simulation and on-chain execution.

Consider adding a whitelisting mechanism for addresses allowed to be used for pre and post-hook transactions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Hinkal Protocol |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Ibrahim Abouzied, Jan Gorzny, Martin Derka, Ruben Koch, Valerian Callens, Fatemeh Heidari |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/hinkal-protocol/66b9b783-8b42-4a4e-89ed-3ef2a2df5958/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/hinkal-protocol/66b9b783-8b42-4a4e-89ed-3ef2a2df5958/index.html

### Keywords for Search

`vulnerability`

