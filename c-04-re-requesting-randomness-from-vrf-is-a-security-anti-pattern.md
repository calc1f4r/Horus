---
# Core Classification
protocol: Bearcave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20532
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-03-01-BearCave.md
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
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[C-04] Re-requesting randomness from VRF is a security anti-pattern

### Overview


This bug report is about the `forceHoneyJarSearch` method used in VRF (Verifiable Random Function) service provider. This method allows the service provider to "kick off another VRF request". This goes against the security standards in using VRF, as it is easily detectable on-chain and can be exploited. The impact of this bug is high, as the VRF service provider has control over who wins the game, and the likelihood is also high, as there is an incentive for a VRF provider to exploit this and it is not hard to do from his side. The recommendation for this bug is to remove the `forceHoneyJarSearch` method as it is exploitable.

### Original Finding Content

**Impact:**
High, as the VRF service provider has control over who wins the game

**Likelihood:**
High, as there is an incentive for a VRF provider to exploit this and it is not hard to do from his side

**Description**

The `forceHoneyJarSearch` method is used to "kick off another VRF request", as mentioned in its NatSpec. This goes against the security standards in using VRF, as stated in the [docs](https://docs.chain.link/vrf/v2/security#do-not-re-request-randomness):

```
Re-requesting randomness is easily detectable on-chain and should be avoided for use cases that want to be considered as using VRFv2 correctly.
```

Basically, the service provider can withhold a VRF fulfillment until a new request that is favorable for them comes.

**Recommendations**

Remove the `forceHoneyJarSearch` method as it is exploitable.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Bearcave |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-03-01-BearCave.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

