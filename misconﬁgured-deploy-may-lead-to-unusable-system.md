---
# Core Classification
protocol: Sai
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17268
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/sai.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/sai.pdf
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
finders_count: 6
finders:
  - Josselin Feist
  - 2017: December 15
  - 2018: Initial report delivered
  - Mark Mossberg
  - Changelog October 24
---

## Vulnerability Title

Misconﬁgured deploy may lead to unusable system

### Overview

See description below for full details.

### Original Finding Content

## Type: Business Logic  
**Target: SaiTub**  

### Difficulty: Low  

### Description  
The `hat` SaiTub state variable is the system parameter controlling the Sai debt ceiling. It is of type `uint256` and never explicitly initialized, thus taking an initial value of zero. This variable is used to enforce the debt ceiling in `SaiTub.draw` (tub.sol:228), which mints Sai.  

```solidity
require(sin.totalSupply() <= hat);
```

If `hat` is not initialized, this `require` will always fail, since `sin.totalSupply()` will always be greater than zero at this point. While `hat` is uninitialized, it will be impossible for CDP users to generate Sai.  

The `hat` variable can only be set via `SaiTub.mold`, which serves as the administration interface for configuring the various SaiTub parameters. This interface should be used in the deploy scripts to ensure that a debt ceiling is always set for the system. However, it is never referenced in any of the deploy scripts in `bin/`. In `bin/deploy-live-public` there is code to configure system parameters which uses `sai cork` with the intention of setting `hat`. The `sai cork` command, however, calls the `SaiTub.cork` interface (sai-cork:8), which does not exist, so this will have no effect.  

```bash
(set -x; seth send "${SAI_TUB?}" "cork(uint256)" "$wad")
```

Additionally, in `bin/deploy-live-public` there appear to be two other uses of non-existent configuration interfaces: `sai cuff` and `sai chop`, which call `SaiTub.cuff` and `SaiTub.chop` respectively. These will also have no effect.  

The `bin/validate-deployment` script is an effective way to verify the state of a newly deployed Sai system. However, the specific `hat` value it checks for (5000000) appears to be inconsistent with the value attempted to be set in `bin/deploy-live-public` (100000000).  

```bash
validate-deployment:14
test $(sai hat) = $(sai wad -h 5000000.0)
deploy-live-public:32
sai cork 100000000.00
```

### Exploit Scenario  
Sai is deployed using flawed deployment scripts which leave the debt ceiling unspecified. Sai users immediately begin to interact with the system, converting Ether to SKR, opening CDPs, and locking SKR into them as collateral. They attempt to draw Sai from the system, find that they cannot, and lose trust in the Sai platform.  

### Recommendation  
In the short term, ensure that the configuration interfaces used by deployment code match those in Sai.  

For long-term confidence in the correctness of the deployment code, use automated means of checking a deployment; the existing `validate-deployment` script is an excellent start towards this. Consider automatically invoking it at the end of the deployment process to be aware of faulty deployment as soon as possible. Going further, it should be possible to express the parameters that the deploy system will set in a format that can be checked for invariants (e.g. `hat` is set, and is nonzero) prior to deployment of the system.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Sai |
| Report Date | N/A |
| Finders | Josselin Feist, 2017: December 15, 2018: Initial report delivered, Mark Mossberg, Changelog October 24, 2017: Added Appendix E with retest results Public release January 31 |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/sai.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/sai.pdf

### Keywords for Search

`vulnerability`

