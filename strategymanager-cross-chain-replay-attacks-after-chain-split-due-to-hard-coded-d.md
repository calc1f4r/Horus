---
# Core Classification
protocol: EigenLabs — EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32156
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/03/eigenlabs-eigenlayer/
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - launchpad

# Audit Details
report_date: unknown
finders_count: 2
finders:
  -  Dominik Muhs
                        
  - Heiko Fisch
---

## Vulnerability Title

StrategyManager - Cross-Chain Replay Attacks After Chain Split  Due to Hard-Coded DOMAIN_SEPARATOR

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



*EigenLabs Quick Summary:*  

A. For the implementation of EIP-712 signatures, the domain separator is set in the initialization of the contract, which includes the chain ID. In the case of a chain split, this ID is subject to change. Thus the domain separator must be recomputed.  

B. The domain separator is calculated using `bytes("EigenLayer")` – the EIP-712 spec requires a keccak256 hash, i.e. `keccak256(bytes("EigenLayer"))`.  

C. The EIP712Domain does not include a version string.


*EigenLabs Response:*  

A. We have modified our implementation to dynamically check for the chain ID. If we detect a change since initialization, we recompute the domain separator. If not, we use the precomputed value.  

B. We changed our computation to use `keccak256(bytes("EigenLayer"))`.  

C. We decided that we would forgo this change for the time being.  

Changes in A. and B. implemented in this commit: [714dbb6](https://github.com/Layr-Labs/eigenlayer-contracts/pull/14/commits/714dbb61655aa9ecdc01bd3d66c2af4558a649a2).




#### Description


A. The `StrategyManager` contract allows stakers to deposit into and withdraw from strategies. A staker can either deposit themself or have someone else do it on their behalf, where the latter requires an EIP-712-compliant signature. The EIP-712 domain separator is computed in the `initialize` function and stored in a state variable for later retrieval:


**src/contracts/core/StrategyManagerStorage.sol:L23-L24**



```
/// @notice EIP-712 Domain separator
bytes32 public DOMAIN_SEPARATOR;

```
**src/contracts/core/StrategyManager.sol:L149-L153**



```
function initialize(address initialOwner, address initialStrategyWhitelister, IPauserRegistry _pauserRegistry, uint256 initialPausedStatus, uint256 _withdrawalDelayBlocks)
    external
    initializer
{
    DOMAIN_SEPARATOR = keccak256(abi.encode(DOMAIN_TYPEHASH, bytes("EigenLayer"), block.chainid, address(this)));

```
Once set in the `initialize` function, the value can’t be changed anymore. In particular, the chain ID is “baked into” the `DOMAIN_SEPARATOR` during initialization. However, it is not necessarily constant: In the event of a chain split, only one of the resulting chains gets to keep the original chain ID, and the other should use a new one. With the current approach to compute the `DOMAIN_SEPARATOR` during initialization, store it, and then use the stored value for signature verification, a signature will be valid on both chains after a split – but it should not be valid on the chain with the new ID. Hence, the domain separator should be computed dynamically.


B. The `name` in the `EIP712Domain` is of type `string`:


**src/contracts/core/StrategyManagerStorage.sol:L18-L19**



```
bytes32 public constant DOMAIN_TYPEHASH =
    keccak256("EIP712Domain(string name,uint256 chainId,address verifyingContract)");

```
What’s encoded when the domain separator is computed is `bytes("EigenLayer")`:


**src/contracts/core/StrategyManager.sol:L153**



```
DOMAIN_SEPARATOR = keccak256(abi.encode(DOMAIN_TYPEHASH, bytes("EigenLayer"), block.chainid, address(this)));

```
According to [EIP-712](https://eips.ethereum.org/EIPS/eip-712),



> The dynamic values `bytes` and `string` are encoded as a `keccak256` hash of their contents.


Hence, `bytes("EigenLayer")` should be replaced with `keccak256(bytes("EigenLayer"))`.


C. The `EIP712Domain` does not include a version string:


**src/contracts/core/StrategyManagerStorage.sol:L18-L19**



```
bytes32 public constant DOMAIN_TYPEHASH =
    keccak256("EIP712Domain(string name,uint256 chainId,address verifyingContract)");

```
That is allowed according to the specification. However, given that most, if not all, projects, as well as OpenZeppelin’s EIP-712 implementation, do include a version string in their `EIP712Domain`, it might be a pragmatic choice to do the same, perhaps to avoid potential incompatibilities.


#### Recommendation


Individual recommendations have been given above. Alternatively, you might want to utilize OpenZeppelin’s `EIP712Upgradeable` library, which will take care of these issues. **Note that some of these changes will break existing signatures.**

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | EigenLabs — EigenLayer |
| Report Date | N/A |
| Finders |  Dominik Muhs
                        , Heiko Fisch |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/03/eigenlabs-eigenlayer/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

