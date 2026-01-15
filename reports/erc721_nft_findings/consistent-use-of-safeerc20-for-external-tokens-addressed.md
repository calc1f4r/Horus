---
# Core Classification
protocol: Thesis - tBTC and Keep
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13781
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/02/thesis-tbtc-and-keep/
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
  - services
  - cross_chain
  - insurance

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Martin Ortner
  - Alexander Wade
---

## Vulnerability Title

Consistent use of SafeERC20 for external tokens ✓ Addressed

### Overview


This bug report is about the use of the SafeERC20 features to interact with potentially broken tokens used in the system. The bug was addressed by making changes to two Github issues, <https://github.com/keep-network/keep-core/issues/1407> and <https://github.com/keep-network/keep-tecdsa/issues/272>.

Examples of the bug include `TokenGrant.receiveApproval` using `safeTransferFrom`, `TokenStaking.receiveApproval` not using `safeTransferFrom` while `safeTransfer` is being used, and `distributeERC20ToMembers` not using `safeTransferFrom`.

The recommendation is to consistently use SafeERC20 to support potentially broken tokens external to the system.

### Original Finding Content

#### Resolution



Addressed with <https://github.com/keep-network/keep-core/issues/1407> and <https://github.com/keep-network/keep-tecdsa/issues/272>.


#### Description


Use `SafeERC20` features to interact with potentially broken tokens used in the system. E.g. `TokenGrant.receiveApproval()` is using `safeTransferFrom` while other contracts aren’t.


#### Examples


* `TokenGrant.receiveApproval` using `safeTransferFrom`


**keep-core/contracts/solidity/contracts/TokenGrant.sol:L200-L200**



```
token.safeTransferFrom(\_from, address(this), \_amount);

```
* `TokenStaking.receiveApproval` not using `safeTransferFrom` while `safeTransfer` is being used.


**keep-core/contracts/solidity/contracts/TokenStaking.sol:L75-L75**



```
token.transferFrom(\_from, address(this), \_value);

```
**keep-core/contracts/solidity/contracts/TokenStaking.sol:L103-L103**



```
token.safeTransfer(owner, amount);

```
**keep-core/contracts/solidity/contracts/TokenStaking.sol:L193-L193**



```
token.transfer(tattletale, tattletaleReward);

```
* `distributeERC20ToMembers` not using `safeTransferFrom`


**keep-tecdsa/solidity/contracts/BondedECDSAKeep.sol:L459-L463**



```
token.transferFrom(
    msg.sender,
    tokenStaking.magpieOf(members[i]),
    dividend
);

```
#### Recommendation


Consistently use `SafeERC20` to support potentially broken tokens external to the system.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Thesis - tBTC and Keep |
| Report Date | N/A |
| Finders | Martin Ortner, Alexander Wade |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/02/thesis-tbtc-and-keep/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

