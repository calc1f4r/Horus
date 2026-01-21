---
# Core Classification
protocol: Sablier
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54676
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/5febedab-9e34-4943-bdd3-891559384740
source_link: https://cdn.cantina.xyz/reports/cantina_sablier_jul2023.pdf
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
finders_count: 2
finders:
  - Zach Obront
  - RustyRabbit
---

## Vulnerability Title

Plugin or target with selfdestruct 

### Overview


This bug report describes an issue with the `delegatecall` function in a proxy contract. Before the upcoming 'Cancun' upgrade, if a `delegatecall` was made to a target contract or plugin that had a `SELFDESTRUCT` call, the proxy would be destroyed and the ETH in the proxy would be sent to the designated address. This created a problem because the current owner of the proxy could not create a new proxy as the registry's mapping still pointed to the destroyed proxy address. After the upgrade, the `SELFDESTRUCT` opcode will not destroy the proxy contract, but the ETH will still be sent to the designated address. This could potentially be an issue if the owner of the proxy calls a contract that has a `SELFDESTRUCT` call. The report recommends that target and plugin contracts be thoroughly vetted before being used and suggests the use of an optional allow list of audited target contracts during proxy creation. However, this may go against the intended purpose of the proxy, which is to allow for arbitrary computations. Due to the difficulty in detecting `SELFDESTRUCT` calls, the report has been marked as "Acknowledged".

### Original Finding Content

## Context: General

## Description
Until the 'Cancun' upgrade scheduled for later this year, whenever a `delegatecall` is made to a target contract or plugin that would do a `SELFDESTRUCT`, the proxy would be destroyed at the end of the transaction and all ETH in the proxy would be sent to the address designated in the `SELFDESTRUCT` call. This would obviously be problematic but would also mean that the current owner of the proxy could not create a new proxy as the registry's proxies mapping for the user still points to the destroyed proxy address.

After the upgrade, the `SELFDESTRUCT` opcode will not destroy the proxy contract but still send the ETH to the designated address. Although target and plugin contracts are gated by the plugins and permissions access control mechanisms, it is still possible for an owner to unsuspectedly call a contract that self-destructs.

## Recommendation
There's no easy way to detect whether a `SELFDESTRUCT` has been called in the `delegatecall`, but this does emphasize the need to assure target and plugin contracts are well vetted before being used. An optional (specified during the proxy's creation) allow list with audited target contracts could be used to aid in this assurance.

## Sablier
Providing an allowlist of target contracts at deployment time would run counter to the intended computational universality of the proxy. The proxy owner should retain the ability to call any arbitrary computation performed in any target and any plugin (at their own risk).

Given the above, Cancun's imminence, and that it is very difficult (or impossible) to detect `SELFDESTRUCT`, we will mark this finding as "Acknowledged".

## Cantina
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Sablier |
| Report Date | N/A |
| Finders | Zach Obront, RustyRabbit |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_sablier_jul2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/5febedab-9e34-4943-bdd3-891559384740

### Keywords for Search

`vulnerability`

