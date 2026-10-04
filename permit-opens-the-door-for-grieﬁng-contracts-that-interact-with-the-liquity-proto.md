---
# Core Classification
protocol: Liquity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18025
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Gustavo Grieco
  - Alexander Remie
  - Maximilian Krüger
  - Michael Colburn
---

## Vulnerability Title

Permit opens the door for grieﬁng contracts that interact with the Liquity Protocol

### Overview

See description below for full details.

### Original Finding Content

## Data Validation

**Target:** TroveManager.sol

**Difficulty:** Low

## Description

The `permit` function can be front-run to break the workflow from third-party smart contracts. The Liquity ERC20 contracts implement `permit`, which allows the allowance of a user to be changed based on a signature check using `ecrecover`:

```solidity
function permit(
    address owner,
    address spender,
    uint amount,
    uint deadline,
    uint8 v,
    bytes32 r,
    bytes32 s
) external override {
    require(deadline == 0 || deadline >= now, 'LUSD: Signature has expired');
    bytes32 digest = keccak256(abi.encodePacked(uint16(0x1901), domainSeparator(), keccak256(abi.encode(
        _PERMIT_TYPEHASH, owner, spender, amount, _nonces[owner]++, deadline))));
    address recoveredAddress = ecrecover(digest, v, r, s);
    require(recoveredAddress != address(0) && recoveredAddress == owner, 'LUSD: Recovered address from the sig is not the owner');
    _approve(owner, spender, amount);
}
```

_Figure 8.1: `permit` in `LUSDToken.sol`._

While this function is correctly implemented in terms of functionality, there is a potential security issue users must be aware of when developing contracts to interact with Liquity tokens:

## Security Considerations

Though the signer of a `Permit` may have a certain party in mind to submit their transaction, another party can always front-run this transaction and call `permit` before the intended party. The end result is the same for the `Permit` signer, however.

_Figure 8.2: Security considerations for ERC2612._

## Exploit Scenario

Alice develops a smart contract that leverages `permit` to perform a `transferFrom` of LUSD without requiring a user to call `approve` first. Eve monitors the blockchain and notices this call to `permit`. She observes the signature and replays it to front-run her call, which produces a revert in Alice’s contract and halts its expected execution.

## Recommendation

Short term, properly document the possibility of griefing `permit` calls to warn users interacting with Liquity tokens. This will allow users to anticipate this possibility and develop alternate workflows in case they are targeted by it.

Long term, carefully monitor the blockchain to detect front-running attempts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Liquity |
| Report Date | N/A |
| Finders | Gustavo Grieco, Alexander Remie, Maximilian Krüger, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf

### Keywords for Search

`vulnerability`

