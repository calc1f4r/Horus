---
# Core Classification
protocol: Moonwell
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26848
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-moonwell
source_link: https://code4rena.com/reports/2023-07-moonwell
github_link: https://github.com/code-423n4/2023-07-moonwell-findings/issues/114

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
  - T1MOH
---

## Vulnerability Title

[M-12] Incorrect chainId of Base in deploy script will force redeployment

### Overview


A bug was discovered in the contract ChainIds.sol which maps `chainId -> wormholeChainId`. This mapping is used in the contract Addresses to associate contract names with their address on a specific chain. The Network ID of Base was set to 84531, when the actual network ID is 8453 according to the Base documentation. This incorrect chain ID resulted in an incorrect deploy and subsequent redeployment. 

The recommended mitigation step is to change the Base Network ID to 8453. This was confirmed by ElliotFriedman (Moonwell).

### Original Finding Content


Incorrect chainId of Base in deploy parameters results in incorrect deploy and subsequent redeployment.

### Proof of Concept

Contract ChainIds.sol is responsible for mapping `chainId -> wormholeChainId` which is used in contract `Addresses` to associate contract name with its address on specific chain. `Addresses` is the main contract which keeps track of all dependency addresses and passed into main `deploy()` and here addresses accessed via block.chainId: <br><https://github.com/code-423n4/2023-07-moonwell/blob/fced18035107a345c31c9a9497d0da09105df4df/test/proposals/mips/mip00.sol#L77>

```solidity
    function deploy(Addresses addresses, address) public {
        ...
            trustedSenders[0].chainId = chainIdToWormHoleId[block.chainid];
            
        ...
            memory cTokenConfigs = getCTokenConfigurations(block.chainid);
    }
```

Here you can see that Network ID of Base set to 84531. But actual network id is 8453 from [Base docs](https://docs.base.org/network-information/).

```solidity
contract ChainIds {
    uint256 public constant baseChainId = 84531;
    uint16 public constant baseWormholeChainId = 30; /// TODO update when actual base chain id is known
    
    uint256 public constant baseGoerliChainId = 84531;
    uint16 public constant baseGoerliWormholeChainId = 30;
    
    ...

    constructor() {
        ...
        chainIdToWormHoleId[baseChainId] = moonBeamWormholeChainId; /// base deployment is owned by moonbeam governance
        ...
    }
}
```

### Recommended Mitigation Steps

Change Base Network ID to 8453.

**[ElliotFriedman (Moonwell) confirmed](https://github.com/code-423n4/2023-07-moonwell-findings/issues/114#issuecomment-1664489765)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Moonwell |
| Report Date | N/A |
| Finders | T1MOH |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-moonwell
- **GitHub**: https://github.com/code-423n4/2023-07-moonwell-findings/issues/114
- **Contest**: https://code4rena.com/reports/2023-07-moonwell

### Keywords for Search

`vulnerability`

