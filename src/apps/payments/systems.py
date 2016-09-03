import urllib
import urlparse
import collections
import httplib

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from .models import PayPalTransaction
from .exceptions import PayPalException

from constance import config



class PayPal(object):
    def __init__(self, returnUrl, currency='USD', error_language='en_US'):
        # Set our headers
        self.headers = {
            'X-PAYPAL-SECURITY-USERID': config.PAYPAL_SECURITY_USERID,
            'X-PAYPAL-SECURITY-PASSWORD': config.PAYPAL_SECURITY_PASSWORD,
            'X-PAYPAL-SECURITY-SIGNATURE': config.PAYPAL_SECURITY_SIGNATURE,
            'X-PAYPAL-SERVICE-VERSION': '1.1.0',
            'X-PAYPAL-REQUEST-DATA-FORMAT': 'NV',
            'X-PAYPAL-RESPONSE-DATA-FORMAT': 'NV'
        }

        if config.PAYPAL_MODE == 'live':
            self.sandbox = False
        elif config.PAYPAL_MODE == 'sandbox':
            self.sandbox = True

        if self.sandbox:
            self.headers['X-PAYPAL-APPLICATION-ID'] = 'APP-80W284485P519543T'
        else:
            self.headers['X-PAYPAL-APPLICATION-ID'] = config.PAYPAL_APPLICATION_ID

        self.returnUrl = returnUrl
        self.cancelUrl = config.PAYPAL_CANCEL_URL
        self.currency = currency
        self.error_language = error_language

    def get_payment_information(self, payKey):
        """ Get payment information by payKey
        """
        if self.sandbox:
            conn = httplib.HTTPSConnection("svcs.sandbox.paypal.com")
        else:
            conn = httplib.HTTPSConnection("svcs.paypal.com")
        params = collections.OrderedDict()
        params['payKey'] = payKey
        params['requestEnvelope.errorLanguage'] = self.error_language
        enc_params = urllib.urlencode(params)
        conn.request(
            "POST",
            "/AdaptivePayments/PaymentDetails/",
            enc_params,
            self.headers
        )
        response = conn.getresponse()
        data = urlparse.parse_qs(response.read())
        return data

    def adaptive_payment(self,
                         comment_object,
                         receiver_amount,
                         receiver_user,
                         sender_user
                         ):
        """ Make adaprive payments
        Returns:
            dict
        """

        # Set our POST Parameters
        params = collections.OrderedDict()
        params['requestEnvelope.errorLanguage'] = self.error_language
        params['requestEnvelope.detailLevel'] = 'ReturnAll'
        params['reverseAllParallelPaymentsOnError'] = 'true'
        params['returnUrl'] = self.returnUrl
        params['cancelUrl'] = self.cancelUrl
        params['actionType'] = 'PAY'
        params['currencyCode'] = self.currency
        params['feesPayer'] = 'EACHRECEIVER'

        params['receiverList.receiver(0).email'] = receiver_user.email
        params['receiverList.receiver(0).amount'] = receiver_amount

        # Add Client Details
        params['clientDetails.ipAddress'] = '127.0.0.1'
        params['clientDetails.deviceId'] = 'mydevice'
        params['clientDetails.applicationId'] = 'PayNvpDemo'

        enc_params = urllib.urlencode(params)

        # Connect to sand box and POST.
        if self.sandbox:
            conn = httplib.HTTPSConnection("svcs.sandbox.paypal.com")
        else:
            conn = httplib.HTTPSConnection("svcs.paypal.com")

        conn.request(
            "POST",
            "/AdaptivePayments/Pay/",
            enc_params,
            self.headers
        )
        response = conn.getresponse()

        # Get the reply and print it out.
        data = urlparse.parse_qs(response.read())

        if data.get('error(0).message'):
            raise PayPalException(data.get('error(0).message'))

        # Set pay key

        payKey = data['payKey'][0]

        transaction = PayPalTransaction.objects.create(
            comment=comment_object,
            currency=self.currency,
            amount=receiver_amount,
            sender_user=sender_user,
            receiver_user=receiver_user,
            paymentExecStatus=getattr(PayPalTransaction,
                                      data['paymentExecStatus'][0]),
            payKey=data['payKey'][0]
        )

        result = {
            'status': response.status,
            'reason': response.reason,
            'data': data,
            'transaction_object': transaction
        }

        if self.sandbox:
            result['pay_url'] = 'https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_ap-payment&paykey=%s' % payKey
        else:
            result['pay_url'] = 'https://www.paypal.com/cgi-bin/webscr?cmd=_ap-payment&paykey=%s' % payKey

        return result
