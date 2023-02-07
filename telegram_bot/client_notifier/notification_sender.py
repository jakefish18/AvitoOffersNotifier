"""
Notifying users about new offer.
"""

import asyncio
from aiogram import Bot

from database.users_handler import UsersHandler
from database.user_offers_handler import UserOfferTypesHandler
from database.offer_queue_handler import OfferQueueHandler


class UsersNotifier:

    def __init__(self, bot: Bot) -> None:
        self.users_handler = UsersHandler()
        self.user_offer_types_handler = UserOfferTypesHandler()
        self.offer_queue_handler = OfferQueueHandler()

        self.bot = bot

    async def run(self) -> None:
        """
        Sending notifies to every user about their events.
        The function works every day.
        The function goes sleep for 1 day after work finish
        """
        # await self._notify_about_bot_update()

        while True:
            offer_queue = self.offer_queue_handler.get_offers()
            print(offer_queue)

            # Check that queue isn't empty
            if len(offer_queue) == 0:
                await asyncio.sleep(5)
                continue

            for offer_type in offer_queue:
                offer_type_item_id = offer_type[0]
                users_to_notify = self.user_offer_types_handler.get_users_by_type_item(offer_type_item_id)
                print(users_to_notify)

                for user in users_to_notify:
                    user_id = user[0]
                    user_telegram_id = self.users_handler.get_user_telegram_id(user_id)


                    await self.bot.send_message(
                        user_telegram_id,
                        "Появилось новое предложение."
                    )
                    await asyncio.sleep(0.3)

            await asyncio.sleep(5)

    async def _notify_about_bot_update(self) -> None:
        """
        Notifying all users about the bot update.
        """
        pass
