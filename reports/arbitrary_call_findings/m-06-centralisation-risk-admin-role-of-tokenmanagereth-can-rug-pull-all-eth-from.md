---
# Core Classification
protocol: SKALE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1605
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-skale-contest
source_link: https://code4rena.com/reports/2022-02-skale
github_link: https://github.com/code-423n4/2022-02-skale-findings/issues/35

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3.000002467536473
rarity_score: 1.000004935072947

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - launchpad
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - kirk-baird
---

## Vulnerability Title

[M-06] Centralisation risk: admin role of `TokenManagerEth` can rug pull all Eth from the bridge

### Overview


This bug report is about a Centralisation risk of the bridge where the `DEFAULT_ADMIN_ROLE` of `TokenManagerEth.sol` is able to modify the ERC20 token on the SChain to any arbitrary address. This would allow the admin role to change the address to one where they have infinite supply, they could then call `exitToMain(amount)` equal to the balance of the DepositBox in the main Ethereum chain. After the message is process on the main Ethereum chain they will receive the entire Eth balance of that contract. 

The `DEFAULT_ADMIN_ROLE` is set in the intiialisation to the `msg.sender` as seen in `initializeTokenManager()` and may then call `setEthErc20Address(IEthErc20 newEthErc20Address)`  setting `newEthErc20Address` to any arbitrary contract they control. This would lead to a rug pull attack. 

The recommended mitigation steps are to consider removing the function `setEthErc20Address()` as `ethErc20` is set in the `initialize()` function and does not need to be changed.

### Original Finding Content

_Submitted by kirk-baird_

There is a Centralisation risk of the bridge where the `DEFAULT_ADMIN_ROLE` of `TokenManagerEth.sol` is able to modify the ERC20 token on the SChain to any arbitrary address. This would allow the admin role to change the address to one where they have infinite supply, they could then call `exitToMain(amount)` equal to the balance of the DepositBox in the main Ethereum chain. After the message is process on the main Ethereum chain they will receive the entire Eth balance of that contract.

The rug pull attack occurs because there is a `DEFAULT_ADMIN_ROLE` which is set in the intiialisation to the `msg.sender` as seen in `initializeTokenManager()` below.

The `DEFAULT_ADMIN_ROLE` may then call `setEthErc20Address(IEthErc20 newEthErc20Address)`  setting `newEthErc20Address` to any arbitrary contract they control.

### Proof of Concept

        function setEthErc20Address(IEthErc20 newEthErc20Address) external override {
            require(hasRole(DEFAULT_ADMIN_ROLE, msg.sender), "Not authorized caller");
            require(ethErc20 != newEthErc20Address, "Must be new address");
            ethErc20 = newEthErc20Address;
        }

<!---->

        function initializeTokenManager(
            string memory newSchainName,
            IMessageProxyForSchain newMessageProxy,
            ITokenManagerLinker newIMALinker,
            ICommunityLocker newCommunityLocker,
            address newDepositBox
        )
            public
            virtual
            initializer
        {
            require(newDepositBox != address(0), "DepositBox address has to be set");

            AccessControlEnumerableUpgradeable.__AccessControlEnumerable_init();
            _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
            _setupRole(AUTOMATIC_DEPLOY_ROLE, msg.sender);
            _setupRole(TOKEN_REGISTRAR_ROLE, msg.sender);

            schainHash = keccak256(abi.encodePacked(newSchainName));
            messageProxy = newMessageProxy;
            tokenManagerLinker = newIMALinker;
            communityLocker = newCommunityLocker;        
            depositBox = newDepositBox;

            emit DepositBoxWasChanged(address(0), newDepositBox);
        }

### Recommended Mitigation Steps

Consider removing the function `setEthErc20Address()` as `ethErc20` is set in the `initialize()` function and does not need to be changed.


**[DimaStebaev (SKALE) disagreed with severity and commented](https://github.com/code-423n4/2022-02-skale-findings/issues/35#issuecomment-1064199292):**
 > Acknowledged, and this can be done only by SKALE chain owner. 

**[GalloDaSballo (judge) commented](https://github.com/code-423n4/2022-02-skale-findings/issues/35#issuecomment-1144015873):**
 > Agree that the admin has the ability to rug users and agree with Med Severity



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3.000002467536473/5 |
| Rarity Score | 1.000004935072947/5 |
| Audit Firm | Code4rena |
| Protocol | SKALE |
| Report Date | N/A |
| Finders | kirk-baird |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-skale
- **GitHub**: https://github.com/code-423n4/2022-02-skale-findings/issues/35
- **Contest**: https://code4rena.com/contests/2022-02-skale-contest

### Keywords for Search

`vulnerability`

