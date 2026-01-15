---
# Core Classification
protocol: Yieldfi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55547
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
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

protocol_categories:
  - yield

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Immeas
  - Jorge
---

## Vulnerability Title

Hardcoded CCIP `feeToken` prevents LINK discount usage

### Overview

See description below for full details.

### Original Finding Content

**Description:** In `BridgeCCIP::send`, the [`feeToken`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/ccip/BridgeCCIP.sol#L126-L133) parameter is hardcoded:
```solidity
// Sends the message to the destination endpoint
Client.EVM2AnyMessage memory evm2AnyMessage = Client.EVM2AnyMessage({
    receiver: abi.encode(_receiver), // ABI-encoded receiver address
    data: abi.encode(_encodedMessage), // ABI-encoded string
    tokenAmounts: new Client.EVMTokenAmount[](0), // Empty array indicating no tokens are being sent
    extraArgs: Client._argsToBytes(Client.EVMExtraArgsV2({ gasLimit: 200_000, allowOutOfOrderExecution: true })),
    // @audit-issue hardcoded fee token
    feeToken: address(0) // For msg.value
});
```

Chainlink CCIP supports paying fees using either the native gas token or `LINK`. By hardcoding `feeToken = address(0)`, the protocol forces all users to pay with the native gas token, removing flexibility.

This design choice simplifies implementation but has cost implications: CCIP offers a [10% fee discount](https://docs.chain.link/ccip/billing#network-fee-table) when using `LINK`, so users holding `LINK` are unable to take advantage of these reduced fees.

**Recommended Mitigation:** Consider allowing users to choose their preferred payment token—either `LINK` or native gas—based on their individual cost and convenience preferences.

**YieldFi:** Fixed in commits [`3cc0b23`](https://github.com/YieldFiLabs/contracts/commit/3cc0b2331c35327a43e95176ce6c5578f145c0ee) and [`e9c160f`](https://github.com/YieldFiLabs/contracts/commit/e9c160fdfd6dd90650c9537fba73c17cb3c53ea5)

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Yieldfi |
| Report Date | N/A |
| Finders | Immeas, Jorge |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

