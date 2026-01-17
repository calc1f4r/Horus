---
# Core Classification
protocol: Centrifuge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27029
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-09-centrifuge
source_link: https://code4rena.com/reports/2023-09-centrifuge
github_link: https://github.com/code-423n4/2023-09-centrifuge-findings/issues/537

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
finders_count: 6
finders:
  - castle\_chain
  - bin2chen
  - nobody2018
  - merlin
  - mert\_eren
---

## Vulnerability Title

[M-01] `onlyCentrifugeChainOrigin()` can't require `msg.sender` equal `axelarGateway`

### Overview


This bug report is about the `execute()` method in the `AxelarRouter.sol` contract. The method has two methods for ensuring the legitimacy of the execution, `axelarGateway.validateContractCall()` and `onlyCentrifugeChainOrigin()`. The `onlyCentrifugeChainOrigin()` method has a restriction `msg.sender == address(axelarGateway)` which is not necessary. This restriction prevents the execution of the `execute()` method from other chains, resulting in the protocol not working properly. 

The security of the command can be guaranteed by `axelarGateway.validateContractCall()`, `sourceChain`, `sourceAddress` without the need to restrict `msg.sender`. The bug was confirmed by hieronx (Centrifuge) and the severity was increased to High by gzeon (judge). Later, the severity was decreased to Medium as the expected setup would have DelayedAdmin able to unstuck the system. The bug was mitigated in a pull request.

### Original Finding Content


In `AxelarRouter.sol`, we need to ensure the legitimacy of the `execute()` method execution, mainly through two methods:

1.  `axelarGateway.validateContractCall ()` to validate if the `command` is approved or not.
2.  `onlyCentrifugeChainOrigin()` is used to validate that `sourceChain` `sourceAddress` is legal.

Let's look at the implementation of `onlyCentrifugeChainOrigin()`:

```solidity
    modifier onlyCentrifugeChainOrigin(string calldata sourceChain, string calldata sourceAddress) {        
@>      require(msg.sender == address(axelarGateway), "AxelarRouter/invalid-origin");
        require(
            keccak256(bytes(axelarCentrifugeChainId)) == keccak256(bytes(sourceChain)),
            "AxelarRouter/invalid-source-chain"
        );
        require(
            keccak256(bytes(axelarCentrifugeChainAddress)) == keccak256(bytes(sourceAddress)),
            "AxelarRouter/invalid-source-address"
        );
        _;
    }
```

The problem is that this restriction `msg.sender == address(axelarGateway)`.

When we look at the official `axelarGateway.sol` contract, it doesn't provide any call external contract 's`execute()` method.

So `msg.sender` cannot be `axelarGateway`, and the official example does not restrict `msg.sender`.

The security of the command can be guaranteed by `axelarGateway.validateContractCall()`, `sourceChain`, `sourceAddress`.

There is no need to restrict `msg.sender`.

`axelarGateway` code address<br>
<https://github.com/axelarnetwork/axelar-cgp-solidity/blob/main/contracts/AxelarGateway.sol>

Can't find anything that calls `router.execute()`.

### Impact

`router.execute()` cannot be executed properly, resulting in commands from other chains not being executed， protocol not working properly.

### Recommended Mitigation

Remove `msg.sender` restriction

```diff
    modifier onlyCentrifugeChainOrigin(string calldata sourceChain, string calldata sourceAddress) {        
-       require(msg.sender == address(axelarGateway), "AxelarRouter/invalid-origin");
        require(
            keccak256(bytes(axelarCentrifugeChainId)) == keccak256(bytes(sourceChain)),
            "AxelarRouter/invalid-source-chain"
        );
        require(
            keccak256(bytes(axelarCentrifugeChainAddress)) == keccak256(bytes(sourceAddress)),
            "AxelarRouter/invalid-source-address"
        );
        _;
    }
```

### Assessed type

Context

**[hieronx (Centrifuge) confirmed](https://github.com/code-423n4/2023-09-centrifuge-findings/issues/537#issuecomment-1723464758)**

**[gzeon (judge) increased severity to High and commented](https://github.com/code-423n4/2023-09-centrifuge-findings/issues/537#issuecomment-1733894416):**
 > This seems High risk to me since the Axelar bridge is a centerpiece of this protocol, and when deployed in a certain way where the AxelarRouter is the only ward, it might cause user deposits to be stuck forever. 

**[gzeon (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2023-09-centrifuge-findings/issues/537#issuecomment-1735848904):**
 > Reconsidering severity to Medium here since the expected setup would have DelayedAdmin able to unstuck the system.

**[hieronx (Centrifuge) commented](https://github.com/code-423n4/2023-09-centrifuge-findings/issues/537#issuecomment-1745247688):**
 > Mitigated in https://github.com/centrifuge/liquidity-pools/pull/168



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Centrifuge |
| Report Date | N/A |
| Finders | castle\_chain, bin2chen, nobody2018, merlin, mert\_eren, maanas |

### Source Links

- **Source**: https://code4rena.com/reports/2023-09-centrifuge
- **GitHub**: https://github.com/code-423n4/2023-09-centrifuge-findings/issues/537
- **Contest**: https://code4rena.com/reports/2023-09-centrifuge

### Keywords for Search

`vulnerability`

