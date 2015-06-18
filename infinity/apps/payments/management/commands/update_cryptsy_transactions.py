from django.core.management.base import BaseCommand
from ...models import CryptsyTransaction
from ...models import CryptsyCredential
from ...cryptsy.v2 import Cryptsy


class Command(BaseCommand):
    help = "Synchronize local cryptsy transactions"

    def handle(self, *args, **kwargs):

        cryptsy_credentials = CryptsyCredential.objects.all()

        for cryptsy_credential in cryptsy_credentials:
            cryptsy = Cryptsy(cryptsy_credential.publickey, cryptsy_credential.privatekey)

            cryptsy_transactions = cryptsy.withdrawals()['data']

            local_transactions = CryptsyTransaction.objects.filter(trxid=None)

            for cryptsy_transaction in cryptsy_transactions:
                for local_transaction in local_transactions:
                    if cryptsy_transaction['timestamp'] == local_transaction.timestamp:
                        local_transaction.trxid = cryptsy_transaction['trxid']
                        local_transaction.save()

                        if local_transaction.trxid:
                            self.stdout.write('Transaction updated')
