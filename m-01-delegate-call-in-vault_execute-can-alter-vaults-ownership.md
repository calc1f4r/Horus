---
# Core Classification
protocol: Fractional
chain: everychain
category: uncategorized
vulnerability_type: delegate

# Attack Vector Details
attack_type: delegate
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3002
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-fractional-v2-contest
source_link: https://code4rena.com/reports/2022-07-fractional
github_link: https://github.com/code-423n4/2022-07-fractional-findings/issues/487

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - delegate

protocol_categories:
  - dexes
  - bridge
  - yield
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 24
finders:
  - _141345_
  - scaraven
  - berndartmueller
  - giovannidisiena
  - minhtrng
---

## Vulnerability Title

[M-01] Delegate call in `Vault#_execute` can alter Vault's ownership

### Overview


This bug report is about a vulnerability in the Vault contract, which is part of the code-423n4/2022-07-fractional repository. The vulnerability is related to the `Vault#execute` function, which calls a target contract's function via `delegatecall` if the caller is either the owner of the Vault or the target contract is part of a merkle tree. The `delegatecall`s have to be used with caution because the contract being called is using the caller's contract storage, meaning the callee contract can alter the caller's contract state. 

The developers seem to be aware of the danger that the callee contract is able to overtake the Vaults ownership, by changing the Vaults `owner` variable, as the `owner` is cached before the `delegatecall` and afterwards checked that the variable did not change. However, changing the `owner` variable is not the only way the callee contract is able to overtake the Vaults ownership. If the `nonce` variable is re-set to `0`, the Vault's `init` function becomes callable again, granting ownership to the caller.

The severity of this vulnerability is rated as MEDIUM (HIGH impact with a LOW likelihood) due to the fact that the `owner` variable check is included, meaning the project rates operational management already as being error-prone, and the high number of security issues in connection to faulty usage of `delegatecall`.

To mitigate this vulnerability, the developers should check the `nonce` variable before and after the `delegatecall` inside the `_execute()` function as well. This can be tested by adding the provided code to the `test/Vault.t.sol` file and running `forge test --match-test "testExecuteNoRevertIfReinitialized" -vvvv`. If the test succeeds, the Vault got re-initialized due to a `delegatecall` altering the Vault's `nonce` variable.

### Original Finding Content

_Submitted by byterocket, also found by 242, &#95;141345&#95;, 0x1f8b, ACai, ayeslick, berndartmueller, BradMoon, cccz, Chom, giovannidisiena, infosec&#95;us&#95;team, Lambda, minhtrng, nine9, oyc&#95;109, PwnedNoMore, reassor, scaraven, slywaters, sseefried, tofunmi, Twpony, and unforgiven_

<https://github.com/code-423n4/2022-07-fractional/blob/main/src/Vault.sol#L62>

<https://github.com/code-423n4/2022-07-fractional/blob/main/src/Vault.sol#L126>

<https://github.com/code-423n4/2022-07-fractional/blob/main/src/Vault.sol#L25>

### Impact

The `Vault#execute` function calls a target contract's function via `delegatecall` if the caller is either the owner of the Vault or the target contract is part of a merkle tree, indicating a permission to call the target contract.

```solidity
// Check that the caller is either a module with permission to call or the owner.
if (!MerkleProof.verify(_proof, merkleRoot, leaf)) {
    if (msg.sender != owner)
        revert NotAuthorized(msg.sender, _target, selector);
}
```

*(See [Vault#execute](https://github.com/code-423n4/2022-07-fractional/blob/main/src/Vault.sol#L62))*

If the checks succeed, the internal `_execute()` function is used to execute the call via `delegatecall`.

`delegatecall`s have to be used with caution because the contract being called is using the caller's contract storage, i.e. the callee contract can alter the caller's contract state (for more info, see [Solidity docs](https://docs.soliditylang.org/en/latest/introduction-to-smart-contracts.html?highlight=delegatecall#delegatecall-callcode-and-libraries)).

The developers seem to be aware of the danger that the callee contract is able to overtake the Vaults ownership, by changing the Vaults `owner` variable, as the `owner` is cached before the `delegatecall` and afterwards checked that the variable did not change:

```solidity
// ...
address owner_ = owner;
// ...
(success, response) = _target.delegatecall{gas:stipend}(_data);
if (owner_ != owner) revert OwnerChanged(owner_, owner);
// ...
```

*(See [Vault#\_execute](https://github.com/code-423n4/2022-07-fractional/blob/main/src/Vault.sol#L126))*

However, changing the `owner` variable is not the only way the callee contract is able to overtake the Vaults ownership. If the `nonce` variable is re-set to `0`, the Vault's `init` function becomes callable again, granting ownership to the caller:

```solidity
function init() external {
    if (nonce != 0) revert Initialized(owner, msg.sender, nonce);
    nonce = 1;
    owner = msg.sender;
}
```

*(See [Vault#init](https://github.com/code-423n4/2022-07-fractional/blob/main/src/Vault.sol#L25))*

Note that other storage variables (i.e. `merkleRoot` and `methods`) could also be altered, but this would not lead to a loss in ownership, i.e. the project could re-set the variables.

Nevertheless, a contract trying, due to being malicious or faulty, to change the Vaults ownership first needs to be permissioned by the owner by adding it to the merkle tree. Otherwise, the contract can not be called.

Due to the fact that the `owner` variable check is included, meaning **the project rates operational management already as being error-prone**, and the high number of security issues in connection to faulty usage of `delegatecall`, the severity is rated as MEDIUM (HIGH impact with a LOW likelihood).

### Proof of Concept

Add the following code to the `test/Vault.t.sol` file and run `forge test --match-test "testExecuteNoRevertIfReinitialized" -vvvv`.

If the test succeeds, the Vault got re-initialized due to a `delegatecall` altering the Vault's `nonce` variable.

```solidity
// Inside contract VaultTest.
function testExecuteNoRevertIfReinitialized() public {
    vaultProxy.init(); // address(this) is owner
    HackyTargetContract targetContract = new HackyTargetContract();
    bytes32[] memory proof = new bytes32[](1);
    bytes memory data = abi.encodeCall(
        targetContract.changeNonce,
        ()
    );

    // Note that the call does NOT revert.
    vaultProxy.execute(address(targetContract), data, proof);

    // Note that the Vault can now be re-initialized as the execute
    // call above set the Vault's nonce to zero.
    vm.prank(address(1));
    vaultProxy.init();

    assertEq(vaultProxy.owner(), address(1));
}

// Outside contract VaultTest.
contract HackyTargetContract {
    address public gap_owner;
    bytes32 public gap_merkleRoot;

    uint256 public nonce;

    function changeNonce() public {
        nonce = 0;
    }
}
```

### Recommended Mitigation Steps

Check the `nonce` variable before and after the `delegatecall` inside the `_execute()` function as well, e.g.:

```solidity
address owner_ = owner;
uint256 nonce_ = nonce;

// Execute delegatecall

if (owner_ != owner || nonce_ != nonce) {
    revert InvalidStateChange();
}

// ...
```

**[mehtaculous (Fractional) confirmed](https://github.com/code-423n4/2022-07-fractional-findings/issues/535)** 

**[HardlyDifficult (judge) commented](https://github.com/code-423n4/2022-07-fractional-findings/issues/487#issuecomment-1196108703):**
 > Due to the use of delegate call, `execute` and/or the fallback function could lead to changing the proxy's storage or even self destructing the proxy instance. If this were to happen, users funds could be put at risk. These attacks are predicated on the current vault owner to maliciously or unintentionally directly call or approve the calling of a malicious plugin -- because of this, I agree with the warden here that this is a Medium risk issue.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Fractional |
| Report Date | N/A |
| Finders | _141345_, scaraven, berndartmueller, giovannidisiena, minhtrng, Twpony, Chom, Lambda, nine9, 0x1f8b, tofunmi, PwnedNoMore, BradMoon, reassor, cccz, ACai, slywaters, oyc_109, infosec_us_team, sseefried, 242, byterocket, ayeslick, unforgiven |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-fractional
- **GitHub**: https://github.com/code-423n4/2022-07-fractional-findings/issues/487
- **Contest**: https://code4rena.com/contests/2022-07-fractional-v2-contest

### Keywords for Search

`Delegate`

