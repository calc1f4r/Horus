---
# Core Classification
protocol: Aave Protocol V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13605
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/09/aave-protocol-v2/
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Sergii Kravchenko
  - Bernhard Mueller
---

## Vulnerability Title

Griefing attack by taking flash loan on behalf of user

### Overview


A bug has been identified in the code/contracts/lendingpool/LendingPool.sol, which allows anyone to execute a flash loan on behalf of other users. This is possible because the arbitrary `receiverAddress` address can be passed as an argument when taking a flash loan from the protocol. If someone gives the allowance to the `LendingPool` contract to make a deposit, the attacker can use this vulnerability to execute a flash loan on behalf of that user, forcing the user to pay fees from the flash loan. This will also prevent the victim from making a successful deposit transaction.

In order to remediate this issue, it is recommended that only the user can take a flash loan. This can be done by ensuring that the `receiverAddress` is always set to the actual user's address and not an arbitrary address. Additionally, it is important to keep the allowance to the `LendingPool` contract as low as possible to reduce the risk of an attack.

### Original Finding Content

#### Description


When taking a flash loan from the protocol, the arbitrary `receiverAddress`  address can be passed as the argument:


**code/contracts/lendingpool/LendingPool.sol:L547-L554**



```
function flashLoan(
  address receiverAddress,
  address asset,
  uint256 amount,
  uint256 mode,
  bytes calldata params,
  uint16 referralCode
) external override {

```
That may allow anyone to execute a flash loan on behalf of other users. In order to make that attack, the `receiverAddress` should give the allowance to the `LendingPool` contract to make a transfer for the amount of `currentAmountPlusPremium`.


#### Example


If someone is giving the allowance to the `LendingPool` contract to make a deposit, the attacker can execute a flash loan on behalf of that user, forcing the user to pay fees from the flash loan. That will also prevent the victim from making a successful deposit transaction.


#### Remediation


Make sure that only the user can take a flash loan.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Aave Protocol V2 |
| Report Date | N/A |
| Finders | Sergii Kravchenko, Bernhard Mueller |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/09/aave-protocol-v2/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

