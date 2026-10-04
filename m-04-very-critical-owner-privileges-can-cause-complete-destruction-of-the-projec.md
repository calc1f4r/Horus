---
# Core Classification
protocol: Trader Joe
chain: everychain
category: uncategorized
vulnerability_type: admin

# Attack Vector Details
attack_type: admin
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5714
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-trader-joe-v2-contest
source_link: https://code4rena.com/reports/2022-10-traderjoe
github_link: https://github.com/code-423n4/2022-10-traderjoe-findings/issues/139

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:
  - admin

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 23
finders:
  - Nyx
  - leosathya
  - ladboy233
  - SooYa
  - 0xSmartContract
---

## Vulnerability Title

[M-04] Very critical Owner privileges can cause complete destruction of the project in a possible privateKey exploit

### Overview


This bug report concerns a vulnerability in the PendingOwnable contract, which is part of the 2022-10-traderjoe project. This vulnerability is related to the `onlyOwner` privileges, which can be used by the owner of the contract to perform certain privileged activities. The vulnerability is considered medium due to the recent increase in private key thefts. 

The proof of concept provided in the report shows that the `onlyOwner` powers are used in various functions in two files, LBFactory.sol and PendingOwnable.sol. 

The report recommends adding a timelock contract to use the `onlyOwner` privileges, as this would provide users with a warning in case of a possible security weakness. Additionally, it is suggested that the `onlyOwner` should be a Multisign wallet, and this should be specified in the project's documentation.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-10-traderjoe/blob/main/src/libraries/PendingOwnable.sol#L42


## Vulnerability details

### Vulnerability details
Typically, the contract’s owner is the account that deploys the contract. As a result, the owner is able to perform certain privileged activities.

However, Owner privileges are numerous and there is no timelock structure in the process of using these privileges.
The Owner is assumed to be an EOA, since the documents do not provide information on whether the Owner will be a multisign structure.

In parallel with the private key thefts of the project owners, which have increased recently, this vulnerability has been stated as medium.

Similar vulnerability;
Private keys stolen:

Hackers have stolen cryptocurrency worth around €552 million from a blockchain project linked to the popular online game Axie Infinity, in one of the largest cryptocurrency heists on record. Security issue : PrivateKey of the project officer was stolen:
https://www.euronews.com/next/2022/03/30/blockchain-network-ronin-hit-by-552-million-crypto-heist


### Proof of Concept

`onlyOwner` powers;
```js
14 results - 2 files

src/LBFactory.sol:
  220:     function setLBPairImplementation(address _LBPairImplementation) external override onlyOwner {
  322:     function setLBPairIgnored() external override onlyOwner {
  355:     function setPreset() external override onlyOwner {
  401:     function removePreset(uint16 _binStep) external override onlyOwner {
  439:     function setFeesParametersOnPair) external override onlyOwner {
  473:     function setFeeRecipient(address _feeRecipient) external override onlyOwner {
  479:     function setFlashLoanFee(uint256 _flashLoanFee) external override onlyOwner {
  490:     function setFactoryLockedState(bool _locked) external override onlyOwner {
  498:     function addQuoteAsset(IERC20 _quoteAsset) external override onlyOwner {
  507:     function removeQuoteAsset(IERC20 _quoteAsset) external override onlyOwner {
  525:     function forceDecay(ILBPair _LBPair) external override onlyOwner {

src/libraries/PendingOwnable.sol:
  59:     function setPendingOwner(address pendingOwner_) public override onlyOwner {
  68:     function revokePendingOwner() public override onlyOwner {
  84:     function renounceOwnership() public override onlyOwner {



```

### Recommendation;

1- A timelock contract should be added to use `onlyOwner` privileges. In this way, users can be warned in case of a possible security weakness.
2- `onlyOwner` can be a Multisign wallet and this part is specified in the documentation

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Trader Joe |
| Report Date | N/A |
| Finders | Nyx, leosathya, ladboy233, SooYa, 0xSmartContract, djxploit, catchup, zzykxx, supernova, pashov, Mukund, Josiah, csanuragjain, cccz, sorrynotsorry, Aymen0909, hansfriese, chaduke, M4TZ1P, Dravee, vv7, wagmi, rvierdiiev |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-traderjoe
- **GitHub**: https://github.com/code-423n4/2022-10-traderjoe-findings/issues/139
- **Contest**: https://code4rena.com/contests/2022-10-trader-joe-v2-contest

### Keywords for Search

`Admin`

