---
# Core Classification
protocol: Entangle Trillion
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51361
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/entangle-labs/entangle-trillion
source_link: https://www.halborn.com/audits/entangle-labs/entangle-trillion
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Broken integration through cosmos addresses

### Overview


The report describes a bug in the proposeBurnAndBridge and proposeBridgeExecuted functions of the BalanceManager.sol contract. The issue is that the function is accepting an address parameter instead of a bytes parameter, which will cause problems for integrations using Cosmos addresses. The report includes a proof of concept test that shows the issue with a broken Cosmos address. The BVSS score for this bug is 10.0, and the recommendation is to change the address variable to a byte array. The Entangle team has fixed the issue by deprecating the feature.

### Original Finding Content

##### Description

In the **proposeBurnAndBridge/proposeBridgeExecuted** function, we are directly getting the address parameter as an argument. However, It should be bytes instead of **address**. This will directly block integrations on the Cosmos (bech32) addresses.

  

[[/contracts/BalanceManager.sol#L144](https://github.com/Entangle-Protocol/entangle-lsd-protocol/blob/48e025e4ddf330e8ac710e82114db704a76d2857/contracts/BalanceManager.sol#L144)](<https://github.com/Entangle-Protocol/entangle-lsd-protocol/blob/48e025e4ddf330e8ac710e82114db704a76d2857/contracts/BalanceManager.sol#L144>)

  

```
function proposeBurnAndBridge(uint64 destChainId, uint128 sid, uint256 synthAmount, address recipient) external {
    bytes4 selector = bytes4(keccak256("HandleBurnAndBridge(bytes)"));
    bytes memory functionParams = abi.encode(destChainId, sid, synthAmount, recipient);
    aggregationSpotter.propose(protocolId, eobChainId, abi.encode(eventProcessorAddress), selector, functionParams);
}
```

  

[[BalanceManager.sol#L218](https://github.com/Entangle-Protocol/entangle-lsd-protocol/blob/48e025e4ddf330e8ac710e82114db704a76d2857/contracts/BalanceManager.sol#L218)](<https://github.com/Entangle-Protocol/entangle-lsd-protocol/blob/48e025e4ddf330e8ac710e82114db704a76d2857/contracts/BalanceManager.sol#L218>)

```
  function proposeBridgeExecuted(uint64 destChainId, uint128 sid, uint256 synthAmount, address recipient) external {
      bytes4 selector = bytes4(keccak256("HandleBridgeExecuted(bytes)"));
      bytes memory functionParams = abi.encode(destChainId, sid, synthAmount, recipient);
      aggregationSpotter.propose(protocolId, eobChainId, abi.encode(eventProcessorAddress), selector, functionParams);
  }
```

##### Proof of Concept

```
    function setUp() public {
        vm.createSelectFork(vm.envString("ETH_URL"));
        vm.rollFork(47442254);

        lsdSystem = new EntangleLSDBootstrapperETH();

        // boostrap the whole Liquid Vault system with Balance manager mock
        lsdSystem.bootstrap();

        protocolId = uint32(1) + (uint32(1) << 31);

        // sid deployed in LSD protocol
        sid = (uint128(lsdSystem.getChainID()) << 64) + (uint128(protocolId) << 32) + (uint128(1));

        aTokenWrapper = address(new ATokenWrapper());
    }

    function testBrokenCosmosAddress() external {
        lsdSystem.proposeBurnAndBridge(1,sid,100,0xF403C135812408BFbE8713b5A23a04b3D48AAE31);
    }
```

  
![Only ETH addresses are allowed](https://halbornmainframe.com/proxy/audits/images/65ca75064e98381432d557c3)

##### BVSS

[AO:A/AC:L/AX:L/C:C/I:C/A:C/D:N/Y:N/R:N/S:C (10.0)](/bvss?q=AO:A/AC:L/AX:L/C:C/I:C/A:C/D:N/Y:N/R:N/S:C)

##### Recommendation

Consider changing address variable with a byte array.

  

**Remediation Plan:** The Entangle team solved the issue by deprecating the feature.

##### Remediation Hash

<https://github.com/Entangle-Protocol/entangle-lsd-protocol/commit/519ab1768dddc4842b09baae55fc0f8a76d98365>

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Entangle Trillion |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/entangle-labs/entangle-trillion
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/entangle-labs/entangle-trillion

### Keywords for Search

`vulnerability`

