---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25222
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-canto
source_link: https://code4rena.com/reports/2022-06-canto
github_link: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/173

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
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-11] `lending-market/Note.sol` Wrong implementation of access control

### Overview


This bug report is about the Lending Market smart contract. The code is written in Solidity, a programming language used to write smart contracts for the Ethereum blockchain. The code in question is from the Note.sol contract, which can be found at the given link. 

The bug is in the _mint_to_Accountant() function, which calls _setAccountantAddress() when accountant == address(0). This is always the case when _mint_to_Accountant() is called for the first time. The _setAccountantAddress() function only checks if msg.sender == admin when accountant != address(0), which is always false. This means that the access control is not working, allowing anyone to become the accountant and mint all the totalSupply to themselves. 

This bug was confirmed by tkkwon1998 (Canto) and Alex the Entreprenerd (judge) commented that the bug has a high severity, as it breaks the invariants of the contract and could potentially force a redeploy.

### Original Finding Content

_Submitted by WatchPug, also found by catchup, Lambda, p4st13r4, and Tutturu_

<https://github.com/Plex-Engineer/lending-market/blob/b93e2867a64b420ce6ce317f01c7834a7b6b17ca/contracts/Note.sol#L13-L31><br>

```solidity
function _mint_to_Accountant(address accountantDelegator) external {
    if (accountant == address(0)) {
        _setAccountantAddress(msg.sender);
    }
    require(msg.sender == accountant, "Note::_mint_to_Accountant: ");
    _mint(msg.sender, type(uint).max);
}

function RetAccountant() public view returns(address) {
    return accountant;
}

function _setAccountantAddress(address accountant_) internal {
    if(accountant != address(0)) {
        require(msg.sender == admin, "Note::_setAccountantAddress: Only admin may call this function");
    }
    accountant = accountant_;
    admin = accountant;
}
```

`_mint_to_Accountant()` calls `_setAccountantAddress()` when `accountant == address(0)`, which will always be the case when `_mint_to_Accountant()` is called for the first time.

And `_setAccountantAddress()` only checks if `msg.sender == admin` when `accountant != address(0)` which will always be `false`, therefore the access control is not working.

L17 will then check if `msg.sender == accountant`, now it will always be the case, because at L29, `accountant` was set to `msg.sender`.

**[tkkwon1998 (Canto) confirmed](https://github.com/code-423n4/2022-06-canto-findings/issues/173)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-06-canto-findings/issues/173#issuecomment-1211378551):**
 > The warden has shown how, due to a flaw in logic, via a front-run, anyone can become the `accountant` and mint all the totalSupply to themselves.
> 
> While I'm not super confident on severity for the front-run as I'd argue the worst case is forcing a re-deploy, the warden has shown a lack of logic in the checks (`msg.sender == admin`) which breaks it's invariants.
> 
> For that reason, I think High Severity to be appropriate.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-canto
- **GitHub**: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/173
- **Contest**: https://code4rena.com/reports/2022-06-canto

### Keywords for Search

`vulnerability`

