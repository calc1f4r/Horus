---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: uncategorized
vulnerability_type: cross_chain

# Attack Vector Details
attack_type: cross_chain
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5922
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/154

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - cross_chain

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0xSmartContract
---

## Vulnerability Title

[M-14] Cross-chain replay attacks are possible with deployLPToken

### Overview


This bug report deals with a vulnerability in the code of the Liquid Staking project. The vulnerability is that mistakes made on one chain can be re-applied to a new chain, as there is no chain.id in the data. This can result in an attacker replaying the action on the correct chain, and stealing the funds from the user. The vulnerability was found through manual code review. The recommended mitigation step for this vulnerability is to include the chain.id in the data.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-11-stakehouse/blob/main/contracts/liquid-staking/LPTokenFactory.sol#L27-L48


## Vulnerability details

### Impact
Mistakes made on one chain can be re-applied to a new chain

There is no chain.id in the data

If a user does `deployLPToken` using the wrong network, an attacker can replay the action on the correct chain, and steal the funds a-la the wintermute gnosis safe attack, where the attacker can create the same address that the user tried to, and steal the funds from there


https://mirror.xyz/0xbuidlerdao.eth/lOE5VN-BHI0olGOXe27F0auviIuoSlnou_9t3XRJseY


### Proof of Concept

```js
contracts/liquid-staking/LPTokenFactory.sol:
  26      /// @param _tokenName Name of the LP token to be deployed
  27:     function deployLPToken(
  28:         address _deployer,
  29:         address _transferHookProcessor,
  30:         string calldata _tokenSymbol,
  31:         string calldata _tokenName
  32:     ) external returns (address) {
  33:         require(address(_deployer) != address(0), "Zero address");
  34:         require(bytes(_tokenSymbol).length != 0, "Symbol cannot be zero");
  35:         require(bytes(_tokenName).length != 0, "Name cannot be zero");
  36: 
  37:         address newInstance = Clones.clone(lpTokenImplementation);
  38:         ILPTokenInit(newInstance).init(
  39:             _deployer,
  40:             _transferHookProcessor,
  41:             _tokenSymbol,
  42:             _tokenName
  43:         );
  44: 
  45:         emit LPTokenDeployed(newInstance);
  46: 
  47:         return newInstance;
  48:     }
```

### Tools Used
Manual Code Review

### Recommended Mitigation Steps
Include the chain.id

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | 0xSmartContract |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/154
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Cross Chain`

