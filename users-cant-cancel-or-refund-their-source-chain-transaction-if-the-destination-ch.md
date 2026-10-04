---
# Core Classification
protocol: Linea
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33300
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
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
  - Dacian
---

## Vulnerability Title

Users can't cancel or refund their source chain transaction if the destination chain transaction continually fails, causing loss of bridged funds

### Overview


This bug report is about a messaging service called Linea that allows users to transfer ETH between two different networks. The process involves two transactions, and if the second one fails, the user may lose their funds with no way of retrieving them. The report suggests implementing a cancellation or refund feature to mitigate this issue. Linea has acknowledged the problem and may consider adding this feature in the future.

### Original Finding Content

**Description:** Linea's messaging service allows users to bridge ETH between Ethereum L1 mainnet and Linea L2.

The bridging process operates in 2 distinct transactions where the first can succeed and the second can fail completely independently of each other.

In the first step of the bridging process on the source chain the user supplies their ETH to the messaging service contract on that chain together with some parameters.

In the last step of the bridging process on the destination chain a delivery service ("postman") or the user themselves calls `claimMessage` or `claimMessageWithProof` to complete the bridging process.

The last step of claiming the message is an arbitrary [call](https://github.com/Consensys/zkevm-monorepo/blob/364b64d2a2704567adac00e3fa428a1901717666/contracts/contracts/messageService/l1/L1MessageService.sol#L144-L154) with arbitrary calldata made to an address of the user's choosing. If this call fails for any reason the user may re-try claiming the message an infinite number of times. However if this call continues to revert (or if the `claim` transaction continually reverts for any other reason), the user:
* will never receive their bridged ETH on the destination chain
* has no way of initiating a cancel or refund transaction on the source chain

**Impact:** This scenario will result in a loss of bridged funds to the user.

**Recommended Mitigation:** Implement a cancel or refund mechanism that users can initiate on the source chain to retrieve their funds if the claim transaction continually reverts on the destination chain.

**Linea:**
Acknowledged. Currently there is no cancellation or refund feature but users can re-try the destination chain delivery as many times as they like. We may consider implementing this in the future.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Linea |
| Report Date | N/A |
| Finders | Dacian |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

