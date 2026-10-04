---
# Core Classification
protocol: Folks Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61066
audit_firm: Immunefi
contest_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2034025%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Malicious%20user%20can%20DoS%20the%20creation%20of%20every%20account%20at%20no%20cost%20by%20front%20running%20it%20with%20the%20same%20accountId.md
source_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2034025%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Malicious%20user%20can%20DoS%20the%20creation%20of%20every%20account%20at%20no%20cost%20by%20front%20running%20it%20with%20the%20same%20accountId.md
github_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2034025%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Malicious%20user%20can%20DoS%20the%20creation%20of%20every%20account%20at%20no%20cost%20by%20front%20running%20it%20with%20the%20same%20accountId.md

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
finders_count: 1
finders:
  - zarkk
---

## Vulnerability Title

Malicious user can DoS the creation of every account at no cost by front running it with the same ```accountId```.

### Overview


This report discusses a vulnerability in the Folks Finance lending platform's smart contract. The vulnerability allows a malicious user to prevent the creation of new accounts on the platform by front-running legitimate account creation requests. This can result in a complete Denial of Service (DoS) and significant financial damage to the platform. The vulnerability does not require any financial cost or advanced technical knowledge, making it easily accessible to attackers. A proof of concept is provided to demonstrate the vulnerability.

### Original Finding Content




Report type: Smart Contract


Target: https://testnet.snowtrace.io/address/0x3324B5BF2b5C85999C6DAf2f77b5a29aB74197cc

Impacts:
- Griefing (e.g. no profit motive for an attacker, but damage to the users or the protocol)

## Description
Malicious user can DoS the creation of every account at no cost by front running it with the same ```accountId```.

## Brief/Intro
The unique bond between ```accountId``` and ```Account ```within the ```createAccount``` function exposes Folks Finance to a critical Denial of Service (DoS) vulnerability. This vulnerability allows a malicious user to front-run legitimate account creation requests, thereby preventing the creation of any new accounts at no cost.

## Vulnerability Details
In order to utilize the lending platform, users must create an account by invoking the ```createAccount``` function of the ```AccountManager``` contract and supplying a unique ```accountId```. Below is the relevant implementation of the function:
```solidity
function createAccount(
        bytes32 accountId,
        uint16 chainId,
        bytes32 addr,
        bytes32 refAccountId
    ) external override onlyRole(HUB_ROLE) {
        // check account is not already created (empty is reserved for admin)
@>        if (isAccountCreated(accountId) || accountId == bytes32(0)) revert AccountAlreadyCreated(accountId);

        // check address is not already registered
        if (isAddressRegistered(chainId, addr)) revert AddressPreviouslyRegistered(chainId, addr);

        // check referrer is well defined
        if (!(isAccountCreated(refAccountId) || refAccountId == bytes32(0)))
            revert InvalidReferrerAccount(refAccountId);

        // create account
        accounts[accountId] = true;
        accountAddresses[accountId][chainId] = AccountAddress({ addr: addr, invited: false, registered: true });
        registeredAddresses[addr][chainId] = accountId;

        emit CreateAccount(accountId, chainId, addr, refAccountId);
    }
```
As demonstrated in the above code, if an account with the specified ```accountId``` has already been created, the creation request will be reverted. This design flaw permits an attacker to front-run the legitimate user's account creation by submitting a transaction with the same ```accountId```. Consequently, this prevents the legitimate user from creating their account and accessing the platform.

## Impact Details
The impact of this vulnerability is critical due to the nature of the attack and its implications. A malicious user can indefinitely prevent the creation of **any** new accounts on the platform by front-running legitimate account creation requests. This results in a complete Denial of Service (DoS), rendering the platform unusable for new users. The attack requires no financial cost or sophisticated technical knowledge, making it highly accessible to attackers. As the core function of the platform is to allow users to create accounts and engage in lending activities, this vulnerability directly compromises the platform's functionality and can lead to significant financial damage to the platform.

## References
https://github.com/Folks-Finance/folks-finance-xchain-contracts/blob/fb92deccd27359ea4f0cf0bc41394c86448c7abb/contracts/hub/AccountManager.sol#L35-L57

        
## Proof of concept
## Proof of Concept
To illustrate this vulnerability, add the following test under the ```"Create Account"``` section in ```AccountManager.test.ts```:
```javascript
it.only("Should fail to create account when malicious has frontrun the leigitimate user, creating an account with the same accountId so to DoS", async () => {
      const { hub, unusedUsers: oldUnusedUsers, accountManager } = await loadFixture(deployAccountManagerFixture);
      const [user, ...unusedUsers] = oldUnusedUsers;

      // user is the malicious
      // unusedUsers[0] is the legitimate

      // Front run the creation of an account with accountId by creating an account with the same accountId.
      const userAddr = convertEVMAddressToGenericAddress(user.address);
      const refAccountId: string = getEmptyBytes(BYTES32_LENGTH);
      const createAccountFrontrun = await accountManager.connect(hub).createAccount(getAccountIdBytes("ACCOUNT_ID"), 0, userAddr, refAccountId);

      // The legitimate user who tries to create his account with the accountId, but he has been frontrunned.
      const user2Addr = convertEVMAddressToGenericAddress(unusedUsers[0].address);
      const createAccountLegit = accountManager.connect(hub).createAccount(getAccountIdBytes("ACCOUNT_ID"), 0, user2Addr, refAccountId);
      // The creation actually reverts since the malicious user has already created an account with the same accountId
      await expect(createAccountLegit).to.be.revertedWithCustomError(accountManager, "AccountAlreadyCreated").withArgs(getAccountIdBytes("ACCOUNT_ID"));

      // This process can be replayed for EVERY account creation and a complete DoS to be performed. 
    });
```


### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Immunefi |
| Protocol | Folks Finance |
| Report Date | N/A |
| Finders | zarkk |

### Source Links

- **Source**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2034025%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Malicious%20user%20can%20DoS%20the%20creation%20of%20every%20account%20at%20no%20cost%20by%20front%20running%20it%20with%20the%20same%20accountId.md
- **GitHub**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2034025%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Malicious%20user%20can%20DoS%20the%20creation%20of%20every%20account%20at%20no%20cost%20by%20front%20running%20it%20with%20the%20same%20accountId.md
- **Contest**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2034025%20-%20%5BSmart%20Contract%20-%20Medium%5D%20Malicious%20user%20can%20DoS%20the%20creation%20of%20every%20account%20at%20no%20cost%20by%20front%20running%20it%20with%20the%20same%20accountId.md

### Keywords for Search

`vulnerability`

