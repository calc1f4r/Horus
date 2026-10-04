# Fluid

## Smart Contract

## Security Assessment

##### VERSION 1.

AUDIT DATES:

AUDITED BY:

```
June 24th to July 31st, 2025
IllIllI
kriko.eth
shaflow
```

- Contents 1 Introduction
      - 1.1 About Zenith
      - 1.2 Disclaimer
      - 1.3 Risk Classification
   - 2 Executive Summary
      - 2.1 About Jupiter
      - 2.2 Scope
      - 2.3 Audit Timeline
      - 2.4 Issues Found
      - 2.5 Audit Note
   - 3 Findings Summary
   - 4 Findings
      - 4.1 Critical Risk
      - 4.2 High Risk
      - 4.3 Medium Risk
      - 4.4 Low Risk
      - 4.5 Informational


### 1

Introduction

#### 1.1 About Zenith

```
Zenith assembles auditors with proven track records: finding critical vulnerabilities in public
audit competitions.
```
```
Our audits are carried out by a curated team of the industry’s top-performing security
researchers, selected for your specific codebase, security needs, and budget.
```
Learn more about us athttps://zenith.security.

#### 1.2 Disclaimer

```
This report reflects an analysis conducted within a defined scope and time frame, based on
provided materials and documentation. It does not encompass all possible vulnerabilities
and should not be considered exhaustive.
```
```
The review and accompanying report are presented on an "as-is" and "as-available" basis,
without any express or implied warranties.
```
```
Furthermore, this report neither endorses any specific project or team nor assures the
complete security of the project.
```
#### 1.3 Risk Classification

##### SEVERITY LEVEL IMPACT: HIGH IMPACT: MEDIUM IMPACT: LOW

Likelihood: High Critical High Medium

Likelihood: Medium High Medium Low

Likelihood: Low Medium Low Low


### 2 Executive Summary

#### 2.1 About Jupiter

```
Jupiter Lend is shaping the future of finance on Solana by Leveraging Fluid's architecture, a
two-layer architecture that separates liquidity to deliver greater capital efficiency.
```
#### 2.2 Scope

The engagement involved a review of the following targets:

Target fluid-contracts-solana

Repository https://github.com/Instadapp/fluid-contracts-solana

Commit Hash d2f9a01fe8f63a4cb9db1035e4b97cbc806a71ed

Files programs/*


#### 2.3 Audit Timeline

June 24th, 2025 Audit start

July 31st, 2025 Audit end

August 14th, 2025 Report published

#### 2.4 Issues Found

##### SEVERITY COUNT

Critical Risk 6

High Risk 3

Medium Risk 16

Low Risk 28

Informational 12

Total Issues 65

#### 2.5 Audit Note

At the time of the engagement, the codebase was still in early development stage with the
client's review process ongoing in parallel.

Some issues identified by the auditing team during the audit were also identified by the
development team internally and in parallel.


### 3 Findings Summary

```
ID Description Status
```
C-1 Incorrect bit masks break the branching algorithm Resolved

C-2 Seed collision in vault accounts Resolved

C-3 Tick 0 is incorrectly handled as ”no tick exists” Resolved

```
C-4 Attackers can use arbitrary TokenReserve accounts to un-
dermine the protocol
```
Resolved

```
C-5 tick_id_data_after_operate account is missing a vault_id
check
```
Resolved

C-6 Price calculation overflow can cause asset underpricing Resolved

H-1 Transaction account count limits will break the vault Acknowledged

```
H-2 Full liquidation did not clear the position debt in the
fetch_latest_position function
```
Resolved

```
H-3 absorb function fails due to double account borrow block-
ing liquidations
```
Resolved

M-1 Meaning of liquidity.status is inverted Resolved

M-2 The reward_rate may be released incorrectly. Resolved

```
M-3 Potential overflow leading to DoS when calculating reward
rate
```
Resolved

```
M-4 Wrong borrow rate may be used after calls to up-
date_token_config()
```
Resolved

M-5 Some Token-2022 extensions may break the protocol Acknowledged

```
M-6 Calls to update_user_borrow/supply_config() break ac-
counting
```
Resolved

```
M-7 The vault’s reserved tokens may be insufficient to cover the
unclaimed tokens
```
Resolved

M-8 Wrong oracle prices used for liquidations Resolved

```
M-9 calculate_new_token_exchange_price will revert if LRRM
reward start time is in the future
```
Resolved


ID Description Status

M-10 Decreasing interest rates will DoS the system Resolved

M-11 The withdrawal gap feature incorrectly reduces amount
available for withdrawal by orders of magnitude

Resolved

M-12 Use of global counters in PDA derivations will allow DOS Resolved

M-13 Overflow in debt calculation prevents position updates for
large borrowers

Resolved

M-14 Positions above liquidation threshold after repayment may
delay other liquidations

Resolved

M-15 Chain rollbacks may cause misconfiguration Resolved

M-16 Stale prices may allow loans using worthless collateral Resolved

L-1 The program initialization may be vulnerable to a front-
running attack

Acknowledged

L-2 Using the deprecated transfer instruction may cause in-
compatibility with some tokens

Resolved

L-3 The f_token metadata will not be initialized. Resolved

L-4 Compound interest deviation in borrow exchange price
calculation

Acknowledged

L-5 No way to close and reclaim rent for some user-related ac-
counts

Resolved

L-6 Incorrect behavior of checked_floor_div Resolved

L-7 Users may be unable to withdraw dust amounts Acknowledged

L-8 Some events may contain incorrect information Resolved

L-9 Missing a check in init_lending to ensure that the mint and
f_token_mint token programs are equal

Resolved

L-10 User supplies and borrows can’t be paused independently Resolved

L-11 Incorrect URI passed to Metaplex Resolved


ID Description Status

L-12 Incorrect token_reserves_liquidity account for
init_lending() ix may require redeployment

Resolved

L-13 The CLAIM token transfer_type does not support with-
drawing and borrowing to different users.

Resolved

L-14 Missing default Pubkey checks Resolved

L-15 Borrow/supply magnification may be applied to exchange
price growth prior to vault creation

Resolved

L-16 The withdrawal_cap is not capped at 100% Resolved

L-17 Vaults cannot work with mixed legacy/Token-2022 bor-
row/supply tokens

Resolved

L-18 No way to change a vault’s authority Acknowledged

L-19 Admin configuration updates can cause limit calculation
discrepancies

Acknowledged

L-20 Use of pause_user() prior to setting user configuration
breaks subsequent configuration

Resolved

L-21 get_ticks_from_remaining_accounts() uses the wrong error
code when program ownership checks fail

Resolved

L-22 add_debt_to_tick() never executes the initialization code
path

Resolved

L-23 The governance signer may lose auth or guardian roles Resolved

L-24 Unrestricted lending program account in rewards transition Resolved

L-25 Prior period rewards may be lost if LRRM.start_rewards() is
called again

Resolved

L-26 Open TODOs Resolved

L-27 Vector field sizes not validated when updating accounts Resolved

L-28 Internal errors are not converted to external ones Acknowledged

I-1 Typos Resolved


ID Description Status

I-2 Dead code Resolved

I-3 Accounts need not be marked as mutable Resolved

I-4 Delayed reward distribution may temporarily prevent with-
drawals

Acknowledged

I-5 The Operate instruction may be called with some accounts
that are not used.

Resolved

I-6 Unused instruction accounts Resolved

I-7 Unused account fields waste rent Resolved

I-8 The init_token_reserve instruction does not check whether
the token decimals are supported

Resolved

I-9 Misleading comments Resolved

I-10 Unhandled SKIP token transfer_type Acknowledged

I-11 There may not be enough user class entries to support fu-
ture tokens

Acknowledged

I-12 Rewards calculation does not credit interest-related TVL
growth

Resolved


### 4 Findings

#### 4.1 Critical Risk

A total of 6 critical risk findings were identified.

[C-1] Incorrect bit masks break the branching algorithm

SEVERITY:Critical IMPACT:High

STATUS:Resolved LIKELIHOOD:High

Target

- programs/vaults/src/module/user.rs
- programs/vaults/src/state/tick_has_debt.rs

Description:

```
In Rust, the bit shift operators have lower precedence than the arithmetic operators. This
means that1 << 4 - 1results in 00001000 rather than 00001111. The code that is
attempting to create a bit mask like the latter, is using syntax that creates the former. This
results in the bit mask not actually setting the lower bits, and instead sets only the indexed
bit. This has the effect of clearing lower ticks in thetick_has_debtdata, which causes the
code that attempts to find the next pure tick, to return the incorrect result, breaking the
branching algorithm.
```
Recommendations:

Add parentheses around the shift operation.

Fluid:Resolved with@56d82546457...

Zenith:Verified.


[C-2] Seed collision in vault accounts

SEVERITY:Critical IMPACT:High

STATUS:Resolved LIKELIHOOD:High

Target

- vaults/src/state/context.rs

Description:

The seeds of the following account types in thevaultprogram can collide with other
accounts of the same type:

- BranchData
- TickHasDebtArray
- TickData
- TickIdLiquidation
- UserPosition
- Mint(inInitPosition)

We'll demonstrate the issue on theBranchDataaccount, although the principle applies to all
the mentioned account types.

```
#[account(
init,
payer=signer,
space=8 +BranchData/:INIT_SPACE,
seeds=[BRANCH_SEED, vault_id.to_string().as_bytes(),
branch_id.to_string().as_bytes()],
bump
)]
pubbranch: AccountLoader<'info,BranchData>,
```
As we can see in the code, the seeds of theBranchDataare built using twou16andu
parameters, which are first converted to String and then to bytes. This, however, means that
vault_id = 1andbranch_id = 11would be converted to"1"and"11"in the string form,
hence[49]and[49, 49]in the bytes form, respectively.vault_id = 11andbranch_id =
1 would be converted to"11"and"1", meaning[49, 49]and[49]in the bytes form.

This means that the seeds of two differentBranchaccounts would be the same, hence


producing the same PDA:

```
seeds 1: [[98, 114, 97, 110, 99, 104], [49], [49, 49]]
seeds 2: [[98, 114, 97, 110, 99, 104], [49, 49], [49]]
```
This would lead to some instructions not being callable due to accounts being already
initialized. Additionally, this collision could allow users to access or modify accounts they
shouldn't control, leading to potentially disastrous scenarios.

Recommendations:

Consider converting the seed parameters to little-endian bytes with theto_le_bytes
method instead, and passing them to the seeds array usingas_slice, which preserves the
binary format of the integers, avoiding collisions:

```
#[account(
init,
payer=signer,
space= 8 +BranchData/:INIT_SPACE,
seeds = [BRANCH_SEED, vault_id.to_string().as_bytes(), branch_id.to_
string().as_bytes()],
```
```
seeds = [BRANCH_SEED, vault_id.to_le_bytes().as_slice(), branch_id.to_le_
bytes().as_slice()],
bump
)]
pub branch: AccountLoader<'info, BranchData>,
```
For comparison, the same parameters used in the report would produce different seeds
(hence different PDAs):

```
seeds 1: [[98, 114, 97, 110, 99, 104], [1, 0], [11, 0, 0, 0]]
seeds 2: [[98, 114, 97, 110, 99, 104], [11, 0], [1, 0, 0, 0]]
```
Note that little-endian encoding is recommended here as it is the standard byte order used
throughout Solana for numerical data serialization.

Fluid:Resolved with@e617d03d457...and@3c50e0cb177...

Zenith:Verified.


[C-3] Tick 0 is incorrectly handled as "no tick exists"

SEVERITY:Critical IMPACT:High

STATUS:Resolved LIKELIHOOD:High

Target

- vaults/src/module/user.rs
- structs.rs

Description:

The system incorrectly treats legitimate tick 0 positions as "no tick exists", causing
liquidation failures and corruption of the vault's risk management system.

Consider a position with 1000000000000 collateral and 999999999999 debt. The ratio of this
position is 281474976710655 , and theget_tick_at_ratiofunction would return-1, which
means the actual tick increased by 1 would be 0. If the exchange price is1e18, with supply
exchange price = 1112777777777 , borrow exchange price = 1000000000000 , and collateral
factor of 90%, the calculated tick comes to zero, meaning this is a valid and healthy
position, and the topmost tick will be set to zero. This means that even if the positions in
this vault become unhealthy, liquidation will become impossible due to the topmost tick
being zero.

When the topmost tick is legitimately set to 0, all liquidation attempts become impossible
due to the validation check in theliquidatefunction, which incorrectly treats
topmost_tick = 0as "no tick exists":

```
ifvault_state.topmost_tick/= 0 {
returnErr(error!(ErrorCodes/:VaultTopTickDoesNotExist));
}
```
Additionally, this creates a cascading corruption issue. When a legitimate tick 0 position is
created, the comparisonif memory_vars.tick /= top_tickbecomes true, setting
topmost_tick = 0. On the next operation,vault_state.get_top_tick()returnsi32/:MIN
because it converts stored 0 toi32/:MIN. This means any subsequent position at tick -100,
-50, etc. will satisfymemory_vars.tick /= i32/:MINand incorrectly become the new
"topmost" tick.

The issue stems from the codebase treating 0 as a sentinel value for "no tick exists" in the
get_top_tick()function:


```
pubfnget_top_tick(&self) />i32{
ifself.topmost_tick/= 0 {
i32/:MIN
}else{
self.topmost_tick
}
}
```
However, this behavior is incorrectly ported from the Solidity implementation, which
correctly distinguishes between these states using bit encoding. In the Solidity version, tick
= 0 is encoded as(sign=1, absolute=0)→ bit pattern = 4 (decimal) → passes check,
while "no tick exists" is encoded as(sign=0, absolute=0)(meaning negative zero) → bit
pattern = 0 (decimal) → fails check.

Similarly, Inset_branch_data_in_memory, ifconnected_minima_tickis 0, it is treated as an
invalid tick. This is inappropriate.

```
pubfnset_branch_data_in_memory(&mutself,branch: &Branch) />Result<()> {
//.
self.minima_tick=self.data.connected_minima_tick;
```
```
// if 0 that means it's a master branch
ifself.minima_tick/= 0 {
self.minima_tick=i32/:MIN;
}
```
```
Ok(())
}
```
For example, suppose a liquidation occurs and the liquidation tick happens to be 0. The
branch's tick would then be set to 0. If the collateral price later recovers, a user may open a
position with a tick higher thantop_tick, causing the branch to be created and connect to
the previous branch with a tick of 0. As a result, the current branch’s
connected_minima_tickbecomes 0.

If the collateral price drops again and another liquidation occurs, with the liquidation tick <
0, then after liquidating thetop_tick, the connected branch will not be liquidated because
itsminima_tickis set toi32/:MIN. However, the connected branch should in fact be
liquidated, since it is at tick = 0, which is greater than the liquidation tick.

Recommendations:

Consider updating the validation logic to usei32/:MINas the "no tick exists" sentinel value:


```
if vault_state.topmost_tick /= 0 {
if vault_state.topmost_tick /= i32/:MIN {
returnErr(error!(ErrorCodes/:VaultTopTickDoesNotExist));
}
```
Additionally, ensure consistent state management by updating the functions in
vault_state.rs:

```
pub fnreset_top_tick(&mut self) {
self.topmost_tick = 0;
self.topmost_tick = i32/:MIN;
}
```
```
pub fn set_top_tick<'info>(
```
```
// //. snippet
```
```
ifnew_top_tick /= i32/:MIN {
// Last user left the vault
self.topmost_tick = 0;
self.topmost_tick = i32/:MIN;
self.reset_branch_liquidated();
}
```
```
// //. snippet
}
```
```
pub fnget_top_tick(&self) -> i32 {
if self.topmost_tick /= 0 {
i32/:MIN
} else {
self.topmost_tick
self.topmost_tick
}
}
```
Lastly, theinit_vault_statefunction should set the topmost tick to thei32/:MINvalue.

Fluid:Resolved with@8bd3005b457...,@ee28bc1d4b6...,@09e1c4aff71..., and
@8ecdb86a39b...


Zenith:Verified.


[C-4] Attackers can use arbitrary TokenReserve accounts to

undermine the protocol

SEVERITY:Critical IMPACT:High

STATUS:Resolved LIKELIHOOD:High

Target

- vaults/src/state/context.rs
- vaults/src/module/user.rs

Description:

Theoperatefunction accepts arbitraryTokenReserveaccounts for both supply and borrow
tokens without validating that these accounts correspond to the correct tokens for the vault.
This allows attackers to manipulate the supply exchange price used in collateral factor
calculations by providing aTokenReserveaccount from a different, more valuable token.

The token reserve accounts are not validated against the vault's configured tokens in the
Operatecontext:

```
#[account(mut)]
pubsupply_token_reserves_liquidity: AccountLoader<'info,TokenReserve>,
#[account(mut)]
pubborrow_token_reserves_liquidity: AccountLoader<'info,TokenReserve>,
```
Theload_exchange_pricesfunction blindly trusts these user-provided accounts:

```
letsupply_token_reserves =supply_token_reserves_account.load()?;
letborrow_token_reserves =borrow_token_reserves_account.load()?;
// //.
let(liq_supply_ex_price,_)
=supply_token_reserves.calculate_exchange_prices()?;
let(_,liq_borrow_ex_price)
=borrow_token_reserves.calculate_exchange_prices()?;
```
While these accounts are expected to be validated when callingoperateon the Liquidity
program, during borrow-only operations, only the borrow token reserve is checked by the
liquidity program, leaving the supply token reserve unchecked. However, the vault still
loads the exchange price from the unchecked supply token reserve for collateral factor


calculations.

An attacker can exploit this by providing aTokenReserveaccount from a different token as
thesupply_token_reserves_liquidity. If the vault's legitimate collateralTokenReservehas
a supply exchange price of 1e12 and the attacker provides aTokenReservefrom a different
token with a supply exchange price of 1.5e12, this inflates the supply exchange price used
in the collateral factor calculation, allowing the attacker to borrow 50% more than their
collateral should support.

The collateral factor calculation usesexchange_rate =
exchange_rate.safe_mul(supply_ex_price)/.safe_div(borrow_ex_price)?;. By
substituting a highersupply_ex_pricefrom a different token's reserve, the attacker
artificially inflates theexchange_rate, which increases theratio_at_cfthreshold, allowing
excessive borrowing.

This enables an attack where the attacker can over-borrow using inflated exchange prices,
then liquidate the over-leveraged position (creating bad debt for the protocol), and repeat
the process with new positions to drain protocol funds.

Similarly, in theliquidateinstruction, theTokenReserveaccount does not undergo a mint
matching check because the program expects this to be verified during the CPI call.

```
#[derive(Accounts)]
pubstructLiquidate<'info> {
////.
// Here we will list all liquidity accounts, needed for CPI call to
liquidity program
// @dev no verification of accounts here, as they are already handled in
liquidity program,
// Hence loading them as AccountInfo
// No need to verify liquidity program key here, as it will be verified
in liquidity program CPI call
#[account(mut)]
pubsupply_token_reserves_liquidity: AccountLoader<'info,TokenReserve>,
#[account(mut)]
pubborrow_token_reserves_liquidity: AccountLoader<'info,TokenReserve>,
////.
}
```
However, there is a special case in theliquidateinstruction: a user can pass indebt_amt =
0 to choose to settle only bad debt. In this case, the instruction exits immediately after
settling the bad debt, and no CPI call occurs. Therefore, the correctness of the passed-in
TokenReserveaccount cannot be guaranteed.

```
pubfnliquidate<'info>(
ctx: Context<'_, '_, 'info, 'info,Liquidate<'info>>,
debt_amt: u64,
```

```
col_per_unit_debt: u64,// min collateral needed to receive per unit of
debt paid back in 1e
absorb: bool,
remaining_accounts_indices: Vec<u8>,// first index is sources, second
is branches, third is ticks, fourth is tick has debt
) />Result<(u128,u128)> {
////.
// Call absorb function to handle bad debt above max limit
// @dev passing vault_state as a mut reference, that means it
will be updated inside the absorb function
self/:absorb(
&mutvault_state,
&tick_accounts,
&tick_has_debt_accounts,
&tick_has_debt_indices,
&branch_accounts,
&mutctx.accounts.new_branch,
memory_vars.max_tick,
)?;
```
```
ifdebt_amt/= 0 {
// If debt_amt was 0, we just wanted to absorb
returnOk(( 0 , 0 ));
}
}
////.
}
```
A malicious actor can choose to pass indebt_amt = 0along with a
borrow_token_reserves_liquidityaccount whose mint does not match. If the
liq_borrow_ex_priceof this account is higher than the actual price, it will cause the
calculatedvault_borrow_ex_priceto be overstated, which ultimately results in a lower
calculatedmax_tick. This causes ticks that should not be classified as bad debt to be
treated as bad debt and settled, leading to users’ loss of funds.

Recommendations:

Add constraints to ensuresupply_token_reserves_liquidityand
borrow_token_reserves_liquiditycorrespond to the vault's configured supply and
borrow tokens:

```
#[account(
mut,
constraint=supply_token_reserves_liquidity.load()/.mint
/=vault_config.load()/.supply_token
```

##### )]

```
pubsupply_token_reserves_liquidity: AccountLoader<'info,TokenReserve>,
```
```
#[account(
mut,
constraint=borrow_token_reserves_liquidity.load()/.mint
/=vault_config.load()/.borrow_token
)]
pubborrow_token_reserves_liquidity: AccountLoader<'info,TokenReserve>,
```
Fluid:Resolved with@94a39a5913d...and@7c235c9f8bf...

Zenith:Verified.


[C-5]tick_id_data_after_operateaccount is missing a

vault_idcheck

SEVERITY:Critical IMPACT:High

STATUS:Resolved LIKELIHOOD:High

Target

- validate.rs

Description:

In theOperateinstruction, thetick_id_data_after_operateaccount is missing avault_id
check inverify_operate.

```
pubfnverify_operate<'info>(ctx: &Context<'_, '_, 'info, 'info,
Operate<'info>>) />Result<()> {
////.
lettick_id_data=&ctx.accounts.tick_id_data;
iftick_id_data.vault_id/=vault_state.vault_id {
returnErr(error!(ErrorCodes/:VaultInvalidVaultId));
}
```
```
letnew_branch=&ctx.accounts.new_branch.load()?;
ifnew_branch.vault_id/=vault_state.vault_id {
returnErr(error!(ErrorCodes/:VaultInvalidVaultId));
}
```
```
Ok(())
}
```
This allows a malicious actor to pass in atick_id_data_after_operateaccount with a
mismatchedvault_id, causing the post tick liquidation history to be written into the
TickIdLiquidationaccount of another vault.

This can lead to loss of funds for other users. Because the historical position update
involves aconnection_factorof 0, it results in a division-by-zero panic.

```
letmutcurrent_connection_factor:
u128=connection_factor.cast()?;
```

##### ////.

```
}else{
// If branch is not merged, the main branch it's connected to
then it'll have minima debt factor
// position debt = debt * base branch minimaDebtFactor /
connectionFactor
letbranch_min_debt_factor:
u128=branches[current_branch_idx]
.load()?
.get_branch_debt_factor()?;
```
```
position_raw_debt=mul_div_normal(
position_raw_debt,
branch_min_debt_factor.cast()?,
@> current_connection_factor.cast()?,
)?;
```
Recommendations:

Check whether thevault_idof thetick_id_data_after_operateaccount matches in the
verify_operatefunction.

Fluid:Resolved with@f84a92a6c1f...

Zenith:Verified.


[C-6] Price calculation overflow can cause asset underpricing

SEVERITY:Critical IMPACT:High

STATUS:Resolved LIKELIHOOD:High

Target

- programs/oracle/src/helper.rs

Description:

The exchange rate of assets is in 18 decimals precision, since therateis initially set to 1e18 (
see here), meaning thatget_exchange_rate_for_hopmust return prices in 18 decimals
precision.

The Pyth oracle, for example, returns price along with theexponentvalue, which is the
decimal precision for that price feed. We assume that this is handled with proper
multiplieranddivisorvalues, and therateis properly converted to 18 decimalshere.

However, if we consider a BTC/USD price feed from Pyth, the returned price at the time of
writing is 11833017161230 , with exponent =-8, meaning 8 decimals. This price should
therefore be multiplied by1e10in order to get it to 18 decimals, yielding
118330171612300000000000.

This, however, means that thefollowing calculation:

```
rate=rate
.saturating_mul(current_hop_rate)
.saturating_div( 10 u128.pow(RATE_OUTPUT_DECIMALS));
```
would overflow, but sincesaturating_mulis used, it would not fail but saturate at
u128/:MAX. The division would then yield 340282366920938463463 in 18 decimals, which
comes to340.282366920938463463USD, which would be a disastrous discount.

Recommendations:

Consider either decreasing the value ofRATE_OUTPUT_DECIMALSor implementing the logic
utilizing theU256type available in theuintcrate.

Fluid:Resolved with@fb6fa428125...


Zenith:Verified.


#### 4.2 High Risk

A total of 3 high risk findings were identified.

[H-1] Transaction account count limits will break the vault

SEVERITY:High IMPACT:High

STATUS:Acknowledged LIKELIHOOD:Medium

Target

- programs/vaults/src/state/context.rs

Description:

Solana transactions are limited to 1232 bytes, which is the amount of data that can fit in a
single network packet. When taking into account the size of headers, signatures, and
addresses, this means legacy transactions can only fit about34 addressesin a transaction.
When using Address Lookup Tables, this limit expands significantly, but has a hard
maximum of 128 addresses. If a transaction requires more than this number of accounts,
then the transaction will not be able to be created.

One area of the code that runs into this limitation is useroperate()instructions. The
OperateAccounts struct by itself lists 34 accounts, leaving 94 accounts available for
provision inremaining_accounts. Two of these are consumed by the two oracle sources,
and at least one account is consumed for atick_has_debt_accountsaccount, leaving 91
forBranchDataaccounts. With the way that branches are created, it is likely for the
accounts limitation to be hit. Consider the case of a range-bound market where users A, B,
and C create positions, and then their branch is partially liquidated. Next, the market goes
back up, and dip buyers create new positions at the top-most tick with positions which
creates a new branch, and then some of them are liquidated. The market goes back up,
new dip buyers take out new loans, and then are partially liquidated when the market goes
back down. Each of these dip-buying-then-liquidation cycles creates a new branch that
must be passed to user A, B, and C'soperate()instructions in order for them to modify
their positions. If there are enough cycles, those users will be unable to modify their
positions, and their positions and collateral will be stuck permanently (until they're
liquidated or absorbed).

Theliquidate()instruction has a similar issue in that if there are a lot of branches that a
large liquidation wants to cover, that transaction will require many branch data, tickdata,
and has debt accounts, which will require them to break up their liquidations into multiple


smaller liquidations, rather than one large one.

Recommendations:

Design a multi-transaction version ofoperate()that allows processing, via a new
mechanism, to be done in stages in different transactions, and ensure that theliquidate()
limitation is documented in code comments, and that the SDK properly calculates the
correct number of accounts to include in order to stay under the limit.

Fluid:Acknowledged. From our observations, branch depth rarely exceeds 5 in practice,
which is what we’ve seen on Ethereum as well. For the operate instruction, we use Address
Lookup Tables, giving us an effective limit of ~64 accounts enough to handle roughly
20–25 branches well above what we expect.

For liquidate, partial liquidation is already supported via the debt_amount parameter. We’re
also considering adding a branch-based restriction similar to debt_amount so that
liquidations always go through, regardless of branch count.

In the meantime, this can be managed at the SDK level by calculating the appropriate
debt_amount based on the passed branches or ticks to ensure partial liquidation when
needed.

If needed in the future, we can also implement a multi-instruction approach to work around
account limits entirely.


[H-2] Full liquidation did not clear the position debt in the

fetch_latest_positionfunction

SEVERITY:High IMPACT:High

STATUS:Resolved LIKELIHOOD:Medium

Target

- structs.rs

Description:

When operating on a position, if a position was previously opened and its tick has been
liquidated, thefetch_latest_positionfunction needs to be called to retrieve the updated
state after liquidation. However, during the tick is full liquidation, the program only sets
position_ticktoi32/:MINbut does not resetposition_raw_debtto zero.

```
pubfnfetch_latest_position(//.) />Result<usize> {
////.
letinitial_position_raw_debt: u64=self.debt_raw.cast()?;
// //.
letmutposition_raw_debt: u64=initial_position_raw_debt;
letmutposition_raw_col: u128= 0 ;
```
```
ifis_fully_liquidated{
position_tick=i32/:MIN;
}else{
//.
}
self.tick=position_tick;
self.debt_raw=position_raw_debt.cast()?;
self.col_raw=position_raw_col;
```
```
Ok(current_branch_idx)
}
```
This can lead to the user opening more debt than intended. For example, if User 1’s
position held 100 debt and was fully liquidated at some point, and now the user attempts
to open a new position with 100 debt, the old 100 debt is not cleared frommemory_vars,
potentially resulting in 200 debt being unintentionally opened.


Recommendations:

Whenis_fully_liquidatedis true, also setposition_raw_debtto zero.

Fluid:Resolved with@b19b3dbc472...

Zenith:Verified.


[H-3]absorbfunction fails due to double account borrow
blocking liquidations

SEVERITY:High IMPACT:High

STATUS:Resolved LIKELIHOOD:Medium

Target

- programs/vaults/src/module/user.rs

Description:

Theabsorbfunctionmay fail in certain cases due to borrowing the sameBranchData
account twice. The function firstloads aBranchDataaccount(orhere), then
attempts to load the same account mutablywithin a loop. Sincebranch_data.idremains
unchanged, the second borrow fails. If the current branch has not yet been liquidated, and
the first historical branch connected to the current branch has become bad debt due to
price fluctuations and needs to be absorbed, the above issue will occur.

Theabsorbfunction is triggered whentopmost_tick > max_tick. Whenabsorbfails, the
entire liquidation system becomes blocked, preventing both bad debt absorption and
liquidation of borderline positions.

Recommendations:

Restructure the function to avoid double borrowing by scoping the initialBranchData
account load to extract all necessary data before attempting to borrow the account
mutably in the processing loop.

Fluid:Resolved with@b70c44d2c0d...

Zenith:Verified.


#### 4.3 Medium Risk

A total of 16 medium risk findings were identified.

[M-1] Meaning ofliquidity.statusis inverted

SEVERITY:Medium IMPACT:Low

STATUS:Resolved LIKELIHOOD:Medium

Target

- programs/liquidity/src/module/admin.rs

Description:

Thepre_operate(),operate(), andclaim()instructions each have the following
constraint:

```
#[account(constraint=liquidity.status/=true @
ErrorCodes/:ProtocolLockdown)]
publiquidity: Box<Account<'info,Liquidity>>,
```
The constraint requires that the status istrue, but elsewhere in thecodeandcomments
trueis interpreted as the "paused" state. Since the initialization code sets the initial state to
true, the instructions above are actuallyunpaused by default. Attempts by auth roles to
pause user operations willfail, requiring debugging, before determining that the input arg
must be flipped instead.

Recommendations:

Change the constraints to use/=instead.

Fluid:Resolved with@e2ad489fabc...

Zenith:Verified.


[M-2] Thereward_ratemay be released incorrectly.

SEVERITY:Medium IMPACT:Medium

STATUS:Resolved LIKELIHOOD:Medium

Target

- helpers.rs

Description:

When the current time exceedsrewards_ended, the program does not specially handle the
final reward distribution up to therewards_endedtime. This may lead to incorrect reward
allocation.

```
fncalculate_new_token_exchange_price(
new_liquidity_exchange_price: u64,
lending: &Account<Lending>,
current_rate_model: &Account<LendingRewardsRateModel>,
f_token_total_supply: u64,
) />Result<(u64,bool)> {
//.
let(mutrewards_rate,rewards_ended,rewards_start_time)
=current_rate_model.get_rate(
old_token_exchange_price
.cast/:<u128>()?
.safe_mul(f_token_total_supply.cast()?)?
.safe_div(EXCHANGE_PRICES_PRECISION.cast()?)?
.cast()?,
)?;
```
```
ifrewards_rate>MAX_REWARDS_RATE.cast()? /|rewards_ended{
// rewardsRate is capped, if it is bigger > MAX_REWARDS_RATE, then
the rewardsRateModel
// is configured wrongly (which should not be possible). Setting
rewards to 0 in that case here.
rewards_rate= 0 ;
}
```
For example: If the current reward distribution period is from time 100 to 200 and the
rewards_rateisrate1, suppose the last system interaction occurs at time 190, and the next


one happens at time 210 — which is afterrewards_ended. At that point,rewards_ratewill
immediately return 0, and the rewards between 190 and 200 will remain undistributed.

If there is another reward distribution queue starting after time 200 withrewards_rate =
rate2, then only the rewards from 200 to 210 will be properly distributed. The rewards
from 190 to 200 will still be lost.

Recommendations:

It is recommended to specifically handle the reward distribution for the period between the
last update time and therewards_endedtime.

Fluid:Resolved with@b2ed0badecb...

Zenith:Verified.


[M-3] Potential overflow leading to DoS when calculating

reward rate

SEVERITY:Medium IMPACT:Medium

STATUS:Resolved LIKELIHOOD:Medium

Target

- lendingRewardRateModel/src/state/state.rs

Description:

When the new token exchange price is calculated in thishelper function, the reward
information is retrieved from the current rate model using theget_ratefunction.

When the current time is after the reward end time, the mathematical operations can
overflow during the final rate calculation:

```
letyearly_reward=next_reward_amount
.safe_mul(SECONDS_PER_YEAR)?
.safe_div(next_duration)?;
letrate=yearly_reward
.safe_mul(100_000_000_000_000)?// 1e14
.safe_div(total_assets)?;
```
Since all of these values are of typeu64, the overflow would occur if either
next_reward_amountis greater than 584942417355 , or if the calculatedyearly_rewardis
greater than 184467.

Since this calculation is part of multiplelendingoperations, includingpreview_mint,
preview_redeem,execute_withdraw, andexecute_deposit, these would revert due to the
overflow until the reward rate model's end time is updated or sufficient time passes beyond
the calculatednew_end_timethreshold.

Recommendations:

Consider casting these values tou128:

```
letyearly_reward=next_reward_amount
.cast/:<u128>()?
```

```
.safe_mul(SECONDS_PER_YEAR)?
.safe_mul(SECONDS_PER_YEAR.cast()?)?
.safe_div(next_duration)?;
.safe_div(next_duration.cast()?)?;
letrate=yearly_reward
.safe_mul(100_000_000_000_000)? // 1e14
.safe_div(total_assets)?;
.safe_div(total_assets.cast()?)?;
```
Fluid:Resolved with@b2ed0badecb...

Zenith:Verified.


[M-4] Wrong borrow rate may be used after calls to
update_token_config()

SEVERITY:Medium IMPACT:Medium

STATUS:Resolved LIKELIHOOD:Medium

Target

- programs/liquidity/src/module/admin.rs

Description:

If there are already live prices, theupdate_token_config()instructioncalculatesand stores
the updated exchange prices after the configuration update. It also updates the
last_update_timestampbut never updates thelast_utilizationor theborrow_rate,
which are directly used to calculate thenextinterest owed/paid. It is possible that interest
growth prior to the instruction, or thefee_on_interestchange, would have otherwise
pushed the utilization past the rate model's kink, and would have either required a much
higher or much lower borrow rate than occurs due to this bug.

The solidity code has thesameissue.

Recommendations:

Calculate and store the updated utilization and borrow rate as is done for theoperate()
instruction, or callupdate_exchange_prices_and_rates()after updating storage.

Fluid:Resolved with@9a5a9e6ad77...and@630b78c05ba...

Zenith:Verified


[M-5] Some Token-2022 extensions may break the protocol

SEVERITY:Medium IMPACT:Medium

STATUS:Acknowledged LIKELIHOOD:Low

Target

- programs/liquidity/src/module/user.rs
- programs/liquidity/src/state/context.rs
- programs/liquidity/src/module/admin.rs
- programs/liquidity/src/module/user.rs

Description:

Some token-2022 extensions may cause problems with the protocol:

- Permanent Delegate- The permanent delegate will always be authorized to transfer
    funds out of the vault and any claim account.
- Pausable- This extension will prevent all users from withdrawing funds for mints with
    this extension, since the liquidity programusesthe deprecatedtransfer()function,
    which disallows this extension.
- Transfer Fees- In addition to breaking claims due to it not being supported for
    transfer(), mints with this feature willbreakthe claim process since the user claim
    balancewon't match the amount actually transferred into the claim account.
- Transfer Hooks- The deprecatedtransfer()function disallows this extension, which
    will break claiming.
- Default Account State-Claimaccounts may be frozen, with no way for theliquidity
    PDA to unfreeze them.
- Mint Close Authority- A token with this extension may change its decimals by closing
    an re-opening with a new decimal amount. This may occur between when the token
    rate is firstset, and when the token is first supplied, potentially violating the maximum
    unit amount constraints. This extension would also allow creating a new mint with a
    permanent delegate.

A related issue is that even normal SPL tokens have afreeze authoritywho can use that
authority to prevent tokens from being transferred to/from any user's address. This may
cause liquidations to fail or may prevent borrowers from repaying loans.


Recommendations:

Disallow tokens that have extensions enabled, and decide on a strategy for handling frozen
accounts and token pauses.

Fluid:Made changes to exclude non-whitelisted extensions, but USDG requires support
for some of the extensions listed above. Resolved with@dd1e564cfa4...and@PR-62.

Zenith:Fluid acknowledges that the dangerous extensions still are allowed in order to
supportUSDG, and that later updates to the transfer fee, hooks, or default state may cause
issues down the road.


[M-6] Calls toupdate_user_borrow/supply_config()break

accounting

SEVERITY:Medium IMPACT:Medium

STATUS:Resolved LIKELIHOOD:Medium

Target

- programs/liquidity/src/module/admin.rs

Description:

Unlike thesoliditycode, theupdate_user_borrow/supply_config()functions use
calculate_exchange_prices()rather than callingupdate_exchange_price()which would
also update thelast_update_timestamp. This means that when the update functions are
called, their internal calls toupdate_exchange_prices_and_rates()calculate fresh prices
on top of what was fetched fromcalculate_exchange_prices(), resulting in a
re-application of the expected interest since the last update.

Recommendations:

Useupdate_exchange_price()in both functions, rather than calling
calculate_exchange_prices()

Fluid:Resolved with@9ea104b9dd6...

Zenith:Verified.


[M-7] The vault's reserved tokens may be insufficient to cover

the unclaimed tokens

SEVERITY:Medium IMPACT:Medium

STATUS:Resolved LIKELIHOOD:Medium

Target

- user.rs

Description:

If the withdrawal or borrow uses a Claim method, the user needs to manually call theclaim
instruction to receive their tokens. During this period, since the tokens remain in the vault,
the corresponding amount must be recorded to prevent it from being borrowed or
withdrawn. Otherwise, it could result in the user’s claim failing due to insufficient funds.

In theoperateinstruction, there is an Inappropriate check: whenwithdraw_to≠
borrow_to, the system processes thewithdrawandborrowtransfers sequentially. If the
Claimtransfer type is used in this case, theborrow_transfermight use an outdated
last_stored_claim_amount, becausetotal_claim_amountwas already increased during
the earlierwithdraw_transfer.

```
pubfnoperate(
ctx: Context<Operate>,
supply_amount: i128,// Used max available in rust i128
borrow_amount: i128,
withdraw_to: Pubkey,
borrow_to: Pubkey,
mint: Pubkey,
transfer_type: TransferType,
) />Result<(u64,u64)> {
//.
}else{
ifwithdraw_transfer_amount> 0 {
letclaim_amount=handle_transfer_or_claim(
&transfer_type,
withdraw_to,
&mutctx.accounts.claim_account,
last_stored_claim_amount,
TokenTransferParams{
```

source: ctx.accounts.vault.to_account_info(),
destination:
ctx.accounts.withdraw_to_account.to_account_info(),
authority:
ctx.accounts.liquidity.to_account_info(),// the liqudity PDA owns the
authority to transfer the tokens
amount: withdraw_transfer_amount,
token_program:
ctx.accounts.token_program.to_account_info(),
signer_seeds: Some(&[&liquidity_seeds]),
mint: None,
},
)?;

total_claim_amount=
total_claim_amount.safe_add(claim_amount)?;
}

ifborrow_transfer_amount> 0 {
letclaim_amount=handle_transfer_or_claim(
&transfer_type,
borrow_to,
&mutctx.accounts.claim_account,
last_stored_claim_amount,
TokenTransferParams{
source: ctx.accounts.vault.to_account_info(),
destination:
ctx.accounts.borrow_to_account.to_account_info(),
authority:
ctx.accounts.liquidity.to_account_info(),// the liqudity PDA owns the
authority to transfer the tokens
amount: borrow_transfer_amount,
token_program:
ctx.accounts.token_program.to_account_info(),
signer_seeds: Some(&[&liquidity_seeds]),
mint: None,
},
)?;

total_claim_amount=
total_claim_amount.safe_add(claim_amount)?;
}
}

token_reserve.add_claim_amount(total_claim_amount)?;
}


For example:

1.The vault currently holds 3000 tokens, withtotal_claim_amount = 2000.

```
2.A request is made forwithdraw = 1000andborrow = 1000, wherewithdraw_to ≠
borrow_to, and thetransfer_typeisClaim.
```
```
3.After executingwithdraw_transfer,total_claim_amountshould increase to 3000. At
this point, no further tokens should be allowed to be withdrawn. However, since the
outdatedlast_stored_claim_amount = 2000is passed intoborrow_transfer, the
subsequentborrow_transferstill passes the checks.
```
```
4.After bothborrow_toandwithdraw_tosuccessfully callclaim, the vault ends up with
only 1000 tokens, whiletotal_claim_amount = 2000. This may cause future user claims
to fail due to insufficient funds in the vault.
```
Recommendations:

It is recommended to update the outdatedlast_stored_claim_amountbefore executing
borrow_transfer.

Fluid:Resolved with@4625f94b131...

Zenith:Verified


[M-8] Wrong oracle prices used for liquidations

SEVERITY:Medium IMPACT:Medium

STATUS:Resolved LIKELIHOOD:Medium

Target

- programs/vaults/src/invokes/oracle.rs

Description:

The oracle program interface supports two separate price-fetching variants used by the
vault -get_exchange_rate_operate()andget_exchange_rate_liquidate(), where the
later has extra limitations on the price returned, e.g. in order to prevent
forced liquidation attacks. During liquidations, the vault calls its
get_exchange_rate_liquidate()function, but this function ends up internally calling the
get_exchange_rate_operate()instruction instead of theget_exchange_rate_liquidate()
function, which means the vault program is vulnerable to forced liquidation attacks.

Recommendations:

Invoke the correct oracle CPI for liquidations.

Fluid:Resolved with@50187fee83d...and@0d5085d552a...

Zenith:Verified


[M-9]calculate_new_token_exchange_pricewill revert if LRRM

reward start time is in the future

SEVERITY:Medium IMPACT:Medium

STATUS:Resolved LIKELIHOOD:Medium

Target

- programs/lending/src/utils/helpers.rs

Description:

Therewards_ratefrom the Lending Rewards Rate Model is one of the factors when
calculating the new token exchange price. The newly calculated price is inflated by the
current rate from the LRRM, based on time elapsed since the last update until the current
time. If the last update occurred before the current rewards start time, the
last_update_timestampis set to therewards_start_timeas we cansee here. In the LRRM
implementation, we can see that if the reward start time is in the future, hencegreater
than the current time, the function will return the start time of the rewards (see here).

This, however, means that later the function will try to subtract this future timestamp from
the current timestamp as we cansee here:

```
lettotal_return_from_rewards: u128=rewards_rate
.cast/:<u128>()?
.safe_mul(curr_timestamp.safe_sub(last_update_timestamp.cast()?)?)?
.safe_div(SECONDS_PER_YEAR)?;
```
Note that this is the same implementation as in Solidity, where the implementation
underflows since it is a part of anuncheckedblock, but it has no impact since the
reward_ratein this case is zero. In the Rust implementation, the
curr_timestamp.safe_sub(last_update_timestamp.cast()?)calculation will return anErr
variant, hence DoSing the calls that rely on calculating the new token exchange price
(which is one of the most essential functions in the protocol).

Recommendations:

Consider usingsaturating_subinstead ofsafe_sub:


```
lettotal_return_from_rewards: u128 =rewards_rate
.cast/:<u128>()?
.safe_mul(curr_timestamp.safe_sub(last_update_timestamp.cast()?)?)?
.safe_mul(curr_timestamp.saturating_sub(last_update_timestamp.cast()?))?
.safe_div(SECONDS_PER_YEAR)?;
```
Fluid:Resolved with@b2ed0badecb...

Zenith:Verified.


[M-10] Decreasing interest rates will DoS the system

SEVERITY:Medium IMPACT:Medium

STATUS:Resolved LIKELIHOOD:Medium

Target

- liquidity/src/state/rate_model.rs

Description:

As per inline commentshereandhere, thedeclining rate is supported before kink.
kink to max must be increasing.. This means that the rate model can be set so that
rate_at_zerois greater thanrate_at_kink1, and it is an expected state. However, rate
models set like this would not work because of underflow in theget_ratefunction.

The veryfirst calculationis:

```
letnum: i128=y2.safe_sub(y1)/.safe_mul(TWELVE_DECIMALS)/.cast()?;
```
It represents the maximum rate minus the minimum rate. If the maximum rate is lower than
the minimum (declining interest rate), thesafe_subwould return an error, hence reverting.
The result of this would be DoS of actions that would leave the utilization in the
non-functioning decreasing rate area of the interest rate curve. The utilization would need
to get back to the increasing rate area in that case for it to work.

Recommendations:

Consider castingy2andy1toi128before the subtraction:

```
let num: i128 = y2.safe_sub(y1)/.safe_mul(TWELVE_DECIMALS)/.cast()?;
let num: i128 = y2
.cast/:<i128>()?
.safe_sub(y1.cast()?)?
.safe_mul(TWELVE_DECIMALS.cast()?)?
.cast()?;
```
Fluid:Resolved with@300b5ec7361...


Zenith:Verified


[M-11] The withdrawal gap feature incorrectly reduces amount

available for withdrawal by orders of magnitude

SEVERITY:Medium IMPACT:Medium

STATUS:Resolved LIKELIHOOD:Medium

Target

- programs/vaults/src/module/user.rs
- programs/vaults/src/utils/operate.rs

Description:

If the supply token being used has fewer than nine decimals, the amount of collateral
deposited isscaled upto nine decimals. Later, this scaled up amount ispassedto the
check_if_withdrawal_safe_for_withdrawal_gap()function where it is divided by the
liquidity_ex_price, which is an un-scaled amount. This means that the resulting amount
being requested is over-estimated by the function, by an order of magnitude for every
decimal the token is below nine. When the withdrawal gap feature is enabled, this will likely
cause the withdrawal request to be rejected, because amounts that should have fit below
the limit are treated as though they are much larger.

Recommendations:

Save the pre-scaled amount, and use it in the call to
check_if_withdrawal_safe_for_withdrawal_gap().

Fluid:Resolved with@e54760bf89a...

Zenith:Verified.


[M-12] Use of global counters in PDA derivations will allow DOS

SEVERITY:Medium IMPACT:Medium

STATUS:Resolved LIKELIHOOD:Medium

Target

- programs/vaults/src/utils/validate.rs
- programs/vaults/src/state/context.rs

Description:

The creation of a new position requires that the caller provides the correct next position's
ID, which is required to be equal to the count of the current number of positions. An
attacker can cheaply DOS the creation of new positions by continuously creating random
amounts of new positions in a transaction in every block with high priority fees, making it
impossible for legitimate users of the protocol to anticipate the correct new position count.

Theinit_tick_id_liquidation()instruction also uses a global counter and therefore
limits the speed with which users can modify their positions after a liquidation. The function
requires that the new ID matches theTickData's currenttotal_ids, and this means new
TickIdLiquidations can't be created until prior ones have been filled.

Recommendations:

For positions, allow random position IDs to be passed to theinit_position()instruction.
TheTokenMetadataextension'sadditional_metadatafield can be used on the NFT's mint in
order to store the position's Pubkey, and the update of the total positions counter can be
done the first time position is used in theoperate()instruction.

For liquidations, allow the creation of multipleTickIdLiquidations at a time, so that they
can be pre-inited prior to them being needed. It may also be worth while to increase the
number of entries pertick_mapin theTickIdLiquidationPDA, so that new
TickIdLiquidations have to be created less frequently.

Fluid:For new position creation, we don’t see a strong DOS risk currently, users can always
retry later or we can patch via upgrade if needed. However, we agree that for position
modification post liquidations this check is important, and we've implemented the proposed
change by removing the check fromInitTickIdLiquidationwith@13b7d96b16d...

Zenith:Position creation DOS is acknowledged, and the liquidation DOS fix is verified.


[M-13] Overflow in debt calculation prevents position updates

for large borrowers

SEVERITY:Medium IMPACT:Medium

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/vaults/src/state/structs.rs

Description:

Users with an existing debt position can experience a denial of service due to an overflow
in thefetch_latest_positionfunction. If the user was liquidated before but retains more
than 1% of the debt, the debt is decreased by 1% (see here). However, the
position_raw_debtvariable was declared asu64(see here), meaning that on values of
1844858893260282 and greater, it will overflow and panic. Since debt is standardized to 9
decimals, this would represent at least1_844_858units of debt, which in USDC, for
example, can mean ~1.8 million USD. Since the function would not work, the user would
not be able to update their position, potentially facing more damage.

Recommendations:

Consider casting the value tou128before multiplying:

```
position_raw_debt = position_raw_debt.safe_mul(9999)/.safe_div(10000)?;
position_raw_debt = position_raw_debt
.cast/:<u128>()?
.safe_mul(9999)?
.safe_div(10000)?
.cast()?;
```
Fluid:Resolved with@819081bcac...

Zenith:Verified.


[M-14] Positions above liquidation threshold after repayment

may delay other liquidations

SEVERITY:Medium IMPACT:Medium

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/vaults/src/module/user.rs

Description:

Users are allowed to repay part of their debts without oracles being consulted, as long as
the position results in a less risky tick with less net borrowing. While these sorts of
operations make the position itself less risky, on Solana with the way the protocol's
accounts are organized, such operations can introduce more risk into the system. Since
any update to an existing position results in a completely new position with potentially new
tick and "has debt" accounts created, this means that any user wishing to liquidate such a
position will have to had provided these accounts in their liquidation instruction. Since
most liquidations will involve the use of an Address Lookup Table which must have been
'activated' (its creation block must appear in the slot hashes sysvar) prior to its use, any
changes to the accounts required for a liquidation ix will require a new ALT and 1-2 blocks
of delay before the instruction can be executed. It is possible that a user is past the
liquidation threshold and, repeatedly over multiple blocks, repays the minimum amount of
debt, which ends up keeping them in the liquidation range over multiple blocks, and
prevents the legitimate liquidation of it or other positions. Eventually, if the market moves
quickly enough, positions may move to the absorption range and become uneconomical
for liquidation.

Recommendations:

Do not let modified positions be added to ticks that are above the liquidation threshold
according to the oracle price.

Fluid:Resolved with@50445ef3c98...

Zenith:Verified.


[M-15] Chain rollbacks may cause misconfiguration

SEVERITY:Medium IMPACT:Medium

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/oracle/src/helper.rs

Description:

When there is a networkoutagethe Solana chain is oftenrolled backto a slot in the past
with a more consistent state. This means that if there have been configuration changes
after that slot, the changes will be rolled back too. One place that is particularly vulnerable
to this is the update of vault oracles. The Pyth oracles in use by the protocol use their own
multiplieranddivisorfields in order to ensure that the price returned has the correct
decimals. Since the Pyth update'sexponentis never read, the multiplier and divisor must
necessarily account for the exponent. If the Pyth feed needs to change its exponent, then
the Fluid protocol will need to update the vault to use aneworacle with new multipliers
and divisors. If this change of oracles is rolled back, then users interacting with the vault
prior to its re-application will be able to use prices with the wrong number of decimals,
allowing them to liquidate positions that otherwise shouldn't be liquidated. Other
configuration parameters such as the collateral factor, paused/frozen state, rate
parameters, and fees may also have negative consequences when they're rolled back.

Recommendations:

Apply the Pyth exponent separately from the multiplier and divisor, and in all programs add
account fields and instructions for tracking and updating the last restart slot, and prevent
new user operations if it doesn't match theLastRestartSlotsysvar.

Fluid:Resolved with@5bd4a17f1a3.... While a positive exponent is theoretically possible, it
has never occurred in practice. Additionally, we always validate the exponent before setting
the feed, so if ever needed can be updated later. The other aspects of the finding relating
to the last restart slot are acknowledged.

Zenith:Verified that the fix solves for the case of negative exponents changing. Positive
exponents, and other configuration rollbacks are acknowledged.


[M-16] Stale prices may allow loans using worthless collateral

SEVERITY:Medium IMPACT:Medium

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/oracle/src/modules/pyth.rs

Description:

On Solana, the Pyth network provides oracle updates every 60 seconds or whenever there
is adeviationof 0.5% or more, for its sponsored feeds. For the non-sponsored feeds, there
are no specific guarantees. The only caveat for the sponsored feeds is that if there is a
networkoutage(which, in the past, has lasted for as many as 19 hours), the Pyth network
may beunableto push updates until the outage is resolved. Since the Fluid protocol is
reading the raw price update account without checking for staleness, when the network
comes back an attacker can use flash loans to take out large loans using the outdated price
and potentially worthless collateral, leaving the protocol with bad debt.

Recommendations:

Add price staleness checks such as the ones provided by the Pyth
get_price_no_older_than()function.

Fluid:Resolved with@08a8d061673...,@b10e51a0ac7..., and@9ea1a950d34...

Zenith:Verified.


#### 4.4 Low Risk

A total of 28 low risk findings were identified.

[L-1] The program initialization may be vulnerable to a

front-running attack

SEVERITY:Low IMPACT:Low

STATUS:Acknowledged LIKELIHOOD:Low

Target

- context.rs

Description:

In the protocol, the initialization of privileged addresses is not protected by access control.
If the project team does not perform the program deployment and initialization within the
same transaction, a malicious actor could front-run the initialization, rendering the program
unusable.

```
#[derive(Accounts)]
pubstructInitLendingAdmin<'info> {
#[account(mut)]
pubauthority: Signer<'info>,
```
```
#[account(
init,
payer=authority,
space=8 +LendingAdmin/:INIT_SPACE,
seeds=[LENDING_ADMIN_SEED],
bump,
)]
publending_admin: Account<'info,LendingAdmin>,
```
```
pubsystem_program: Program<'info,System>,
}
```
```
#[derive(Accounts)]
```

pubstructInitLendingRewardsAdmin<'info> {
#[account(mut)]
pubauthority: Signer<'info>,

```
#[account(
init,
payer=authority,
space=8 +LendingRewardsAdmin/:INIT_SPACE,
seeds=[b"lending_rewards_admin"],
bump,
)]
publending_rewards_admin: Account<'info,LendingRewardsAdmin>,
```
pubsystem_program: Program<'info,System>,
}

#[derive(Accounts)]
pubstructInitLiquidity<'info> {
#[account(mut)]
pubsigner: Signer<'info>,

```
#[account(
init,
seeds=[LIQUIDITY_SEED],
payer=signer,
space= 8 +Liquidity/:INIT_SPACE,
bump
)]
publiquidity: Account<'info,Liquidity>,
```
```
#[account(
init,
seeds=[AUTH_LIST_SEED],
payer=signer,
space= 8 +AuthorizationList/:INIT_SPACE,
bump
)]
pubauth_list: Account<'info,AuthorizationList>,
```
pubsystem_program: Program<'info,System>,
}


Recommendations:

It is recommended to add access control to these functions, restricting them so that only
specific hardcoded addresses are allowed to call them.

Fluid:Acknowledged


[L-2] Using the deprecatedtransferinstruction may cause

incompatibility with some tokens

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- spl.rs

Description:

The program allows integration with tokens from the Token2022 program. However, many
parts of the code still use the deprecatedtransferinstruction for transfers. This leads to
incompatibility with tokens that have certain extensions, as the transfers may fail.

```
pubfntransfer_spl_tokens(params: TokenTransferParams) />Result<()> {
//.
ifletSome(seeds)=signer_seeds{
#[allow(deprecated)]
token_interface/:transfer(
CpiContext/:new_with_signer(token_program.clone(),
transfer_ix,seeds),
amount,
)?
}else{
#[allow(deprecated)]
token_interface/:transfer(CpiContext/:new(token_program.clone(),
transfer_ix),amount)?
}
}
```
```
Ok(())
}
```
```
fndeposit_to_liquidity(ctx: &Context<Deposit>,amount: u64,mint: Pubkey)
/>Result<u64> {
//.
// Transfer tokens to liquidity
transfer_spl_tokens(TokenTransferParams{
```

```
source: ctx.accounts.depositor_token_account.to_account_info(),//
depositor token account
destination: ctx.accounts.vault.to_account_info(),// vault, aka
liquidity mint PDA
authority: ctx.accounts.signer.to_account_info(), // msg.sender
amount, // amount
token_program: ctx.accounts.token_program.to_account_info(),//
token program
signer_seeds: None,
mint: None,//
})?;
//.
}
```
Specifically, extensions likeTransferHookAccount,TransferFeeAmount, and
PausableAccountrequire the mint account to be included in the instruction.

```
pub(crate)fnprocess_transfer(
program_id: &Pubkey,
accounts: &[AccountInfo],
amount: u64,
transfer_instruction: TransferInstruction,
) />ProgramResult{
//.
else{
// Transfer hook extension exists on the account, but no mint
// was provided to figure out required accounts, abort
ifsource_account
.get_extension/:<TransferHookAccount>()
.is_ok()
{
returnErr(TokenError/:MintRequiredForTransfer.into());
}
```
```
// Transfer fee amount extension exists on the account, but no
mint
// was provided to calculate the fee, abort
ifsource_account
.get_extension_mut/:<TransferFeeAmount>()
.is_ok()
{
returnErr(TokenError/:MintRequiredForTransfer.into());
}
```
```
// Pausable extension exists on the account, but no mint
// was provided to see if it's paused, abort
```

```
ifsource_account.get_extension/:<PausableAccount>().is_ok() {
returnErr(TokenError/:MintRequiredForTransfer.into());
}
```
```
( 0 ,None,None)
};
//.
}
```
Recommendations:

It is recommended to avoid using the deprecatedtransferinstruction. If the mint account
is not passed in the instruction, consider retrieving the mint account address from the
TokenAccount’s data instead.

Fluid:Resolved with@dd1e564cfa4...

Zenith:Verified.


[L-3] Thef_tokenmetadata will not be initialized.

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:High

Target

- admin.rs

Description:

Since theinitialize_token_metadatacall is commented out in theinit_lending
instruction, thef_tokenmetadata cannot be created.

```
pubfninit_lending(
ctx: Context<InitLending>,
symbol: String,
liquidity_program: Pubkey,
) />Result<()> {
//.
// ctx.accounts.initialize_token_metadata(symbol)?;
```
```
Ok(())
}
```
Recommendations:

It is recommended to uncomment theinitialize_token_metadatacall so that the
metadata for thef_tokencan be created when theinit_lendinginstruction is executed.

Fluid:Resolved with@4cefb7357c4...

Zenith:Verified.


[L-4] Compound interest deviation in borrow exchange price

calculation

SEVERITY:Low IMPACT:Low

STATUS:Acknowledged LIKELIHOOD:Low

Target

- lending/src/state/token_reserve.rs

Description:

The borrow exchange price calculation in thecalculate_exchange_pricesfunctionuses a
simple interest approximation that produces different results based on update frequency,
leading to price inconsistencies between different update patterns.

The current implementation accumulates interest linearly per update:

```
borrow_exchange_price=borrow_exchange_price.safe_add(
borrow_exchange_price
.safe_mul(borrow_rate)?
.safe_mul(seconds_since_last_update)?
.safe_div(SECONDS_PER_YEAR.safe_mul(FOUR_DECIMALS)?)?
)?;
```
This creates divergent outcomes for identical time periods with different update
frequencies:

- 1 update after 10 seconds: Results in price P₁
- 10 updates during 10 seconds: Results in price P₂ (where P₂ > P₁)

The deviation becomes significant with longer update intervals:

- Per-second updates vs 1 annual update (6% APR): 1.061820282945 vs 1.06 (0.17%
    difference)
- Per-second updates vs 1 annual update (10% APR): 1.105154345224 vs 1.10 (0.47%
    difference)

While the difference might be insignificant, it becomes more significant with higher borrow
rates and is worth considering.


Recommendations:

Consider calculating the new price using a compound interest approximation.

Fluid:Acknowledged


[L-5] No way to close and reclaim rent for some user-related
accounts

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/liquidity/src/state/context.rs
- programs/vaults/src/state/context.rs

Description:

TheUserClaimaccounts must be created by users prior to being passed as accounts for
the various operation-related instructions. They cost rent to store, but once the user is done
with them, there is no way to close the accounts and reclaim the rent.

User positions have a similar issue in that theUserPositionand associated NFTMint
accounts are never closed, even after the position is fully closed.

Recommendations:

Provide instructions for closing the accounts.

Fluid:Resolved theUserClaimpart with@996368afea0.... Acknowledged the
user-position-related part of the submission. While we don't plan to support this at initial
launch, we’ll definitely consider adding it later if and when there's a clear need for it.

Zenith:Verified theUserClaimpart.


[L-6] Incorrect behavior ofchecked_floor_div

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- floor_div.rs

Description:

The methodchecked_floor_divis supposed to round numbers down, however it performs
this rounding incorrectly. As we can see in the following code:

```
fnchecked_floor_div(&self,rhs: $t) />Option<$t> {
letquotient=self.checked_div(rhs)?;
```
```
letremainder=self.checked_rem(rhs)?;
```
```
ifremainder/=<$t>/:zero() {
quotient.checked_sub(<$t>/:one())
}else{
Some(quotient)
}
}
```
If the remainder is not zero, 1 will be subtracted from the result. This works for negative
integers, as for example-3 / 2would yield-1and-1as a remainder, and rounding down
means the result should be-2(hence subtracted by 1). However, if we divided3 / 2, the
result is 1 and the remainder is 1 , meaning the result will be subtracted by 1 , resulting in 0 ,
while 1 should be the correct result. While this could potentially be a disastrous mistake,
the function is not used anywhere in the scope for now, hence the low severity rating.

Recommendations:

Consider subtracting one only if the remainder isless thanzero:

```
fnchecked_floor_div(&self, rhs: $t)-> Option<$t> {
letquotient=self.checked_div(rhs)?;
```

```
letremainder=self.checked_rem(rhs)?;
```
```
if remainder /= <$t>/:zero() {
if remainder < <$t>/:zero() {
quotient.checked_sub(<$t>/:one())
}else{
Some(quotient)
}
}
```
Fluid:Resolved with@9bea6051f89...

Zenith:Verified


[L-7] Users may be unable to withdraw dust amounts

SEVERITY:Low IMPACT:Low

STATUS:Acknowledged LIKELIHOOD:Low

Target

- programs/liquidity/src/module/user.rs

Description:

The solana implementation of the liquidity protocol, unlike thesolidityone, rejects any
operate()instruction where both of the amounts are underMIN_OPERATE_AMOUNT. This
means that if a user only has a dust amount remaining (e.g. they meant to withdraw all, but
accidentally left some dust), they'll be unable to withdraw it without re-depositing enough
to cover the minimum. This may be especially problematic for interest-free suppliers, as
interest will never push them over the minimum.

Recommendations:

It's not clear what specific risk this threshold is protecting against, but if it is in fact required,
withdrawal requests that result in the remaining supply being under this amount should be
rejected.

Fluid:Acknowledged. As a general practice across our protocols, we enforce limits on
both extremely small and extremely large amounts to mitigate risks such as dust
accumulation, unintended donations, or large-value manipulation. In the rare case a user
wishes to withdraw the remaining dust, they can simply deposit a small amount and then
withdraw their full balance. Also note that by default, for every protocol that we deploy we
create a small dust position of a few $ that is the first user and will stay in forever, so no
actual user will ever face any issues around being locked as the last user because of some
edge case revert or underflow. On EVM we do not have the exact same check, but the
checks that revert withUserModule__OperateAmountInsufficienttarget a similar issue
there, where the user amount would be too small to cause a change in storage values and
is thus rejected. This min operate amount check is intended to replicate a similar effect.


[L-8] Some events may contain incorrect information

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/liquidity/src/module/admin.rs
- programs/liquidity/src/state/context.rs
- programs/vaults/src/module/admin.rs

Description:

Some fields of emitted events may contain incorrect information:

- LogUpdateRateDataV1-rate_data.tokenis never constrained to match
    UpdateRateData.mint
- LogUpdateRateDataV2-rate_data.tokenis never constrained to match
    UpdateRateData.mint
- LogUpdateUserSupplyConfigs-user_supply_config.useris never constrained to
    matchUpdateUserSupplyConfig.protocol
- LogUpdateUserBorrowConfigs-user_borrow_config.useris never constrained to
    matchUpdateUserBorrowConfig.protocol
- For thepre_operate()ix, there is no constraint forcing themintof each supply to
    match themintinput argument. However, in that case, there is no emit to show the
    incorrect input argument.
- For theupdate_core_settings()ix, the inputs toLogUpdateCoreSettingsare multiplied
    by 10, but all come from the input parameters struct, where they're already all scaled to
    FOUR_DECIMALS.
- For theupdate_oracle()ix, there is no constraint forcing theoracleto match the
    storedoracle_program.

Recommendations:

Add constraints to ensure that the input struct/account fields match the input
accounts/arguments

Fluid:Resolved with@ca3cc093234...,@3865cb916aa...,@50187fee83d...,
@a78dc328f41..., and@a8166fce948...


Zenith:Verified.


[L-9] Missing a check ininit_lendingto ensure that themint

andf_token_minttoken programs are equal

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- context.rs

Description:

In theinit_lendinginstruction, thef_token_mintaccount is initialized using the provided
token_program. However, there is no check to ensure that thistoken_programmatches the
token program associated with themint. Iff_token_mintandmintare created using
different token programs, subsequent instructions such asDepositwill fail.

```
pubstructInitLending<'info> {
// @dev Only the auths can initialize the lending
#[account(mut, constraint=lending_admin.auths.contains(&signer.key())
@ErrorCodes/:FTokenOnlyAuth)]
pubsigner: Signer<'info>,
```
```
#[account(has_one=liquidity_program.key())]
publending_admin: Account<'info,LendingAdmin>,
```
```
pubmint: InterfaceAccount<'info,Mint>,
```
```
#[account(
init,
seeds=[F_TOKEN_MINT_SEED, mint.key().as_ref()],
bump,
payer=signer,
mint/:decimals=mint.decimals,
mint/:authority=lending_admin,
mint/:token_program=token_program,
)]
pubf_token_mint: Box<InterfaceAccount<'info,Mint>>,
```

Recommendations:

It is recommended to add a constraint to ensure that thef_token_mintis initialized using
the same token program as themintaccount.

Fluid:Resolved with@56ccd1d5fab...

Zenith:Verified.


[L-10] User supplies and borrows can't be paused

independently

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/liquidity/src/state/context.rs

Description:

During theinit_new_protocol()instruction, theMints associated with the supply and
borrow positions arenotrequired to be equal. However, during thepause_user()
instruction, only oneMintcan be supplied, and it's used forbothPDAs, and both supplies
are required to be paused at thesame time. This behavior differs from the solidity code,
whichallowseither one or both supplies to be paused at a time.

Recommendations:

Introduce a flag to thepause_user()instruction indicating that either one or both supplies
should be paused, or document the difference, with regard to the solidity code, in a code
comment.

Fluid:Resolved with@4e50499e8bd...,@1a255df6bd9..., and@928623a29f0...

Zenith:Verified.


[L-11] Incorrect URI passed to Metaplex

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/lending/src/state/context.rs

Description:

The hard-coded URI"https://fluid.io"is passed to the Metaplex program for all
fTokens. The metaplex programexpectsa per-token URI that points to a JSON document,
and neither of these expectations are fulfilled.

Recommendations:

{{ ... }} Construct a per-fToken URI which points to a JSON document with theexpected
metadata format.

Fluid:Resolved with@4cefb7357c4...

Zenith:Verified.


[L-12] Incorrecttoken_reserves_liquidityaccount for

init_lending()ix may require redeployment

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/lending/src/state/context.rs
- programs/vaults/src/module/admin.rs

Description:

There are no constraints to force thetoken_reserves_liquidityaccount's owner to match
theliquidity_programinput argument. This means that the lending program used by the
lending_adminmay not match thetoken_reserves_liquidity, which will cause operations
involving reserves to be incorrect. Since only one fToken mint can be created for a given
underlying mint, and theinit_lending()ix itself won't fail, in order to create a correct
fToken mint the lending program will have to be redeployed.

The vault program has a similar issue in thatinitialize_vault_admin()takes in an
arbitrary address as itsliquidityparameter, but the use ofUserSupplyPositionand
UserBorrowPositionin theOperateAccounts struct, and the use ofTokenReservein the
InitVaultStateContextAccounts struct means that only the
vault-compile-time-program-ID of the liquidity program can be used.

Recommendations:

For the lending program:

```
#[account(has_one = mint)]
#[account(has_one = mint, owner = liquidity_program)]
pub token_reserves_liquidity: AccountLoader<'info, TokenReserve>,
```
For the vault program, add a check toinitialize_vault_admin()that ensures that the
parameter matches the compile-time-program-ID of the liquidity program.

Fluid:Resolved with@1ac36ee9d29...

Zenith:Verified.


[L-13] TheCLAIMtokentransfer_typedoes not support

withdrawing and borrowing to different users.

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Medium

Target

- context.rs

Description:

In theoperateinstruction, withdrawing and borrowing to different addresses is allowed, but
this is incompatible with theCLAIMtokentransfer_typebecause this method requires
authorizing tokens to a single claim account, and only one claim account is defined in the
ctx.

```
#[derive(Accounts)]
#[instruction(_supply_amount: i128, _borrow_amount: i128, withdraw_to:
Pubkey, borrow_to: Pubkey, mint: Pubkey)]
pubstructOperate<'info> {
//.
#[account(mut, has_one=mint)]
pubclaim_account: AccountLoader<'info,UserClaim>,
```
```
pubtoken_program: Interface<'info,TokenInterface>,
pubassociated_token_program: Program<'info,AssociatedToken>,
}
```
Recommendations:

It is recommended to define twoclaimaccounts in the ctx to support the case where
withdrawing and borrowing addresses are different.

```
pubstructOperate<'info> {
//.
#[account(mut, has_one=mint)]
pub claim_account: AccountLoader<'info, UserClaim>,
```

```
pub withdraw_claim_account: AccountLoader<'info, UserClaim>,
```
```
#[account(mut, has_one = mint)]
pub borrow_claim_account: AccountLoader<'info, UserClaim>,
```
```
pub token_program: Interface<'info, TokenInterface>,
pub associated_token_program: Program<'info, AssociatedToken>,
}
```
Fluid:Resolved with@8e7618716d1...and@3ff7ee74f00...

Zenith:Verified.


[L-14] Missing default Pubkey checks

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/vaults/src/module/admin.rs
- programs/oracle/src/lib.rs

Description:

The vault program has multiple places where it checks for and rejects the default PubKey,
but there are a few places without checks:

- initialize_vault_admin()-liquidityandauthority
- init_vault_config()-params.supply_token,params.borrow_token,params.oracles,
    params.oracle_program,params.rebalancer
- update_oracle()-new_oracle

The oracle program is missing a check in theinit_admin()ix.

Recommendations:

Add the missing checks

Fluid:Resolved with@1ac36ee9d29...,@f655ca4d54e...,@ca3cc093234..., and
@df2b8741a7c...

Zenith:Verified.


[L-15] Borrow/supply magnification may be applied to

exchange price growth prior to vault creation

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/vaults/src/module/admin.rs

Description:

In theinit_vault_state()instruction, thesupply/borrow_token_reserves_liquidity
liquidity programTokenReserveaccounts are loaded, and the values they currently have
stored for theirsupply/borrow_exchange_pricefields are stored, without modification, to
the vault'sVaultStateaccount. It is possible that the stored value is from a timestamp far in
the past, or that the vaules were from very different timestamps in the past. When the
actual exchange price for the vault is calculated, itappliesmagnification factors to the
difference in price between the stored price and the current live price. This means that the
magnification may be applied to price growth that occurred prior to the vault's creation.

Recommendations:

Use the results ofcalculate_exchange_prices(), rather than using the reserve accounts'
fields.

Fluid:Resolved with@f4c77f677ac...

Zenith:Verified.


[L-16] Thewithdrawal_capis not capped at 100%

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/vaults/src/module/admin.rs

Description:

Thewithdrawal_capfield is meant to be capped at100%, but is actually capped at 102.3%
due to the copying of a bug in thesoliditycode. Both theinit_vault_config()and
update_core_settings()instructions have the bug, butupdate_withdraw_gap()does not.

Recommendations:

UseTHREE_DECIMALSrather thanX10for this parameter's validations.

Fluid:Resolved with@a1acb78118a...

Zenith:Verified.


[L-17] Vaults cannot work with mixed legacy/Token-2022

borrow/supply tokens

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/vaults/src/module/admin.rs

Description:

The liquidity layer is coded such that both legacy and token-2022 tokens can be used a
supply or borrow tokens. The vault code allows theseMintaccounts to be passed as
InterfaceAccountaccounts, but when it comes to verification of the ATAs, it forces both
ATAs to use thesametoken_program, effectively preventing the use of multiple token
versions.

Recommendations:

Addsupply_token_programandborrow_token_programaccounts to theOperateand
LiquidateAccounts structs.

Fluid:Resolved with@9e5659f380e...

Zenith:Verified.


[L-18] No way to change a vault's authority

SEVERITY:Low IMPACT:Low

STATUS:Acknowledged LIKELIHOOD:Low

Target

- programs/vaults/src/module/admin.rs

Description:

In the case of a protocol key compromise, there is no function that allows the changing of
each vault'sauthorityaddress.

Recommendations:

Add a function to modify the vault's authority

Fluid:Acknowledged. All program authorities will be set to a team controlled multi sig.
Moreover if needed, we can add support for authority migration in a future upgrade.


[L-19] Admin configuration updates can cause limit calculation

discrepancies

SEVERITY:Low IMPACT:Low

STATUS:Acknowledged LIKELIHOOD:Medium

Target

- liquidity/src/module/admin.rs

Description:

The admins have the ability to call theupdate_user_supply_configand
update_user_borrow_configinstructions to update the relevant values in
UserSupplyPositionorUserBorrowPosition, respectively. These values can potentially
impact the withdrawal and borrow limits - namely, the values ofexpand_pct,
expand_duration, andbase_withdrawal_limitfromUserSupplyPositioninfluence the
withdrawal limit, whileexpand_pct,expand_duration,base_debt_ceiling, and
max_debt_ceilinginfluence the borrow limit. Since the outcome limit is based on time
elapsed between respective liquidity updates, thelast_updatevalue is tracked in both
account types and is updated every time the limits are updated.

However, it is not updated when the key values are changed, which means that the next
time the limit should be updated, it will use the newly updated changes, leading to
discrepancies and potentially undesired behavior. The following table demonstrates
changes to values vs. expected values ifexpand_pctis changed:


The table showcases how the limits change when theexpand_pctfield is changed at
timestamp 1200 (withdraw<sub>2</sub> and withdraw<sub>3</sub>) vs. when it stays
the same (withdraw<sub>1</sub>).

Recommendations:

Consider updating the withdraw and borrow limits, along with the last update time of these
accounts, when callingupdate_user_supply_configorupdate_user_borrow_config.

Fluid:Acknowledged


[L-20] Use ofpause_user()prior to setting user configuration

breaks subsequent configuration

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/liquidity/src/module/admin.rs

Description:

TheUserSupplyPositionandUserBorrowPositionaccounts have theirstatusfields set to
2 duringinitialization, to indicate that configuration has not yet been done. If a guardian or
governance ends up callingpause_user(), those accounts'statuswill be changed to 1
without storing the fact that it had been 2. When the user is eventually unpaused, the
statusis changed to 0 , regardless of whether it had been 2 prior to the pause. Having
configs_not_set()return false due to this change, will mean that initial configuration
setting will beskipped.

Recommendations:

Do not allow unconfigured users to be paused.

Fluid:Resolved with@698a5fb3443...and@6223ecf0502...

Zenith:Verified.


[L-21]get_ticks_from_remaining_accounts()uses the wrong

error code when program ownership checks fail

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/vaults/src/state/tick.rs

Description:

If the program ownership checks fail for any of theTickDataPDAs read from
remaining_accounts, theget_ticks_from_remaining_accounts()function errors with
ErrorCodes/:VaultBranchOwnerNotValid, which is only supposed to be used by
get_branches_from_remaining_accounts().

Recommendations:

Add aVaultTickDataOwnerNotValiderror to theErrorCodesenum, and use it in the
function.

Fluid:Resolved with@8e0bc0ac949...

Zenith:Verified.


[L-22]add_debt_to_tick()never executes the initialization

code path

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/vaults/src/module/admin.rs
- programs/vaults/src/utils/operate.rs

Description:

Unlike the Solidity version of vaults, theinit_tick()instruction unconditionally initializes
total_idstoone. This means that when theoperate()instruction reaches the
add_debt_to_tick()function, that function always finds thattick_idis greater than zero,
and thus if the position hasn't been liquidated, the execution flow goes to theif-blockrather
than the else-block. As the comments indicate, the else block is supposed to be where the
first initialization occurs. There are no negative effects of the current processing, however,
becauseupdate_tick_has_debt()ends up being called in both blocks, and this is the only
processing that needs to occur for initialization, given thetick_idis already non-zero.

Recommendations:

Remove thetick_id > 0checks in this function since the result will always be true, and
update the comments to reflect the actual flows.

Fluid:Resolved with@e03f7a155f4...and@13b7d96b16d...

Zenith:Verified.


[L-23] The governance signer may lose auth or guardian roles

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/liquidity/src/module/admin.rs
- programs/lending/src/module/admin.rs

Description:

During initialization, theinit_liquidity()functionaddstheliquidity.authorityto both
theauth_list.auth_usersandauth_list.auth_guardians, but there are no checks in
update_auths()orupdate_guardians()to ensure that the governance address is still
present. Unlike thesoliditycode, it's possible to remove all users from both the auth and
guardian roles, permanently removing the ability to pause the program in case of
emergencies.

The lending program has ananalogousissue with itsupdate_auths()instruction.

Recommendations:

Do not allow the governance address to be removed duringupdate_auths()and
update_guardians()for either program.

Fluid:Resolved with@a6fd1b21994...and@6e69529bc96...

Zenith:Verified


[L-24] Unrestricted lending program account in rewards

transition

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/lendingRewardRateModel/src/state/context.rs

Description:

Thetransition_to_next_rewardsinstruction of the LRRM program accepts any account
as thelending_program. Although the inline comment says it is checked during the lending
program invoke, this is not true, as we can see at theinvocation site.

This means that the transition can call into any program, which can mean that the desired
update of the specificLendingaccount won't occur, meaning the rewards for the period
between lending's last update and the current reward's end time won't be accounted for.
The impact is not significant since theLendingaccount is updated frequently with every
liquidity operation, hence the low severity rating.

Recommendations:

Consider restricting thelending_programto be the correct and expected lending program.

Fluid:Resolved with@709c3d3c8f8...

Zenith:Verified.


[L-25] Prior period rewards may be lost if

LRRM.start_rewards()is called again

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/lendingRewardRateModel/src/state/context.rs

Description:

UnlikeTransitionToNextRewards.next(), which callsupdate_rate()so that the prior
period's rewards are checkpointed, thestart()function does not do any checkpointing of
the prior rewards. If there are no new mints or burns for the prior period's duration, when
the newstart()period's settings get configured, the old rewards will never have been
doled out. If there are queued rewards, the function does not clear them.

Recommendations:

Callupdate_rate()if there already are settings, or only allowstart()to be called once
(require all subsequent changes to usenext()). Also consider erroring if there are queued
rewards.

Fluid:Resolved with@6e84bcffaed...and@27ffd7ef943...

Zenith:Verified.


[L-26] Open TODOs

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/oracle/src/modules/pyth.rs
- crates/library/src/math/*.rs

Description:

All open TODOs should be addressed before deployment:

```
// @todo @dev should we add pyth confidence check here?
```
Adding a confidence check is recommended since the aggregation algorithm is essentially
aweighted median, which may not actually be the right price to use if all prices are equally
spaced, and very far apart from each other. Consider, at least, disallowing new debt
positions if the confidence interval is much larger than expected.

```
// @todo Check license and audit for this code
```
Any licensing issues should be resolved as soon as possible.

Recommendations:

Address the TODOs

Fluid:Resolved with@86913c5b14b...,@9e6049b5030..., and@diff-4dd85a1...

Zenith:Verified.


[L-27] Vector field sizes not validated when updating accounts

SEVERITY:Low IMPACT:Low

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/liquidity/src/state/state.rs
- programs/liquidity/src/module/admin.rs
- programs/lending/src/state/state.rs
- programs/lendingRewardRateModel/src/state/state.rs

Description:

TheAuthorizationListaccount uses the#[max_len]attribute to allow anchor to calculate
the right size to allocate, but the various instructions for updating the account's fields never
ensure their sizes fall within the expected bounds. Even thoughuser_classesis limited to
100 entries, many more entries can be added, as long as the serialized size of the updated
data fits within the account's size. If too many entries are added touser_classes, this may
permanently prevent further entries from being added toauth_usersandguardians, since
once created, user classes cannot be removed.

TheLendingAdmin's andLendingRewardsAdmin'sauthsfields are also missing bounds
checks during updates, which will result in serialization failure errors, rather than with a
descriptive error, when too many entries are added

Recommendations:

Require that the vector lengths respect the allocated maximums, inupdate_auths(),
update_guardians(),update_user_class(), and theupdate_auths()functions for lending
and rewards admins.

Fluid:Resolved with@9ad38077b41...

Zenith:Verified.


[L-28] Internal errors are not converted to external ones

SEVERITY:Low IMPACT:Low

STATUS:Acknowledged LIKELIHOOD:Low

Target

- programs/library/src/errors.rs
- programs/library/src/token/spl.rs
- programs/vaults/src/invokes/mint.rs

Description:

The various programs in the project rely on the library crate for low-level operations,
including math and token transfers. The library crate defines its ownErrorCodesenum for
the errors it produces, but none of the programs calling these functions convert the
library's error codes to their own. This will, for instance, result incast()failures appearing
to beUserClassNotFoundfailures, rather thanLibraryCastingFailureones, since the IDL
only includes the error code enum values from the current program. In addition, the library
itself does not convert its own CPI failures to its own error codes, which complicates error
handling.

The vault program also does SPL-related operations without converting those CPI failures.

Recommendations:

Usemap_err()to convert between error enums, or use thiserror's#[from]attribute.

Fluid:Acknowledged


#### 4.5 Informational

A total of 12 informational findings were identified.

[I-1] Typos

SEVERITY:Informational IMPACT:Informational

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/**/*.rs

Description:

The following typos were identified:

recepient->recipient

```
pubrecepient: AccountInfo<'info>,
```
```
pubrecepient: Pubkey,
```
```
pubrecepient_token_account: Box<InterfaceAccount<'info,TokenAccount>>,
```
```
pubfnclaim(ctx: Context<Claim>,mint: Pubkey,recepient: Pubkey) />
Result<()> {
```
liqudity->liquidity

```
//.// the liqudity PDA owns the authority to transfer the tokens
```
dvision->division

```
// easy to check as that variable is NOT the result of a dvision etc.
```

bororwers->borrowers

```
// borrowRatio_ /> x of total bororwers paying yield. scale to 1e17.
```
atleast->at least

```
// //. needs to be atleast 1e73 to overflow max limit of ~1e77 in uint256
```
receipient->recipient

```
pubreceipient_token_account: Box<InterfaceAccount<'info,TokenAccount>>,
```
ratemodel->rate model

```
/// @dev To read PDA of rewards ratemodel to get_rate instruction
```
assset->asset

```
/// @dev exchange price for the underlying assset in the liquidity protocol
(without rewards)
```
resuing->reusing

```
// This let us save on two extra accounts, hence resuing existing to built
the correct accounts context.
```
Address if->Address of

```
publiquidity_program: Pubkey,// Address if liquidity program
```
to built->to build

```
// This let us save on two extra accounts, hence resuing existing to built
the correct accounts context.
```
AccountInfo->UncheckedAccount

```
// Hence loading them as AccountInfo
```
slightlty->slightly


```
// partials precision is slightlty above 1e9 so this will make sure that on
every liquidation atleast 1 partial gets liquidated
```
supplt_position->supply_position

```
letsupplt_position=
ctx.accounts.vault_supply_position_on_liquidity.load()?;
```
coeffcient->coefficient

```
pubdebt_liquidity: u64,// Debt liquidity at this branch, 56 coeffcient | 8
exponent
```
pratials->partials

```
pubfnget_current_pratials_ratio(minima_tick_partials: u32,ratio: u128)
/>Result<(u128,u128)> {
```
acccount->account

```
// No init_if_needed, as the acccount supplying must already exist in order
to supply
```
recepient->recipient

```
pubrecepient: AccountInfo<'info>,
```
receipient->recipient

```
pubreceipient_borrow_token_account: Box<InterfaceAccount<'info,
TokenAccount>>,
```
sence->since

```
// sence sending vault_supply_token_account here as a dummy value
```
liquidiation->liquidation

```
// get liquidiation max limit tick (tick at liquidation max limit ratio)
```
Parms->Params


```
pubstructInitVaultConfigParms{
```
udpate->update

```
pubfnudpate_state_at_liq_end(&mutself,tick: i32,branch_id: u32) />
Result<()> {
```
substraction->subtraction

```
// liquidity Exchange Prices always increases in next block. Hence
substraction with old will never be negative
```
liquidityWithdrawaLimit->liquidityWithdrawalLimit

```
// (liquidityUserSupply - withdrawalGap - liquidityWithdrawaLimit) should be
less than user's withdrawal
```
remainining_accounts->remaining_accounts

```
letremainining_accounts=ctx
```
is_iquidate->is_liquidate

```
fnget_exchange_rate(&self,nonce: u16,is_iquidate: bool) />Result<u128> {
```
Recommendations:

We recommend fixing the typos.

Fluid:Resolved with@a0930e2d0af...and@a3392bee9a6...

Zenith:Verified.


[I-2] Dead code

SEVERITY:Informational IMPACT:Informational

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/liquidity/src/state/context.rs
- programs/liquidity/src/state/state.rs
- programs/liquidity/src/state/token_reserve.rs
- programs/lending/src/state/state.rs
- programs/lending/src/state/seeds.rs
- programs/lending/src/errors.rs
- programs/vaults/src/errors.rs
- programs/vaults/src/errors.rs
- programs/vaults/src/errors.rs
- programs/vaults/src/events.rs
- programs/vaults/src/state/branch.rs

Description:

The targets listed above point to code that is never executed, which adds unnecessary
cognitive load during reviews.

Recommendations:

Remove the unused code, or refactor/rewrite other code to call the functions/use the errors.

Fluid:Resolved with@88d2665d99a...and@6cc13dad136...

Zenith:Verified.


[I-3] Accounts need not be marked as mutable

SEVERITY:Informational IMPACT:Informational

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/liquidity/src/state/context.rs
- programs/lending/src/state/context.rs
- programs/vaults/src/state/context.rs
- programs/oracle/src/state/context.rs
- programs/lendingRewardRateModel/src/state/context.rs

Description:

TheUpdateAuth,UpdateRevenueCollector,UpdateUserClass,UpdateUserWithdrawalLimit,
UpdateUserSupplyConfig,UpdateUserBorrowConfig,
UpdateExchangePrice,UpdateRateData,UpdateTokenConfig,ChangeStatus,PauseUser,
AdminContext,UpdateAuths,StopLendingRewards, andLendingRewardsAccounts structs all
include a mutableauthorityaccount, even though their respective instructions never
modify theirauthorityaccounts. This will lead to unnecessary transaction contention,
possibly leading to higher transaction costs required for these instructions.

In addition, thePreOperate.protocol,PreOperate.vault,Operate.protocol,
Operate.liqudity,Claim.user,UpdateRewardsRateModel.signer,UpdateAuth.signer,
UpdateRebalancer.signer,Withdraw.rate_model,UpdateRate.signer,
UpdateRate.f_token_mint,InitLending.lending_admin,InitLending.mint,
InitPosition.vault_admin,Operate.vault_config,Operate.tick_id_data,
Operate.supply_rate_model,Operate.borrow_rate_model,Operate.liquidity(once
liquidity'sOperate.liquiditystops being mutable),Operate.liquidity_program,
Liquidate.vault_config,Liquidate.supply_token,Liquidate.borrow_token,
Liquidate.top_tick_data,Liquidate.supply_rate_model,Liquidate.borrow_rate_model,
Liquidate.liquidity(once liquidity'sOperate.liquiditystops being mutable),
Liquidate.liquidity_program,OracleInit.oracle_admin, and
LendingRewards.lending_rewards_adminaccounts need not be mutable.

Recommendations:

Remove themutmodifier from the listed accounts.

Fluid:Resolved with@dd092438d1d...,@b0881dfdb6b..., and@pull/62


Zenith:Verified.


[I-4] Delayed reward distribution may temporarily prevent

withdrawals

SEVERITY:Informational IMPACT:Informational

STATUS:Acknowledged LIKELIHOOD:Low

Target

- helpers.rs

Description:

For a given token's lending, in addition to earning interest from the liquidity, extra rewards
can also be flexibly configured through thelendingRewardRateModel. These rewards
increase the price of thef_tokenover time.

```
fncalculate_new_token_exchange_price(
new_liquidity_exchange_price: u64,
lending: &Account<Lending>,
current_rate_model: &Account<LendingRewardsRateModel>,
f_token_total_supply: u64,
) />Result<(u64,bool)> {
//.
lettotal_return_in_percent=total_return_from_rewards.safe_add(
new_liquidity_exchange_price
.safe_sub(old_liquidity_exchange_price)?
.cast/:<u128>()?
.safe_mul(RETURN_PERCENT_PRECISION)?
.safe_div(old_liquidity_exchange_price.cast()?)?
.cast()?,
)?;
```
```
letnew_token_exchange_price: u64=old_token_exchange_price.safe_add(
old_token_exchange_price
.cast/:<u128>()?
.safe_mul(total_return_in_percent.cast()?)?
.safe_div(RETURN_PERCENT_PRECISION)?
.cast()?,
)?;
```
```
Ok((new_token_exchange_price,rewards_ended))
```

##### }

However, the reward tokens are not distributed when the rewards are enabled. Instead,
they are distributed through an off-chain bot via therebalanceinstruction. If the
distribution is delayed, it could, in extreme cases, result in the position not holding enough
tokens to allow all users to withdraw.

Recommendations:

It is recommended to improve the reward distribution method.

Fluid:Acknowledged


[I-5] TheOperateinstruction may be called with some accounts

that are not used.

SEVERITY:Informational IMPACT:Informational

STATUS:Resolved LIKELIHOOD:Low

Target

- context.rs

Description:

When only supplying tokens, thewithdraw_to_account,borrow_to_account, and
claim_accountare not used. If thetransferTypeis notCLAIM, there is no need to pass in
theclaim_account. However, every timeOperateis called, these accounts are still required
to be passed in, which may cause inconvenience.

```
pubstructOperate<'info> {
//.
#[account(
mut,
associated_token/:mint=mint,
associated_token/:authority=withdraw_to,
associated_token/:token_program=token_program
)]
pubwithdraw_to_account: Box<InterfaceAccount<'info,TokenAccount>>,
```
```
#[account(
mut,
associated_token/:mint=mint,
associated_token/:authority=borrow_to,
associated_token/:token_program=token_program
)]
pubborrow_to_account: Box<InterfaceAccount<'info,TokenAccount>>,
```
```
#[account(mut, has_one=mint)]
pubclaim_account: AccountLoader<'info,UserClaim>,
```
```
pubtoken_program: Interface<'info,TokenInterface>,
pubassociated_token_program: Program<'info,AssociatedToken>,
}
```

Recommendations:

It is recommended to make these accounts optional by usingOption, allowing them to be
provided only when needed.

Fluid:Resolved with@bdf526de478...

Zenith:Verified.


[I-6] Unused instruction accounts

SEVERITY:Informational IMPACT:Informational

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/liquidity/src/state/context.rs
- programs/lending/src/state/context.rs
- programs/vaults/src/state/context.rs

Description:

Theupdate_exchange_price()requires anauthoritysigner, but the instruction is meant to
be permissionless, and thus the account is never checked against anything.

TheInitLending.associated_token_program,UpdateRate.signer,
Deposit.borrow_token_reserves_liquidity, andLiquidate.vault_adminaccounts are
also unused.

TheLiquidate.top_tick_datadoesn't have any constraints that force it to match the
topmost tick, so anyTickDatafrom the vault can be passed. Outside of being loaded to
confirm ownership and PDA validity inverify_liquidate(), it's not used for anything.

Recommendations:

Remove the unused accounts.

Fluid:Resolved with@6e523fbe7e1...,@acb79b768db..., and@3bcc21a8edf...

Zenith:Verified.


[I-7] Unused account fields waste rent

SEVERITY:Informational IMPACT:Informational

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/liquidity/src/state/state.rs
- programs/liquidity/src/state/rate_model.rs
- programs/liquidity/src/state/token_reserve.rs
- programs/liquidity/src/state/user_borrow_position.rs
- programs/liquidity/src/state/user_supply_position.rs
- programs/lending/src/state/state.rs
- programs/vaults/src/state/vault_state.rs
- programs/vaults/src/state/branch.rs
- programs/vaults/src/state/tick_has_debt.rs
- programs/vaults/src/state/vault_state.rs
- programs/vaults/src/state/tick.rs
- programs/vaults/src/state/position.rs
- programs/oracle/src/state/state.rs
- programs/lendingRewardRateModel/src/state/state.rs

Description:

TheRateModel,AuthorizationList,UserClaim,TokenReserve,UserBorrowPosition,
UserSupplyPosition,BranchData,TickHasDebtArray,VaultState,TickData,UserPosition,
Oracle,LendingRewardsAdmin, andLendingRewardsRateModelaccounts all contain abump
field which costs rent and adds CU overhead, but isn't actually used anywhere.
Lending.borrow_position_on_liquidityandVaultState.total_positionsare also
unused.

TheLendingRewardsAdmin.lending_programis also unused. It looks as though the
update_rate()function is meant to work with any lending program rather than only the
compile-time one. If so, this field should be removed. If not, then the various instructions
calling that function should constrain the input arg to match that member, and the CPI
should be done with the crate's CPI method rather than the genericinvoke().


Recommendations:

Remove the fields from the listed structs, and the code that sets their values.

Fluid:Resolved with@5921357d276...and@0946eab44bc.... Acknowledging
LendingRewardsAdmin.bump,Oracle.bump, andLendingRewardsRateModel.bump.

Zenith:Verified resolved instances.


[I-8] Theinit_token_reserveinstruction does not check

whether the token decimals are supported

SEVERITY:Informational IMPACT:Informational

STATUS:Resolved LIKELIHOOD:Low

Target

- admin.rs

Description:

Theinit_token_reserveinstruction initializes thetoken_reserveandrate_modelaccounts
for the corresponding token but does not callcheck_token_decimals_rangeto verify
whether the token decimals are supported. This check is only performed later when the
update_rate_datainstruction is called.

```
pubfninit_token_reserve(context: Context<InitTokenReserve>) />Result<()>
{
letmuttoken_reserve=context.accounts.token_reserve.load_init()?;
```
```
token_reserve.mint=context.accounts.mint.key();
token_reserve.vault=context.accounts.vault.key();
token_reserve.bump=context.bumps.token_reserve;
token_reserve.last_update_timestamp
=Clock/:get()/.unix_timestamp.cast()?;
token_reserve.supply_exchange_price=EXCHANGE_PRICES_PRECISION.cast()?;
token_reserve.borrow_exchange_price=EXCHANGE_PRICES_PRECISION.cast()?;
```
```
letmutrate_model=context.accounts.rate_model.load_init()?;
```
```
rate_model.mint=context.accounts.mint.key();
rate_model.bump=context.bumps.rate_model;
```
```
Ok(())
}
```
```
pubfnupdate_rate_data_v1(
context: Context<UpdateRateData>,
rate_data: RateDataV1Params,
) />Result<()> {
```

```
check_token_decimals_range(&context.accounts.mint)?;
//.
}
```
Iftoken_reserveandrate_modelaccounts are initialized for an unsupported token, the
issue will only be detected upon callingupdate_rate_data, resulting in wasted rent and
transaction fees for the admin.

Recommendations:

It is recommended to callcheck_token_decimals_rangeduring theinit_token_reserve
instruction to verify whether the token decimals are supported.

Fluid:Resolved with@62dd8a70cab...

Zenith:Verified.


[I-9] Misleading comments

SEVERITY:Informational IMPACT:Informational

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/lending/src/state/context.rs
- programs/vaults/src/state/vault_config.rs

Description:

The following comments are misleading, which adds unnecessary cognitive load during
reviews:

- In theDepositandWithdrawstructs, the address constraint is on thelending_admin
    member, but for this instruction they were moved, but the comment was never removed:

```
#[account(mut, address=lending_admin.liquidity_program)]
/// CHECK: Safe, we check the address in the lending_admin PDA
publiquidity_program: AccountInfo<'info>,
```
- The instruction'ssupply_token_reserves_liquidityis never used in any CPI calls:

```
#[account(has_one=mint)]
/// CHECK: Safe as this will be verified in liquidity program CPI call
pubsupply_token_reserves_liquidity: AccountLoader<'info,TokenReserve>,
```
- This comment looks like it was a left-over from a refactoring:

```
puboracle: Pubkey, // Oracle PDA hops, maximum 4
```
Recommendations:

Update the comments to reflect the current behavior.

Fluid:Resolved with@6e0cb693443...and@35abf6da668...


Zenith:Verified.


[I-10] UnhandledSKIPtokentransfer_type

SEVERITY:Informational IMPACT:Informational

STATUS:Acknowledged LIKELIHOOD:Low

Target

- token.rs

Description:

Thetransfer_typeenum defines three types.

```
pubenumTransferType{
SKIP, // skip transfer
DIRECT,// transfer directly to the user (no claim)
CLAIM, // transfer to claim account and then can be claimed by user
later
}
```
However, inhandle_transfer_or_claimonly the other two types of transfers are handled.
TheSKIPtype transfer is not processed, which may cause errors when this type of transfer
is used in integration.

```
pubfnhandle_transfer_or_claim(
transfer_type: &TransferType,
claimer: Pubkey,
claim_account: &mutAccountLoader<UserClaim>,
last_stored_claim_amount: u64,
transfer_params: TokenTransferParams,
) />Result<u64> {
//.
matchtransfer_type{
TransferType/:DIRECT/> {
transfer_spl_tokens(transfer_params)?;
Ok( 0 )
}
TransferType/:CLAIM/> {
letmutclaim_account=claim_account.load_mut()?;
```

```
ifclaim_account.user/=claimer{
returnErr(ErrorCodes/:InvalidUserClaim.into());
}
```
```
claim_account.approve(transfer_params.amount)?;
returnOk(transfer_params.amount);
}
_/>returnErr(ErrorCodes/:InvalidTransferType.into()),
}
}
```
Recommendations:

It is recommended to either remove theSKIP transfer_typeor implement the
corresponding handling logic.

Fluid:Acknowledged


[I-11] There may not be enough user class entries to support

future tokens

SEVERITY:Informational IMPACT:Informational

STATUS:Acknowledged LIKELIHOOD:Low

Target

- programs/liquidity/src/state/state.rs

Description:

TheAuthorizationList.user_classesaccount field is meant to track which liquidity
program users are allowed to be paused. If there is no entry, it defaults to allowed, but if it's
set to one for a user, that user cannot be paused. For every fToken (one per liquidity supply
token) and for every vault (one per supply-and-borrow token pair), a new protocol/user is
created in the liquidity program. Currently, according to fluid.io, for Solidity there are six
fTokens, and 85 vaults. If the Solana version of fluid is as successful or greater over time,
and a lot of user classes need to be set to unpauseable, theAuthorizationListPDA may
run out of space.

Recommendations:

Significantly increase the size of theuser_classesfield.

Fluid:Acknowledged. This feature is rarely used we typically don’t list users as
un-pausable, and by default all users can be paused, which is the intended behavior. Given
this, the current field size has been sufficient. If ever required, we can expand the field in a
future upgrade.


[I-12] Rewards calculation does not credit interest-related TVL
growth

SEVERITY:Informational IMPACT:Informational

STATUS:Resolved LIKELIHOOD:Low

Target

- programs/lending/src/utils/helpers.rs

Description:

The rewards calculation for both the prior (or current) and the current (or next period), use
the TVL calculated using the prior exchange prices. Consider the case where the TVL is
right above the cutoff, but then a user withdraws such that the TVL is now just below the
limit. If there are no mints or burns until after the queued rewards period has elapsed, there
will be zero rewards even though it is likely that, due to interest growth, TVL will grow above
the limit without a new mint needing to occur.

Recommendations:

If this is expected behavior, it might be worth while to document in a code comment that
theupdate_rate()instruction can be used to get credit for TVL growth due to interest.

Fluid:We've added the comment here:@e143c8abe75.... Thestart_tvlis only used to
set some minimal realistic amount to avoid any weird edge cases, by default this has always
been set to ~$1k worth of the token. Realistically, we can assume that any fToken that gets
rewards, has a TVL way above the configuredstart_tvl. Using the older exchange price is
then actually beneficial to users as they get accounted a slightly higher rewards rate. Also,
we can assume frequent interactions on any fToken, especially on one that has active
rewards going on.

Zenith:Verified.


