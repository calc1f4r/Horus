---
# Core Classification
protocol: Orbital Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19026
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-28-Orbital Finance.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-H-1 A malicious operator can drain the vault funds in one transaction

### Overview


This bug report is about a vulnerability in the `trade()` function of a vault operator, which allows an operator to steal all the funds in the vault by performing a sandwich attack. In this attack, the operator first flashloans a large amount of funds, then skews the token proportions in a pool which can be used for trading, by almost completely depleting the target token. The operator then performs the trade at >99% slippage and sells target tokens for source tokens on the manipulated pool, returning to the original ratio. The operator then pays off the flashloan and keeps the tokens traded at 99% slippage. 

The team's recommended mitigation was to enforce sensible slippage parameters. In response, the team integrated a Chainlink Interface to allow for off-chain price knowledge in a new contract, ChainlinkInterface.sol. This contract has an "addPriceFeed" function, on a per token basis, and a function "getMinReceived", which performs the needed math to get the min expected back from a trade. This function is called by the VaultManager at trade time, which then checks against the caller's minReceived input. Additionally, a slippage for a given pair is now get and set by the AuxInfo.sol contract.

The team then reviewed the mitigation and added a stale price feed check to the "getMinReceived" function, as well as a sequencer uptime check. This ensures that the price feed is up to date and that the sequencer is up when deployed on L2.

### Original Finding Content

**Description:**
The vault operator can swap tokens using the `trade()` function. They pass the following 
structure for each trade:
```solidity
         struct tradeInput { 
             address spendToken;
               address receiveToken;
                 uint256 spendAmt;
                   uint256 receiveAmtMin;
                address routerAddress;
         uint256 pathIndex;
         }
```
Notably, **receiveAmtMin** is used to guarantee acceptable slippage. An operator can simply 
pass 0 to make sure the trade is executed. This allows an operator to steal all the funds in the 
vault by architecting a sandwich attack. 
1. Flashloan a large amount of funds
2. Skew the token proportions in a pool which can be used for trading, by almost 
completely depleting the target token.
3. Perform the trade at >99% slippage
4. Sell target tokens for source tokens on the manipulated pool, returning to the original 
ratio.
5. Pay off the flashloan, and keep the tokens traded at 99% slippage.
In fact, this attack can be done in one TX, different to most sandwich attacks.

**Recommended Mitigation:**
The contract should enforce sensible slippage parameters.

**Team response:**
"Added Chainlink Interface to allow for off-chain price knowledge, in a new contract, 
ChainlinkInterface.sol, which is deployed by the VaultManager at deploy time, and ownership 
is given to the protocol owner. This contract has an "addPriceFeed" function, on per token 
basis. All feeds are assumed to be in USD units. Then, the function "getMinReceived", performs 
the needed math to get the min expected back from a trade. This function is called by the 
VaultManager at trade time, which then checks against the caller's minReceived input. 
Additionally, a slippage for a given pair is now get and set by the AuxInfo.sol contract.

**Mitigation review:**
The integration with Chainlink oracle introduces new issues. There is no check for a stale price 
feed, which makes trading possibly incur high slippage costs. 
```solidity
               (,int priceFromInt,,,) = AIFrom.latestRoundData();
         (,int priceToInt,,,) = AITo.latestRoundData();
```
Additionally, when the contracts are deployed on L2, there is a sequencer down-time issue, 
as detailed here(https://docs.chain.link/data-feeds/l2-sequencer-feeds). The contract should check the sequencer is up when deployed on L2.

**Team Response:**
"Stale price feed check added ChainlinkInterface.sol, "getMinReceived" function, lines 90 - 94. 
Sequencer uptime check added to "getMinReceived" function, line 76."

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Orbital Finance |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-28-Orbital Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

