---
# Core Classification
protocol: Atomic Loans
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 14000
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2019/09/atomic-loans/
github_link: none

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
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Steve Marx

---

## Vulnerability Title

There is no way to convert between custom and non-custom funds  Won't Fix

### Overview


A bug was reported in the code of Funds.sol, which is a part of the Ethereum network. The issue is that users cannot switch between a custom and non-custom fund without creating a new Ethereum account. This is because the code only allows one fund per account and does not provide a way to delete a fund once it exists. Therefore, users who want to switch between custom and non-custom funds must create a new address to do so. This bug could be a problem for users if the default parameters change in a way that they find unappealing. The recommendation is to either allow funds to be deleted or allow funds to be switched between custom and non-custom.

### Original Finding Content

#### Resolution



Users who want to switch between custom and non-custom funds can create a new address to do so. This is not actually a big burden because lenders need to use agent software to manage their funds anyway. That workflow typically involves generating a new address because the private key needs to be given to the agent software.


#### Description


Each fund is created using either `Funds.create()` or `Funds.createCustom()`. Both enforce a limitation that there can only be one fund per account:


**code/ethereum/contracts/Funds.sol:L348-L355**



```
function create(
    uint256  maxLoanDur\_,
    uint256  maxFundDur\_,
    address  arbiter\_,
    bool     compoundEnabled\_,
    uint256  amount\_
) external returns (bytes32 fund) {
    require(fundOwner[msg.sender].lender != msg.sender || msg.sender == deployer); // Only allow one loan fund per address

```
**code/ethereum/contracts/Funds.sol:L383-L397**



```
function createCustom(
    uint256  minLoanAmt\_,
    uint256  maxLoanAmt\_,
    uint256  minLoanDur\_,
    uint256  maxLoanDur\_,
    uint256  maxFundDur\_,
    uint256  liquidationRatio\_,
    uint256  interest\_,
    uint256  penalty\_,
    uint256  fee\_,
    address  arbiter\_,
    bool     compoundEnabled\_,
    uint256  amount\_
) external returns (bytes32 fund) {
    require(fundOwner[msg.sender].lender != msg.sender || msg.sender == deployer); // Only allow one loan fund per address

```
These functions are the only place where `bools[fund].custom` is set, and there’s no way to delete a fund once it exists. This means there’s no way for a given account to switch between a custom and non-custom fund.


This could be a problem if, for example, the default parameters change in a way that a user finds unappealing. They may want to switch to using a custom fund but find themselves unable to do so without moving to a new Ethereum account.


#### Recommendation


Either allow funds to be deleted or allow funds to be switched between custom and non-custom.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Atomic Loans |
| Report Date | N/A |
| Finders | Steve Marx
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2019/09/atomic-loans/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

