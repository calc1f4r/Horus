---
# Core Classification
protocol: ENS
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21873
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-04-ens
source_link: https://code4rena.com/reports/2023-04-ens
github_link: https://github.com/code-423n4/2023-04-ens-findings/issues/124

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
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MalfurionWhitehat
---

## Vulnerability Title

[M-07] Missing recursive calls handling in `OffchainDNSResolver` CCIP-aware contract

### Overview


This bug report is about the `resolveCallback` function from `OffchainDNSResolver`, which is used as part of the EIP-3668 standard to properly resolve DNS names using an off-chain gateway and validating RRsets against the DNSSEC oracle. The issue is that the function lacks proper error handling, specifically, a try/catch block to properly bubble up `OffchainLookup` error from the `dnsresolver` extracted from the RRset. This is in violation of the EIP, as it specifies that when a CCIP-aware contract wishes to make a call to another contract, and the possibility exists that the callee may implement CCIP read, the calling contract MUST catch all `OffchainLookup` errors thrown by the callee, and revert with a different error if the `sender` field of the error does not match the callee address.

The result of this bug would be an OffchainLookup that looks valid to the client, as the sender field matches the address of the contract that was called, but does not execute correctly. The proof of concept is as follows: Client calls `OffchainDNSResolver.resolve`, which reverts with `OffchainLookup`, and prompts the client to execute `resolveCallback` after having fetched the necessary data from the `gatewayURL`; the RRset returned by the gateway contains a `dnsresolver` that is a CCIP-aware contract, and also supports the `IExtendedDNSResolver.resolve.selector` interface; calling `IExtendedDNSResolver(dnsresolver).resolve(name,query,context);` could trigger another `OffchainLookup` error, but with a `sender` that does not match the `dnsresolver`, which would be just returned to the client without any modifications; as a result, the `sender` field would be incorrect as per the EIP.

In order to address this issue, it is recommended to use the recommended example from the EIP in order to support nested lookups. This has been confirmed by Arachnid (ENS).

### Original Finding Content


<https://github.com/code-423n4/2023-04-ens/blob/main/contracts/dnsregistrar/OffchainDNSResolver.sol#L109-L113><br>
<https://github.com/code-423n4/2023-04-ens/blob/main/contracts/dnsregistrar/OffchainDNSResolver.sol#L119>

The `resolveCallback` function from `OffchainDNSResolver` is used as part of the EIP-3668 standard to properly resolve DNS names using an off-chain gateway and validating RRsets against the DNSSEC oracle.

The issue is that the function lacks proper error handling, specifically, a try/catch block to properly bubble up `OffchainLookup` error from the `dnsresolver` extracted from the RRset. As the EIP specifies,

> *When a CCIP-aware contract wishes to make a call to another contract, and the possibility exists that the callee may implement CCIP read, the calling contract MUST catch all `OffchainLookup` errors thrown by the callee, and revert with a different error if the `sender` field of the error does not match the callee address.*<br>
> *\[...]*<br>
> *Where the possibility exists that a callee implements CCIP read, a CCIP-aware contract MUST NOT allow the default solidity behaviour of bubbling up reverts from nested calls.*

### Impact

As per the EIP, the result would be an OffchainLookup that looks valid to the client, as the sender field matches the address of the contract that was called, but does not execute correctly.

### Proof of Concept

1.  Client calls `OffchainDNSResolver.resolve`, which reverts with `OffchainLookup`, and prompts the client to execute `resolveCallback` after having fetched the necessary data from the `gatewayURL`
2.  The RRset returned by the gateway contains a `dnsresolver` that is a CCIP-aware contract, and also supports the `IExtendedDNSResolver.resolve.selector` interface
3.  Calling `IExtendedDNSResolver(dnsresolver).resolve(name,query,context);` could trigger another `OffchainLookup` error, but with a `sender` that does not match the `dnsresolver`, which would be just returned to the client without any modifications
4.  As a result, the `sender` field would be incorrect as per the EIP

### Recommended Mitigation Steps

Use the [recommended example](https://eips.ethereum.org/EIPS/eip-3668#example-1) from the EIP in order to support nested lookups.

**[Arachnid (ENS) confirmed](https://github.com/code-423n4/2023-04-ens-findings/issues/124#issuecomment-1536309975)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | ENS |
| Report Date | N/A |
| Finders | MalfurionWhitehat |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-ens
- **GitHub**: https://github.com/code-423n4/2023-04-ens-findings/issues/124
- **Contest**: https://code4rena.com/reports/2023-04-ens

### Keywords for Search

`vulnerability`

