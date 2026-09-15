---
# Core Classification
protocol: Yield Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16967
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/YieldProtocol.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/YieldProtocol.pdf
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
finders_count: 1
finders:
  - Gustavo Grieco | ​Trail of Bits Michael Colburn | ​Trail of Bits
---

## Vulnerability Title

​pot.chi()

### Overview

See description below for full details.

### Original Finding Content

## Data Validation

## Target
**YDai.sol**

## Difficulty
**Low**

## Description
The Yield contracts interact with the Dai Savings Rate (DSR) contracts from MakerDAO to obtain the rate accumulator value without properly calling a function to update its value. DSR works using the pot contracts from MakerDAO. Once these contracts are deployed, they require the drip function to be called in order to update the accumulated interest rate:

![Figure 3.1: pot](https://makerdao.com/)

The Yield Protocol uses DSR. In particular, YDai uses the pot contracts directly to provide interest to its users:

```solidity
/// @dev Mature yDai and capture chi and rate
function mature() public override {
    require(
        // solium-disable-next-line security/no-block-members
        now > maturity,
        "YDai: Too early to mature"
    );
    require(
        isMature != true,
        "YDai: Already matured"
    );
    (, rate0,,,) = _vat.ilks(WETH); // Retrieve the MakerDAO Vat
    rate0 = Math.max(rate0, UNIT); // Floor it at 1.0
    chi0 = _pot.chi();
    isMature = true;
    emit Matured(rate0, chi0);
}
```
*Figure 3.1: mature function in YDai.*

However, the drip function is never called on any contract. It could be called manually by the users or the Yield off-chain components; however, this was not documented.

## Exploit Scenario
Alice locks DAI in a fyDAI token expecting to obtain a certain interest rate. However, the call to drip is never performed, so Alice obtains less interest than expected after the fyDAI token matures.

## Recommendation
**Short term:** Add a call to `pot.drip` every time the `pot.chi` is used. This will ensure that users receive the correct amount of interest after maturation.

**Long term:** Review every interaction with the MakerDAO contracts to make sure your code works as expected.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Yield Protocol |
| Report Date | N/A |
| Finders | Gustavo Grieco | ​Trail of Bits Michael Colburn | ​Trail of Bits |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/YieldProtocol.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/YieldProtocol.pdf

### Keywords for Search

`vulnerability`

