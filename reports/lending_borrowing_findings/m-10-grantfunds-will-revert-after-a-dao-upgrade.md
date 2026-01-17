---
# Core Classification
protocol: Spartan Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42263
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-07-spartan
source_link: https://code4rena.com/reports/2021-07-spartan
github_link: https://github.com/code-423n4/2021-07-spartan-findings/issues/17

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
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-10] `grantFunds` will revert after a DAO upgrade.

### Overview


The user gpersoon has submitted a bug report stating that when the DAO is upgraded through the `moveDao` function, the DAO address in the `Reserve.sol` contract is not updated. This causes an issue when the `grantFunds` function is called because it tries to access the `_RESERVE.grantFunds` function, which has a modifier that checks for the DAO address. However, since the DAO address was not updated, the modifier does not allow access and the `grantFunds` function fails. The user recommends calling the `setIncentiveAddresses` function after a DAO upgrade to prevent this issue in the future. This has been confirmed by verifyfirst and will be implemented in the future to future-proof the protocol.

### Original Finding Content

_Submitted by gpersoon_

When the DAO is upgraded via `moveDao`, it also updates the DAO address in BASE. However it doesn't update the DAO address in the `Reserve.sol` contract. This could be done with the function `setIncentiveAddresses(..)`

Now the next time `grantFunds` of `DAO.sol` is called, its tries to call `_RESERVE.grantFunds(...)`

The `grantFunds` of `Reserve.sol` has the modifier `onlyGrantor()`, which checks the msg`.sender` == DAO.
However in the mean time, the DAO has been updated and `Reserve.sol` doesn't know about it and thus the modifier will not allow access to the function. Thus `grantFunds` will revert.

`Dao.sol` [L452](https://github.com/code-423n4/2021-07-spartan/blob/main/contracts/Dao.sol#L452)
```solidity
function moveDao(uint _proposalID) internal {
    address _proposedAddress = mapPID_address[_proposalID]; // Get the proposed new address
    require(_proposedAddress != address(0), "!address"); // Proposed address must be valid
    DAO = _proposedAddress; // Change the DAO to point to the new DAO address
    iBASE(BASE).changeDAO(_proposedAddress); // Change the BASE contract to point to the new DAO address
    daoHasMoved = true; // Set status of this old DAO
    completeProposal(_proposalID); // Finalise the proposal
}

function grantFunds(uint _proposalID) internal {
    uint256 _proposedAmount = mapPID_param[_proposalID]; // Get the proposed SPARTA grant amount
    address _proposedAddress = mapPID_address[_proposalID]; // Get the proposed SPARTA grant recipient
    require(_proposedAmount != 0, "!param"); // Proposed grant amount must be valid
    require(_proposedAddress != address(0), "!address"); // Proposed recipient must be valid
    _RESERVE.grantFunds(_proposedAmount, _proposedAddress); // Grant the funds to the recipient
    completeProposal(_proposalID); // Finalise the proposal
}
```
`Reserve.sol` [L17](https://github.com/code-423n4/2021-07-spartan/blob/main/contracts/outside-scope/Reserve.sol#L17)
```solidity
modifier onlyGrantor() {
    require(msg.sender == DAO || msg.sender == ROUTER || msg.sender == DEPLOYER || msg.sender == LEND || msg.sender == SYNTHVAULT, "!DAO");
    _;
}

function grantFunds(uint amount, address to) external onlyGrantor {
    ....
}

function setIncentiveAddresses(address _router, address _lend, address _synthVault, address _Dao) external onlyGrantor {
    ROUTER = _router;
    LEND = _lend;
    SYNTHVAULT = _synthVault;
    DAO = _Dao;
}
```
Recommend calling `setIncentiveAddresses(..)` when a DAO upgrade is done.

**[verifyfirst (Spartan) confirmed](https://github.com/code-423n4/2021-07-spartan-findings/issues/17#issuecomment-885430701):**
 > Non critical, however this will be implemented to future proof the protocol



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Spartan Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-spartan
- **GitHub**: https://github.com/code-423n4/2021-07-spartan-findings/issues/17
- **Contest**: https://code4rena.com/reports/2021-07-spartan

### Keywords for Search

`vulnerability`

