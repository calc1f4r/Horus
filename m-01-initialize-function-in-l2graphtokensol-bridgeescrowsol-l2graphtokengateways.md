---
# Core Classification
protocol: The Graph
chain: everychain
category: uncategorized
vulnerability_type: initializer

# Attack Vector Details
attack_type: initializer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6178
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-the-graph-l2-bridge-contest
source_link: https://code4rena.com/reports/2022-10-thegraph
github_link: https://github.com/code-423n4/2022-10-thegraph-findings/issues/149

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - initializer

protocol_categories:
  - dexes
  - bridge
  - cdp
  - yield
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - csanuragjain
  - ladboy233
---

## Vulnerability Title

[M-01] Initialize function in L2GraphToken.sol, BridgeEscrow.sol, L2GraphTokenGateway.sol, L1GraphTokenGateway.sol can be invoked multiple times from the implementation contract

### Overview


A bug has been identified in the code of the GitHub repository code-423n4/2022-10-thegraph. The vulnerability lies in the initialize functions of the contracts L2GraphToken.sol, BridgeEscrow.sol, L2GraphTokenGateway.sol, and L1GraphTokenGateway.sol. If the implementation contract is compromised, an attacker can reinitialize the contracts and become the owner, allowing them to drain the user's funds.

The proof of concept involves the attacker compromising the implementation contract, reinitializing the BridgeEscrow contract, and becoming the governor. With the governor access, the attacker can call the approve function to approve a malicious contract and drain all the GRT token from the BridgeEscrow.

The recommended mitigation step is to use the modifier “initializer” to protect the initialize function from being reinitiated. This modifier should be added to the initialize function of the contracts.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-10-thegraph/blob/309a188f7215fa42c745b136357702400f91b4ff/contracts/l2/gateway/L2GraphTokenGateway.sol#L87
https://github.com/code-423n4/2022-10-thegraph/blob/309a188f7215fa42c745b136357702400f91b4ff/contracts/l2/token/L2GraphToken.sol#L48
https://github.com/code-423n4/2022-10-thegraph/blob/309a188f7215fa42c745b136357702400f91b4ff/contracts/gateway/L1GraphTokenGateway.sol#L99
https://github.com/code-423n4/2022-10-thegraph/blob/309a188f7215fa42c745b136357702400f91b4ff/contracts/gateway/BridgeEscrow.sol#L20


## Vulnerability details

## Impact

initialize function in L2GraphToken.sol, BridgeEscrow.sol, L2GraphTokenGateway.sol, L1GraphTokenGateway.sol 

can be invoked multiple times from the implementation contract.

this means a compromised implementation can reinitialize the contract above and 

become the owner to complete the privilege escalation then drain the user's fund.

Usually in Upgradeable contract, a initialize function is protected by the modifier

```solidity
 initializer
```

to make sure the contract can only be initialized once.

## Proof of Concept
Provide direct links to all referenced code in GitHub. Add screenshots, logs, or any other relevant proof that illustrates the concept.

1. The implementation contract is compromised,

2. The attacker reinitialize the BridgeEscrow contract

```
    function initialize(address _controller) external onlyImpl {
        Managed._initialize(_controller);
    }
```

the onlyGovernor modifier's result depends on the controller because

```solidity
    function _onlyGovernor() internal view {
        require(msg.sender == controller.getGovernor(), "Caller must be Controller governor");
    }
```

3. The attacker have the governor access to the BridgeEscrow, 

4. The attack can call the approve function to approve malicious contract 

```solidity
     function approveAll(address _spender) external onlyGovernor {
        graphToken().approve(_spender, type(uint256).max);
    }
```

5. The attack can drain all the GRT token from the BridgeEscrow.

## Tools Used

Manual Review

## Recommended Mitigation Steps

We recommend the project use the modifier 

```solidity
 initializer
```

to protect the initialize function from being reinitiated

```solidity
   function initialize(address _owner) external onlyImpl initializer  {
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | The Graph |
| Report Date | N/A |
| Finders | csanuragjain, ladboy233 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-thegraph
- **GitHub**: https://github.com/code-423n4/2022-10-thegraph-findings/issues/149
- **Contest**: https://code4rena.com/contests/2022-10-the-graph-l2-bridge-contest

### Keywords for Search

`Initializer`

