---
# Core Classification
protocol: Amun
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6531
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-amun-contest
source_link: https://code4rena.com/reports/2021-12-amun
github_link: https://github.com/code-423n4/2021-12-amun-findings/issues/78

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
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - harleythedog
---

## Vulnerability Title

[M-09] Failed transfer with low level call could be overlooked

### Overview


This bug report is about a vulnerability in the `CallFacet.sol` contract, which is used in a lot of different places. The vulnerability is that the `_call` function does not check for the existence of the contract before calling it, which could lead to ether getting stuck in the contract if the user is interacting with a deleted contract. This vulnerability was reported in a Uniswap audit, and the recommended mitigation step is to check for the contract's existence prior to executing `_target.call`.

### Original Finding Content


_Submitted by harleythedog_

#### Impact

The `CallFacet.sol` contract has the function `_call` :

    function  _call(
    	address  _target,
    	bytes  memory  _calldata,
    	uint256  _value
    ) internal {
    	require(address(this).balance >= _value, "ETH_BALANCE_TOO_LOW");
    	(bool success, ) = _target.call{value: _value}(_calldata);
    	require(success, "CALL_FAILED");
    	emit  Call(msg.sender, _target, _calldata, _value);
    }

This function is utilized in a lot of different places. According to the [Solidity docs](<[https://docs.soliditylang.org/en/develop/control-structures.html#error-handling-assert-require-revert-and-exceptions](https://docs.soliditylang.org/en/develop/control-structures.html#error-handling-assert-require-revert-and-exceptions)>), "The low-level functions `call`, `delegatecall` and `staticcall` return `true` as their first return value if the account called is non-existent, as part of the design of the EVM. Account existence must be checked prior to calling if needed".

As a result, it is possible that this call will not work but `_call` will not notice anything went wrong. It could be possible that a user is interacting with an exchange or token that has been deleted, but `_call` will not notice that something has gone wrong and as a result, ether can become stuck in the contract. For this reason, it would be better to also check for the contract's existence prior to executing `_target.call`.

For reference, see a similar high severity reported in a Uniswap audit here (report # 9): <https://github.com/Uniswap/v3-core/blob/main/audits/tob/audit.pdf>

#### Proof of Concept

See `_call` here: [`CallFacet.sol` L108](https://github.com/code-423n4/2021-12-amun/blob/98f6e2ff91f5fcebc0489f5871183566feaec307/contracts/basket/contracts/facets/Call/CallFacet.sol#L108).

#### Recommended Mitigation Steps

To ensure tokens don't get stuck in edge case where user is interacting with a deleted contract, make sure to check that contract actually exists before calling it.

**[loki-sama (Amun) confirmed](https://github.com/code-423n4/2021-12-amun-findings/issues/78)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Amun |
| Report Date | N/A |
| Finders | harleythedog |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-amun
- **GitHub**: https://github.com/code-423n4/2021-12-amun-findings/issues/78
- **Contest**: https://code4rena.com/contests/2021-12-amun-contest

### Keywords for Search

`vulnerability`

