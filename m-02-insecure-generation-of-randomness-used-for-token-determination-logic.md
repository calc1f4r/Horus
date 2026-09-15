---
# Core Classification
protocol: Phimaterial
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43699
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Shieldify/2023-07-27-PHIMaterial.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-02] Insecure Generation of Randomness Used for Token Determination Logic

### Overview


This bug report is about a vulnerability in the code of a smart contract called `EmissionLogic.sol`. This contract is used to determine the rarity and identification number of a `MaterialObject`. The problem is that the function responsible for this uses a source of randomness that can be predicted by others, making it insecure. This can potentially allow malicious actors to create more rare and exclusive `MaterialObjects`. The affected code is located in line 49 of the `src/EmissionLogic.sol` file. The recommended solution is to use a decentralized oracle, specifically `Chainlink's VRF`, for generating random numbers. This will help prevent the vulnerability and protect the application on the Polygon network, which is prone to block reorganizations. The team has acknowledged the issue but currently does not have plans to implement the recommended solution. 

### Original Finding Content

**Severity**

Medium Risk

**Description**

`EmissionLogic.sol` contains the `determineTokenByLogic()` function that determines the rarity and `tokenId` of a `MaterialObject`.
It generates a `uint256 random` value that relies on variables like `block.timestamp` and `tx.origin` as a source of randomness is a common vulnerability, as the outcome can be predicted by calling contracts or validators. In the context of blockchains, the best and most secure source of randomness is that which is generated off-chain in a verified manner.

The function also uses `block.prevrandao` whose random seed calculation is by epoch basis, which means that entropy within 2 epochs is low and sometimes [`even predictable`](https://github.com/ethereum/annotated-spec/blob/master/phase0/beacon-chain.md#aside-randao-seeds-and-committee-generation). Users of PREVRANDAO would need to check that a validator has provided a block since the last time they called PREVRANDAO. Otherwise, they won't necessarily be drawing statistically independent random outputs on successive calls to PREVRANDAO.

In the context of Phi's business logic, improper insecure randomness generation could allow malicious actors to mint more rare/exclusive `MaterialObject` items.

**Location of Affected Code**

File: [`src/EmissionLogic.sol#L49`](https://github.com/PHI-LABS-INC/DailyMaterial/blob/355376812ba1e2eeed97d5447c2afea83a3ca8f1/src/EmissionLogic.sol#L49)

```solidity
uint256 random = uint256(keccak256(abi.encodePacked(block.prevrandao, block.timestamp, tx.origin)));
```

**Recommendation**

Consider using a decentralized oracle for the generation of random numbers, such as `Chainlink's VRF`. It is important to take into account the `requestConfirmations` variable that will be used in the `VRFv2Consumer` contract when implementing VRF. The purpose of this value is to specify the minimum number of blocks you wish to wait before receiving randomness from the Chainlink VRF service. The inclusion of this value is motivated by the occurrence of chain reorganizations, which result in the alteration of blocks and transactions. Addressing this concern is crucial for the successful implementation of this application on the Polygon network because it is prone to block reorgs and they happen almost on a daily basis.

Shieldify recommends setting the `requestConfirmations` value to at least 5, so that the larger portion of the reorgs that happen are properly taken into account and won't impact the randomness generation.

**Team Response**

Acknowledged, but currently will not be mitigated as the team does not have plans to implement Chainlink functionality yet.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Phimaterial |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Shieldify/2023-07-27-PHIMaterial.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

