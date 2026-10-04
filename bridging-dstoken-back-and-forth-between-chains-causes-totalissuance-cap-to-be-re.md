---
# Core Classification
protocol: Securitize Bridge Cctp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64320
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
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
  - MrPotatoMagic
  - Dacian
---

## Vulnerability Title

Bridging `DSToken` back-and-forth between chains causes `totalIssuance` cap to be reached, preventing further issuances and cross-chain transfers

### Overview


The bug report describes an issue with the `StandardToken::totalIssuance` function. This function is supposed to keep track of the total number of tokens ever issued, but it is not properly decreased when tokens are burned. This has consequences for cross-chain bridging using `SecuritizeBridge`, where the `totalIssuance` is increased each time tokens are transferred between chains. This can lead to the cap being hit on one of the chains, causing further issuances and transfers to fail. The report suggests several potential solutions, including having bridging decrement `totalIssuance` on the source chain or modifying the cap check to account for bridged tokens separately. The bug has been fixed by Securitize in their code, and has been verified by Cyfrin.

### Original Finding Content

**Description:** `StandardToken::totalIssuance` is not decreased by burns but is used to enforce maximum cap, since `totalIssuance` is supposed to track the total number of tokens ever issued, not the current "supply".

However there is an interesting consequence to this when considering cross-chain bridging via `SecuritizeBridge`; `receiveWormholeMessages` calls `DSToken::issueTokens` on the destination chain which increases `StandardToken::totalIssuance`.

**Impact:** Consider this scenario:
* Alice bridges from Ethereum -> Arbitrum with 1000 `DSToken`
* Alice bridges back from Arbitrum -> Ethereum with the "same" 1000 `DSToken`
* Alice keeps doing this over and over again

This process continually increases the `totalIssuance` on both chains, even though it is just the same tokens going back and forth; at some point this will cause the cap to be hit on one of the chains. This doesn't even require malicious investors, just investors who bridge back-and-forth frequently.

Once the cap is hit further issuances and cross-chain transfers will revert on that chain.

**Recommended Mitigation:** Potential mitigations include:
* have bridging actually decrement `totalIssuance` on the source chain
* have `SecuritizeBridge::receiveWormholeMessages` call `DSToken::issueTokensCustom` passing a `reason == "BRIDGING"` then  in `TokenLibrary::issueTokensCustom` don't increment `totalIssuance` for `"BRIDGING"` reason
* track the number of bridged tokens separately and modify the cap check to account for this

**Securitize:** Fixed in commit [c2e62c9](https://github.com/securitize-io/dstoken/commit/c2e62c9c1137bb7c6f548b72f960d864c42445fc); the cap was deprecated and associated checks removed. There is a similar compliance-related check that uses `totalSupply` so correctly accounts for burns.

**Cyfrin:** Verified.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Bridge Cctp |
| Report Date | N/A |
| Finders | MrPotatoMagic, Dacian |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

