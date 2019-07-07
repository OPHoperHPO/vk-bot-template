# Functions file for bot.
# Module version: 1.4
# Writen by Anodev.
# Contain all functions for bot.

# Imports
import re
import requests
from vk_api import VkUpload
from vk_api.utils import get_random_id


# Define classes.
class BotFunctions(object):
    def __init__(self, config, texts, vk_session):
        """Bot functions."""

        # Init vk vars
        self.vk = vk_session.get_api()
        self.upload = VkUpload(vk_session)

        # Init other vars for functions
        self.texts_id = texts

        # Init other functions
        # ADD HERE NEW FUNCTION!
        self.Help = Help(bot_func_obj=self)
        self.SendUserMessage = SendUserMessage(bot_func_obj=self)
        self.SearchSomethingInSearchEngine = SearchSomethingInSearchEngine(bot_func_obj=self)

# ADD A NEW FUNCTION AS A CLASS! STRICTLY FOLLOW THE EXAMPLE BELOW!


class Help(object):
    def __init__(self, bot_func_obj):
        """Sends help message. """
        """Example of '_exception_' function"""
        """Look this message in texts/txt/help_message.txt"""
        # Init vk vars
        self.vk = bot_func_obj.vk
        # Init func vars
        self.text = bot_func_obj.texts_id

    def run(self, chat_id):
        """Sends help message. """
        self.vk.messages.send(
            peer_id=chat_id,
            message=self.text.get_text('Main', 'help_message'),
            random_id=get_random_id())
        return True


class SendUserMessage(object):
    def __init__(self, bot_func_obj):
        """Sends a message to the user his message as if the bot did."""
        # Init vk vars
        self.vk = bot_func_obj.vk

        # Init functions vars
        self.text = bot_func_obj.texts_id

    def run(self, chat_id, message, activation_word):
        """Main function. Sends a message to the user his message as if the bot did."""
        # Check for empty message.
        if len(activation_word) == len(message):
            self.vk.messages.send(
                peer_id=chat_id,
                random_id=get_random_id(),
                message=self.text.get_text('Common Errors', 'empty_message_error'))
            return False

        # Clean message.
        message = re.split('(?i)^{0} '.format(activation_word), message, maxsplit=1)
        message = message[1]

        # Send user message.
        self.vk.messages.send(
            peer_id=chat_id,
            random_id=get_random_id(),
            message=message)
        return True


class SearchSomethingInSearchEngine(object):
    def __init__(self, bot_func_obj):
        """Search something in search engine."""
        # TODO Make changer for search engine. Switch DuckDuckGo to Google!
        # Init vk vars
        self.vk = bot_func_obj.vk
        self.upload = bot_func_obj.upload

        # Init func vars
        self.text = bot_func_obj.texts_id
        self.session = requests.Session()

    def run(self, chat_id, message, activation_word):
        """Main function. Sends to user search result from search engine."""
        # Check for empty message.
        if len(activation_word) == len(message):
            self.vk.messages.send(
                peer_id=chat_id,
                random_id=get_random_id(),
                message=self.text.get_text('Common Errors', 'empty_message_error'))
            return False

        # Clean message.
        message = re.split('(?i)^{0} '.format(activation_word), message, maxsplit=1)
        message = message[1]

        # Send request to API search engine.
        response = self.session.get(
            'http://api.duckduckgo.com/',
            params={
                'q': message,
                'format': 'json'
            }).json()
        text = response.get('AbstractText')
        image_url = response.get('Image')

        # Check for 'not found' error.
        if not text:
            self.vk.messages.send(
                peer_id=chat_id,
                random_id=get_random_id(),
                message=self.text.get_text('Common Errors', 'not_found_error'))
            return True

        # Init attachments list
        attachments = []

        # Check for image URL if exist attach to message.
        if image_url:
            image = self.session.get(image_url, stream=True)
            photo = self.upload.photo_messages(photos=image.raw)[0]

            # Add to attachments list
            attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))

            # Send message to user.
            self.vk.messages.send(
                peer_id=chat_id,
                attachment=','.join(attachments),
                random_id=get_random_id(),
                message=text
            )
            return True
