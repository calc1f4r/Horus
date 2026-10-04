---
# Core Classification
protocol: SEDA Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55234
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/729
source_link: none
github_link: https://github.com/sherlock-audit/2024-12-seda-protocol-judging/issues/222

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - x0lohaclohell
---

## Vulnerability Title

H-7: Use of Vulnerable IBC-Go v8.4.0 - Non-Deterministic JSON Unmarshalling Can Cause Chain Halt

### Overview


This bug report discusses a critical vulnerability found in the IBC-Go v8.4.0 protocol, which is being used by the Seda protocol. The vulnerability, identified by user x0lohaclohell, can cause non-deterministic behavior and potentially halt the chain if an attacker sends a specially crafted acknowledgement packet through an IBC channel. This poses a high security risk as any user with permission to open an IBC channel can exploit the vulnerability. The root cause of the issue is the usage of the vulnerable IBC-Go v8.4.0. The recommended mitigation is to upgrade to the latest patched version, v8.6.1. The protocol team has already fixed this issue in their code.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-12-seda-protocol-judging/issues/222 

## Found by 
x0lohaclohell

### Summary

The protocol is using IBC-Go v8.4.0, which contains a critical vulnerability ([ASA-2025-004](https://github.com/cosmos/ibc-go/security/advisories/GHSA-jg6f-48ff-5xrw)) in the deserialization of IBC acknowledgements. This flaw results in non-deterministic behavior, which can lead to a chain halt if an attacker opens an IBC channel and sends a specially crafted acknowledgement packet.

Since any user with permission to open an IBC channel can exploit this issue, the vulnerability has an almost certain likelihood of occurrence, making it a critical security risk.

### Root Cause

Usage of [IBC-Go v8.4.0](https://github.com/sherlock-audit/2024-12-seda-protocol/blob/051b5e88a2f530792913910ebf98c50f431b1e3b/seda-chain/go.mod#L32), 

### Impact

An attacker can halt the chain by introducing a malformed acknowledgement packet.


### Mitigation

Upgrade to the latest patched version of IBC-Go: v8.6.1 

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/sedaprotocol/seda-chain/pull/523

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | SEDA Protocol |
| Report Date | N/A |
| Finders | x0lohaclohell |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-12-seda-protocol-judging/issues/222
- **Contest**: https://app.sherlock.xyz/audits/contests/729

### Keywords for Search

`vulnerability`

