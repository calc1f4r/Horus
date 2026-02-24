---
# Core Classification
protocol: zkSync
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33191
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-zksync
source_link: https://code4rena.com/reports/2024-03-zksync
github_link: https://github.com/code-423n4/2024-03-zksync-findings/issues/53

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
  - liquid_staking
  - cdp
  - yield
  - launchpad
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - oakcobalt
---

## Vulnerability Title

[M-03] State transition manager is unable to force upgrade a deployed ST, which invalidates the designed safeguard for 'urgent high risk situation'

### Overview


The bug report is about an issue with the State Transition Manager (STM) in the zkSync project. The STM is used to upgrade the Smart Contract (ST) in case of an urgent high-risk situation. However, the current implementation of the STM does not allow for this upgrade to be forced, which goes against the intended design and renders the safeguard mechanism useless. The report provides proof of concept and code snippets to explain the issue and recommends adding a new method to fix it. The developers have confirmed the finding and the judge has assessed it as a medium-risk vulnerability.

### Original Finding Content


### Impact

State transition manager (STM) will be unable to force upgrade a deployed ST against intended design for 'urgent high risk situation'.

This invalidates the designed safeguard mechanism of an STM force upgrade and ST.

### Proof of Concept

According to [doc](https://github.com/code-423n4/2024-03-zksync/blob/main/docs/Smart%20contract%20Section/L1%20ecosystem%20contracts.md#configurability-in-the-first-release), `in case of urgent high risk situation, STM might force upgrade the contract`(ST).

However, the above safeguard of force upgrading ST is not possible due to StateTransitionManger.sol's incomplete implementation.

(1) A deployed chain(ST) can choose to perform a mandatory upgrade at its own convenience. It's also possible for an ST to postpone an upgrade set by the state transition manager. An ST will perform an upgrade through `upgradeChainFromVersion()` on the Admin facet.

```solidity
//code/contracts/ethereum/contracts/state-transition/chain-deps/facets/Admin.sol
    function upgradeChainFromVersion(
        uint256 _oldProtocolVersion,
        Diamond.DiamondCutData calldata _diamondCut
|>    ) external onlyAdminOrStateTransitionManager {
...
```

(<https://github.com/code-423n4/2024-03-zksync/blob/4f0ba34f34a864c354c7e8c47643ed8f4a250e13/code/contracts/ethereum/contracts/state-transition/chain-deps/facets/Admin.sol#L103>)
Note that although `upgradeChainFromVersion()` is access-controlled by both chain admin and StateTransitionManager contract. StateTransitionManager will not be able to call it, because no methods or flows on StateTransitionManger.sol will invoke the call.

(2) Another method on Admin facet for upgrade is `executeUpgrade()` which is access-controlled by only StateTransitionManager contract. However, `executeUpgrade()` can only be invoked inside `_setChainIdUpgrade()`. And `_setChainIdUpgrade()` can only be invoked inside `createNewChain()`. This means, after a chain(ST)'s genesis, `executeUpgrade()` cannot be invoked by stateTransitionManger again to perform further upgrades.

```solidity
//code/contracts/ethereum/contracts/state-transition/chain-deps/facets/Admin.sol
    function executeUpgrade(
        Diamond.DiamondCutData calldata _diamondCut
|>    ) external onlyStateTransitionManager {
        Diamond.diamondCut(_diamondCut);
        emit ExecuteUpgrade(_diamondCut);
    }
```

(<https://github.com/code-423n4/2024-03-zksync/blob/4f0ba34f34a864c354c7e8c47643ed8f4a250e13/code/contracts/ethereum/contracts/state-transition/chain-deps/facets/Admin.sol#L123>)

```solidity
    function _setChainIdUpgrade(
        uint256 _chainId,
        address _chainContract
    ) internal {
...
          //@audit executeUpgrade of an ST will only be called once at chain deployment, because _setChainIdUpgrade() is only invoked when creating a new chain.
|>        IAdmin(_chainContract).executeUpgrade(cutData);
...
```

(<https://github.com/code-423n4/2024-03-zksync/blob/4f0ba34f34a864c354c7e8c47643ed8f4a250e13/code/contracts/ethereum/contracts/state-transition/StateTransitionManager.sol#L226>)

As a result of (1)&(2), StateChainManager cannot force upgrade an ST `in case of urgent high risk situation`. This invalidates the safeguard of force upgrade as stated by doc.

### Recommended Mitigation Steps

In StateTransitionManager.sol, add a method that can call `executeUpgrade()` or `upgradeChainFromVersion()` on a local chain.

**[saxenism (zkSync) confirmed and commented](https://github.com/code-423n4/2024-03-zksync-findings/issues/53#issuecomment-2036919937):**
 > Agree with the finding. Thank you :)

**[0xsomeone (judge) commented](https://github.com/code-423n4/2024-03-zksync-findings/issues/53#issuecomment-2082860557):**
 > The Warden has demonstrated how, in an urgent high-risk situation, a forced upgrade cannot be performed in contradiction with the project's documentation.
> 
> Based on the fact that the vulnerability is correct and would surface in a low-likelihood scenario, a medium-risk assessment is appropriate.
***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | zkSync |
| Report Date | N/A |
| Finders | oakcobalt |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-zksync
- **GitHub**: https://github.com/code-423n4/2024-03-zksync-findings/issues/53
- **Contest**: https://code4rena.com/reports/2024-03-zksync

### Keywords for Search

`vulnerability`

