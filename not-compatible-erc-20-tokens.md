---
# Core Classification
protocol: Mantle Network (Bridge Contracts)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60554
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/mantle-network-bridge-contracts/b3babf24-0c57-449a-bc29-8133c665734a/index.html
source_link: https://certificate.quantstamp.com/full/mantle-network-bridge-contracts/b3babf24-0c57-449a-bc29-8133c665734a/index.html
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
finders_count: 4
finders:
  - Mustafa Hasan
  - Roman Rohleder
  - Julio Aguliar
  - Guillermo Escobero
---

## Vulnerability Title

Not Compatible ERC-20 Tokens

### Overview


This bug report is about a problem with the accounting approach for deposits and burning/minting operations in two files called `L1StandardBridge.sol` and `L2StandardBridge.sol`. The issue affects certain ERC-20 tokens that have specific characteristics such as transfer fees, deflationary/inflationary behavior, or blocklists. Currently, users can deploy any token in L2 and link it to an L1 token, but this can lead to issues and block user funds in `L1StandardBridge.sol`. The report recommends informing users of this risk and implementing a token allowlist to prevent these issues.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> Token transfers through the official canonical bridge require registration through our token list.

**File(s) affected:**`L1StandardBridge.sol`, `L2StandardBridge.sol`

**Description:** The accounting approach for deposits in `L1StandardBridge.sol` and burning and minting operations in `L2StandardBridge.sol` are not compatible with ERC-20 tokens that (but not limited to):

*   Have a transfer, minting, or burning fee
*   Are deflationary/inflationary (i.e. the balance of an account can change "arbitrarily", without a transfer operation)
*   Its L2 version unexpectedly reverts when minting, burning, or transferring
*   Its L2 version does not implement minting and burning operations properly (e.g. mints or burns more or fewer tokens than expected, leading to duplicate funds or issues when withdrawing from L2)
*   Implement blocklists

Currently, the system allows anyone to deploy a compatible token in L2 and link it to an L1 token. Users are responsible for ensuring that the ERC-20 L2 token is correct and that its behavior is not in the abovementioned list. **Interacting with a non-compatible token will block user funds in `L1StandardBridge.sol`.**

**Recommendation:**

1.   Users should be informed of this risk when interacting with the smart contracts directly ([Optimism Documentation](https://community.optimism.io/docs/developers/bridge/standard-bridge/#depositing-erc20s)). If a user interface is expected to be the main access to the system, the available tokens should be verified by the Mantle team. We strongly recommend showing an alert when interacting with non-verified (and potentially non-compatible) tokens.
2.   Consider implementing a token allowlist and only including tokens validated by the Mantle team.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Mantle Network (Bridge Contracts) |
| Report Date | N/A |
| Finders | Mustafa Hasan, Roman Rohleder, Julio Aguliar, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/mantle-network-bridge-contracts/b3babf24-0c57-449a-bc29-8133c665734a/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/mantle-network-bridge-contracts/b3babf24-0c57-449a-bc29-8133c665734a/index.html

### Keywords for Search

`vulnerability`

