---
# Core Classification
protocol: Swivel
chain: everychain
category: uncategorized
vulnerability_type: ecrecover

# Attack Vector Details
attack_type: ecrecover
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 870
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-swivel-contest
source_link: https://code4rena.com/reports/2021-09-swivel
github_link: https://github.com/code-423n4/2021-09-swivel-findings/issues/61

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:
  - ecrecover

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - cmichel
  - 0xRajeev
  - gpersoon
  - nikitastupin.
---

## Vulnerability Title

[H-04] return value of 0 from ecrecover not checked

### Overview


This bug report is about a vulnerability in the Solidity function ecrecover. The error result of 0 is not checked for, which can lead to unexpected transactions. This can be seen in the Proof of Concept code provided in the report. To mitigate this vulnerability, it is recommended to verify that the result from ecrecover isn't 0. This will help prevent any unexpected transactions from occurring.

### Original Finding Content

_Submitted by gpersoon, also found by 0xRajeev, cmichel, and nikitastupin_.

#### Impact

The solidity function `ecrecover` is used, however the error result of 0 is not checked for.
See documentation:
<https://docs.soliditylang.org/en/v0.8.9/units-and-global-variables.html?highlight=ecrecover#mathematical-and-cryptographic-functions>
"recover the address associated with the public key from elliptic curve signature or return zero on error. "

Now you can supply invalid input parameters to the `Sig.recover` function, which will then result 0.
If you also set `o.maker` to be 0 then this will match and an invalid signature is not detected.

So you can do all kinds of illegal & unexpected transactions.

#### Proof of Concept

<https://github.com/Swivel-Finance/gost/blob/v2/test/swivel/Swivel.sol#L476-L484>
```solidity
  function validOrderHash(Hash.Order calldata o, Sig.Components calldata c) internal view returns (bytes32) {
  ...
  require(o.maker == Sig.recover(Hash.message(domain, hash), c), 'invalid signature');
  return hash;
  }
```

<https://github.com/Swivel-Finance/gost/blob/v2/test/swivel/Sig.sol#L16-L23>
```solidity
  function recover(bytes32 h, Components calldata c) internal pure returns (address) {
  ...
  return ecrecover(h, c.v, c.r, c.s);
```

#### Tools Used

#### Recommended Mitigation Steps

Verify that the result from `ecrecover` isn't 0

**[JTraversa (Swivel) acknowledged](https://github.com/code-423n4/2021-09-swivel-findings/issues/61)**
**[JTraversa (Swivel) commented](https://github.com/code-423n4/2021-09-swivel-findings/issues/61#issuecomment-961456683):**
> Id say this is noteable, but because all actions require approvals from o.maker, having 0x00 as o.maker with an "invalid" but valid signature should not be impactful.
> The suggestion would be to filter 0x00 makers from the orderbook? (which we do)

 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Swivel |
| Report Date | N/A |
| Finders | cmichel, 0xRajeev, gpersoon, nikitastupin. |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-swivel
- **GitHub**: https://github.com/code-423n4/2021-09-swivel-findings/issues/61
- **Contest**: https://code4rena.com/contests/2021-09-swivel-contest

### Keywords for Search

`ecrecover`

