---
# Core Classification
protocol: Coinbase Verified Pools
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41969
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Coinbase-Verified-Pools-Spearbit-Security-Review-September-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Coinbase-Verified-Pools-Spearbit-Security-Review-September-2024.pdf
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
finders_count: 4
finders:
  - Christoph Michel
  - Phaze
  - 0xDjango
  - Noah Marconi
---

## Vulnerability Title

Verified smart wallet accounts can be used as proxies to facilitate swaps

### Overview


This bug report discusses a potential issue with a smart contract wallet called VerifiedPoolsBasicHook.sol. This wallet allows for interactions with Coinbase's verified pools, which can be used for swaps and creating wrapper contracts. However, there is a risk that these wallets could be used to bypass Coinbase's policies and perform unauthorized exchanges, potentially with sanctioned funds. The impact of this bug is high and the likelihood is low to medium. The recommendation is to restrict which smart contract wallets can receive attestations or to ensure that this type of activity is in violation of Coinbase's Terms of Service. Both Coinbase and Spearbit have acknowledged the issue. 

### Original Finding Content

Severity: Medium Risk
Context: VerifiedPoolsBasicHook.sol#L260-L344
Description: Smart contract wallets such as ERC-4337 contracts can receive attestations which allow interacting
with Coinbase's verified pools. These wallets can be used as proxies executing swaps and creating wrapper
contracts for managed positions.
Even if these wallets do not contain logic allowing arbitrary actors to bypass Coinbase's policies at the time of the
attestation issuance, the required logic can be included at a later time as these are often upgradeable and include
delegatecall functionality.
Impact: High: This scenario allows swaps to be performed by sanctioned entities bypassing the sanctions list and
KYC verification. The verified contract does not require any upfront capital and is able to profit from this exchange.
Likelihood: Low/Medium: This requires a KYC verified user to violate Coinbase's ToS and to potentially interact
with sanctioned funds. This exchange can be performed permissionlessly allowing any entity to perform swaps
immediately. Wrapper contracts for liquidity positions only work until the attestation is revoked.
Recommendation: Consider only allowing a certain set of smart contract wallets to receive attestations. Other-
wise ensure that such a service is in clear violation of the ToS.
Coinbase: Acknowledging the potential issue and noting that this would be a clear violation of our Terms of Service
by the user.
Spearbit: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Coinbase Verified Pools |
| Report Date | N/A |
| Finders | Christoph Michel, Phaze, 0xDjango, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Coinbase-Verified-Pools-Spearbit-Security-Review-September-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Coinbase-Verified-Pools-Spearbit-Security-Review-September-2024.pdf

### Keywords for Search

`vulnerability`

