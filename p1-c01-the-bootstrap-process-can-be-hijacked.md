---
# Core Classification
protocol: Eco Contracts Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11635
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/eco-contracts-audit/
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

protocol_categories:
  - dexes
  - yield
  - cross_chain
  - launchpad
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[P1-C01] The bootstrap process can be hijacked

### Overview


This bug report is about the BeamBootstrap contract and its related components. The BeamBootstrap contract stores its owner in the deployAccount variable, which is transferred to 20 ForwardProxy contracts through BeamInitializable. The issue is that the initialize function of BeamInitializable is public, so it can be called more than once. This means that an attacker can deploy a malicious contract and feed it to the 20 ForwardProxy contracts, thus hijacking the entire Bootstrap process.

To fix this issue, consider requiring that only the owner can call the initialize function, thus making it possible to call it only once during initialization with the onlyConstruction modifier. The issue has been partially fixed so the destruct function can now be called only by the owner. The initialize function can be called only once, but it can still be called by any account, not just by its current owner.

### Original Finding Content

###### Critical


Components: [`deploy`](https://github.com/BeamNetwork/currency/tree/af3428020545e3f3ae2f3567b94e1fbc5e5bdb4c/contracts/deploy) and [proxy](https://github.com/BeamNetwork/currency/tree/af3428020545e3f3ae2f3567b94e1fbc5e5bdb4c/contracts/proxy)


The [`BeamBootstrap`](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/BeamBootstrap.sol#L10) contract stores its owner in the [`deployAccount`](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/BeamBootstrap.sol#L11) [variable](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/BeamBootstrap.sol#L11), which also gets transferred to [20](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/BeamBootstrap.sol#L17) [`ForwardProxy`](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/BeamBootstrap.sol#L17) contracts through [`BeamInitializable`](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/BeamInitializable.sol#L9).


The `BeamInitializable` contract also uses an ownership pattern, which allows only the owner to [set the implementation](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/BeamInitializable.sol#L23) that will be delegated from the proxy and to [`selfdestruct`](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/BeamInitializable.sol#L45) [the contract](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/BeamInitializable.sol#L45).


The issue here is that the [`initialize`](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/BeamInitializable.sol#L16) [function](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/BeamInitializable.sol#L16) is `public`. It does not have a restriction that only the owner can call, and it can be called more than once.


For an attacker to hijack the entire Bootstrap process, it would only require them to deploy a malicious contract like this:



```
contract Malicious {
    address public owner;

    constructor(address _owner) public {
        owner = _owner;
    }
}
```

This sets an address in their control as the `owner`. Then, they can feed it to the 20 `FordwardProxy`s through a `BeamInitializable` interface, call `initialize` with the address of the `Malicious` contract, and give themselves ownership of all the `ForwardProxy`s.


They can also get ownership of the original `BeamInitializable` contract, but that does not seem to give them any gain.


Test case: <https://gist.github.com/mattaereal/9a7fe9d20b3c3253b1effe049cb9211e>


Consider requiring that only the `owner` can call the `initialize` function, thus making it possible to call it only once during initialization with the [`onlyConstruction`](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/ForwardTarget.sol#L11) [modifier](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/ForwardTarget.sol#L11).


***Update:*** *Partially fixed. The* [*`destruct`*](https://github.com/BeamNetwork/currency/blob/af3428020545e3f3ae2f3567b94e1fbc5e5bdb4c/contracts/deploy/EcoInitializable.sol#L56) *function now can be called only by the* *`owner`**. The* [*`initialize`*](https://github.com/BeamNetwork/currency/blob/af3428020545e3f3ae2f3567b94e1fbc5e5bdb4c/contracts/deploy/EcoInitializable.sol#L62) *function can be called only once. However,* *`initialize`* *can still be called by any account, not just by its current owner. Eco’s statement for this issue:*



> The problem highlighted here has two parts to consider. First, the addresses reserved by `EcoBootstrap` respond to the `initialize` call described. These proxy contracts have their `implementation` slot set, so the `onlyConstruction` modifier will prevent calls. The modifier might not protect the underlying implementation contract though – since the underlying implementation isn’t itself a proxy contract the `implementation` slot might not be set. Fortunately, the `ForwardTarget` constructor is run when the `EcoInitializable` contract is deployed, and it sets the `implementation` slot. This makes it impossible to call `initialize` on the underlying implementation contract.
> 
> 
> Per OpenZeppelin’s audit, `initialize` can only be called once on any proxy, and it’s always called immediately during proxy construction – ensured by the `ForwardProxy` constructor. Further, the `onlyConstruction` modifier checks the `implementation` slot, which is set in the `EcoInitializable` constructor preventing any calls at all on contracts that are deployed directly. OpenZeppelin’s finding is correct, any account can make the one permissible call `initialize`, but there is no exposure here because either the `ForwardProxy` constructor or the `EcoInitializable` constructor always consumes the call.
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Eco Contracts Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/eco-contracts-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

