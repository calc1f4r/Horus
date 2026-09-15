---
# Core Classification
protocol: DYAD
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33461
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-dyad
source_link: https://code4rena.com/reports/2024-04-dyad
github_link: https://github.com/code-423n4/2024-04-dyad-findings/issues/830

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
finders_count: 46
finders:
  - bhilare\_
  - ducanh2706
  - 0xShitgem
  - ahmedaghadi
  - steadyman
---

## Vulnerability Title

[H-05] Unable to withdraw Kerosene from `vaultmanagerv2::withdraw` as it expects a `vault.oracle()` method which is missing in Kerosene vaults

### Overview


The VaultManagerV2 contract has a bug in its withdraw function, which is responsible for withdrawing both exogenous collateral (weth/wsteth) and endogenous collateral (Kerosene). The function expects the vault passed as an argument to have an oracle method, which is not the case for the BoundedKerosineVault or UnboundedKerosineVault contracts. This means that when a user tries to withdraw Kerosene deposited into the contract, the call will fail and the Kerosene will remain stuck in the contract permanently. A proof of concept test has been added to highlight this issue. The recommended solution is to have separate withdraw functions for exogenous collateral and Kerosene to avoid added complexity in the function logic. 

### Original Finding Content


`VaultManagerV2` has one `withdraw` function responsible for withdrawing both exogenous collateral (weth/wsteth) and endogenous collateral (Kerosene). However, the function expects the `vault` passed as an argument to have an `oracle` method. This is the case for `Vault` contracts, but not the case for the `BoundedKerosineVault` or `UnboundedKerosineVault` contracts. This means that whenever a user attempts to withdraw Kerosene deposited into the contract the call will revert, meaning the Kerosene remains stuck in the contract permanently.

### Proof of Concept

Add the following test to `v2.t.sol` to highlight this:

```solidity
  function testCannotWithdrawKero() public {
    // Set up alice
    licenseVaultManager();
    address alice = makeAddr("alice");
    uint aliceTokenId = sendNote(alice);
    sendKerosene(alice, 10_000 ether);

    // Alice deposits kerosene into the protocol
    vm.startPrank(alice);
    contracts.vaultManager.addKerosene(aliceTokenId, address(contracts.unboundedKerosineVault));
    Kerosine(MAINNET_KEROSENE).approve(address(contracts.vaultManager), 10_000 ether);
    contracts.vaultManager.deposit(aliceTokenId, address(contracts.unboundedKerosineVault), 10_000 ether);
    
    assertEq(ERC20(MAINNET_KEROSENE).balanceOf(alice), 0);

    vm.roll(block.number + 42);
    
    // Alice attempts to withdraw her kerosene but the tx reverts
    contracts.vaultManager.withdraw(aliceTokenId, address(contracts.unboundedKerosineVault), 10_000 ether, alice);
  }
```

The test reverts with the following stack traces:

```solidity
    ├─ [9243] VaultManagerV2::withdraw(645, UnboundedKerosineVault: [0x416C42991d05b31E9A6dC209e91AD22b79D87Ae6], 10000000000000000000000 [1e22], alice: [0x328809Bc894f92807417D2dAD6b7C998c1aFdac6])
    │   ├─ [558] 0xDc400bBe0B8B79C07A962EA99a642F5819e3b712::ownerOf(645) [staticcall]
    │   │   └─ ← [Return] alice: [0x328809Bc894f92807417D2dAD6b7C998c1aFdac6]
    │   ├─ [2623] 0x305B58c5F6B5b6606fb13edD11FbDD5e532d5A26::mintedDyad(VaultManagerV2: [0xA8452Ec99ce0C64f20701dB7dD3abDb607c00496], 645) [staticcall]
    │   │   └─ ← [Return] 0
    │   ├─ [261] UnboundedKerosineVault::asset() [staticcall]
    │   │   └─ ← [Return] 0xf3768D6e78E65FC64b8F12ffc824452130BD5394
    │   ├─ [262] 0xf3768D6e78E65FC64b8F12ffc824452130BD5394::decimals() [staticcall]
    │   │   └─ ← [Return] 18
    │   ├─ [214] UnboundedKerosineVault::oracle() [staticcall]
    │   │   └─ ← [Revert] EvmError: Revert
    │   └─ ← [Revert] EvmError: Revert
```

### Recommended Mitigation

Given that the `value` of exogenous and endogenous collateral is calculated differently it is necessary to handle withdrawal of exogenous collateral and Kerosene differently. It would avoid added complexity to the function logic to have two different `withdraw` and `withdrawKerosene` functions.

**[shafu0x (DYAD) confirmed and commented](https://github.com/code-423n4/2024-04-dyad-findings/issues/830#issuecomment-2091709439):**
 > Good find. This is correct.

*Note: For full discussion, see [here](https://github.com/code-423n4/2024-04-dyad-findings/issues/830).*

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | DYAD |
| Report Date | N/A |
| Finders | bhilare\_, ducanh2706, 0xShitgem, ahmedaghadi, steadyman, Mahmud, SBSecurity, cinderblock, web3km, 0xfox, Infect3d, carrotsmuggler, 3th, ke1caM, iamandreiski, itsabinashb, bbl4de, alix40, Evo, btk, d3e4, ljj, dinkras, y4y, TheSchnilch, Aamir, 4rdiii, 0x486776, Egis\_Security, 0xSecuri, Circolors, Al-Qa-qa, 0xlemon, dimulski, Limbooo, amaron, 1, 2, shaflow2, 0xnilay, Honour, sashik\_eth, AlexCzm, 0x175 |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-dyad
- **GitHub**: https://github.com/code-423n4/2024-04-dyad-findings/issues/830
- **Contest**: https://code4rena.com/reports/2024-04-dyad

### Keywords for Search

`vulnerability`

