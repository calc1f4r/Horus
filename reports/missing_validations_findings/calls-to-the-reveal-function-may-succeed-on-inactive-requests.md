---
# Core Classification
protocol: Pyth Data Association Entropy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37881
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-01-pyth-entropy-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-01-pyth-entropy-securityreview.pdf
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
finders_count: 2
finders:
  - Tjaden Hess
  - Elvis Skoždopolj
---

## Vulnerability Title

Calls to the reveal function may succeed on inactive requests

### Overview

See description below for full details.

### Original Finding Content

## Entropy Security Assessment

## Difficulty: Not Applicable

## Type:
Testing

## Target: Entropy.sol

### Description

Revealing inactive Entropy requests may succeed due to missing validation, allowing requests with a sequence number of zero to be revealed. The Entropy contract uses a commitment-and-reveal scheme to generate random numbers. Users can request a random number from any registered randomness provider by using the `request` function, and once the provider has shared their secret with them, they can reveal the resulting random number by calling the `reveal` function. This function finds the corresponding request based on the provider address and the request sequence number, performs validation on it, and then finally clears the request so that it cannot be reexecuted, as shown in **Figure 10.1**.

```solidity
function reveal (
    address provider,
    uint64 sequenceNumber,
    bytes32 userRandomness,
    bytes32 providerRevelation
) public override returns (bytes32 randomNumber) {
    EntropyStructs.Request storage req = findRequest(
        provider,
        sequenceNumber
    );
    
    // Check that there is a request for the given provider/sequence number.
    if (req.provider != provider || req.sequenceNumber != sequenceNumber)
        revert EntropyErrors.NoSuchRequest();
    if (req.requester != msg.sender) revert EntropyErrors.Unauthorized();
    [...]
    clearRequest(provider, sequenceNumber);
    [...]
}
```

**Trail of Bits**

**Figure 10.1:** The `reveal` function of Entropy.sol

The `findRequest` function generates the request keys—the short key representing an index in the `_state.requests` fixed-size array and the key representing a key in the `_state.requestsOverflow` mapping—and matches one of the requests, as shown in **Figure 10.2**.

```solidity
function findRequest (
    address provider,
    uint64 sequenceNumber
) internal view returns (EntropyStructs.Request storage req) {
    (bytes32 key, uint8 shortKey) = requestKey(provider, sequenceNumber);
    req = _state.requests[shortKey];
    
    if (req.provider == provider && req.sequenceNumber == sequenceNumber) {
        return req;
    } else {
        req = _state.requestsOverflow[key];
    }
}
```

**Figure 10.2:** The `findRequest` function of Entropy.sol

When clearing a request at the end of a reveal, the `clearRequest` function either deletes the request from the `_state.requestsOverflow` mapping or invalidates it by setting the sequence number of the request to zero, as shown in **Figure 10.3**.

```solidity
function clearRequest(address provider, uint64 sequenceNumber) internal {
    (bytes32 key, uint8 shortKey) = requestKey(provider, sequenceNumber);
    EntropyStructs.Request storage req = _state.requests[shortKey];
    
    if (req.provider == provider && req.sequenceNumber == sequenceNumber) {
        req.sequenceNumber = 0;
    } else {
        delete _state.requestsOverflow[key];
    }
}
```

**Figure 10.3:** The `clearRequest` function of Entropy.sol

However, while a request with a sequence number of zero is considered inactive, the `reveal` function does not revert if sequence number zero is passed as an input to the function. Since the `_state.requests` fixed-sized array has a size of 32 elements, it is reasonable to assume that two different sequence numbers could result in the same short key, allowing inactive requests to be revealed.

### Recommendations

- **Short term:** Add validation to the `reveal` function to ensure that it reverts if the sequence number is zero.
  
- **Long term:** Use advanced testing techniques such as fuzzing to more easily discover issues such as this. Defining a property that an inactive request cannot be revealed and using Echidna to test the property could help discover this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Pyth Data Association Entropy |
| Report Date | N/A |
| Finders | Tjaden Hess, Elvis Skoždopolj |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-01-pyth-entropy-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-01-pyth-entropy-securityreview.pdf

### Keywords for Search

`vulnerability`

