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
solodit_id: 55545
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 1.00
financial_impact: low

# Scoring
quality_score: 5
rarity_score: 2

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

Static `gasLimit` will result in overpayment

### Overview

See description below for full details.

### Original Finding Content

**Description:** Since [unspent gas is not refunded](https://docs.chain.link/ccip/best-practices#setting-gaslimit), Chainlink recommends carefully setting the `gasLimit` within the `extraArgs` parameter to avoid overpaying for execution.

In [`BridgeCCIP::send`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/ccip/BridgeCCIP.sol#L131), the `gasLimit` is hardcoded to `200_000`, which is also Chainlink’s default:

```solidity
extraArgs: Client._argsToBytes(Client.EVMExtraArgsV2({ gasLimit: 200_000, allowOutOfOrderExecution: true })),
```

This hardcoded value directly affects every user bridging tokens, as they will be consistently overpaying for execution costs on the destination chain.

**Recommended Mitigation:** A more efficient approach would be to measure the gas usage of the `_ccipReceive` function using tools like Hardhat or Foundry and set the `gasLimit` accordingly—adding a margin for safety. This ensures that the protocol avoids overpaying for gas on every cross-chain message.

This issue also reinforces the importance of making `extraArgs` mutable, so the gas limit and other parameters can be adjusted if execution costs change over time (e.g., due to protocol upgrades like [EIP-1884](https://eips.ethereum.org/EIPS/eip-1884)).

**YieldFi:** Fixed in commit [`3cc0b23`](https://github.com/YieldFiLabs/contracts/commit/3cc0b2331c35327a43e95176ce6c5578f145c0ee)

**Cyfrin:** Verified. `extraArgs` is now passed as a parameter to the call.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 5/5 |
| Rarity Score | 2/5 |
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

