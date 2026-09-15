---
# Core Classification
protocol: Cudos
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2272
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-cudos-contest
source_link: https://code4rena.com/reports/2022-05-cudos
github_link: https://github.com/code-423n4/2022-05-cudos-findings/issues/14

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
  - synthetics

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - csanuragjain
  - danb
  - IllIllI
  - AmitN
  - GermanKuber
---

## Vulnerability Title

[M-02] Admin drains all ERC based user funds using `withdrawERC20()`

### Overview


This bug report is about a vulnerability in the code of the Gravity Bridge contract for Gravity.sol. The vulnerability allows an admin to drain all ERC20 funds stored in the contract at will, meaning all ERC20 based Cudos tokens (and any other ERC20 tokens stored in the contract) could be extracted by anyone with admin role and later sold. This would leave users funds bridged on Cudos Cosmos chain with no ERC20 representation stored across the bridge.

The bug was discovered by the development team, and the proof of concept involves an admin waiting until CUDOS bridge has decent TVL from users bridging their CUDOS tokens from Ethereum to the CUDOS Cosmos chain. The admin then manually calls withdrawERC20(address _tokenAddress) with the ERC token address of the CUDOS token, and the withdrawERC20() function checks if user has admin role and if so withdraws all the tokens of a given token address straight to the admin's personal wallet. The admin can then exchange CUDOS on DEX and then send funds to tornado cash, leaving all user funds at risk.

The recommended mitigation steps include deleting the function or alternatively, sending all funds to the '0' address to burn rather than give them to the admin. The code should be changed to the following:

```
function burnERC20(
	address _tokenAddress) 
	external {
	require(cudosAccessControls.hasAdminRole(msg.sender), "Recipient is not an admin");
	uint256 totalBalance = IERC20(_tokenAddress).balanceOf(address(0));
	- IERC20(_tokenAddress).safeTransfer(msg.sender , totalBalance);
     +   IERC20(_tokenAddress).safeTransfer(address(0) , totalBalance);
}
```

### Original Finding Content


[Gravity.sol#L632-L638](https://github.com/code-423n4/2022-05-cudos/blob/de39cf3cd1f1e1cf211819b06d4acf6a043acda0/solidity/contracts/Gravity.sol#L632-L638)<br>
[Gravity.sol#L595-L609](https://github.com/code-423n4/2022-05-cudos/blob/de39cf3cd1f1e1cf211819b06d4acf6a043acda0/solidity/contracts/Gravity.sol#L595-L609)

Ability for admin to drain all ERC20 funds stored in contract at will, meaning all ERC20 based Cudos tokens (and any other ERC20 tokens stored in the contract) could be extracted by anyone with admin role and later sold, leaving users funds bridged on Cudos Cosmos chain with no ERC20 representation stored across the bridge - similar in impact as the wormhole hack.

This issue ought to fall within the limits the team allocated on assessing the governance role setups, since it describes a full-fledged security risk regarding users' funds. Crucially, this function is not in the [original Gravity Bridge contract for Gravity.sol](https://github.com/Gravity-Bridge/Gravity-Bridge/blob/f65d9da692c1af76f8188bd17b55dea58c1d8723/solidity/contracts/Gravity.sol).

Furthermore, the function has not been commented and does not appear in the documentation, suggesting that it has perhaps not yet been reasoned through by the development team and it's critical this is flagged in the security audit.

### Proof of Concept

Firstly, User with admin role granted waits until CUDOS bridge has decent TVL from users bridging their CUDOS tokens from Ethereum to the CUDOS Cosmos chain,

Secondly, User manually calls withdrawERC20(address \_tokenAddress) with the ERC token address of the CUDOS token

     function withdrawERC20(
    			address _tokenAddress) 
    			external {
    			require(cudosAccessControls.hasAdminRole(msg.sender), "Recipient is not an admin");
    			uint256 totalBalance = IERC20(_tokenAddress).balanceOf(address(this));
    			IERC20(_tokenAddress).safeTransfer(msg.sender , totalBalance);
    } 

Thirdly, withdrawERC20() function checks if user has admin role and if so withdraws all the tokens of a given token address straight to the admin's personal wallet

```
               require(cudosAccessControls.hasAdminRole(msg.sender), "Recipient is not an admin");
		uint256 totalBalance = IERC20(_tokenAddress).balanceOf(address(this));
		IERC20(_tokenAddress).safeTransfer(msg.sender , totalBalance);
```

Fourth, user exchanges CUDOS on DEX and then sends funds to tornado cash, leaving all user funds at risk.

### Tools Used

My own logical reasoning and discussion with team on Discord for confirmation of admin roles and function's logic.

### Recommended Mitigation Steps

Delete the function or alternatively, send all funds to the '0' address to burn rather than give them to the admin.

Change withdrawERC20 to:

    function burnERC20(
    	address _tokenAddress) 
    	external {
    	require(cudosAccessControls.hasAdminRole(msg.sender), "Recipient is not an admin");
    	uint256 totalBalance = IERC20(_tokenAddress).balanceOf(address(0));
    	- IERC20(_tokenAddress).safeTransfer(msg.sender , totalBalance);
         +   IERC20(_tokenAddress).safeTransfer(address(0) , totalBalance);
    }

**[maptuhec (Cudos) acknowledged and commented](https://github.com/code-423n4/2022-05-cudos-findings/issues/14#issuecomment-1123247894):**
 > The reason we have created this functions is that, if the bridge stop working, the funds for the users would be locked, and there is no chance to withdraw them. CUDOS have no intention and incentive to maliciously withdraw the ERC20 tokes, because that would lead to losing the trust in its clients and thus killing their own network. The best way for handling this is to communicate this with the community so they can be aware.

**[Albert Chon (judge) decreased severity to Medium](https://github.com/code-423n4/2022-05-cudos-findings/issues/14)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Cudos |
| Report Date | N/A |
| Finders | csanuragjain, danb, IllIllI, AmitN, GermanKuber, pcrypt0, WatchPug, dirky, kirk-baird, 0x1337 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-cudos
- **GitHub**: https://github.com/code-423n4/2022-05-cudos-findings/issues/14
- **Contest**: https://code4rena.com/contests/2022-05-cudos-contest

### Keywords for Search

`vulnerability`

