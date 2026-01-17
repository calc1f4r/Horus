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
solodit_id: 17688
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf
github_link: none

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
finders_count: 3
finders:
  - Troy Sargent
  - Anish Naik
  - Nat Chin
---

## Vulnerability Title

The relayer is a single point of failure

### Overview


This bug report is about CrosslayerPortal, a centralized service that is responsible for critical functionalities in the Mosaic ecosystem. The service is responsible for managing withdrawals and transfers across chains, executing cross-chain message calls, collecting fees, and refunding fees in case of failed transfers or withdrawals. Because it is centralized, it is more vulnerable to attack, and an attacker gaining root access to the server can shut down the system or cause funds to be drained. To address this, it is recommended that an incident response plan is documented and exposed ports and services are monitored. In the long term, an external security audit of the source code and a decentralized relayer architecture should be considered.

### Original Finding Content

## Difficulty: Low

## Type: Patching

### Target: CrosslayerPortal

## Description
Because the relayer is a centralized service that is responsible for critical functionalities, it constitutes a single point of failure within the Mosaic ecosystem. The relayer is responsible for the following tasks:

- Managing withdrawals across chains
- Managing transfers across chains
- Managing the accrued interest on all users’ investments
- Executing cross-chain message call requests
- Collecting fees for all withdrawals, transfers, and cross-chain message calls
- Refunding fees in case of failed transfers or withdrawals

The centralized design and importance of the relayer increase the likelihood that the relayer will be targeted by an attacker.

## Exploit Scenario
Eve, an attacker, is able to gain root access on the server that runs the relayer. Eve can then shut down the Mosaic system by stopping the relayer service. Eve can also change the source code to trigger behavior that can lead to the drainage of funds.

## Recommendations
- **Short term:** Document an incident response plan and monitor exposed ports and services that may be vulnerable to exploitation.
- **Long term:** Arrange an external security audit of the core and peripheral relayer source code. Additionally, consider implementing a decentralized relayer architecture more resistant to system takeovers.

## Trail of Bits
Advanced Blockchain Security Assessment  
PUBLIC

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

