---
# Core Classification
protocol: Symbiotic
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64348
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
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
finders_count: 4
finders:
  - 0kage
  - Aleph-v
  - ChainDefenders](https://x.com/DefendersAudits) ([@1337web3](https://x.com/1337web3) & [@PeterSRWeb3
  - Farouk
---

## Vulnerability Title

`__NoncesUpgradeable_init` is not invoked

### Overview

See description below for full details.

### Original Finding Content

**Description:** The `__NoncesUpgradeable_init` function from the `NoncesUpgradeable` contract is not being called during the initialization of the `VotingPowerProvider` abstract contract. Since `VotingPowerProvider` inherits from `NoncesUpgradeable`, failing to initialize the nonce-related state can lead to incorrect nonce management, potentially causing issues with replay protection in signature verification or other related functionalities.

**Recommended Mitigation:** Update the `__VotingPowerProvider_init` function to include a call to `__NoncesUpgradeable_init()`

```solidity
function __VotingPowerProvider_init(
VotingPowerProviderInitParams memory votingPowerProviderInitParams
) internal virtual onlyInitializing {
__NetworkManager_init(votingPowerProviderInitParams.networkManagerInitParams);
VotingPowerProviderLogic.initialize(votingPowerProviderInitParams);
__OzEIP712_init(votingPowerProviderInitParams.ozEip712InitParams);
__NoncesUpgradeable_init(); // /@audit Add this line to properly initialize nonce state
}
```

**Symbiotic:** Acknowledged. Not invoked to optimize bytecode size. Should be safe since it's not initializing any state inside

**Cyfrin:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Symbiotic |
| Report Date | N/A |
| Finders | 0kage, Aleph-v, ChainDefenders](https://x.com/DefendersAudits) ([@1337web3](https://x.com/1337web3) & [@PeterSRWeb3, Farouk |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

