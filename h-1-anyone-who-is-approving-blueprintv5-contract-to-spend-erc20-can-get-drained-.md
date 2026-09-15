---
# Core Classification
protocol: Crestal Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55092
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/755
source_link: none
github_link: https://github.com/sherlock-audit/2025-03-crestal-network-judging/issues/260

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
finders_count: 89
finders:
  - dreamcoder
  - 0xpetern
  - Praise03
  - 0xAadi
  - Artur
---

## Vulnerability Title

H-1: Anyone who is approving `BlueprintV5` contract to spend ERC20 can get drained because `Payment::payWithERC20`

### Overview


The bug report discusses an issue found in the `BlueprintV5` contract, which is used for handling payments with ERC20 tokens. It was discovered that the function `payWithERC20` can also be used to drain funds from anyone interacting with the contract and approving the use of the payment token. This is because the function is public and can be called by anyone with a valid token address and the victim's address. The bug can only occur if the admin has enabled the use of the payment token and the victim has approved the token for use by the contract. The impact of this bug is that the victim can lose their funds to the attacker. The bug has been fixed by making the `payWithERC20` function internal.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-03-crestal-network-judging/issues/260 

## Found by 
0x180db, 0x73696d616f, 0xAadi, 0xDemon, 0xEkko, 0xGondar, 0xGutzzz, 0xYjs, 0xadarum, 0xaudron, 0xc0ffEE, 0xhiros, 0xjarix, 0xlucky, 0xpetern, Anirruth, Arav, Artur, Buggx0, CasinoCompiler, Chaindecompiler, ChaosSR, Cybrid, Edoscoba, FalseGenius, GODSPEED, Harry\_cryptodev, Harsh, HolyHak, IzuMan, JasonBPMIASN, Kodyvim, KungFuPanda, Kwesi, MSK, Matic68, OlaHamid, OpaBatyo, Oxpreacher, Pelz, Pihu, Praise03, Ryonen, Trepid, ZOL, ZafiN, abhishek\_thakur, anchabadze, auditism, bube, c3phas, dennis, dreamcoder, eLSeR17, farismaulana, gegul, ggbond, gxh191, hirugohan, ihtishamsudo, ilyadruzh, j3x, jacopod, jprod15, krot-0025, lom\_ack, makeWeb3safe, patitonar, ph, phrax, princekay, radcipher, redtrama, resosiloris, roccomania, sa9933, sabanaku77, seeques, shady4, skid0016, skipper, tachida2k, thimthor, vivekd, w33kEd, x0rc1ph3r, y4y, yaioxy, zxriptor

### Summary

`payWithERC20` is supposed to be used inside `BlueprintV5` contract to handle payment. But this function also can be used to drain anyone who is interact with `BlueprintV5` and using it to approve payment token when creating an agent.

### Root Cause

[Payment.sol#L25-L32](https://github.com/sherlock-audit/2025-03-crestal-network/blob/main/crestal-omni-contracts/src/Payment.sol#L25-L32)

```Solidity
@>    function payWithERC20(address erc20TokenAddress, uint256 amount, address fromAddress, address toAddress) public {
        // check from and to address
        require(fromAddress != toAddress, "Cannot transfer to self address");
        require(toAddress != address(0), "Invalid to address");
        require(amount > 0, "Amount must be greater than 0");
        IERC20 token = IERC20(erc20TokenAddress);
        token.safeTransferFrom(fromAddress, toAddress, amount);
    }
```

the root cause simply because this function is public function, meaning anyone can call this and supply valid token address, then fill `fromAddress` with any address that still have allowance/approving the payment token to be spend by `BlueprintV5` contract

### Internal Pre-conditions

1. admin enable usdc or any erc20 token as payment by calling `Blueprint::addPaymentAddress`

### External Pre-conditions

1. victim approve the spending of usdc or any erc20 token set in last step for `BlueprintV5` contract address proxy
2. the amount approved should be greater than the amount used for creating agent with token cost
3. victim call the function to create agent (optional)

### Attack Path

1. attacker call `payWithERC20` supplying the parameter with usdc address, victim address and sufficient amount to be sent into attacker address

### Impact

user/victim who interacted would lose their funds drained by attacker

### PoC

_No response_

### Mitigation

make the `Payment::payWithERC20` internal

## Discussion

**spidemen2024**

Got it

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/crestalnetwork/crestal-omni-contracts/pull/16

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Crestal Network |
| Report Date | N/A |
| Finders | dreamcoder, 0xpetern, Praise03, 0xAadi, Artur, 0x180db, 0xDemon, 0xEkko, Kodyvim, tachida2k, bube, jacopod, krot-0025, princekay, skid0016, Cybrid, auditism, 0xc0ffEE, ChaosSR, Ryonen, patitonar, 0xjarix, 0xGondar, OlaHamid, ggbond, Pelz, 0xlucky, seeques, Arav, MSK, sabanaku77, roccomania, Anirruth, Trepid, y4y, gegul, makeWeb3safe, sa9933, ilyadruzh, Harry\_cryptodev, gxh191, ihtishamsudo, jprod15, w33kEd, x0rc1ph3r, Harsh, 0xYjs, Matic68, zxriptor, JasonBPMIASN, OpaBatyo, redtrama, KungFuPa, farismaulana, IzuMan, Pihu, thimthor, ZOL, c3phas, 0xGutzzz, 0xadarum, Oxpreacher, hirugohan, phrax, dennis, skipper, Edoscoba, 0xhiros, j3x, resosiloris, shady4, FalseGenius, GODSPEED, ZafiN, radcipher, anchabadze, yaioxy, ph, HolyHak, Chaindecompiler, CasinoCompiler, Buggx0, lom\_ack, Kwesi, vivekd, 0x73696d616f, abhishek\_thakur, 0xaudron, eLSeR17 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-03-crestal-network-judging/issues/260
- **Contest**: https://app.sherlock.xyz/audits/contests/755

### Keywords for Search

`vulnerability`

