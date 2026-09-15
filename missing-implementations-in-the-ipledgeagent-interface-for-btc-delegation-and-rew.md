---
# Core Classification
protocol: BTC Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50886
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/coredao/btc-staking
source_link: https://www.halborn.com/audits/coredao/btc-staking
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Missing Implementations in the IPledgeAgent Interface for BTC Delegation and Reward Distribution

### Overview

See description below for full details.

### Original Finding Content

##### Description

The **IPledgeAgent** smart contract provides a framework for delegating Bitcoin (BTC) to the Core network, facilitating staking, reward claims, and the transfer of staked BTC among validators. The contract includes functions for parsing transaction data, validating Bitcoin transaction proofs, managing staking receipts, and distributing rewards. However, the **IPledgeAgent** interface does not reflect all the functionalities implemented in the contract, particularly the newer functions related to BTC delegation.

  

```
interface IPledgeAgent {
  function addRoundReward(address[] calldata agentList, uint256[] calldata rewardList) payable external;
  function getHybridScore(address[] calldata candidates, uint256[] calldata powers, uint256 round) external returns(uint256[] memory);
  function setNewRound(address[] calldata validatorList, uint256 round) external;
  function distributePowerReward(address candidate, address[] calldata miners) external;
  function onFelony(address agent) external;
}
```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:P/S:C (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:P/S:C)

##### Recommendation

Consider implementing missing interface definitions.

  

### Remediation Plan

**SOLVED :** The **CoreDAO team** solved the issue by adding missing interfaces.

##### Remediation Hash

<https://github.com/coredao-org/core-genesis-contract/commit/b582f0d4b94ce9f6baa91283ccda6274a95952de>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | BTC Staking |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/coredao/btc-staking
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/coredao/btc-staking

### Keywords for Search

`vulnerability`

