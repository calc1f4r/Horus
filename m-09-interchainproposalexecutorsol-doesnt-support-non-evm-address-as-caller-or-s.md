---
# Core Classification
protocol: Axelar Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28769
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-axelar
source_link: https://code4rena.com/reports/2023-07-axelar
github_link: https://github.com/code-423n4/2023-07-axelar-findings/issues/25

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
  - bridge
  - services
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - UniversalCrypto
  - T1MOH
  - Chom
---

## Vulnerability Title

[M-09] `InterchainProposalExecutor.sol` doesn't support non-evm address as caller or sender

### Overview


Axelar supports different blockchain chains, such as Polkadot and Tron, with different address standards. However, these addresses can't be whitelisted in `InterchainProposalExecutor.sol` to execute proposals. This means that the `InterchainProposalSender` implementation from a non-EVM chain can't interact with `InterchainProposalExecutor.sol` on the EVM chain. Currently, `sourceAddress` is represented as `address`, not `string`. To fix this issue, the code should be changed so that `sourceAddress` is represented as `string` instead of `address`. Support for non-EVM addresses has been added and the relevant public pull requests can be viewed on GitHub.

### Original Finding Content


Axelar is supposed to support different chains, not only EVM. And these chains can have a different address standard like Polkadot or Tron. These addresses can't be whitelisted in `InterchainProposalExecutor.sol` to execute proposal. Thus, `InterchainProposalSender` implementation from non-EMV chain can't interact with `InterchainProposalExecutor.sol` on the EVM chain.

### Proof of Concept

Here, you can see that `sourceAddress` is represented as `address`, not `string`:

```solidity
    // Whitelisted proposal callers. The proposal caller is the contract that calls the `InterchainProposalSender` at the source chain.
    mapping(string => mapping(address => bool)) public whitelistedCallers;

    // Whitelisted proposal senders. The proposal sender is the `InterchainProposalSender` contract address at the source chain.
    mapping(string => mapping(address => bool)) public whitelistedSenders;

    ...

    /**
     * @dev Set the proposal caller whitelist status
     * @param sourceChain The source chain
     * @param sourceCaller The source caller
     * @param whitelisted The whitelist status
     */
    function setWhitelistedProposalCaller(
        string calldata sourceChain,
        address sourceCaller,
        bool whitelisted
    ) external override onlyOwner {
        whitelistedCallers[sourceChain][sourceCaller] = whitelisted;
        emit WhitelistedProposalCallerSet(sourceChain, sourceCaller, whitelisted);
    }

    /**
     * @dev Set the proposal sender whitelist status
     * @param sourceChain The source chain
     * @param sourceSender The source sender
     * @param whitelisted The whitelist status
     */
    function setWhitelistedProposalSender(
        string calldata sourceChain,
        address sourceSender,
        bool whitelisted
    ) external override onlyOwner {
        whitelistedSenders[sourceChain][sourceSender] = whitelisted;
        emit WhitelistedProposalSenderSet(sourceChain, sourceSender, whitelisted);
    }
```

### Recommended Mitigation Steps

Don't convert `sourceAddress` to `address`, use `string` instead.

```solidity
    // Whitelisted proposal callers. The proposal caller is the contract that calls the `InterchainProposalSender` at the source chain.
-   mapping(string => mapping(address => bool)) public whitelistedCallers;
+   mapping(string => mapping(string => bool)) public whitelistedCallers;

    // Whitelisted proposal senders. The proposal sender is the `InterchainProposalSender` contract address at the source chain.
-    mapping(string => mapping(address => bool)) public whitelistedSenders;
+    mapping(string => mapping(string => bool)) public whitelistedSenders;
```

### Assessed type

Invalid Validation

**[deanamiel (Axelar) confirmed and commented](https://github.com/code-423n4/2023-07-axelar-findings/issues/25#issuecomment-1695951653):**
 > Support has been added for non-EVM addresses.
 >
> Public PR links:<br>
> https://github.com/axelarnetwork/interchain-governance-executor/pull/21<br>
> https://github.com/axelarnetwork/interchain-governance-executor/pull/33

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Axelar Network |
| Report Date | N/A |
| Finders | UniversalCrypto, T1MOH, Chom |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-axelar
- **GitHub**: https://github.com/code-423n4/2023-07-axelar-findings/issues/25
- **Contest**: https://code4rena.com/reports/2023-07-axelar

### Keywords for Search

`vulnerability`

