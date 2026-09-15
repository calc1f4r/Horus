---
# Core Classification
protocol: Dipcoin Perpetual
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64744
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/dipcoin-perpetual/ea7e8c75-4423-49da-a381-1d39997cfff7/index.html
source_link: https://certificate.quantstamp.com/full/dipcoin-perpetual/ea7e8c75-4423-49da-a381-1d39997cfff7/index.html
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
  - Hamed Mohammadi
  - Adrian Koegl
  - Tim Sigl
---

## Vulnerability Title

Missing On-Chain ZK Proof Verification

### Overview


The client has acknowledged a bug in their system that affects the `library.move`, `order.move`, and `isolated_trading.move` files. The bug allows for authentication to be bypassed when the scheme byte is set to `SIGNED_USING_ZK_WALLET (3)`, as the function `library::verify_signature()` does not validate any zkLogin-related proofs or check the corresponding public key. The team recommends either verifying ZK proofs on-chain or clearly documenting that zkLogin security is enforced off-chain and not by the contracts themselves.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> Since we operate as an on-chain/off-chain hybrid system, our off-chain infrastructure requires user trust. Additionally, ZK proof verification exclusively applies to ZKLogin users and does not impact wallet users.

**File(s) affected:**`library.move`, `order.move`, `isolated_trading.move`

**Description:** In `library::verify_signature()`, when the scheme byte equals `SIGNED_USING_ZK_WALLET (3)`, the function sets `is_verified = true` without validating any zkLogin-related proofs or checking whether `public_key` corresponds to the claimed zkLogin identity.

The team indicated that these zkLogin proofs are verified off-chain, but the on-chain contracts do not check that such verification actually happened. As a result, any bug in the off-chain verification pipeline would make the on-chain authentication bypassable, since scheme `3` is accepted unconditionally.

**Recommendation:** For zkLogin / ZK wallets, the strongest option is to verify ZK proofs on-chain. If on-chain verification is not wanted, it should be clearly documented that zkLogin security is enforced entirely by off-chain infrastructure and that the contracts themselves do not verify any zkLogin signatures or proofs.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Dipcoin Perpetual |
| Report Date | N/A |
| Finders | Hamed Mohammadi, Adrian Koegl, Tim Sigl |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/dipcoin-perpetual/ea7e8c75-4423-49da-a381-1d39997cfff7/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/dipcoin-perpetual/ea7e8c75-4423-49da-a381-1d39997cfff7/index.html

### Keywords for Search

`vulnerability`

