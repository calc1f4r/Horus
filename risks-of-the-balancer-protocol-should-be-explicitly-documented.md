---
# Core Classification
protocol: Bera Bex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52845
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Bex-Spearbit-Security-Review-September-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Bex-Spearbit-Security-Review-September-2024.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - J4X
  - Xiaoming90
  - 0xIcingdeath
---

## Vulnerability Title

Risks of the Balancer protocol should be explicitly documented

### Overview

See description below for full details.

### Original Finding Content

Severity: Low Risk
Context: Global scope
Description: Due to the high level of complexity that the Vault brings to the system, we recommend documenting
all historical issues that has affected Balancer, to ensure that these issues are adequately mitigated in this Balancer
Fork. An example of such analysis can be seen below.
Issue Affected Pool Description Mitigation
Rate Manipulation (exploited) - Aug 2023 Boosted Pools, Linear Pools Clause in LinearMath that should only be executed on INIT to ensure a non =1 rate was executed, and attacker received heavily discounted funds No mitigation – Linear Pools deprecated
Rate Manipulation < 1 - June 2023 Boosted Pools, Composable Stable Pools Incorrect rounding direction allows an attacker to drop rate down too low for free assets. V5 enforces strict invariant
Read-only reentrancy - Feb 2023 Stable Pool, Phantom Stable, Linear Pool, Composable Stable, Weighted, Managed getRate function minted wrong amounts, which in combination with handleEth tricked the system into giving attacker arbitrary code execution through a callback-type-mechanism
Incorrect Rounding – Oct 2023 Boosted Pool, Linear, Composable Stable Pool Attacker can call swapDecrease multiple times which mistakenly gives users tokens out for free  V5 Composable Stable Pools were paused; Linear Pools could no longer be. Wrapper contracts for tokens were changed to block swaps instead.
Merkle Orchard Duplicate Claims – Feb 2023 Merkle Orchard, Vault An attacker can claim multiple times, which results in the Vault giving user significantly more than expected. Merkle Orchard to be deployed
Privilege Escalation – Dec 2022 AuthorizerAdapter A privilege escalation bug in the authorizer contract allowed callers to perform actions that otherwise should not have been possible. The TimelockAuthorizer contract was updated to fix the canPerform function, but seemingly Balancer v2 only uses the temporary fix still (AdapterWithValidation , Entrypoint , Authorizer – after having checked forks such as Beethoven and others, it seems the new timelock authorizer is not yet in use.*
Double entry point tokens – May 2022 Vault, ProtocolFeeCollector Double entrypoint on SNX or sBTC would calculate the protocol fees incorrectly, resulting in the pool thinking it had more than it did. The leftover fees would be sent to the protocol fee collector. SNX double entry point removed. System documented for double entry point token risks.
Modification of pool parameters – May 2022 Stable Pool Factory, Meta Stable Pool Factory, Stable Phantom Pool, Investment Pool Owners of the 6-11 multisig can change pool parameters in a way that's problematic for the behaviour of the pool.  Due to multisig involvement, this was not fixed.
Once Berachain commences discusses with Balancer Integrations team, the timelock/authorizer contract flows
should be double-checked.
Recommendation: Document all the known issues of the Balancer codebase, including their mitigations and if
Berachain's mitigation differs, how. This should include in-code documentation for all mitigations, as well.
Berachain: Acknowledges the risk.
Spearbit: Client acknowledges the risks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Bera Bex |
| Report Date | N/A |
| Finders | J4X, Xiaoming90, 0xIcingdeath |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Bex-Spearbit-Security-Review-September-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Bex-Spearbit-Security-Review-September-2024.pdf

### Keywords for Search

`vulnerability`

