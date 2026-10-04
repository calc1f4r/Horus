---
# Core Classification
protocol: Epoch Island - LP Pool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60101
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/epoch-island-lp-pool/64638fd7-bde9-4af9-94ec-451c45faad3c/index.html
source_link: https://certificate.quantstamp.com/full/epoch-island-lp-pool/64638fd7-bde9-4af9-94ec-451c45faad3c/index.html
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
  - Poming Lee
  - Roman Rohleder
  - Adrian Koegl
---

## Vulnerability Title

Specially designed ERC20 tokens and malicious ERC20 tokens can cause loss of funds

### Overview


This bug report explains that the current protocol does not work well with certain types of ERC20 tokens that have dynamic balance mechanisms. This means that the token balance can change over time, which goes against the protocol's assumption of static balances. This could lead to incorrect calculations or unintended consequences in the contract. Additionally, the open design of the protocol allows for any ERC20 token to be used, which could potentially introduce malicious tokens that exploit the contract or deceive users. The report recommends implementing a whitelist of approved tokens to prevent these issues.

### Original Finding Content

**Update**
The client provided the following explanation:

> These contracts are not designed to be used with tokens that rebase or change balance over time. There will be a whitelist of tokens implemented on the frontend which enables certain verified tokens to be used with the contract.

**File(s) affected:**`EpochUpsidePoolV1.sol`

**Description:** The protocol's current architecture does not account for the unique behaviors of various specialized ERC20 tokens, including interest-bearing, deflationary, and rebasing tokens. These tokens are characterized by their dynamic balance mechanisms, where the token balance can autonomously change over time due to factors like transaction fees, re-distribution, or balance adjustments. This aspect contradicts the protocol's underlying assumption of static token balances, potentially leading to inaccurate calculations or unintended interactions within the contract.

Additionally, the protocol's open design, which allows liquidity providers (LPs) to utilize any ERC20 token, poses a significant risk. This unrestricted approach could enable LPs to introduce malicious tokens, crafted specifically to exploit the contract's mechanics or defraud takers. Such tokens might be engineered to perform a rug-pull – abruptly devaluing or making the tokens non-transferable after a transaction – or to otherwise deceive and manipulate the takers. This vulnerability necessitates a more stringent approach to token vetting and validation within the contract, to safeguard against these deceptive strategies and ensure the integrity of transactions.

**Recommendation:** Consider a well-formulated whitelisting mechanism and carefully permit tokens.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Epoch Island - LP Pool |
| Report Date | N/A |
| Finders | Poming Lee, Roman Rohleder, Adrian Koegl |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/epoch-island-lp-pool/64638fd7-bde9-4af9-94ec-451c45faad3c/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/epoch-island-lp-pool/64638fd7-bde9-4af9-94ec-451c45faad3c/index.html

### Keywords for Search

`vulnerability`

