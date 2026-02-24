---
# Core Classification
protocol: Beanstalk
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31198
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
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

protocol_categories:
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator
  - privacy

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Alex Roan
  - Giovanni Di Siena
  - Carlos Amarante
---

## Vulnerability Title

`LibTokenPermit` logic is susceptible to signature replay attacks in the case of a hard fork

### Overview


Report Summary:

A bug has been found in the implementation of a function called `_buildDomainSeparator` in the `LibTokenPermit` library of the Beanstalk protocol. This function uses a static constant called `CHAIN_ID` from another contract called `C.sol` to generate a unique identifier for each transaction. However, this can lead to a signature replay attack on a forked chain, where signed permits from the Ethereum mainnet can be used on the forked chain. This could potentially affect the liquidity of BEAN, as it has a portion of its liquidity in WETH. To mitigate this issue, it is recommended to modify the `_buildDomainSeparator` function to read the current chain ID directly from the `block.chainid` global context variable. It is also suggested to cache the current chain ID on contract creation for gas efficiency. 

### Original Finding Content

**Description:** Due to the implementation of [`LibTokenPermit::_buildDomainSeparator`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Token/LibTokenPermit.sol#L59-L69) using the static `CHAIN_ID` [constant](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Token/LibTokenPermit.sol#L65) specified in [`C.sol`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/C.sol#L92-L94), in the case of a hard fork, all signed permits from Ethereum mainnet can be replayed on the forked chain.

**Impact:** A signature replay attack on the forked chain means that any signed permit given to an address on one of the chains can be re-used on the other as long as the account nonce is respected. Given that BEAN has a portion of its liquidity in WETH, it could be susceptible to some parallelism with the [Omni Bridge calldata replay exploit](https://medium.com/neptune-mutual/decoding-omni-bridges-call-data-replay-exploit-f1c7e339a7e8) on ETHPoW.

**Recommended Mitigation:** Modify the `_buildDomainSeparator` implementation to read the current `block.chainid` global context variable directly. If gas efficiency is desired, it is recommended to cache the current chain id on contract creation and only recompute the domain separator if a change of chain id is detected (i.e. `block.chainid` != cached chain id).

```diff
    function _buildDomainSeparator(bytes32 typeHash, bytes32 name, bytes32 version) internal view returns (bytes32) {
        return keccak256(
            abi.encode(
                typeHash,
                name,
                version,
-               C.getChainId(),
+               block.chainid,
                address(this)
            )
        );
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Beanstalk |
| Report Date | N/A |
| Finders | Alex Roan, Giovanni Di Siena, Carlos Amarante |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

