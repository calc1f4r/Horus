---
# Core Classification
protocol: Advanced Blockchain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17690
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf
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
finders_count: 3
finders:
  - Troy Sargent
  - Anish Naik
  - Nat Chin
---

## Vulnerability Title

DoS risk created by cross-chain message call requests on certain networks

### Overview


This bug report is about a data validation issue in the CrosslayerPortal/contracts/functionCalls/* system. The issue is that if a user sends numerous cross-chain message call requests, the relayer would need to act upon them, even if they are part of a DoS attack. This could prevent other users from interacting with the system. 

The exploit scenario is that Eve creates a theoretically infinite series of transactions on a low-fee, low-latency network. This would fill the internal queue of the relayer with malicious transactions, and Alice would have to wait an undefined amount of time for her transaction to be executed. 

The short-term recommendation is to create multiple queues that work across various chains to mitigate this DoS risk. The long-term recommendation is to analyze the implications of the ability to create numerous message calls on low-fee networks and its impact on relayer performance.

### Original Finding Content

## PUBLIC

## 11. Missing validation in takeFees function

**Difficulty:** Medium

**Type:** Data Validation

**Target:** CrosslayerPortal/contracts/functionCalls/*

### Description
Cross-chain message calls that are requested on a low-fee, low-latency network could facilitate a DoS, preventing other users from interacting with the system. If a user, through the `MsgSender` contract, sent numerous cross-chain message call requests, the relayer would have to act upon the emitted events regardless of whether they were legitimate or part of a DoS attack.

### Exploit Scenario
Eve creates a theoretically infinite series of transactions on Arbitrum, a low-fee, low-latency network. The internal queue of the relayer is then filled with numerous malicious transactions. Alice requests a cross-chain message call; however, because the relayer must handle many of Eve’s transactions first, Alice has to wait an undefined amount of time for her transaction to be executed.

### Recommendations
- **Short term:** Create multiple queues that work across the various chains to mitigate this DoS risk.
- **Long term:** Analyze the implications of the ability to create numerous message calls on low-fee networks and its impact on relayer performance.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Advanced Blockchain |
| Report Date | N/A |
| Finders | Troy Sargent, Anish Naik, Nat Chin |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf

### Keywords for Search

`vulnerability`

