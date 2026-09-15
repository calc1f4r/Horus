---
# Core Classification
protocol: GoGoPool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8831
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-gogopool-contest
source_link: https://code4rena.com/reports/2022-12-gogopool
github_link: https://github.com/code-423n4/2022-12-gogopool-findings/issues/702

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 20
finders:
  - dic0de
  - jadezti
  - HollaDieWaldfee
  - Faith
  - simon135
---

## Vulnerability Title

[M-04] requireNextActiveMultisig will always return the first enabled multisig which increases the probability of stuck minipools

### Overview


This bug report is regarding a vulnerability in the code of the project 2022-12-gogopool. The vulnerability increases the probability of funds being stuck if the same address is always returned by the function `requireNextActiveMultisig`. The proof of concept is provided in the report, and can be found in the link. 

The impact of this vulnerability is that the probability of funds being stuck increases if `requireNextActiveMultisig` always returns the same address. 

The recommended mitigation step is to use a strategy such as round robin to assign the next active multisig to the minipool. The code for this is provided in the report. 

In conclusion, this bug report is about a vulnerability in the code which can lead to funds being stuck, and the recommended mitigation step is to use a round robin strategy to assign the next active multisig to the minipool.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-12-gogopool/blob/aec9928d8bdce8a5a4efe45f54c39d4fc7313731/contracts/contract/MultisigManager.sol#L80-L91


## Vulnerability details


For every created minipool a multisig address is set to continue validator interactions.

Every minipool multisig address get assigned by calling `requireNextActiveMultisig`.

This function always return the first enabled multisig address.

In case the specific address is disabled all created minipools will be stuck with this address which increase the probability of also funds being stuck.

## Impact
Probability of funds being stuck increases if `requireNextActiveMultisig` always return the same address.

## Proof of Concept
https://github.com/code-423n4/2022-12-gogopool/blob/aec9928d8bdce8a5a4efe45f54c39d4fc7313731/contracts/contract/MultisigManager.sol#L80-L91

## Tools Used
Manual review

## Recommended Mitigation Steps
Use a strategy like [round robin](https://en.wikipedia.org/wiki/Round-robin_item_allocation) to assign next active multisig to minipool

Something like this :

```solidity
private uint nextMultisigAddressIdx;

function requireNextActiveMultisig() external view returns (address) {
    uint256 total = getUint(keccak256("multisig.count"));
    address addr;
    bool enabled;

    uint256 i = nextMultisigAddressIdx; // cache last used
    if (nextMultisigAddressIdx==total) {
        i = 0;
    }

    for (; i < total; i++) {
        (addr, enabled) = getMultisig(i);
        if (enabled) {
            nextMultisigAddressIdx = i+1;
            return addr;
        }
    }
    
    revert NoEnabledMultisigFound();
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | GoGoPool |
| Report Date | N/A |
| Finders | dic0de, jadezti, HollaDieWaldfee, Faith, simon135, enckrish, kaliberpoziomka8552, 0xbepresent, Jeiwan, sk8erboy, Saintcode_, betweenETHlines, gz627, nogo, imare, AkshaySrivastav, btk, 0Kage |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-gogopool
- **GitHub**: https://github.com/code-423n4/2022-12-gogopool-findings/issues/702
- **Contest**: https://code4rena.com/contests/2022-12-gogopool-contest

### Keywords for Search

`vulnerability`

