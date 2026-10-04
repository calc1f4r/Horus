---
# Core Classification
protocol: Tradable
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44919
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-09-01-Tradable.md
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
  - Zokyo
---

## Vulnerability Title

Lack of proper integration with Gelato relay

### Overview


The report states that there is a bug in the protocol that uses Gelato for gasless transactions. This means that users can send transactions without having a balance of the native token. However, with off-chain relaying, the user who initiates the transaction is no longer recognized. This creates a problem because the target smart contract needs to verify the origin of the message and ensure that it was forwarded by the designated relayer. To solve this issue, Gelato suggests using an ERC-2771 compliant contract that encodes data to relay the original msgSender. However, the TradableSideVault contract does not have this compatibility, making any function with the onlyGelatoRelay modifier unusable. This is because the _msgSender() function returns the address of the relayer instead of the original user. The recommendation is to implement Gelato's ERC-2771 compliant logic and follow security best practices.

### Original Finding Content

**Severity**: High

**Status**:  Resolved

**Description**

The protocol employs Gelato for gasless transactions, enabling users to send transactions without a native token balance. However, with off-chain relaying, msg.sender no longer denotes the user initiating the transaction. When relaying a message to a target smart contract function, it becomes crucial for the function to authenticate the origin of the message and verify that it was correctly forwarded by the designated relayer. To address this challenge, Gelato recommends the utilization of an ERC-2771 compliant contract. This type of contract implements data encoding to relay the original _msgSender from off-chain, ensuring that only the trusted forwarder is able to encode this value. However, the TradableSideVault contract uses GelatoRelayContext, which lacks ERC-2771 compatibility. As a result, any function with the onlyGelatoRelay modifier becomes unusable. The use of the _msgSender() function originates from the Context.sol contract which solely returns the msg.sender value. In the situation where a transaction is initiated through the Gelato relayer, invoking `_msgSender()` will yield the address used by the relayer to forward the transaction, rather than the original user’s address.

**Recommendation**: 

Implement the Gelato’s ERC-2771 complaint logic and follow the security best practices.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Tradable |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-09-01-Tradable.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

