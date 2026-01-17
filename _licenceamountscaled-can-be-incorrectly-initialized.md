---
# Core Classification
protocol: TokenCard
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16888
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/TokenCard.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/TokenCard.pdf
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
  - Michael Colburn | Trail of Bits Gustavo Grieco | Trail of Bits John Dunlap | Trail of Bits
---

## Vulnerability Title

_licenceAmountScaled can be incorrectly initialized

### Overview

See description below for full details.

### Original Finding Content

## Denial of Service

**Type:** Denial of Service  
**Target:** wallet.sol  

**Diﬃculty:** High  

## Description

The licence contract collects a percentage fee when a user loads her card. The fee percentage is recorded in the `_licenceAmountScaled` state variable. This state variable can be initialized during the contract deployment as shown in Figure 1 or updated using `updateLicenceAmount` as shown in Figure 2.

```solidity
constructor(
    address _owner_,
    bool _transferable_,
    uint _licence_,
    address _float_,
    address _holder_,
    address _tknAddress_
) Ownable(_owner_, _transferable_) public {
    _licenceAmountScaled = _licence_;
    _cryptoFloat = _float_;
    _tokenHolder = _holder_;
    if (_tknAddress_ != address(0)) {
        _tknContractAddress = _tknAddress_;
    }
}
```
_Figure 8.1: Constructor of licence contract_

```solidity
function updateLicenceAmount(uint _newAmount) external onlyDAO {
    require(1 <= _newAmount && _newAmount <= MAX_AMOUNT_SCALE, "licence amount out of range");
    _licenceAmountScaled = _newAmount;
    emit UpdatedLicenceAmount(_newAmount);
}
```
_Figure 8.2: updateLicenceAmount function_

When `_licenceAmountScaled` is updated after initialization, the contract performs a sanity check to make sure the new value is a reasonable amount. However, `_licenceAmountScaled` can be set to any unsigned integer value in the call to the contract constructor. This allows for no licence fee to be set upon initialization, which is explicitly disallowed when updating the licence amount.

## Exploit Scenario

When deploying the contract, there is a typo in the licence parameter. Instead of a 0.5% fee, the contract is deployed with a 50% fee. Any users loading their cards before this mistake is noticed will pay excessively high fees.

## Recommendation

- **Short term:** Add a validation check when initially setting `_licenceAmountScaled`.
- **Long term:** Ensure validation is carried out for relevant parameters when developing new contracts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | TokenCard |
| Report Date | N/A |
| Finders | Michael Colburn | Trail of Bits Gustavo Grieco | Trail of Bits John Dunlap | Trail of Bits |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/TokenCard.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/TokenCard.pdf

### Keywords for Search

`vulnerability`

