from ast import Constant
import discord
import os
import constants
import feedparser


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        print('Got message from {0.author}: {0.content}'.format(message))

        msgContent: str = message.content
        if msgContent.lower().startswith(constants.BOT_NAME):
            await self.handle_command(message)

    async def handle_command(self, message: discord.Message):
        msgContent: str = message.content
        print("Handling Command")
        # Remove uneneccessary elements
        msgContent = self.remove_element_from_msg(
            constants.BOT_NAME, msgContent)

        print("cmd msg: {}".format(msgContent))
        # Add RSS Feed Command
        if msgContent.lower().startswith(constants.COMMAND_ADD_RSS):
            print("Handling Add Command")
            msgContent = self.remove_element_from_msg(
                constants.COMMAND_ADD_RSS, msgContent)
            rss_feed_url: str = msgContent.split(' ')[0]

            await message.channel.send('Searching for RSS feed...')
            rss = feedparser.parse(rss_feed_url)
            await message.channel.send('Found the following info:' +
                                       '\nEntries:{}\nDescription:{}'
                                       .format(len(rss.entries),
                                               rss.feed.description))

    def remove_element_from_msg(self, word: str, from_message: str) -> str:
        new_message: str = from_message.replace(word, ' ')
        new_message = new_message.strip()
        print("removing {} from {}.".format(word, from_message))
        print("final msg: {}".format(new_message))
        return new_message


client = MyClient()
client.run(str(os.getenv('DISCORD_RSS_FEED_SUBSCRIBER_TOKEN')))
