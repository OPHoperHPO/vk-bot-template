# -*- coding: utf-8 -*-
# This is a bot for vk.com.
# Developed by Anodev. https://github.com/OPHoperHPO

import vk_api
import lib.utils as utils
from threading import Thread
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEvent, VkBotEventType


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
    longpoll = VkBotLongPoll(vk_session, group_id=group_id)

    # Init bot functions
    command_center = utils.CommandCentre(config_obj, utils_text_obj, vk_session)

    # Clean potentially danger data.
    del token_longpoll, group_id

    # Return data
    return longpoll, command_center, config_obj, utils_text_obj


def main(longpoll, command_centre_m, config, utils_text):
    """Main part of script"""
    # Functions for threads
    def thread_for_conversation(event, command_centre_t):
        """Run command centre for conversation."""
        message_object = event.object
        # Call command center
        command_centre_t.run_function(message_object)

    def thread_for_user_chat(event, command_centre_t):
        """Run command centre for user chat."""
        message_object = event.object
        # Call command center
        command_centre_t.run_function(message_object)

    # Init thread vars
    thread_Conv = False
    thread_UChat = False

    # Run longpoll listening.
    for event in longpoll.listen():
        # Check for message in conversation.
        if event.type == VkBotEventType.MESSAGE_NEW and event.object.text and event.from_chat:
            if thread_Conv:
                if thread_Conv.isAlive() is False:
                    # Stop the thread when the thread work finish.
                    thread_Conv.join()
            # Make Thread
            thread_Conv = Thread(target=thread_for_conversation, args=(event, command_centre_m))
            # Start thread
            thread_Conv.start()

        # Check for message from user.
        if event.type == VkBotEventType.MESSAGE_NEW and event.object.text and event.from_user:
            if thread_UChat:
                if thread_UChat.isAlive() is False:
                    # Stop the thread when the thread work finish.
                    thread_UChat.join()
            # Make Thread
            thread_UChat = Thread(target=thread_for_user_chat, args=(event, command_centre_m))
            # Start thread
            thread_UChat.start()



if __name__ == "__main__":
    # Change this if you want to change the path to config.json!
    path_to_config_file = 'config/config.json'
    # Run script
    longpoll, command_center, config, utils_text = init(path_to_config_file)
    main(longpoll, command_center, config, utils_text)
