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
solodit_id: 55544
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

Hardcoded `extraArgs` violates CCIP best practices

### Overview

See description below for full details.

### Original Finding Content

**Description:** When sending cross-chain messages via CCIP, Chainlink recommends keeping the `extraArgs` parameter mutable to allow for future upgrades or configuration changes, as outlined in their [best practices](https://docs.chain.link/ccip/best-practices#using-extraargs).

However, this recommendation is not followed in [`BridgeCCIP::send`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/ccip/BridgeCCIP.sol#L126-L133), where `extraArgs` is hardcoded:
```solidity
// Sends the message to the destination endpoint
Client.EVM2AnyMessage memory evm2AnyMessage = Client.EVM2AnyMessage({
    receiver: abi.encode(_receiver), // ABI-encoded receiver address
    data: abi.encode(_encodedMessage), // ABI-encoded string
    tokenAmounts: new Client.EVMTokenAmount[](0), // Empty array indicating no tokens are being sent
    // @audit-issue `extraArgs` hardcoded
    extraArgs: Client._argsToBytes(Client.EVMExtraArgsV2({ gasLimit: 200_000, allowOutOfOrderExecution: true })),
    feeToken: address(0) // For msg.value
});
```

**Impact:** Because `extraArgs` is hardcoded, any future changes would require deploying a new version of the bridge contract.

**Recommended Mitigation:** Consider making `extraArgs` mutable by either passing it as a parameter to the `send` function or deriving it from configurable contract storage.

**YieldFi:** Fixed in commits [`3cc0b23`](https://github.com/YieldFiLabs/contracts/commit/3cc0b2331c35327a43e95176ce6c5578f145c0ee) and [`fd4b7ab5`](https://github.com/YieldFiLabs/contracts/commit/fd4b7ab57a5ae2ac366b4d9d086eb372defc7f8c)

**Cyfrin:** Verified. `extraArgs` is now passed as a parameter to the call.

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

