---
# Core Classification
protocol: Genesis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50906
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/coredao/genesis-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/coredao/genesis-smart-contract-security-assessment
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
  - Halborn
---

## Vulnerability Title

BURN ADDRESS SHOULD BE DEFINED AS DIFFERENT THAN SYSTEM CONTRACTS

### Overview


The CoreDAO chain has a bug where the system contracts, which are contracts that were deployed at the beginning of the blockchain, are not using the designated burn address. This means that any funds that are supposed to be burned will not go to the correct address. This bug has a medium impact and is likely to happen. The recommendation is to keep the current implementation, but it will require software updates to fix the issue.

### Original Finding Content

##### Description

The **CoreDAO** chain implements a number of dedicated built-in system contracts. Unlike smart contracts deployed by blockchain users, built-in system contracts were deployed at genesis time. The system contracts are increasing one by one. Instead of using the burn address as an [address](0x0000000000000000000000000000000000001008), the address can be defined different from the system contract addresses.

Code Location
-------------

[contracts/System.sol#L20](https://github.com/coredao-org/core-genesis-contract/blob/audit-halborn/contracts/System.sol#L20)

#### System.sol

```
  address public constant VALIDATOR_CONTRACT_ADDR = 0x0000000000000000000000000000000000001000;
  address public constant SLASH_CONTRACT_ADDR = 0x0000000000000000000000000000000000001001;
  address public constant SYSTEM_REWARD_ADDR = 0x0000000000000000000000000000000000001002;
  address public constant LIGHT_CLIENT_ADDR = 0x0000000000000000000000000000000000001003;
  address public constant RELAYER_HUB_ADDR = 0x0000000000000000000000000000000000001004;
  address public constant CANDIDATE_HUB_ADDR = 0x0000000000000000000000000000000000001005;
  address public constant GOV_HUB_ADDR = 0x0000000000000000000000000000000000001006;
  address public constant PLEDGE_AGENT_ADDR = 0x0000000000000000000000000000000000001007;
  address public constant BURN_ADDR = 0x0000000000000000000000000000000000001008;
  address public constant FOUNDATION_ADDR = 0x0000000000000000000000000000000000001009;

```

* System Burn contract should not be updated during the upgrades.
* All burned funds will be located on the Burn address.
* In the BSC, BurnContract address is deleted from the [constant](https://github.com/bnb-chain/bsc/blob/master/core/systemcontracts/const.go) contract addresses.

##### Score

Impact: 5  
Likelihood: 1

##### Recommendation

**RISK ACCEPTED**: After some internal discussion, the `CoreDAO team` has decided to maintain the current implementation. Both the BSC implementation and the Core implementation require software updates to change the way in which the burn address works.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Genesis |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/coredao/genesis-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/coredao/genesis-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

