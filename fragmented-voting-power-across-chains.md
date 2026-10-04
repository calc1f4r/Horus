---
# Core Classification
protocol: Shape Token Contract
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62721
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-shapenetwork-token-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-shapenetwork-token-securityreview.pdf
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
finders_count: 1
finders:
  - Quan Nguyen Trail of Bits PUBLIC
---

## Vulnerability Title

Fragmented voting power across chains

### Overview


This bug report discusses a problem with the governance system of the $SHAPE token. The token is designed to be able to move across different chains in the Superchain ecosystem, but when it is moved to follower chains, its voting power is not properly accounted for. This means that decisions can be made by a minority of token holders, undermining the democratic principles of the governance system. A malicious actor could take advantage of this by timing a proposal when a significant portion of tokens have been moved to other networks, allowing them to pass a harmful proposal with only a small portion of the total token supply. The report recommends adding warnings about this issue in the user interface and documentation, and redesigning the governance mechanism in the long term to account for tokens across all chains.

### Original Finding Content

## Difficulty: High

## Type: Data Validation

### Description
The governance mechanism of the $SHAPE token fails to account for tokens bridged to follower chains, resulting in inaccurate voting power distribution and potential governance manipulation.

The Superchain ERC-20 implementation allows $SHAPE tokens to be transferred across multiple chains in the Superchain ecosystem while maintaining their financial fungibility. When tokens are bridged from the leader chain to follower chains, the bridge mechanism mints equivalent tokens on the destination chain while burning them on the source chain. However, the current implementation only considers token balances on the leader chain when calculating voting power for governance decisions. This creates a disconnect between the total token supply and actual governance representation, as tokens on follower chains maintain their financial utility but lose their governance rights. Consequently, governance decisions can be made by a minority of token holders who keep their tokens on the leader chain, undermining the democratic principles of the governance system.

### Exploit Scenario
A malicious actor could monitor the distribution of $SHAPE tokens across chains and strategically time a governance proposal when a significant portion of tokens have been bridged to follower chains. For example, if 60% of the total token supply is bridged to other networks for DeFi activities, the attacker could pass a harmful proposal with only 21% of the total token supply (becoming a majority of the 40% remaining on the leader chain). This allows for governance capture with a minority position of the total token supply.

### Recommendations
- **Short term:** Add clear warnings in the UI and documentation about the governance implications of bridging tokens away from the leader chain.
- **Long term:** Redesign the governance mechanism to account for token balances across all chains in the Superchain ecosystem.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Shape Token Contract |
| Report Date | N/A |
| Finders | Quan Nguyen Trail of Bits PUBLIC |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-shapenetwork-token-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-shapenetwork-token-securityreview.pdf

### Keywords for Search

`vulnerability`

