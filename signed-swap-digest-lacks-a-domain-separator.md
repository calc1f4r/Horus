---
# Core Classification
protocol: Uniswap Foundation:
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63032
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Kyber-Hook-Uniswap-Foundation-Spearbit-Security-Review-October-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Kyber-Hook-Uniswap-Foundation-Spearbit-Security-Review-October-2025.pdf
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

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - R0bert
  - Alireza Arjmand
  - 0xluk3
  - Akshay Srivastav
---

## Vulnerability Title

Signed swap digest lacks a domain separator

### Overview


This bug report describes an issue with two smart contracts, called `UniswapV4KEMHook` and `PancakeSwapInfinityKEMHook`, that are used for trading on different blockchain networks. These contracts use a method of creating a unique code, called a "digest", to verify the authenticity of a trade. However, this method does not include important information such as the network and contract identity, which means that an attacker can use a valid signature from one network and use it on another network, causing unintended trades to occur. The recommendation is to add this missing information to the digest to prevent these attacks. Kyber and Spearbit have acknowledged the issue and are working on implementing a solution.

### Original Finding Content

## Severity: Medium Risk

## Context
- PancakeSwapInfinityKEMHook.sol#L124-L135
- UniswapV4KEMHook.sol#L118-L129

## Description
Both `UniswapV4KEMHook` and `PancakeSwapInfinityKEMHook` rebuild a quote digest by hashing:

```
keccak256(
    abi.encode(
        sender,
        key,
        params.zeroForOne,
        maxAmountIn,
        maxExchangeRate,
        exchangeRateDenom,
        nonce,
        expiryTime
    )
);
```

The tuple ties the authorization to the router (`sender`), the full `PoolKey` (which includes the hook address), trade direction, price and input caps, nonce, and expiry. Crucially, no domain separator is folded in: chain ID, deployment salt, and contract identity outside key are absent. 

If the same hook instance (or the same `PoolKey`) is deployed on multiple networks, as `CREATE3`-based salt mining allows, an attacker can lift any valid signature + nonce from chain A and replay it on chain B. Because the digest matches, `SignatureChecker.isValidSignatureNow` succeeds and the swap executes without the signer's intention. That breaks the core guarantee that signed quotes are single-instance authorizations, allowing cross-chain replay swaps.

## Recommendation
Introduce domain separation for the signed payload in both hooks. Adopt an EIP712 domain that at minimum commits to `chainid`.

## Kyber: Acknowledged.
- The quote has a very short expiry time and only affects the `EG` amount, not `poolFee`.
- To avoid the operational costs and LP migration burden of redeployment across chains, we will implement chain-specific operator signing keys as a mitigation measure.

## Spearbit: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Uniswap Foundation: |
| Report Date | N/A |
| Finders | R0bert, Alireza Arjmand, 0xluk3, Akshay Srivastav |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Kyber-Hook-Uniswap-Foundation-Spearbit-Security-Review-October-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Kyber-Hook-Uniswap-Foundation-Spearbit-Security-Review-October-2025.pdf

### Keywords for Search

`vulnerability`

