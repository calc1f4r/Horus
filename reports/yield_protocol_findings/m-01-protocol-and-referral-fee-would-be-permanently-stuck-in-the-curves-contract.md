---
# Core Classification
protocol: Curves Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35082
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-01-curves
source_link: https://code4rena.com/reports/2024-01-curves
github_link: https://github.com/code-423n4/2024-01-curves-findings/issues/1294

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

# Audit Details
report_date: unknown
finders_count: 62
finders:
  - codegpt
  - XORs33r
  - zhaojohnson
  - ahmedaghadi
  - cats
---

## Vulnerability Title

[M-01] Protocol and referral fee would be permanently stuck in the Curves contract when selling a token

### Overview


The token `Curves` has a bug during its sale where all fees are subtracted from the selling price and transferred to the seller. However, the `protocolFee` is not transferred to the designated destination and remains in the contract. Additionally, if there is no referral address defined, the referral fee is not transferred and remains in the contract. The recommended solution is to use the `buyValue` variable to handle both protocol and referral fees and transfer it to the designated destination. The severity of this bug has been decreased to Medium and the team behind `Curves` has acknowledged the issue.

### Original Finding Content


During the sale of a token `Curves._transferFee` subtracts all the fees from the selling price and transfers the remaining to the seller [here](<https://github.com/code-423n4/2024-01-curves/blob/main/contracts/Curves.sol#L231>).

```solidity
        uint256 sellValue = price - protocolFee - subjectFee - referralFee - holderFee;
        (bool success1, ) = firstDestination.call{value: isBuy ? buyValue : sellValue}("");
```

However, the `protocolFee` taken away is not transferred to the `protocolFeeDestination` in the remainder of the `_transferFee` function [here](<https://github.com/code-423n4/2024-01-curves/blob/main/contracts/Curves.sol#L231-L250>). It stays back in the contract with no other of way of retrieval.

Furthermore, `referralFee` is taken away without checking if a referral address actually exists. In the event that there is no referral defined, the third transfer is never executed [here](<https://github.com/code-423n4/2024-01-curves/blob/main/contracts/Curves.sol#L240>). This leaves the referral fee in the contract, again no retrieval mechanism.

### Recommended Mitigation Steps

The `buyValue` ([here](<https://github.com/code-423n4/2024-01-curves/blob/main/contracts/Curves.sol#L230C59-L230C59>)) variable already has the logic for jointly handling the protocol and referral fee. It can be given a more generic name, and be transferred to the `protocolDestination` for both buying and selling transactions.

```solidit
    uint256 protocolShare = referralDefined ? protocolFee : protocolFee + referralFee;
    uint256 sellValue = price - protocolFee - subjectFee - referralFee - holderFee;

    (bool success, ) = (feesEconomics.protocolFeeDestination).call{value: protocolShare}("");
    if (!success) revert CannotSendFunds();
    if(!isBuy) {
        (bool success1, ) = (msg.sender).call{value: sellValue}("");
        if(!success1) revert CannotSendFunds();
    }
```

**[alcueca (Judge) decreased severity to Medium](https://github.com/code-423n4/2024-01-curves-findings/issues/1294#issuecomment-1922137714)**

**[andresaiello (Curves) acknowledged](https://github.com/code-423n4/2024-01-curves-findings/issues/1294#issuecomment-2073079291)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Curves Protocol |
| Report Date | N/A |
| Finders | codegpt, XORs33r, zhaojohnson, ahmedaghadi, cats, SovaSlava, ro1sharkm, grearlake, 0x11singh99, zxriptor, 0xPhantom, Ryonen, mrudenko, MrPotatoMagic, Silvermist, klau5, aslanbek, KupiaSec, SpicyMeatball, mahdirostami, haxatron, khramov, ktg, anshujalan, ether\_sky, Soliditors, alexfilippov314, Cosine, Topmark, DanielArmstrong, \_eperezok, CDSecurity, developerjordy, c0pp3rscr3w3r, cccz, para8956, Aymen0909, dd0x7e8, nuthan2x, sl1, Oxsadeeq, todorc, nonseodion, FastChecker, rouhsamad, dimulski, Inference, whoismatthewmc1, cu5t0mpeo, 1, 2, tonisives, adeolu, deepplus, UbiquitousComputing, 0x0bserver, hals, petro\_1912, fishgang, lukejohn |

### Source Links

- **Source**: https://code4rena.com/reports/2024-01-curves
- **GitHub**: https://github.com/code-423n4/2024-01-curves-findings/issues/1294
- **Contest**: https://code4rena.com/reports/2024-01-curves

### Keywords for Search

`vulnerability`

