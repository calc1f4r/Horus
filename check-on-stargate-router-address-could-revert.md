---
# Core Classification
protocol: Sushi
chain: everychain
category: uncategorized
vulnerability_type: layerzero

# Attack Vector Details
attack_type: layerzero
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19622
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/sushi/sushi-swap-stable-pool/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/sushi/sushi-swap-stable-pool/review.pdf
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
  - layerzero

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Check on Stargate Router Address Could Revert

### Overview


This bug report outlines a potential issue with the Stargate tosgReceive() call, which could cause tokens transferred from Stargate to be left in the SushiXSwap contract on the destination chain. This would happen if the Stargate router is redeployed, which is difficult to estimate the likelihood of. To prevent a loss of user funds, the require on line 80 could be removed, or the contract could be monitored for any chance that the router addresses could change and redeployed if necessary.

### Original Finding Content

## Description

The development team pointed out that, if the call by Stargate to `sgReceive()` were to revert, the tokens transferred from Stargate would be left in the SushiXSwap contract on the destination chain, where they could be transferred away freely by any user.

One possible condition under which this transaction could revert is if the Stargate router is redeployed, perhaps as part of an upgrade. The `require` on line [80] would then cause the transaction to revert, resulting in a loss of funds. It is difficult to estimate the likelihood of this issue as it is outside the scope of this review to investigate Stargate’s likelihood of redeploying their router. However, whatever their stated policy, there could still be a redeployment and so a risk remains that could result in a loss of user funds.

## Recommendations

One possible solution is to remove the `require` on line [80]. This is discussed in more detail in SXS-13. Alternatively, monitor Stargate carefully for any chance that any of their router addresses could change and redeploy this contract if that occurs.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Sushi |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/sushi/sushi-swap-stable-pool/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/sushi/sushi-swap-stable-pool/review.pdf

### Keywords for Search

`LayerZero`

