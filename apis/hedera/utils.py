# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
import os
from functools import wraps

# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.contrib import messages
from django.utils.decorators import method_decorator

# --------------------------------------------------------------
# 3rd party imports
# --------------------------------------------------------------
from hedera import (
    Client, AccountId, PrivateKey,
    TokenCreateTransaction,TokenMintTransaction, 
    TokenType,TokenSupplyType,TokenId,TokenAssociateTransaction,
	AccountCreateTransaction,Hbar, AccountBalanceQuery, TransferTransaction,
    NftId, AccountInfoQuery
    )
from jnius import autoclass

OPERATOR_ID = AccountId.fromString(os.environ["OPERATOR_ID"])
OPERATOR_KEY = PrivateKey.fromString(os.environ["OPERATOR_KEY"])

client = Client.forTestnet()
client.setOperator(OPERATOR_ID, OPERATOR_KEY)

Collections = autoclass("java.util.Collections")

class AccountManager:
    '''
    Manager to handle Hedera Account endpoints
    '''
    def __init__ (self, *args, **kwargs):
        self.account = kwargs.get("account")

    def create_new_account(self):
        '''
        Creates new accounts for demo purposes.
        '''
        self.private = PrivateKey.generate()
        self.public = self.private.getPublicKey()
        tran = AccountCreateTransaction()
        self.resp = tran.setKey(self.public).setInitialBalance(Hbar.fromTinybars(10_000_000_000)).execute(client)
        self.receipt = self.resp.getReceipt(client)
        acc_id = self.receipt.accountId
        balance = AccountBalanceQuery().setAccountId(acc_id).execute(client)
        balance_text = balance.hbars.toString()
        return {
            'acc_id' : acc_id.toString(),
            'public_key' : self.public.toString(),
            'private_key' : self.private.toString(),
            'balance': balance_text,
            'node': self.resp.nodeId
            }

    def query_account_balance(self, **kwargs):
        nft = kwargs.get("nft")
        acc_id = self.account.account_id
        acc_query = AccountBalanceQuery(
            ).setAccountId(AccountId.fromString(acc_id)
            ).execute(client)
        hbar = acc_query.hbars.toString()
        response = {
            "hbars":hbar,
            "tokens": {}
        }
        if nft:
            nft_id = NftId(TokenId.fromString(nft.token.hedera_token_id), nft.hedera_serials)
            tokens = acc_query.tokens._map.get(nft_id.toString())
            response["tokens"][nft_id.toString()] = tokens
        return response

    def query_account_info(self, **kwargs):
        acc_id = self.account.account_id
        acc_query = AccountInfoQuery(
            ).setAccountId(AccountId.fromString(acc_id)
            ).execute(client)
        nfts = acc_query.ownedNfts
        key = acc_query.key
        response = {
            "key":key.toString(),
            "nfts": nfts
        }
        return response


class TokenManager:

    def create_token(self, **kwargs):

        max_supply = kwargs.get("max_supply")
        token_name = kwargs.get("token_name")
        token_symbol = kwargs.get("token_symbol")

        token_tran = TokenCreateTransaction(
        ).setTokenName(token_name 
        ).setTokenSymbol(token_symbol 
        ).setTokenType(TokenType.NON_FUNGIBLE_UNIQUE 
        ).setDecimals(0 
        ).setInitialSupply(0 
        ).setSupplyType(TokenSupplyType.FINITE 
        ).setMaxSupply(max_supply
        ).setTreasuryAccountId(OPERATOR_ID 
        ).setAdminKey(OPERATOR_KEY.getPublicKey()
        ).setSupplyKey(OPERATOR_KEY.getPublicKey()
        ).setPauseKey(OPERATOR_KEY.getPublicKey()
        ).setFreezeKey(OPERATOR_KEY.getPublicKey()
        ).setWipeKey(OPERATOR_KEY.getPublicKey()
        ).freezeWith(client
        ).sign(OPERATOR_KEY
        ).execute(client)

        receipt = token_tran.getReceipt(client)
        token_id = receipt.tokenId

        print(f'Success! token id: {token_id.toString()}')
        return token_id.toString()

    def mint_new_nft(self, **kwargs):
        
        self.nft = kwargs.get("nft")
        
        token_mint = TokenMintTransaction(
        ).setTokenId(TokenId.fromString(self.nft.token.hedera_token_id)
        ).addMetadata([ord(s) for s in self.nft.get_ipfs_file_cid]
        ).freezeWith(client
        ).sign(OPERATOR_KEY
        ).execute(client)

        receipt = token_mint.getReceipt(client)
        serial_number = receipt.serials[0]
        print(f'Success! NFT serial number {serial_number}')
        self.nft.hedera_serials = serial_number
        self.nft.save()

        return serial_number


    def associate(self, **kwargs):
        self.account = kwargs.get("account")
        self.token = kwargs.get("token")
        account_id = self.account.account_id
        account_secret_key = self.account.account_private_key
        token_id = self.token.hedera_token_id
        token_ass = TokenAssociateTransaction(
            ).setAccountId(AccountId.fromString(account_id)
            ).setTokenIds(Collections.singletonList(TokenId.fromString(token_id))
            ).freezeWith(client
            ).sign(PrivateKey.fromString(account_secret_key)
            ).execute(client)

        return token_ass

    def transfer(self, **kwargs):
        self.account = kwargs.get("account")
        self.nft = kwargs.get("nft")
        account_id = self.account.account_id
        token_id = self.nft.token.hedera_token_id
        nft_serial_number = int(self.nft.hedera_serials)
        nft_id = NftId(TokenId.fromString(token_id), nft_serial_number)
        transfer = TransferTransaction(
            ).addNftTransfer(nft_id, OPERATOR_ID, AccountId.fromString(account_id)
            ).freezeWith(client
            ).sign(OPERATOR_KEY
            ).execute(client)

        return transfer



