---
# Core Classification
protocol: P2P.org
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56811
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Staking%20Lending%20Proxy%20(2)/README.md#1-risk-of-token-freeze-in-emergency-situations
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
  - MixBytes
---

## Vulnerability Title

Risk of Token Freeze in Emergency Situations

### Overview


The bug report discusses an issue with the `P2pSuperformProxy` contract. The contract enforces a requirement that the receiver address for a transaction must be the same as the contract itself. However, there is a possibility that the contract may enter an emergency state, during which the normal withdrawal process is interrupted. This can result in the contract's balance remaining unchanged and assets becoming locked. The recommendation is to make sure that the contract does not revert when the balance change is zero and to implement a rescue mechanism to recover any locked assets. The bug has been fixed in a recent commit.

### Original Finding Content

##### Description
The `P2pSuperformProxy` contract enforces:
```solidity
require(
    req.superformData.receiverAddress == address(this),
    P2pSuperformProxy__ReceiverAddressShouldBeP2pSuperformProxy(
        req.superformData.receiverAddress
            )
        );
```

  1.  Superform may enter an emergency state during which the normal withdrawal flow is interrupted.
  2.  In such an emergency, calling withdraw may only enqueue an emergency withdrawal request without actually transferring assets, so the proxy’s balance may remain unchanged. If withdraw reverts when the balance delta is zero, it will break the emergency flow and block further recovery.
  3.  During this emergency flow, tokens can be sent by the Superform administrator to **receiverAddress** (the proxy itself) — a path that never occurs in normal operation — and without a rescue mechanism these assets will become permanently locked.

##### Recommendation
We recommend:
  1.  Ensure that withdraw never reverts when the proxy’s balance change is zero. Treat a zero-delta result as a successful no-op to preserve the emergency withdrawal queue flow.
  2.  Implement a client-accessible rescue mechanism to recover any ERC-20 or native tokens held by the proxy as a result of the emergency flow.

> **Client's Commentary:**
> Fixed in https://github.com/p2p-org/p2p-lending-proxy/commit/b7b2a4ff5b321afa7d9edaddf62953411eab8ff0

---

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | P2P.org |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Staking%20Lending%20Proxy%20(2)/README.md#1-risk-of-token-freeze-in-emergency-situations
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

