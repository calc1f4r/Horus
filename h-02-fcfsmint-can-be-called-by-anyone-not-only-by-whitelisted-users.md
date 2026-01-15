---
# Core Classification
protocol: Vallarok
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44183
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Vallarok-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[H-02] `FCFSMint()` Can Be Called By Anyone, Not Only By Whitelisted Users

### Overview


This bug report highlights an issue with the `FCFSMint()` function in the `RunaAGI.sol` file. The function is supposed to only be called by whitelisted users, but there is no verification in place to ensure this. This could lead to unauthorized users being able to mint additional NFTs. The team has acknowledged the issue and it is recommended that they add a check to verify the user's whitelist status before allowing them to call the function.

### Original Finding Content

## Severity

High Risk

## Description

From the ReadMе, we can see that the `FCFSMint()` function should be called only by whitelisted users:

> Ability to participate in the FCFS phase where every whitelisted wallet can mint two additional NFTs

But as we can see in the functions thus verification is completely missing.

## Location of Affected Code

File: [contracts/RunaAGI.sol#L135](https://github.com/purple-banana/contract-runa/blob/7153c2ffbf3a5e958af921f0ab92e20c5035d9bf/contracts/RunaAGI.sol#L135)

```solidity
function FCFSMint(uint256 _salt, bytes32 _msgHash, bytes memory _signature) external payable {
    require(isFCFSMintingActive, "FCFS minting is not active");
    require(saleSupplyMinted + 1 <= saleSupply, "Maximum supply reached");
    require(msg.value == salePrice, "Incorrect ether amount");
    require(fcfsMinted[msg.sender] + 1 <= 2, "Limit reached");

    bytes32 msgHash = keccak256(abi.encodePacked(msg.sender, _salt));
    bytes32 signedMsgHash = msgHash.toEthSignedMessageHash();

    require(signedMsgHash == _msgHash, "Invalid message hash!");
    require(_msgHash.recover(_signature) == signer, "Invalid signer!");
    signatures[_signature] = true;

    _safeMint(msg.sender, _tokenIdCounter.current());
    _tokenIdCounter.increment();
    _totalSupply++;
    saleSupplyMinted++;
    fcfsMinted[msg.sender] += 1;
}
```

## Recommendation

Consider adding a check if the user calling the function is whitelisted.

## Team Response

Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Vallarok |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Vallarok-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

