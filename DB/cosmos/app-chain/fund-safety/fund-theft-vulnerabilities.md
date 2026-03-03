---
protocol: generic
chain: cosmos
category: fund_safety
vulnerability_type: fund_theft_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: fund_safety_logic

primitives:
  - theft_auth_bypass
  - theft_manipulation
  - theft_reentrancy
  - theft_delegatecall
  - theft_replay
  - theft_frontrunning
  - theft_surplus
  - race_condition
  - missing_slippage

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - fund_safety
  - staking
  - defi

language: go|solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Funds Theft Auth Bypass
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Cannot Blame Operator for Proposed Validator | `reports/cosmos_cometbft_findings/cannot-blame-operator-for-proposed-validator.md` | MEDIUM | ConsenSys |
| [H-08] Attacker can deploy vaults with a malicious Staking c | `reports/cosmos_cometbft_findings/h-08-attacker-can-deploy-vaults-with-a-malicious-staking-contract.md` | HIGH | Code4rena |
| `LiquidationAccountant.claim()` can be called by anyone caus | `reports/cosmos_cometbft_findings/h-14-liquidationaccountantclaim-can-be-called-by-anyone-causing-vault-insolvency.md` | HIGH | Sherlock |
| Anyone can deposit and mint withdrawal proxy shares to captu | `reports/cosmos_cometbft_findings/h-20-anyone-can-deposit-and-mint-withdrawal-proxy-shares-to-capture-distributed-.md` | HIGH | Sherlock |
| Lack of access control in PublicVault.sol#transferWithdrawRe | `reports/cosmos_cometbft_findings/h-26-lack-of-access-control-in-publicvaultsoltransferwithdrawreserve-let-user-ca.md` | HIGH | Sherlock |
| liquidationAccountant can be claimed at any time | `reports/cosmos_cometbft_findings/h-34-liquidationaccountant-can-be-claimed-at-any-time.md` | HIGH | Sherlock |
| _deleteLienPosition can be called by anyone to delete any li | `reports/cosmos_cometbft_findings/h-4-_deletelienposition-can-be-called-by-anyone-to-delete-any-lien-they-wish.md` | HIGH | Sherlock |
| There are no Illuminate PT transfers from the owner in ERC50 | `reports/cosmos_cometbft_findings/h-7-there-are-no-illuminate-pt-transfers-from-the-owner-in-erc5095s-withdraw-and.md` | HIGH | Sherlock |

### Funds Theft Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| CVGT Staking Pool State Manipulation | `reports/cosmos_cometbft_findings/cvgt-staking-pool-state-manipulation.md` | HIGH | OtterSec |
| [H-08] Adversary can use `send_nft` to bypass the payment an | `reports/cosmos_cometbft_findings/h-08-adversary-can-use-send_nft-to-bypass-the-payment-and-steal-sellers-token-in.md` | HIGH | Code4rena |
| Unlimited mint of Illuminate PTs is possible whenever any ma | `reports/cosmos_cometbft_findings/h-1-unlimited-mint-of-illuminate-pts-is-possible-whenever-any-market-is-uninitia.md` | HIGH | Sherlock |
| [H-18] Old stakers can steal deposits of new stakers in Stak | `reports/cosmos_cometbft_findings/h-18-old-stakers-can-steal-deposits-of-new-stakers-in-stakingfundsvault.md` | HIGH | Code4rena |
| [H-20] Possibly reentrancy attacks in _distributeETHRewardsT | `reports/cosmos_cometbft_findings/h-20-possibly-reentrancy-attacks-in-_distributeethrewardstouserfortoken-function.md` | HIGH | Code4rena |
| [H-21] bringUnusedETHBackIntoGiantPool in GiantMevAndFeesPoo | `reports/cosmos_cometbft_findings/h-21-bringunusedethbackintogiantpool-in-giantmevandfeespool-can-be-used-to-steal.md` | HIGH | Code4rena |
| Tier winner can steal excess funds from tiered percentage bo | `reports/cosmos_cometbft_findings/h-3-tier-winner-can-steal-excess-funds-from-tiered-percentage-bounty-if-any-depo.md` | HIGH | Sherlock |
| Any public vault without a delegate can be drained | `reports/cosmos_cometbft_findings/h-30-any-public-vault-without-a-delegate-can-be-drained.md` | HIGH | Sherlock |

### Funds Theft Reentrancy
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-02] The reentrancy vulnerability in _safeMint can allow a | `reports/cosmos_cometbft_findings/h-02-the-reentrancy-vulnerability-in-_safemint-can-allow-an-attacker-to-steal-al.md` | HIGH | Code4rena |
| [H-20] Possibly reentrancy attacks in _distributeETHRewardsT | `reports/cosmos_cometbft_findings/h-20-possibly-reentrancy-attacks-in-_distributeethrewardstouserfortoken-function.md` | HIGH | Code4rena |

### Funds Theft Delegatecall
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| DELEGATECALL to staking precompile allows theft of all stake | `reports/cosmos_cometbft_findings/delegatecall-to-staking-precompile-allows-theft-of-all-staked-mon.md` | HIGH | Spearbit |

### Funds Theft Replay
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Signature Replay Attack Possible Between Stake, Unstake and  | `reports/cosmos_cometbft_findings/signature-replay-attack-possible-between-stake-unstake-and-reward-functions-enab.md` | HIGH | Quantstamp |

### Funds Theft Frontrunning
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-18] Old stakers can steal deposits of new stakers in Stak | `reports/cosmos_cometbft_findings/h-18-old-stakers-can-steal-deposits-of-new-stakers-in-stakingfundsvault.md` | HIGH | Code4rena |
| [H-21] bringUnusedETHBackIntoGiantPool in GiantMevAndFeesPoo | `reports/cosmos_cometbft_findings/h-21-bringunusedethbackintogiantpool-in-giantmevandfeespool-can-be-used-to-steal.md` | HIGH | Code4rena |
| A part of ETH rewards can be stolen by sandwiching `claimDel | `reports/cosmos_cometbft_findings/m-3-a-part-of-eth-rewards-can-be-stolen-by-sandwiching-claimdelayedwithdrawals.md` | MEDIUM | Sherlock |
| Deposit Theft by Crashing LP Spot Prices Through MEV | `reports/cosmos_cometbft_findings/m-4-deposit-theft-by-crashing-lp-spot-prices-through-mev.md` | MEDIUM | Sherlock |

### Funds Theft Surplus
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Tier winner can steal excess funds from tiered percentage bo | `reports/cosmos_cometbft_findings/h-3-tier-winner-can-steal-excess-funds-from-tiered-percentage-bounty-if-any-depo.md` | HIGH | Sherlock |
| [VLTS3-13] Direct theft of surplus balance when unstaking st | `reports/cosmos_cometbft_findings/vlts3-13-direct-theft-of-surplus-balance-when-unstaking-sthype.md` | HIGH | Hexens |

### Funds Missing Slippage
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-04] Withdrawals logic allows MEV exploits of TVL changes  | `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md` | HIGH | Code4rena |
| Illuminate's PT doesn't respect users' slippage specificatio | `reports/cosmos_cometbft_findings/h-1-illuminates-pt-doesnt-respect-users-slippage-specifications-for-underlyings.md` | HIGH | Sherlock |
| Illuminate's PT doesn't respect users' slippage specificatio | `reports/cosmos_cometbft_findings/h-12-illuminates-pt-doesnt-respect-users-slippage-specifications.md` | HIGH | Sherlock |
| [M-01] Missing slippage protection in `AerodromeDexter.sol`  | `reports/cosmos_cometbft_findings/m-01-missing-slippage-protection-in-aerodromedextersol-swapexacttokensfortokens.md` | MEDIUM | Code4rena |
| [M-04] Lack of deadline for uniswap AMM | `reports/cosmos_cometbft_findings/m-04-lack-of-deadline-for-uniswap-amm.md` | MEDIUM | Code4rena |
| [M-07] Lack of slippage and deadline during withdraw and dep | `reports/cosmos_cometbft_findings/m-07-lack-of-slippage-and-deadline-during-withdraw-and-deposit.md` | MEDIUM | Code4rena |
| `rebalanceLite` should provide a slippage protection | `reports/cosmos_cometbft_findings/m-1-rebalancelite-should-provide-a-slippage-protection.md` | MEDIUM | Sherlock |
| Slippage on `MetapoolRouter.addLiquidityOneETHKeepYt` | `reports/cosmos_cometbft_findings/m-5-slippage-on-metapoolrouteraddliquidityoneethkeepyt.md` | MEDIUM | Sherlock |

---

# Fund Theft Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Fund Theft Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Funds Theft Auth Bypass](#1-funds-theft-auth-bypass)
2. [Funds Theft Manipulation](#2-funds-theft-manipulation)
3. [Funds Theft Reentrancy](#3-funds-theft-reentrancy)
4. [Funds Theft Delegatecall](#4-funds-theft-delegatecall)
5. [Funds Theft Replay](#5-funds-theft-replay)
6. [Funds Theft Frontrunning](#6-funds-theft-frontrunning)
7. [Funds Theft Surplus](#7-funds-theft-surplus)
8. [Funds Missing Slippage](#8-funds-missing-slippage)

---

## 1. Funds Theft Auth Bypass

### Overview

Implementation flaw in funds theft auth bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 14 audit reports with severity distribution: HIGH: 8, MEDIUM: 6.

> **Key Finding**: This bug report is about a problem with the StakeModuleLib.sol code in the Portal contracts. The code allows anyone to blame an operator who does not withdraw in time, but there is an additional scenario where the operator should be blamed. When a validator is in the PROPOSED state, the operator can

### Vulnerability Description

#### Root Cause

Implementation flaw in funds theft auth bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies funds theft auth bypass in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to funds operations

### Vulnerable Pattern Examples

**Example 1: Cannot Blame Operator for Proposed Validator** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/cannot-blame-operator-for-proposed-validator.md`
```solidity
function blameOperator(
 PooledStaking storage self,
 DSML.IsolatedStorage storage DATASTORE,
 bytes calldata pk
) external {
 require(
 self.validators[pk].state == VALIDATOR\_STATE.ACTIVE,
 "SML:validator is never activated"
 );
 require(
 block.timestamp > self.validators[pk].createdAt + self.validators[pk].period,
 "SML:validator is active"
 );

 \_imprison(DATASTORE, self.validators[pk].operatorId, pk);
}
```

**Example 2: [H-08] Attacker can deploy vaults with a malicious Staking contract** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-08-attacker-can-deploy-vaults-with-a-malicious-staking-contract.md`
```solidity
function test__deploy_malicious_staking_contract() public {
    addTemplate("Adapter", templateId, adapterImpl, true, true);
    addTemplate("Strategy", "MockStrategy", strategyImpl, false, true);
    addTemplate("Vault", "V1", vaultImpl, true, true);

    // Pretend this malicious Staking contract allows attacker to withdraw
    // all the funds from it while allowing users to use it like a normal Staking contract
    MultiRewardStaking maliciousStaking = new MultiRewardStaking();

    vm.startPrank(alice);
    address vault = controller.deployVault(
      VaultInitParams({
        asset: iAsset,
        adapter: IERC4626(address(0)),
        fees: VaultFees({
          deposit: 100,
          withdrawal: 200,
          management: 300,
          performance: 400
        }),
        feeRecipient: feeRecipient,
        owner: address(this)
      }),
      DeploymentArgs({ id: templateId, data: abi.encode(uint256(100)) }),
      DeploymentArgs({ id: 0, data: "" }),
      address(maliciousStaking),
      "",
      VaultMetadata({
        vault: address(0),
        staking: address(maliciousStaking),
        creator: alice,
        metadataCID: metadataCid,
        swapTokenAddresses: swapTokenAddresses,
        swapAddress: address(0x5555),
        exchange: uint256(1)
// ... (truncated)
```

**Example 3: `LiquidationAccountant.claim()` can be called by anyone causing vault insolvency** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-14-liquidationaccountantclaim-can-be-called-by-anyone-causing-vault-insolvency.md`
```
// Vulnerable pattern from Astaria:
Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/188
```

**Example 4: There are no Illuminate PT transfers from the owner in ERC5095's withdraw and re** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-7-there-are-no-illuminate-pt-transfers-from-the-owner-in-erc5095s-withdraw-and.md`
```solidity
/// @notice At or after maturity, Burns `shares` from `owner` and sends exactly `assets` of underlying tokens to `receiver`. Before maturity, sends `assets` by selling shares of PT on a YieldSpace AMM.
    /// @param a The amount of underlying tokens withdrawn
    /// @param r The receiver of the underlying tokens being withdrawn
    /// @param o The owner of the underlying tokens
    /// @return uint256 The amount of principal tokens burnt by the withdrawal
    function withdraw(
        uint256 a,
        address r,
        address o
    ) external override returns (uint256) {
        // Pre maturity
        if (block.timestamp < maturity) {
            uint128 shares = Cast.u128(previewWithdraw(a));
            // If owner is the sender, sell PT without allowance check
            if (o == msg.sender) {
                uint128 returned = IMarketPlace(marketplace).sellPrincipalToken(
                    underlying,
                    maturity,
                    shares,
                    Cast.u128(a - (a / 100))
                );
                Safe.transfer(IERC20(underlying), r, returned);
                return returned;
                // Else, sell PT with allowance check
            } else {
                uint256 allowance = _allowance[o][msg.sender];
                if (allowance < shares) {
                    revert Exception(
                        20,
                        allowance,
                        shares,
                        address(0),
                        address(0)
                    );
                }
// ... (truncated)
```

**Example 5: [M-07] `Vested CSX` to `Regular CSX` Conversion Process Enables Potential Unauth** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-07-vested-csx-to-regular-csx-conversion-process-enables-potential-unauthorized.md`
```solidity
/// @notice Executes a forced withdrawal of tokens from the contract.
/// @dev Can only be called by the council to mitigate against malicious vesters.
/// @param amount Specifies the amount of tokens to be withdrawn.
function cliff(uint256 amount) external onlyCouncil {
  if (amount > vesting.amount || amount == 0) {
    revert NotEnoughTokens();
  }
  vesting.amount -= amount;
  cliffedAmount += amount;
  sCsxToken.unStake(amount);
  csxToken.safeTransfer(msg.sender, amount);
  emit Cliff(msg.sender, amount, vesting.amount);
}
```

**Variant: Funds Theft Auth Bypass - HIGH Severity Cases** [HIGH]
> Found in 8 reports:
> - `reports/cosmos_cometbft_findings/h-08-attacker-can-deploy-vaults-with-a-malicious-staking-contract.md`
> - `reports/cosmos_cometbft_findings/h-14-liquidationaccountantclaim-can-be-called-by-anyone-causing-vault-insolvency.md`
> - `reports/cosmos_cometbft_findings/h-20-anyone-can-deposit-and-mint-withdrawal-proxy-shares-to-capture-distributed-.md`

**Variant: Funds Theft Auth Bypass in Astaria** [HIGH]
> Protocol-specific variant found in 5 reports:
> - `reports/cosmos_cometbft_findings/h-14-liquidationaccountantclaim-can-be-called-by-anyone-causing-vault-insolvency.md`
> - `reports/cosmos_cometbft_findings/h-20-anyone-can-deposit-and-mint-withdrawal-proxy-shares-to-capture-distributed-.md`
> - `reports/cosmos_cometbft_findings/h-26-lack-of-access-control-in-publicvaultsoltransferwithdrawreserve-let-user-ca.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in funds theft auth bypass logic allows exploitation through missing validation,
func secureFundsTheftAuthBypass(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 14 audit reports
- **Severity Distribution**: HIGH: 8, MEDIUM: 6
- **Affected Protocols**: Csx, EigenLabs — EigenLayer, Astaria, Olas, Popcorn
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Funds Theft Manipulation

### Overview

Implementation flaw in funds theft manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 17 audit reports with severity distribution: HIGH: 13, MEDIUM: 4.

> **Key Finding**: The report highlights a potential vulnerability in the CVGT staking state that can be exploited by manipulating the CVGT mint and CVGTStakingPoolState accounts. This allows attackers to set any CVGT on a poolstate and stability_pool_state, as well as spoof the CVGTStakingPoolState, potentially enabl

### Vulnerability Description

#### Root Cause

Implementation flaw in funds theft manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies funds theft manipulation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to funds operations

### Vulnerable Pattern Examples

**Example 1: CVGT Staking Pool State Manipulation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/cvgt-staking-pool-state-manipulation.md`
```rust
pub struct Initialize<'info> {
    #[account()]
    pub cvgt: Box<Account<'info, Mint>>,
}
```

**Example 2: [H-08] Adversary can use `send_nft` to bypass the payment and steal seller's tok** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-08-adversary-can-use-send_nft-to-bypass-the-payment-and-steal-sellers-token-in.md`
```rust
File: contracts/codedestate/src/execute.rs
fn send_nft(
    &self,
    deps: DepsMut,
    env: Env,
    info: MessageInfo,
    contract: String,
    token_id: String,
    msg: Binary,
) -> Result<Response<C>, ContractError> {
    // Transfer token
    self._transfer_nft(deps, &env, &info, &contract, &token_id)?; // @c4-contest: just transfer token, no trade settlement logic

    let send = Cw721ReceiveMsg {
        sender: info.sender.to_string(),
        token_id: token_id.clone(),
        msg,
    };

    // Send message
    Ok(Response::new()
        .add_message(send.into_cosmos_msg(contract.clone())?)
        .add_attribute("action", "send_nft")
        .add_attribute("sender", info.sender)
        .add_attribute("recipient", contract)
        .add_attribute("token_id", token_id))
}

pub fn _transfer_nft(
    &self,
    deps: DepsMut,
    env: &Env,
    info: &MessageInfo,
    recipient: &str,
    token_id: &str,
// ... (truncated)
```

**Example 3: Unlimited mint of Illuminate PTs is possible whenever any market is uninitialize** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-1-unlimited-mint-of-illuminate-pts-is-possible-whenever-any-market-is-uninitia.md`
```solidity
/// @notice mint swaps the sender's principal tokens for Illuminate's ERC5095 tokens in effect, this opens a new fixed rate position for the sender on Illuminate
    /// @param p principal value according to the MarketPlace's Principals Enum
    /// @param u address of an underlying asset
    /// @param m maturity (timestamp) of the market
    /// @param a amount being minted
    /// @return bool true if the mint was successful
    function mint(
        uint8 p,
        address u,
        uint256 m,
        uint256 a
    ) external unpaused(u, m, p) returns (bool) {
        // Fetch the desired principal token
        address principal = IMarketPlace(marketPlace).token(u, m, p);

        // Transfer the users principal tokens to the lender contract
        Safe.transferFrom(IERC20(principal), msg.sender, address(this), a);

        // Mint the tokens received from the user
        IERC5095(principalToken(u, m)).authMint(msg.sender, a);

        emit Mint(p, u, m, a);

        return true;
    }
```

**Example 4: [H-18] Old stakers can steal deposits of new stakers in StakingFundsVault** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-18-old-stakers-can-steal-deposits-of-new-stakers-in-stakingfundsvault.md`
```go
if (i == 0 && !Syndicate(payable(liquidStakingNetworkManager.syndicate())).isNoLongerPartOfSyndicate(_blsPubKeys[i])) {
    // Withdraw any ETH accrued on free floating SLOT from syndicate to this contract
    // If a partial list of BLS keys that have free floating staked are supplied, then partial funds accrued will be fetched
    _claimFundsFromSyndicateForDistribution(
        liquidStakingNetworkManager.syndicate(),
        _blsPubKeys
    );

    // Distribute ETH per LP
    updateAccumulatedETHPerLP();
}

// If msg.sender has a balance for the LP token associated with the BLS key, then send them any accrued ETH
LPToken token = lpTokenForKnot[_blsPubKeys[i]];
require(address(token) != address(0), "Invalid BLS key");
require(token.lastInteractedTimestamp(msg.sender) + 30 minutes < block.timestamp, "Last transfer too recent");
_distributeETHRewardsToUserForToken(msg.sender, address(token), token.balanceOf(msg.sender), _recipient);
```

**Example 5: Tier winner can steal excess funds from tiered percentage bounty if any deposits** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-3-tier-winner-can-steal-excess-funds-from-tiered-percentage-bounty-if-any-depo.md`
```
// Vulnerable pattern from OpenQ:
Source: https://github.com/sherlock-audit/2023-02-openq-judging/issues/275
```

**Variant: Funds Theft Manipulation - MEDIUM Severity Cases** [MEDIUM]
> Found in 4 reports:
> - `reports/cosmos_cometbft_findings/m-08-factorycreate-is-vulnerable-to-reorg-attacks.md`
> - `reports/cosmos_cometbft_findings/m-4-deposit-theft-by-crashing-lp-spot-prices-through-mev.md`
> - `reports/cosmos_cometbft_findings/m-5-malicious-or-compromised-admin-of-certain-lsts-could-manipulate-the-price.md`

**Variant: Funds Theft Manipulation in Stakehouse Protocol** [HIGH]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/h-18-old-stakers-can-steal-deposits-of-new-stakers-in-stakingfundsvault.md`
> - `reports/cosmos_cometbft_findings/h-20-possibly-reentrancy-attacks-in-_distributeethrewardstouserfortoken-function.md`
> - `reports/cosmos_cometbft_findings/h-21-bringunusedethbackintogiantpool-in-giantmevandfeespool-can-be-used-to-steal.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in funds theft manipulation logic allows exploitation through missing validation
func secureFundsTheftManipulation(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 17 audit reports
- **Severity Distribution**: HIGH: 13, MEDIUM: 4
- **Affected Protocols**: Brahma, Goat Tech, Astaria, Stakehouse Protocol, Convergent
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Funds Theft Reentrancy

### Overview

Implementation flaw in funds theft reentrancy logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 2.

> **Key Finding**: This bug report is about a reentrancy vulnerability in the _safeMint function of the XDEFIDistribution.sol contract. This function is called by the lock function which changes the totalDepositedXDEFI variable. Since the updateDistribution function does not have the noReenter modifier, an attacker ca

### Vulnerability Description

#### Root Cause

Implementation flaw in funds theft reentrancy logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies funds theft reentrancy in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to funds operations

### Vulnerable Pattern Examples

**Example 1: [H-02] The reentrancy vulnerability in _safeMint can allow an attacker to steal ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-the-reentrancy-vulnerability-in-_safemint-can-allow-an-attacker-to-steal-al.md`
```solidity
function _safeMint(
    address to,
    uint256 tokenId,
    bytes memory _data
) internal virtual {
    _mint(to, tokenId);
    require(
        _checkOnERC721Received(address(0), to, tokenId, _data),
        "ERC721: transfer to non ERC721Receiver implementer"
    );
}
...
function _checkOnERC721Received(
    address from,
    address to,
    uint256 tokenId,
    bytes memory _data
) private returns (bool) {
    if (to.isContract()) {
        try IERC721Receiver(to).onERC721Received(_msgSender(), from, tokenId, _data) returns (bytes4 retval) {
            return retval == IERC721Receiver.onERC721Received.selector;
```

**Example 2: [H-20] Possibly reentrancy attacks in _distributeETHRewardsToUserForToken functi** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-20-possibly-reentrancy-attacks-in-_distributeethrewardstouserfortoken-function.md`
```
// Vulnerable pattern from Stakehouse Protocol:
## Lines of code

https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/SyndicateRewardsProcessor.sol#L51-L73
https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/GiantMevAndFeesPool.sol#L146-L167
https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/GiantPoolBase.sol#L66-L90
https://github.com/code-
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in funds theft reentrancy logic allows exploitation through missing validation, 
func secureFundsTheftReentrancy(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 2 audit reports
- **Severity Distribution**: HIGH: 2
- **Affected Protocols**: XDEFI, Stakehouse Protocol
- **Validation Strength**: Single auditor

---

## 4. Funds Theft Delegatecall

### Overview

Implementation flaw in funds theft delegatecall logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: This bug report discusses a critical risk issue found in a commit of a protocol. The staking precompile does not properly enforce the EVMC message kind, which can lead to malicious contracts stealing staked MON. The issue has been fixed in a later commit, but the report recommends enforcing `CALL` f

### Vulnerability Description

#### Root Cause

Implementation flaw in funds theft delegatecall logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies funds theft delegatecall in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to funds operations

### Vulnerable Pattern Examples

**Example 1: DELEGATECALL to staking precompile allows theft of all staked MON** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/delegatecall-to-staking-precompile-allows-theft-of-all-staked-mon.md`
```
// Vulnerable pattern from Monad:
## Security Report
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in funds theft delegatecall logic allows exploitation through missing validation
func secureFundsTheftDelegatecall(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: HIGH: 1
- **Affected Protocols**: Monad
- **Validation Strength**: Single auditor

---

## 5. Funds Theft Replay

### Overview

Implementation flaw in funds theft replay logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: This bug report is about a vulnerability found in the SapienRewards and SapienStaking contracts. These contracts have a function called "verifyOrder()" which uses the same signature format and validation logic. This allows an attacker to reuse signatures across different contract functions, allowing

### Vulnerability Description

#### Root Cause

Implementation flaw in funds theft replay logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies funds theft replay in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to funds operations

### Vulnerable Pattern Examples

**Example 1: Signature Replay Attack Possible Between Stake, Unstake and Reward Functions Ena** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/signature-replay-attack-possible-between-stake-unstake-and-reward-functions-enab.md`
```go
bytes32 messageHash = keccak256(abi.encodePacked(userWallet, rewardAmount, orderId));
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in funds theft replay logic allows exploitation through missing validation, inco
func secureFundsTheftReplay(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: HIGH: 1
- **Affected Protocols**: Sapien
- **Validation Strength**: Single auditor

---

## 6. Funds Theft Frontrunning

### Overview

Implementation flaw in funds theft frontrunning logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 2, MEDIUM: 2.

> **Key Finding**: This bug report is about a vulnerability in the StakingFundsVault contract that allows stakers to the MEV+fees vault to steal funds from new stakers who staked after a validator was registered and the derivatives were minted. A single staker who staked 4 ETH can steal all funds deposited by new stak

### Vulnerability Description

#### Root Cause

Implementation flaw in funds theft frontrunning logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies funds theft frontrunning in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to funds operations

### Vulnerable Pattern Examples

**Example 1: [H-18] Old stakers can steal deposits of new stakers in StakingFundsVault** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-18-old-stakers-can-steal-deposits-of-new-stakers-in-stakingfundsvault.md`
```go
if (i == 0 && !Syndicate(payable(liquidStakingNetworkManager.syndicate())).isNoLongerPartOfSyndicate(_blsPubKeys[i])) {
    // Withdraw any ETH accrued on free floating SLOT from syndicate to this contract
    // If a partial list of BLS keys that have free floating staked are supplied, then partial funds accrued will be fetched
    _claimFundsFromSyndicateForDistribution(
        liquidStakingNetworkManager.syndicate(),
        _blsPubKeys
    );

    // Distribute ETH per LP
    updateAccumulatedETHPerLP();
}

// If msg.sender has a balance for the LP token associated with the BLS key, then send them any accrued ETH
LPToken token = lpTokenForKnot[_blsPubKeys[i]];
require(address(token) != address(0), "Invalid BLS key");
require(token.lastInteractedTimestamp(msg.sender) + 30 minutes < block.timestamp, "Last transfer too recent");
_distributeETHRewardsToUserForToken(msg.sender, address(token), token.balanceOf(msg.sender), _recipient);
```

**Example 2: [H-21] bringUnusedETHBackIntoGiantPool in GiantMevAndFeesPool can be used to ste** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-21-bringunusedethbackintogiantpool-in-giantmevandfeespool-can-be-used-to-steal.md`
```
// Vulnerable pattern from Stakehouse Protocol:
## Lines of code

https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/GiantMevAndFeesPool.sol#L126
```

**Example 3: A part of ETH rewards can be stolen by sandwiching `claimDelayedWithdrawals()`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-3-a-part-of-eth-rewards-can-be-stolen-by-sandwiching-claimdelayedwithdrawals.md`
```go
receive() external payable {
    (bool success,) = address(rewardDistributor()).call{value: msg.value}('');
    require(success);
}
```

**Example 4: Deposit Theft by Crashing LP Spot Prices Through MEV** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-4-deposit-theft-by-crashing-lp-spot-prices-through-mev.md`
```
// Vulnerable pattern from Blueberry:
Source: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/220
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in funds theft frontrunning logic allows exploitation through missing validation
func secureFundsTheftFrontrunning(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 4 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 2
- **Affected Protocols**: Blueberry, Stakehouse Protocol, Rio Network
- **Validation Strength**: Moderate (2 auditors)

---

## 7. Funds Theft Surplus

### Overview

Implementation flaw in funds theft surplus logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 2.

> **Key Finding**: This bug report is about a vulnerability in a tiered percentage bounty contract where a tier winner can exploit the bounty to steal funds if the main deposit is refundable by the time the bounty is closed. The vulnerability is caused by the balance snapshot, which is taken when the bounty is closed,

### Vulnerability Description

#### Root Cause

Implementation flaw in funds theft surplus logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies funds theft surplus in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to funds operations

### Vulnerable Pattern Examples

**Example 1: Tier winner can steal excess funds from tiered percentage bounty if any deposits** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-3-tier-winner-can-steal-excess-funds-from-tiered-percentage-bounty-if-any-depo.md`
```
// Vulnerable pattern from OpenQ:
Source: https://github.com/sherlock-audit/2023-02-openq-judging/issues/275
```

**Example 2: [VLTS3-13] Direct theft of surplus balance when unstaking stHYPE** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/vlts3-13-direct-theft-of-surplus-balance-when-unstaking-sthype.md`
```go
token1.deposit{value: balanceSurplus}();
// Pool reserves are measured as balances, hence we can replenish it with token1
// by transfering directly
token1.safeTransfer(stexInterface.pool(), balanceSurplus);
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in funds theft surplus logic allows exploitation through missing validation, inc
func secureFundsTheftSurplus(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 2 audit reports
- **Severity Distribution**: HIGH: 2
- **Affected Protocols**: OpenQ, Valantis
- **Validation Strength**: Moderate (2 auditors)

---

## 8. Funds Missing Slippage

### Overview

Implementation flaw in funds missing slippage logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 11 audit reports with severity distribution: HIGH: 4, MEDIUM: 7.

> **Key Finding**: This bug report discusses a vulnerability in the Renzo protocol that allows for exploitation of the system by manipulating asset prices. This can result in value being lost to malicious actors and causing losses for ezETH holders. The report outlines three possible scenarios in which this vulnerabil

### Vulnerability Description

#### Root Cause

Implementation flaw in funds missing slippage logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies funds missing slippage in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to funds operations

### Vulnerable Pattern Examples

**Example 1: [H-04] Withdrawals logic allows MEV exploits of TVL changes and zero-slippage ze** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md`
```
// Vulnerable pattern from Renzo:
Deposit and withdrawal requests can be done immediately with no costs or fees, and both use the current oracle prices and TVL calculation ([`deposit`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/RestakeManager.sol#L499-L504), and [`withdraw`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Withdraw/WithdrawQueue.sol#L217)). Crucially, the [withdrawal amount is calculated at withdrawal request submission time](https://github.com/code-423n4/2024-04-renzo/blob/ma
```

**Example 2: Illuminate's PT doesn't respect users' slippage specifications for underlyings** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-1-illuminates-pt-doesnt-respect-users-slippage-specifications-for-underlyings.md`
```go
// File: src/tokens/ERC5095.sol : ERC5095.withdraw()   #1

271                    uint128 returned = IMarketPlace(marketplace).sellPrincipalToken(
272                        underlying,
273                        maturity,
274                        shares,
275 @>                     Cast.u128(a - (a / 100))
276:                   );
```

**Example 3: Illuminate's PT doesn't respect users' slippage specifications** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-12-illuminates-pt-doesnt-respect-users-slippage-specifications.md`
```go
// File: src/tokens/ERC5095.sol : ERC5095.withdraw()   #1

219                    uint128 returned = IMarketPlace(marketplace).sellPrincipalToken(
220                        underlying,
221                        maturity,
222                        shares,
223 @>                     Cast.u128(a - (a / 100))
224                    );
225                    Safe.transfer(IERC20(underlying), r, returned);
226:                   return returned;
```

**Example 4: [M-01] Missing slippage protection in `AerodromeDexter.sol` `swapExactTokensForT** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-missing-slippage-protection-in-aerodromedextersol-swapexacttokensfortokens.md`
```go
uint256 _balanceBefore = ERC20(_tokenOut).balanceOf(address(this));
@>>        router.swapExactTokensForTokens(_amountIn, 0, routeOf[_tokenIn][_tokenOut], address(this), block.timestamp);
```

**Example 5: [M-04] Lack of deadline for uniswap AMM** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-lack-of-deadline-for-uniswap-amm.md`
```
// Vulnerable pattern from Asymmetry Finance:
<https://github.com/code-423n4/2023-03-asymmetry/blob/main/contracts/SafEth/derivatives/Reth.sol#L83-L102>

### Proof of Concept

The ISwapRouter.exactInputSingle params (used in the rocketpool derivative) does not include a deadline currently.

    ISwapRouter.ExactInputSingleParams memory params = ISwapRouter
        .ExactInputSingleParams({
            tokenIn: _tokenIn,
            tokenOut: _tokenOut,
            fee: _poolFee,
            recipient: address(this),
            amountIn: _a
```

**Variant: Funds Missing Slippage - MEDIUM Severity Cases** [MEDIUM]
> Found in 7 reports:
> - `reports/cosmos_cometbft_findings/m-01-missing-slippage-protection-in-aerodromedextersol-swapexacttokensfortokens.md`
> - `reports/cosmos_cometbft_findings/m-04-lack-of-deadline-for-uniswap-amm.md`
> - `reports/cosmos_cometbft_findings/m-07-lack-of-slippage-and-deadline-during-withdraw-and-deposit.md`

**Variant: Funds Missing Slippage in Renzo** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md`
> - `reports/cosmos_cometbft_findings/m-07-lack-of-slippage-and-deadline-during-withdraw-and-deposit.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in funds missing slippage logic allows exploitation through missing validation, 
func secureFundsMissingSlippage(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 11 audit reports
- **Severity Distribution**: HIGH: 4, MEDIUM: 7
- **Affected Protocols**: Illuminate Round 2, Persistence, Napier Finance - LST/LRT Integrations, Flex Perpetuals, Sorella Labs
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Funds Theft Auth Bypass
grep -rn 'funds|theft|auth|bypass' --include='*.go' --include='*.sol'
# Funds Theft Manipulation
grep -rn 'funds|theft|manipulation' --include='*.go' --include='*.sol'
# Funds Theft Reentrancy
grep -rn 'funds|theft|reentrancy' --include='*.go' --include='*.sol'
# Funds Theft Delegatecall
grep -rn 'funds|theft|delegatecall' --include='*.go' --include='*.sol'
# Funds Theft Replay
grep -rn 'funds|theft|replay' --include='*.go' --include='*.sol'
# Funds Theft Frontrunning
grep -rn 'funds|theft|frontrunning' --include='*.go' --include='*.sol'
# Funds Theft Surplus
grep -rn 'funds|theft|surplus' --include='*.go' --include='*.sol'
# Funds Missing Slippage
grep -rn 'funds|missing|slippage' --include='*.go' --include='*.sol'
```

## Keywords

`adversary`, `allow`, `allows`, `anyone`, `appchain`, `attack`, `attacker`, `attacks`, `auth`, `balance`, `between`, `blame`, `bounty`, `bringunusedethbackintogiantpool`, `bypass`, `called`, `cannot`, `causing`, `changes`, `claims`, `condition`, `contract`, `cosmos`, `cvgt`, `delegatecall`, `deploy`, `deposits`, `direct`, `enabling`, `excess`
