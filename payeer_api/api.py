import re
import requests


def validate_wallet(wallet):
    if not re.match('P\d{7,12}$', wallet):
        raise ValueError('Wrong wallet format!')


class PayeerAPIException(Exception):
    """Base payeer api exception class"""


class PayeerAPI:
    """Payeer API Client"""

    def __init__(self, account, apiId, apiPass):
        """
        :param account: Your account number in the Payeer system. Example: P1000000
        :param apiId: The API user’s ID; given out when adding the API
        :param apiPass: The API user's secret key
        """
        validate_wallet(account)
        self.account = account
        self.apiId = apiId
        self.apiPass = apiPass
        self.api_url = 'https://payeer.com/ajax/api/api.php'
        self.auth_data = {'account': self.account, 'apiId': self.apiId, 'apiPass': self.apiPass}
        self.auth_check()

    def request(self, **kwargs):
        """The main request method for Payeer API"""
        data = self.auth_data
        if kwargs:
            data.update(kwargs)
        resp = requests.post(url=self.api_url, data=data).json()
        error = resp.get('errors')
        if error:
            raise PayeerAPIException(error)
        else:
            return resp

    def auth_check(self):
        """
        Authorization Check
        :return: True if auth is successful
        """
        self.request()

    def get_balance(self):
        """
        Balance Check
        Obtain wallet balance.
        """
        return self.request(action='balance')['balance']

    def check_user(self, user):
        """
        Checking Existence of Account
        :param user: user’s account number in the format P1000000
        :return: True if exists
        """
        try:
            self.request(action='checkUser', user=user)
        except PayeerAPIException:
            return False
        return True

    def get_exchange_rate(self, output='N'):
        """
        Automatic Conversion Rates
        :param output: select currencies for conversion rates (N - get deposit rates Y - get withdrawal rates)
        :return: dict
        """
        return self.request(action='getExchangeRate', output=output)['rate']

    def get_pay_systems(self):
        """
        Getting Available Payment Systems
        :return: dict
        """
        return self.request(action='getPaySystems')['list']

    def get_history_info(self, history_id):
        """
        Getting Information about a Transaction
        :param history_id: transaction ID
        :return: dict
        """
        return self.request(action='historyInfo', historyId=history_id)['info']

    def shop_order_info(self, shop_id, order_id):
        """
        Information on a Store Transaction
        :param shop_id: merchant ID (m_shop)
        :param order_id: transaction ID in your accounting system (m_orderid)
        :return: dict
        """
        return self.request(action='shopOrderInfo', shopId=shop_id, orderId=order_id)

    def transfer(self, sum, to, cur_in='USD', cur_out='USD',
                 comment=None, protect=None, protect_period=None, protect_code=None):
        """
        Transferring Funds
        :param sum: amount withdrawn (the amount deposited will be calculated automatically, factoring in all fees from the recipient)
        :param to: user’s Payeer account number or email address
        :param cur_in: currency with which the withdrawal will be performed	(USD, EUR, RUB)
        :param cur_out: deposit currency (USD, EUR, RUB)
        :param comment: comments on the transfer
        :param protect: activation of transaction protection, set Y to enable
        :param protect_period: protection period: 1–30 days
        :param protect_code: protection code
        :return: True if the payment is successful
        """
        validate_wallet(to)
        data = {'action': 'transfer', 'sum': sum, 'to': to, 'curIn': cur_in, 'curOut': cur_out}
        if comment: data['comment'] = comment
        if protect:
            data['protect'] = protect
            if protect_period: data['protectPeriod'] = protect_period
            if protect_code: data['protectCode'] = protect_code
        resp = self.request(**data)
        if resp.get('historyId', 0) > 0:
            return True
        else:
            return False

    def check_output(self, ps, ps_account, sum_in, cur_in='USD', cur_out='USD'):
        """
        Checking Possibility of Payout
        This method allows you to check the possibility of a payout without actually creating a payout
        (you can get the withdrawal/reception amount or check errors in parameters)
        :param ps: ID of selected payment system
        :param ps_account: recipient's account number in the selected payment system
        :param sum_in: amount withdrawn (the amount deposited will be calculated automatically, factoring in all fees from the recipient)
        :param cur_in: currency with which the withdrawal will be performed
        :param cur_out: deposit currency
        :return: True if the payment is successful
        """
        data = {'action': 'initOutput', 'ps': ps, 'param_ACCOUNT_NUMBER': ps_account,
                'sumIn': sum_in, 'curIn': cur_in, 'curOut': cur_out}
        try:
            self.request(**data)
        except PayeerAPIException:
            return False
        return True

    def output(self, ps, ps_account, sum_in, cur_in='USD', cur_out='USD'):
        """
        Payout
        :param ps: ID of selected payment system
        :param ps_account: recipient's account number in the selected payment system
        :param sum_in: amount withdrawn (the amount deposited will be calculated automatically, factoring in all fees from the recipient)
        :param cur_in: currency with which the withdrawal will be performed
        :param cur_out: deposit currency
        :return:
        """
        data = {'action': 'output', 'ps': ps, 'param_ACCOUNT_NUMBER': ps_account,
                'sumIn': sum_in, 'curIn': cur_in, 'curOut': cur_out}
        return self.request(**data)

    def history(self, **kwargs):
        """
        History of transactions
        :param sort: sorting by date (asc, desc)
        :param count: count of records (max 1000)
        :param from: begin of the period
        :param to: end of the period
        :param type: transaction type (incoming - incoming payments, outgoing - outgoing payments)
        :param append: id of the previous transaction
        :return:
        """
        kwargs['action'] = 'history'
        return self.request(**kwargs)['history']
