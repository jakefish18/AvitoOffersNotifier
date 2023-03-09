"""
Notifying users about new offer.
"""

import asyncio
import logging
from aiogram import Bot

from database.users_handler import UsersHandler
from database.user_offers_handler import UserOfferTypesHandler
from database.offer_queue_handler import OfferQueueHandler
from database.offers_handler import OffersHandler
from avito_parser.avito_parser import AvitoOffer
from telegram_bot.bot_config import PATH_TO_PROJECT


logging.basicConfig(
    level=logging.INFO,
    filename=f"{PATH_TO_PROJECT}logs/client_notifier.log",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


class UsersNotifier:

    def __init__(self, bot: Bot) -> None:
        self.users_handler = UsersHandler()
        self.user_offer_types_handler = UserOfferTypesHandler()
        self.offer_queue_handler = OfferQueueHandler()
        self.offers_handler = OffersHandler()

        self.bot = bot

    async def run(self) -> None:
        """
        Sending notifies to every user about new offers.
        """
        # await self._notify_about_bot_update()

        while True:
            logging.info("User notifier new circle started")
            offer_queue = self.offer_queue_handler.get_offers()

            # Check that queue isn't empty
            if len(offer_queue) == 0:
                logging.info("Offer queue is empty")
                await asyncio.sleep(10)
                continue

            for offer_type in offer_queue:
                offer_type_item_id = offer_type[0]
                offer_id = offer_type[1]

                logging.info(f"Notifying about type: {offer_type_item_id} offer: {offer_id}")

                users_to_notify = self.user_offer_types_handler.get_users_by_type_item(offer_type_item_id)
                offer: AvitoOffer = self.offers_handler.get_offer_info(offer_id)

                new_offer_message = f"Появилось новое предложение!\n" \
                                    f"Название: {offer.title}\n"\
                                    f"Цена: {offer.price} {offer.currency}\n" \
                                    f"Город: {offer.city}\n" \
                                    f"Ссылка: {offer.url}"

                for user in users_to_notify:
                    user_id = user[0]
                    user_telegram_id = self.users_handler.get_user_telegram_id(user_id)

                    logging.info(f"Notifying about type: {offer_type_item_id} offer: {offer_id} user: {user_id}")

                    await self.bot.send_message(
                        user_telegram_id,
                        new_offer_message
                    )

                    await asyncio.sleep(0.3)

            logging.info("User notifier circle finished")
            await asyncio.sleep(10)

    async def _notify_about_bot_update(self) -> None:
        """
        Notifying all users about the bot update.
        """
        pass
