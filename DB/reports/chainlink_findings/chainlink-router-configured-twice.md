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
solodit_id: 55548
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

Chainlink router configured twice

### Overview

See description below for full details.

### Original Finding Content

**Description:** In `BridgeCCIP`, there is a dedicated storage slot for the CCIP router address, [`router`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/ccip/BridgeCCIP.sol#L32-L33):

```solidity
contract BridgeCCIP is CCIPReceiver, Ownable {
    address public router;
```

This value can be updated by the admin through [`BridgeCCIP::setRouter`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/ccip/BridgeCCIP.sol#L69-L73):

```solidity
function setRouter(address _router) external onlyAdmin {
    require(_router != address(0), "!router");
    router = _router;
    emit SetRouter(msg.sender, _router);
}
```

The `router` is then used in [`BridgeCCIP::send`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/ccip/BridgeCCIP.sol#L157) to send messages via CCIP:

```solidity
IRouterClient(router).ccipSend{ value: msg.value }(_dstChain, evm2AnyMessage);
```

However, the inherited `CCIPReceiver` contract already defines an immutable router address (`i_ccipRouter`), which is used to validate that incoming CCIP messages originate from the correct router.

This introduces an inconsistency: if `BridgeCCIP.router` is changed, the contract will continue to *send* messages via the new router, but *receive* messages only from the original, immutable `i_ccipRouter`. This mismatch could break cross-chain communication or make message delivery non-functional.

**Recommended Mitigation:** Since the router address in `CCIPReceiver` is immutable, any future change to the router would already require redeployment of the `BridgeCCIP` contract. Therefore, the `router` storage slot and the `setRouter` function in `BridgeCCIP` are redundant and potentially misleading. We recommend removing both and relying exclusively on the `i_ccipRouter` value inherited from `CCIPReceiver`.

**YieldFi:** Fixed in commit [`3cc0b23`](https://github.com/YieldFiLabs/contracts/commit/3cc0b2331c35327a43e95176ce6c5578f145c0ee)

**Cyfrin:** Verified. `router` removed and `i_ccipRouter` used from the inherited contract.

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

