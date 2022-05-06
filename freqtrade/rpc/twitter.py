import logging
from datetime import datetime
from typing import Any, Dict

import tweepy

from freqtrade.enums import RPCMessageType
from freqtrade.rpc import RPC, RPCException, RPCHandler


logger = logging.getLogger(__name__)

""" Twitter module """


class Twitter(RPCHandler):
    """This class all all Twitter communication"""

    def __init__(self, rpc: RPC, config: Dict[str, Any]) -> None:
        """
        Init the Twitter call, and init the super class RPCHandler
        :param rpc: instance of RPC Helper class
        :param config: Configuration object
        :return: None
        """
        self._config = config
        self._auth = tweepy.OAuth1UserHandler(
            self._config["twitter"]["consumer_api_key"],
            self._config["twitter"]["consumer_api_secret"],
            self._config["twitter"]["access_token"],
            self._config["twitter"]["access_token_secret"],
        )
        self._api = tweepy.API(self._auth)
        auth = tweepy.OAuth1UserHandler(
            self._config["twitter"]["consumer_api_key"],
            self._config["twitter"]["consumer_api_secret"],
            self._config["twitter"]["access_token"],
            self._config["twitter"]["access_token_secret"],
        )
        self.api = tweepy.API(auth)

        super().__init__(rpc, config)

    def send_msg(self, msg: Dict[str, Any]) -> None:

        logger.info(
            f"BUY-SELL-OR-CANCEL-ORDER LOOK AT THE self.rpc.send_message in freqtradebot.py"
        )
        logger.info(msg)
        UPDATE_STATUSES = [
            RPCMessageType.BUY,
            RPCMessageType.BUY_FILL,
            RPCMessageType.BUY_CANCEL,
            RPCMessageType.SELL,
            RPCMessageType.SELL_CANCEL,
            RPCMessageType.SELL_FILL,
        ]
        if msg["type"] in UPDATE_STATUSES:
            _status = self.api.update_status(
                f"""type: {msg["type"]} \n 
                pair: {msg["pair"]} \n 
                open_rate: {msg["open_rate"]} \n 
                order_type: {msg["order_type"]} \n 
                open_date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""
            )
            logger.info(_status)
