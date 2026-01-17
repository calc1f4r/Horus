---
# Core Classification
protocol: Open Dollar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29359
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-opendollar
source_link: https://code4rena.com/reports/2023-10-opendollar
github_link: https://github.com/code-423n4/2023-10-opendollar-findings/issues/187

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
finders_count: 13
finders:
  - ni8mare
  - 0xhacksmithh
  - kutugu
  - bitsurfer
  - twicek
---

## Vulnerability Title

[M-11] Test addresses and incorrect interface in code prevent integration with UniswapV3 and Camelot

### Overview


This bug report is about the testing addresses for Camelot and UniswapV3 factories still being used in the code, which will prevent integration with UniswapV3 and Camelot. The addresses in the code are set to Goerli addresses instead of Mainnet, and the correct interface to get the `camelotPair` is also commented out. The severity of this bug was determined to be medium. The recommended mitigation steps suggest that the protocol team make the changes necessary to be compatible with Arbitrum One. Additionally, it was suggested that there may be a better way to manage this than manually changing the constant variable in the Registry.

### Original Finding Content


Testing addresses for Camelot and UniswapV3 factories are still used in the code:

[CamelotRelayer.sol#L20](https://github.com/open-dollar/od-contracts/blob/f4f0246bb26277249c1d5afe6201d4d9096e52e6/src/contracts/oracles/CamelotRelayer.sol#L20)

```solidity
  address internal constant _CAMELOT_FACTORY = GOERLI_CAMELOT_V3_FACTORY;
```

[UniV3Relayer.sol#L18](https://github.com/open-dollar/od-contracts/blob/f4f0246bb26277249c1d5afe6201d4d9096e52e6/src/contracts/oracles/UniV3Relayer.sol#L18)

```solidity
  address internal constant _UNI_V3_FACTORY = GOERLI_UNISWAP_V3_FACTORY;
```

Additionally, the correct interface to get the `camelotPair` is commented out:

[CamelotRelayer.sol#L41-L42](https://github.com/open-dollar/od-contracts/blob/f4f0246bb26277249c1d5afe6201d4d9096e52e6/src/contracts/oracles/CamelotRelayer.sol#L41-L42)

```solidity
    // camelotPair = ICamelotFactory(_CAMELOT_FACTORY).getPair(_baseToken, _quoteToken);
    camelotPair = IAlgebraFactory(_CAMELOT_FACTORY).poolByPair(_baseToken, _quoteToken);
```

### Impact

It will prevent integration with UniswapV3 and Camelot.

### Recommended Mitigation Steps

Make the changes necessary to be compatible with Arbitrum One.

**[MiloTruck (Judge) commented](https://github.com/code-423n4/2023-10-opendollar-findings/issues/187#issuecomment-1790139769):**
 > While the protocol team is most likely aware of this and these addresses are probably set to testnet ones currently for testing purposes, it is an undeniable fact that if the current code was to be deployed without any modifications, the `CamelotRelayer` and `UniV3Relayer` contracts would not function as expected.
> 
> As such, I believe medium severity is appropriate.

**[pi0neerpat (OpenDollar) commented](https://github.com/code-423n4/2023-10-opendollar-findings/issues/187#issuecomment-1805211162):**
 > The problem stated is that the Camelot and Uniswap factory addresses set in the Registry are set to Goerli addresses, not Mainnet. In production, we will swap Goerli addresses for Mainnet. Perhaps there is a better way to manage this than manually changing the constant variable in the Registry, however the recommendation does provide a helpful suggestion.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Open Dollar |
| Report Date | N/A |
| Finders | ni8mare, 0xhacksmithh, kutugu, bitsurfer, twicek, pep7siup, 1, 2, spark, Arz, btk |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-opendollar
- **GitHub**: https://github.com/code-423n4/2023-10-opendollar-findings/issues/187
- **Contest**: https://code4rena.com/reports/2023-10-opendollar

### Keywords for Search

`vulnerability`

