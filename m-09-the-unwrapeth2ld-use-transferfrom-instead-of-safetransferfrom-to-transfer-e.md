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
solodit_id: 5553
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-ens-contest
source_link: https://code4rena.com/reports/2022-07-ens
github_link: https://github.com/code-423n4/2022-07-ens-findings/issues/157

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
finders_count: 9
finders:
  - rbserver
  - cccz
  - CRYP70
  - berndartmueller
  - RedOneN
---

## Vulnerability Title

[M-09] The `unwrapETH2LD` use `transferFrom` instead of `safeTransferFrom` to transfer ERC721 token

### Overview


This bug report is about a vulnerability in the `unwrapETH2LD` function in the NameWrapper.sol contract. The vulnerability occurs when the `newRegistrant` is an unprepared contract. This could result in the ERC721 token being locked up in the unprepared contract. The proof of concept is that the OZ safeTransfer comments explicitly discourage the usage of this method. The recommended mitigation steps are to change the `registrar.transferFrom` to `registrar.safeTransferFrom` in the code. This will ensure that the tokens are safely transferred to the unprepared contract.

### Original Finding Content


[NameWrapper.sol#L327-L346](https://github.com/code-423n4/2022-07-ens/blob/ff6e59b9415d0ead7daf31c2ed06e86d9061ae22/contracts/wrapper/NameWrapper.sol#L327-L346)<br>

The `unwrapETH2LD` use `transferFrom` to transfer ERC721 token, the `newRegistrant` could be an unprepared contract.

### Proof of Concept

Should a ERC-721 compatible token be transferred to an unprepared contract, it would end up being locked up there. Moreover, if a contract explicitly wanted to reject ERC-721 safeTransfers.<br>
Plus take a look to [the OZ safeTransfer comments](https://docs.openzeppelin.com/contracts/4.x/api/token/erc721#IERC721-transferFrom-address-address-uint256-):<br>
`Usage of this method is discouraged, use safeTransferFrom whenever possible.`

### Recommended Mitigation Steps

```diff
    function unwrapETH2LD(
        bytes32 labelhash,
        address newRegistrant,
        address newController
    ) public override onlyTokenOwner(_makeNode(ETH_NODE, labelhash)) {
        _unwrap(_makeNode(ETH_NODE, labelhash), newController);
-       registrar.transferFrom(
+       registrar.safeTransferFrom(
            address(this),
            newRegistrant,
            uint256(labelhash)
        );
    }
```

**[jefflau (ENS) disputed and commented](https://github.com/code-423n4/2022-07-ens-findings/issues/157#issuecomment-1196450983):**
 > Transfer is to the contract itself, so there is no point in using `safeTransferFrom`. For other situations where `transferFrom` the behaviour is intended.

**[LSDan (judge) commented](https://github.com/code-423n4/2022-07-ens-findings/issues/157#issuecomment-1204004769):**
 > > Transfer is to the contract itself, so there is no point in using `safeTransferFrom`. For other situations where `transferFrom` the behaviour is intended.
> 
> That's incorrect in the report above. This is transferring from, not to, the contract itself.

**[jefflau (ENS) commented](https://github.com/code-423n4/2022-07-ens-findings/issues/157#issuecomment-1204016628):**
 > > That's incorrect in the report above. This is transferring from, not to, the contract itself.
> 
> Yes sorry, that is true. I was replying to some of the duplicates that I closed such as: [#126](https://github.com/code-423n4/2022-07-ens-findings/issues/126), [#147](https://github.com/code-423n4/2022-07-ens-findings/issues/147). 



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
| Finders | rbserver, cccz, CRYP70, berndartmueller, RedOneN, benbaessler, 0x29A, Amithuddar, Sm4rty |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-ens
- **GitHub**: https://github.com/code-423n4/2022-07-ens-findings/issues/157
- **Contest**: https://code4rena.com/contests/2022-07-ens-contest

### Keywords for Search

`vulnerability`

