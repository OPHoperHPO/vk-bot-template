# -*- coding: utf-8 -*-
# This is a bot for vk.com.
# Developed by Anodev. https://github.com/OPHoperHPO

import time
import vk_api
from libs import utils
import requests.exceptions
from threading import Thread
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def init(path_config_file):
    """Init part of script"""
    # Init very important modules.
    config_obj = utils.Config(path_config_file)
    utils_text_obj = utils.Text(config_obj)

    # Init vars.
    token_longpoll = config_obj.get_config_var('Auth', 'token_longpoll')
    group_id = config_obj.get_config_var('Auth', 'group_id')

    # Init vk api.
    vk_session = vk_api.VkApi(token=token_longpoll)
    longpoll_i = VkBotLongPoll(vk_session, group_id=group_id)

    # Init bot functions
    command_centre_i = utils.CommandCentre(config_obj, utils_text_obj, vk_session)

    # Clean potentially danger data.
    del token_longpoll, group_id

    # Return data
    return longpoll_i, command_centre_i, config_obj, utils_text_obj


def main(longpoll_m, command_centre_m):
    """Main part of script"""
    # Define functions
    def run_listening():
        """Runs longpoll_m listening"""
        # Define functions for threads
        def thread_for_conversation(event_obj_th, command_centre_t):
            """Run command centre for conversation."""
            message_object = event_obj_th.object
            # Call command centre
            command_centre_t.run_function(message_object)

        def thread_for_user_chat(event_obj_th2, command_centre_t):
            """Run command centre for user chat."""
            message_object = event_obj_th2.object
            # Call command centre
            command_centre_t.run_function(message_object)

        # Init thread vars
        thread_Conv = False
        thread_UChat = False

        for event in longpoll_m.listen():
            # Check for Conversation
            if event.type == VkBotEventType.MESSAGE_NEW and event.object.text and event.from_chat:
                if thread_Conv:
                    if thread_Conv.isAlive() is False:
                        # Stop thread when thread work finish.
                        thread_Conv.join()
                # Make Thread
                thread_Conv = Thread(target=thread_for_conversation, args=(event, command_centre_m))
                # Start thread
                thread_Conv.start()

            # Check for message from user.
            if event.type == VkBotEventType.MESSAGE_NEW and event.object.text and event.from_user:
                if thread_UChat:
                    if thread_UChat.isAlive() is False:
                        # Stop thread when thread work finish.
                        thread_UChat.join()
                # Make Thread
                thread_UChat = Thread(target=thread_for_user_chat, args=(event, command_centre_m))
                # Start thread
                thread_UChat.start()

    def check_internet_connection():
        """Checks internet connection by sending a request to vk.com"""
        try:
            request = requests.get(url='https://vk.com/')
            if request.status_code == 200:
                return True
            else:
                return True
        except requests.exceptions.RequestException:
            return False

    # Prevent crash bot when the internet goes down
    while True:
        try:
            # Run longpoll_m listening.
            run_listening()
        except requests.exceptions.RequestException:
            while True:
                # Check internet connection
                internet_status = check_internet_connection()
                # If everything is bad, we wait and try to connect again
                if internet_status:
                    break
                else:
                    print('VK_BOT [Longpoll Listening Error!]: Internet does not work!')
                # Time to rest!
                time.sleep(120)


if __name__ == "__main__":
    # Change this if you want to change config.json path!
    path_to_config_file = './config/config.json'
    # Run script
    longpoll, command_centre, config, utils_text = init(path_to_config_file)
    main(longpoll, command_centre)
