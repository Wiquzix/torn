from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.exceptions import AddressNotFound, BadAddress, ValidationError
from tronpy.keys import to_base58check_address

class TronService:
    def __init__(self):
        self.client = Tron(provider=HTTPProvider('https://nile.trongrid.io'))

    async def get_wallet_info(self, address: str) -> dict:
        try:

            try:
                address = to_base58check_address(address)
            except:
                raise ValueError("Invalid TRON address format")

            account = self.client.get_account(address)
            if not account:
                return {
                    "wallet_address": address,
                    "bandwidth": 0,
                    "energy": 0,
                    "trx_balance": 0.0
                }

            try:
                bandwidth = self.client.get_account_resource(address)
            except:
                bandwidth = {"freeNetLimit": 0, "NetLimit": 0, "EnergyLimit": 0}
            
            balance_in_sun = account.get("balance", 0)
            balance_in_trx = float(balance_in_sun) / 1_000_000
            
            return {
                "wallet_address": address,
                "bandwidth": int(bandwidth.get("freeNetLimit", 0)) + int(bandwidth.get("NetLimit", 0)),
                "energy": int(bandwidth.get("EnergyLimit", 0)),
                "trx_balance": balance_in_trx
            }
        except (AddressNotFound, BadAddress, ValidationError) as e:
            raise ValueError(f"Error processing TRON address: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}") 