---
# Core Classification
protocol: Gro Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 411
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-gro-protocol-contest
source_link: https://code4rena.com/reports/2021-06-gro
github_link: https://github.com/code-423n4/2021-06-gro-findings/issues/51

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xRajeev
  - pauliax
---

## Vulnerability Title

[M-02] Safe addresses can only be added but not removed

### Overview


This bug report details a vulnerability in the addSafeAddress() function of a smart contract. This function takes an address and adds it to a “safe list" which is used in eoaOnly() to give exemption to safe addresses that are trusted smart contracts. This means that if an address is added to the safe list, it cannot be removed and the protocol cannot prevent flash loan manipulations from that source. The bug report includes a proof of concept, which consists of links to the relevant code, and a recommended mitigation step, which is to change addSafeAddress() to isSafeAddress() and add an additional bool parameter to allow both enabling/disabling of safe addresses.

### Original Finding Content

_Submitted by 0xRajeev, also found by pauliax_


The `addSafeAddress()`  takes an address and adds it to a “safe list". This is used in `eoaOnly()` to give exemption to safe addresses that are trusted smart contracts, when all other smart contacts are prevented from protocol interaction. The stated purpose is to allow only such partner/trusted smart contract integrations (project rep mentioned Argent wallet as the only one for now but that may change) an exemption from potential flash loan threats. But if there is a safe listed integration that needs to be later disabled, it cannot be done. The protocol will have to rely on other measures (outside the scope of this contest) to prevent flash loan manipulations which are specified as an area of critical concern.

**Scenario:** A trusted integration/partner address is added to the safe list. But that wallet/protocol/DApp is later manipulated (by the project, its users or an attacker) to somehow launch a flash loan attack on the protocol. However, its address cannot be removed from the safe list and the protocol cannot prevent flash loan manipulations from that source because of its exemption. Contract/project will have to be redeployed.

Recommend changing `addSafeAddress()` to `isSafeAddress()` with an additional bool parameter to allow both the enabling _AND_ disabling of safe addresses.

**[kristian-gro (Gro) confirmed but disagreed with severity](https://github.com/code-423n4/2021-06-gro-findings/issues/51#issuecomment-880043980):**
> low risk - Made specifically for one partner in beta period, and planned to be removed. We added the removal function for sanity.
> 
> Confirmed and Fix has been implemented in release version.

**[ghoul-sol (Judge) commented](https://github.com/code-423n4/2021-06-gro-findings/issues/51#issuecomment-886327301):**
 > I'll keep medium risk because this could put the protocol into a one way street and not being able to remove safe addresses is quite dangerous. Medium risk.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Gro Protocol |
| Report Date | N/A |
| Finders | 0xRajeev, pauliax |

### Source Links

- **Source**: https://code4rena.com/reports/2021-06-gro
- **GitHub**: https://github.com/code-423n4/2021-06-gro-findings/issues/51
- **Contest**: https://code4rena.com/contests/2021-07-gro-protocol-contest

### Keywords for Search

`vulnerability`

