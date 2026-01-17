---
# Core Classification
protocol: Rolla
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42533
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-03-rolla
source_link: https://code4rena.com/reports/2022-03-rolla
github_link: https://github.com/code-423n4/2022-03-rolla-findings/issues/12

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
  - options_vault

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-02] `COLLATERAL_MINTER_ROLE` can be granted by the deployer of `QuantConfig` and mint arbitrary amount of tokens

### Overview


The report discusses a bug in the mintCollateralToken() function of the CollateralToken contract. This function allows an address with the COLLATERAL_MINTER_ROLE to mint an unlimited amount of collateral tokens. If the private key of the deployer or an address with this role is compromised, it poses a risk of centralization. The report recommends removing the COLLATERAL_MINTER_ROLE and making the Controller contract the only minter. The bug has been confirmed and resolved by the Rolla project. 

### Original Finding Content

_Submitted by cccz, also found by danb, and WatchPug_

        function mintCollateralToken(
            address recipient,
            uint256 collateralTokenId,
            uint256 amount
        ) external override {
            require(
                quantConfig.hasRole(
                    quantConfig.quantRoles("COLLATERAL_MINTER_ROLE"),
                    msg.sender
                ),
                "CollateralToken: Only a collateral minter can mint CollateralTokens"
            );

            emit CollateralTokenMinted(recipient, collateralTokenId, amount);

            _mint(recipient, collateralTokenId, amount, "");
        }

Using the mintCollateralToken() function of CollateralToken, an address with COLLATERAL_MINTER_ROLE can mint an arbitrary amount of tokens.

If the private key of the deployer or an address with the COLLATERAL_MINTER_ROLE is compromised, the attacker will be able to mint an unlimited amount of collateral tokens.

We believe this is unnecessary and poses a serious centralization risk.

### Proof of Concept

[CollateralToken.sol#L101-L117](https://github.com/code-423n4/2022-03-rolla/blob/main/quant-protocol/contracts/options/CollateralToken.sol#L101-L117)<br>
[CollateralToken.sol#L138-L160](https://github.com/code-423n4/2022-03-rolla/blob/main/quant-protocol/contracts/options/CollateralToken.sol#L138-L160)<br>

### Recommended Mitigation Steps

Consider removing the COLLATERAL_MINTER_ROLE, make the CollateralToken only mintable by the owner, and make the Controller contract to be the owner and therefore the only minter.

**[0xca11 (Rolla) confirmed](https://github.com/code-423n4/2022-03-rolla-findings/issues/12#issuecomment-1102152105)**

**[alcueca (judge) commented](https://github.com/code-423n4/2022-03-rolla-findings/issues/12#issuecomment-1094436993):**
 > Per sponsor comment on [#47](https://github.com/code-423n4/2022-03-rolla-findings/issues/47#issuecomment-1079940591):
> 
> "The roles are renounced as per our deployment config covered in the docs. But this bug is still valid as the role OPTIONS_MINTER_ROLE can be reassigned".
> 
> Taking this one as main, with the vulnerability being that several of the MINTER and BURNER roles can be reassigned and have unnecessary powers that can be used to rug users.

**[0xca11 (Rolla) resolved and commented](https://github.com/code-423n4/2022-03-rolla-findings/issues/12#issuecomment-1102152105):**
 > All roles were removed from the protocol, and now only the Controller contract can mint QTokens and CollateralTokens.
 > 
 > [RollaProject/quant-protocol#90](https://github.com/RollaProject/quant-protocol/pull/90)



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Rolla |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-rolla
- **GitHub**: https://github.com/code-423n4/2022-03-rolla-findings/issues/12
- **Contest**: https://code4rena.com/reports/2022-03-rolla

### Keywords for Search

`vulnerability`

