---
# Core Classification
protocol: Initia_2025-06-17
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61427
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Initia-security-review_2025-06-17.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] Unvalidated External Image URLs from NFT Metadata

### Overview


The bug report discusses a problem with how NFT image URLs are handled in various components, such as `CollectionDetails.tsx` and `NftDetails.tsx`. These URLs are not being properly validated or sanitized before being rendered, which can lead to potential security issues. An attacker can use this vulnerability to execute cross-site scripting (XSS) attacks, spoof branding or UI, load offensive or phishing content, or exploit cache poisoning. The report recommends enforcing strict validation for external images, hardening rendering components, and strengthening metadata sourcing. This will help prevent potential attacks and improve the security of the code.

### Original Finding Content


## Severity

**Impact:** Medium  

**Likelihood:** Medium

## Description

In multiple components (`CollectionDetails.tsx`, `NftDetails.tsx`, etc.), NFT image URLs sourced from on-chain metadata or third-party APIs are passed directly into rendering components like `<NftThumbnail />` without validation or sanitization.

Example vulnerable code:

```
<NftThumbnail src={nft.image} />
```

This creates a **trust boundary violation**, since NFT images may originate from:

- Untrusted domains or IPFS gateways.
- Inline `data:` URIs (e.g. `data:image/svg+xml`).
- Malformed or malicious payloads (e.g. embedded `<script>` in SVG).

These images ultimately reach shared components such as `Image.tsx`, which may not enforce strict URL validation.

#### Impact
An attacker can:
- Execute **XSS** via malicious SVG or `data:` URIs.
- **Spoof branding** or UI with attacker-controlled images.
- Load **offensive or phishing** content.
- Exploit **cache poisoning** or unexpected proxy behavior.

#### Code Location

[link](https://github.com/initia-labs/widget/blob/c7c7fc23a5d65cafbd8d748711a607abf695052a/packages/widget-react/src/pages/wallet/tabs/nft/CollectionItem.tsx#L24)


## Recommendations

**Enforce strict validation before rendering any external image:**

- Allow only `https:` URLs or trusted `ipfs://` schemes.
- Block `data:`, `javascript:`, and unknown protocols.
- Use a shared utility (e.g. `isSafeImageUrl`) for consistent validation.

**Harden rendering components (`NftThumbnail.tsx`, `Image.tsx`):**

- Add domain allowlists or trusted gateway filters.
- Reject or sanitize inline SVGs and `image/svg+xml` MIME types.
- Apply content-type checks if fetched via proxy.

**Strengthen metadata sourcing:**

- Use trusted NFT registries (e.g. `nft.storage`, `mintscan`).
- Consider signature validation or allowlisting known creators.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Initia_2025-06-17 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Initia-security-review_2025-06-17.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

