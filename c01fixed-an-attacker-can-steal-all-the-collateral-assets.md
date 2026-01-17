---
# Core Classification
protocol: Opyn Gamma Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11224
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/opyn-gamma-protocol-audit/
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[C01][Fixed] An attacker can steal all the collateral assets

### Overview


A bug was discovered in the `Controller` contract of the GammaProtocol platform which could allow malicious users to steal all the collateral assets from the platform. The bug was found in the `_redeem` internal function which is called when users send a `Redeem` action type. The function does not check if the oToken passed in the arguments correspond to a real oToken from the platform. This means that an attacker could deploy a malicious oToken contract with the same assets and structure of an existing legit oToken, and call the `operate` function with the arguments as specified. The `Controller` contract would then burn the attacker’s malicious oTokens and pay out the collateral asset from the pool, resulting in the attacker stealing all the collateral assets from the platform. The bug has since been fixed in Pull Request #301.

### Original Finding Content

The [`Controller` contract](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Controller.sol#L27) allows users to interact with the majority of the platform, being able to open a vault, deposit collateral assets, minting oTokens, or redeem their oTokens. All of these actions start by calling the [`operate` function](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Controller.sol#L331) which then calls the [`_runActions` function](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Controller.sol#L450) and redirects the call to the respective [action’s internal function](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Controller.sol#L482-L503).


Once one oToken expires, if an oToken holder wants to exercise their right and collect the payout for their oTokens, the user must send a [`Redeem` action type](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/libs/Actions.sol#L24) which would end up in a call to the [`_redeem` internal function](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Controller.sol#L707).


However, in this action a malicious user can steal all the collateral assets following the attack vector below:


1.The attacker deploys a malicious oToken contract which has the same assets and structure of an existing legit oToken, especially an oToken with the most amount of collateral asset.


2.The attacker then calls the `operate` function and passes on the argument as follows:



```
[{
actionType : Redeem,
owner : attacker address,
secondAddress : attacker address,
asset : malicious oToken,
vaultId : anything,
amount : the max amount of oToken redeemable,
index: anything,
data : anything
}]

```

The `Controller` contract will first call the `_runActions` function with these arguments, `vaultUpdated` will not be set to true because `actionType == Actions.ActionType.Redeem` and will skip a [conditional statement](https://github.com/opynfinance/GammaProtocol/blob/d151621b33134789b29dc78eb89dad2b557b25b9/contracts/Controller.sol#L469), and then the internal function will be called for the redeem action with these arguments:



```
_redeem(attacker address, malicious oToken address, amount)

```

3.The `_redeem` function does not check if given oToken is a real one or not, it only checks if:


* `now > otoken.expiryTimstamp`
* `isSettlementAllowed(maliciousOtoken)`


But both of these conditions can be engineered in the malicious oToken to lead to a successful redeem process.  

The `Controller` contract will then burn the attacker’s malicious oTokens and pay out the collateral asset from the pool, resulting in the attacker stealing all the collateral assets from the platform.


Consider validating if the oToken passed in the arguments correspond to a real oToken from the platform.


**Update:** *Fixed in [PR#301](https://github.com/opynfinance/GammaProtocol/pull/301).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Opyn Gamma Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/opyn-gamma-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

