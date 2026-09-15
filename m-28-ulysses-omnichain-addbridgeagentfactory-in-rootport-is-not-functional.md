---
# Core Classification
protocol: Maia DAO Ecosystem
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26097
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-maia
source_link: https://code4rena.com/reports/2023-05-maia
github_link: https://github.com/code-423n4/2023-05-maia-findings/issues/372

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
  - cross_chain
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - bin2chen
  - Fulum
  - its\_basu
  - zzebra83
  - 0xMilenov
---

## Vulnerability Title

[M-28] Ulysses omnichain - `addbridgeagentfactory` in `rootPort` is not functional

### Overview


The `addbridgeagentfactory` function is responsible for adding a new bridge agent factory to the `rootPort` however the current implementation contains faulty logic. This faulty logic is demonstrated in the following line: `bridgeAgentFactories[bridgeAgentsLenght++] = _bridgeAgentFactory;` as it attempts to access an index that does not yet exist in the `bridgeAgentFactories` array which should return an out of bounds error. Additionally, the function does not update the `isBridgeAgentFactory` mapping which is used to enable toggling the factory, i.e. enabling or disabling it via the `toggleBridgeAgentFactory` function.

The code hints that this is a key governance action and it is unclear from the code what the overall impact would be to the functioning of the protocol. This is why it is rated as medium rather than high. A Proof of Concept (POC) was provided which demonstrated the faulty logic and returned an "Index out of bounds" error. The recommended mitigation steps are to implement the function as follows: `isBridgeAgentFactory[_bridgeAgentFactory] = true; bridgeAgentFactories.push(_bridgeAgentFactory); bridgeAgentFactoriesLenght++;` which is also identical to how the branch ports implement this functionality. The type of bug is Governance and it has been confirmed and addressed.

### Original Finding Content


The `addbridgeagentfactory` function is responsible for adding a new bridge agent factory to the `rootPort`.

However the current implementation is faulty. The faulty logic is in the following line:

    bridgeAgentFactories[bridgeAgentsLenght++] = _bridgeAgentFactory;

A couple of problems here: The function is attempting to access an index that does not yet exist in the `bridgeAgentFactories` array; this should return an out of bounds error. The function also does not update the `isBridgeAgentFactory` mapping; once a new bridge agent factory is added, a new Dict item with a key equal to the address of new bridge agent factory and value of true is added. This mapping is then used to enable toggling the factory, i.e. enabling or disabling it via the `toggleBridgeAgentFactory` function.

Impact: The code hints that this is a key governance action. It does not work at the moment; however, with regards to impact, at this moment it is unclear from the code what the overall impact would be to the functioning of the protocol. That is why it is rated as medium rather than high. Feedback from sponsors is welcome to determine severity.

### Proof of Concept

        function testAddRootBridgeAgentFactoryBricked() public {
        //Get some gas
        hevm.deal(address(this), 1 ether);

        RootBridgeAgentFactory newBridgeAgentFactory = new RootBridgeAgentFactory(
            ftmChainId,
            WETH9(ftmWrappedNativeToken),
            local`AnyCall`Address,
            address(ftmPort),
            dao
        );

        rootPort.addBridgeAgentFactory(address(newBridgeAgentFactory));
        
        require(rootPort.bridgeAgentFactories(0)==address(bridgeAgentFactory), "Initial Factory not in factory list");
        require(rootPort.bridgeAgentFactories(1)==address(newBridgeAgentFactory), "New Factory not in factory list");

    }

The above POC demonstrates this; it attempts to call the function in question and returns an "Index out of bounds" error.

### Recommended Mitigation Steps

        function addBridgeAgentFactory(address _bridgeAgentFactory) external onlyOwner {
        // @audit this function is broken
        // should by implemented as so
        isBridgeAgentFactory[_bridgeAgentFactory] = true;
        bridgeAgentFactories.push(_bridgeAgentFactory);
        bridgeAgentFactoriesLenght++;

        emit BridgeAgentFactoryAdded(_bridgeAgentFactory);
    }

The correct implementation is above. This is also identical to how the branch ports implement this functionality.

### Assessed type

Governance

**[0xBugsy (Maia) confirmed](https://github.com/code-423n4/2023-05-maia-findings/issues/372#issuecomment-1632699891)**

**[0xLightt (Maia) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/372#issuecomment-1709172882):**
 > Addressed [here](https://github.com/Maia-DAO/eco-c4-contest/tree/372).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Maia DAO Ecosystem |
| Report Date | N/A |
| Finders | bin2chen, Fulum, its\_basu, zzebra83, 0xMilenov |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-maia
- **GitHub**: https://github.com/code-423n4/2023-05-maia-findings/issues/372
- **Contest**: https://code4rena.com/reports/2023-05-maia

### Keywords for Search

`vulnerability`

