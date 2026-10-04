---
# Core Classification
protocol: Sparkn
chain: everychain
category: uncategorized
vulnerability_type: blacklisted

# Attack Vector Details
attack_type: blacklisted
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27423
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/cllcnja1h0001lc08z7w0orxx
source_link: none
github_link: https://github.com/Cyfrin/2023-08-sparkn

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
  - blacklisted
  - usdc

# Audit Details
report_date: unknown
finders_count: 25
finders:
  - Aamirusmani1552
  - bronzepickaxe
  - DevABDee
  - Tripathi
  - InAllHonesty
---

## Vulnerability Title

Blacklisted STADIUM_ADDRESS address cause fund stuck in the contract forever

### Overview


This bug report is about a vulnerability that occurs when the `STADIUM_ADDRESS` address is blacklisted by the token used for rewards. This leads to funds being stuck in the contract indefinitely, which is a high severity issue. The bug was found during a manual review of the code, and the relevant GitHub link is provided. 

The vulnerability occurs when the owner calls `setContest` with the correct `salt`. The organizer then sends USDC as rewards to a pre-determined Proxy address. If `STADIUM_ADDRESS` is blacklisted by the USDC operator, when the contest is closed, the Organizer calls `deployProxyAndDistribute` with the registered `contestId` and `implementation` to deploy a proxy and distribute rewards, but the call to `Distributor._commissionTransfer` reverts at Line 164 due to the blacklisting. This means the USDC held at the Proxy contract becomes stuck forever.

It is recommended to allow `STADIUM_ADDRESS` to be updatable by a dedicated admin role to avoid token transfer blacklisting. Additionally, since `STADIUM_ADDRESS` is no longer `immutable`, `storage` collision should be taken into account.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-08-sparkn/tree/main/src/Distributor.sol#L164">https://github.com/Cyfrin/2023-08-sparkn/tree/main/src/Distributor.sol#L164</a>


## Summary
The vulnerability relates to the immutability of `STADIUM_ADDRESS`. If this address is blacklisted by the token used for rewards, the system becomes unable to make transfers, leading to funds being stuck in the contract indefinitely.

## Vulnerability Details
1. Owner calls `setContest` with the correct `salt`.
2. The Organizer sends USDC as rewards to a pre-determined Proxy address.
3. `STADIUM_ADDRESS` is blacklisted by the USDC operator.
4. When the contest is closed, the Organizer calls `deployProxyAndDistribute` with the registered `contestId` and `implementation` to deploy a proxy and distribute rewards. However, the call to `Distributor._commissionTransfer` reverts at Line 164 due to the blacklisting.
5. USDC held at the Proxy contract becomes stuck forever.

```solidity
// Findings are labeled with '<= FOUND'
// File: src/Distributor.sol
116:    function _distribute(address token, address[] memory winners, uint256[] memory percentages, bytes memory data)
117:        ...
154:        _commissionTransfer(erc20);// <= FOUND
155:        ...
156:    }
				...
163:    function _commissionTransfer(IERC20 token) internal {
164:        token.safeTransfer(STADIUM_ADDRESS, token.balanceOf(address(this)));// <= FOUND: Blacklisted STADIUM_ADDRESS address cause fund stuck in the contract forever
165:    }
```

## Impact
This vulnerability is marked as High severity because a blacklisted `STADIUM_ADDRESS` would lead to funds being locked in the Proxy address permanently. Funds are already held in the Proxy, and the Proxy's `_implementation` cannot be changed once deployed. Even the `ProxyFactory.distributeByOwner()` function cannot rescue the funds due to the revert.

## Tools Used
Manual Review

## Recommendations
It is recommended to allow `STADIUM_ADDRESS` to be updatable by a dedicated admin role to avoid token transfer blacklisting. Moreover, since `STADIUM_ADDRESS` is no longer `immutable`, `storage` collision should be taken into account.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Sparkn |
| Report Date | N/A |
| Finders | Aamirusmani1552, bronzepickaxe, DevABDee, Tripathi, InAllHonesty, serialcoder, imkapadia, Magnetto, 0xhals, radeveth, Cosine, 0x4non, crippie, Kose, Madalad, castleChain, 33audits, dontonka, pep7siup, tsar, dipp, thekmj, MrjoryStewartBaxter |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-08-sparkn
- **Contest**: https://www.codehawks.com/contests/cllcnja1h0001lc08z7w0orxx

### Keywords for Search

`Blacklisted, USDC`

