---
# Core Classification
protocol: 0x v3 Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13941
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2019/10/0x-v3-staking/
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
  - liquid_staking
  - dexes
  - yield
  - services
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Alex Wade
  - Steve Marx
---

## Vulnerability Title

MixinParams.setParams bypasses safety checks made by standard StakingProxy upgrade path. ✓ Fixed

### Overview


This bug report is about a vulnerability in the staking contracts of a 0xProject. The parameters of the staking contracts are configurable, and can be set by an authorized address. There is a possibility of setting unsafe or nonsensical values for the contract parameters, such as setting epochDurationInSeconds to 0, cobbDouglassAlphaNumerator to a value larger than cobbDouglassAlphaDenominator, rewardDelegatedStakeWeight to a value over 100% of the staking reward, and more. This issue was fixed in 0xProject/0x-monorepo#2279, where the parameter validity is asserted in `setParams()`. It is recommended to ensure that calls to `setParams` check that the provided values are within the same range currently enforced by the proxy.

### Original Finding Content

#### Resolution



This is fixed in [0xProject/0x-monorepo#2279](https://github.com/0xProject/0x-monorepo/pull/2279). Now the parameter validity is asserted in `setParams()`.


#### Description


The staking contracts use a set of configurable parameters to determine the behavior of various parts of the system. The parameters dictate the duration of epochs, the ratio of delegated stake weight vs operator stake, the minimum pool stake, and the Cobb-Douglas numerator and denominator. These parameters can be configured in two ways:


1. An authorized address can deploy a new `Staking` contract (perhaps with altered parameters), and configure the `StakingProxy` to delegate to this new contract. This is done by calling


	* `StakingProxy.detachStakingContract`:
	
	
	**code/contracts/staking/contracts/src/StakingProxy.sol:L82-L90**
	
	
	
	```
	/// @dev Detach the current staking contract.
	/// Note that this is callable only by an authorized address.
	function detachStakingContract()
	    external
	    onlyAuthorized
	{
	    stakingContract = NIL\_ADDRESS;
	    emit StakingContractDetachedFromProxy();
	}
	
	```
	* `StakingProxy.attachStakingContract(newContract)`:
	
	
	**code/contracts/staking/contracts/src/StakingProxy.sol:L72-L80**
	
	
	
	```
	/// @dev Attach a staking contract; future calls will be delegated to the staking contract.
	/// Note that this is callable only by an authorized address.
	/// @param \_stakingContract Address of staking contract.
	function attachStakingContract(address \_stakingContract)
	    external
	    onlyAuthorized
	{
	    \_attachStakingContract(\_stakingContract);
	}
	
	```During the latter call, the `StakingProxy` performs a delegatecall to `Staking.init`, then checks the values of the parameters set during initialization:


**code/contracts/staking/contracts/src/StakingProxy.sol:L208-L219**



```
// Call `init()` on the staking contract to initialize storage.
(bool didInitSucceed, bytes memory initReturnData) = stakingContract.delegatecall(
    abi.encodeWithSelector(IStorageInit(0).init.selector)
);
if (!didInitSucceed) {
    assembly {
        revert(add(initReturnData, 0x20), mload(initReturnData))
    }
}
  
// Assert initialized storage values are valid
\_assertValidStorageParams();

```
2. An authorized address can call `MixinParams.setParams` at any time and set the contract’s parameters to arbitrary values.


The latter method introduces the possibility of setting unsafe or nonsensical values for the contract parameters: `epochDurationInSeconds` can be set to 0, `cobbDouglassAlphaNumerator` can be larger than `cobbDouglassAlphaDenominator`, `rewardDelegatedStakeWeight` can be set to a value over 100% of the staking reward, and more.


Note, too, that by using `MixinParams.setParams` to set all parameters to 0, the `Staking` contract can be re-initialized by way of `Staking.init`. Additionally, it can be re-attached by way of `StakingProxy.attachStakingContract`, as the delegatecall to `Staking.init` will succeed.


#### Recommendation


Ensure that calls to `setParams` check that the provided values are within the same range currently enforced by the proxy.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | 0x v3 Staking |
| Report Date | N/A |
| Finders | Alex Wade, Steve Marx |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2019/10/0x-v3-staking/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

