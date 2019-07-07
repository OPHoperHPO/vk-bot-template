# Utils file for bot.
# Module version: 0.5
# Writen by Anodev.

import json
import re
import lib.functions as functions


class Config(object):
    def __init__(self, path_config_file):
        """Read config.json and return params"""
        with open(path_config_file, "r") as read_file:
            self.data = json.load(read_file)

    def get_all_config_block(self, block):
        """Get all config parameters in this block"""
        all_configs = self.data[str(block)]
        return all_configs

    def get_config_var(self, block, var):
        """Get vars from config"""
        var = self.data[str(block)][str(var)]
        return var


class Text(object):
    def __init__(self, config):
        """Read texts_id.json and return text"""
        self.texts_folder = config.get_config_var('Bot Settings', 'texts_folder')
        with open('texts/texts_id.json', "r") as read_file:
            self.texts_id = json.load(read_file)

    def get_all_files_block(self, block):
        """Get all files in this block"""
        all_t_id = self.texts_id[str(block)]
        return all_t_id

    def get_filename(self, block, var):
        """Get single filename"""
        single_t_id = self.texts_id[str(block)][str(var)]
        return single_t_id

    def get_text(self, block, id):
        """Gets text from text file"""
        filename = self.texts_id[str(block)][str(id)]
        match = re.search('.txt$', filename)
        if match:
            with open(str(self.texts_folder) + filename) as f:
                text = f.read()
            return text
        else:
            return filename


class CommandCentre(object):
    def __init__(self, config, text_obj, vk_session):
        """Calls specific function if commands matches."""
        # Init all commands files
        commands_files = text_obj.get_all_files_block('Commands')
        texts_folder = text_obj.texts_folder

        # Init auth vars
        accessed_functions_folder = config.get_config_var('Bot Settings', 'accessed_functions')
        accessed_functions_files = config.get_all_config_block('Accessed Functions')

        # Make dictionary with function id and list of synonyms
        for function_id in commands_files:
            with open(texts_folder + commands_files[function_id]) as f:
                commands_files[function_id] = f.read().split('\n')

        # Make dictionary with access_level and list of accessed_functions
        for access_level in accessed_functions_files:
            with open(accessed_functions_folder + accessed_functions_files[access_level]) as f:
                accessed_functions_files[access_level] = f.read().split('\n')

        # Init objects vars
        self.commands_text = commands_files
        self.bot_functions_obj = functions.BotFunctions(config, text_obj, vk_session)

        # Get settings from config and init auth
        self.accessed_functions_text = accessed_functions_files
        self.access_levels = config.get_all_config_block('Access Levels')

        # Clean all temp vars
        del commands_files, texts_folder, accessed_functions_files, accessed_functions_folder

    def run_function(self, message_object):
        """Runs bot function"""
        # Get message text from message object.
        message_text = message_object.text
        # Get list of all functions with their commands
        for function_id in self.commands_text:
            function_commands = self.commands_text[function_id]
            # Check for command match
            activation_word, result = self.command_match(function_commands, message_text)
            if result:
                # Call our function
                self.call_function(function_id, activation_word, message_object)
                # Function was running.
                return True
        # Function wasn't running.
        return False

    def check_access_level(self, function_id, from_id):
        """Checks user access level."""
        # Check auth level for from_id.
        for auth_level in self.access_levels:
            list_of_ids = self.access_levels[auth_level]
            if from_id in list_of_ids:
                # Checks access level for this user.
                if auth_level == 'bot_creator':
                    # If auth control passed return requested function id.
                    if function_id in self.accessed_functions_text[auth_level]:
                        return function_id, True
                    else:
                        return 'auth_not_passed', False
                if auth_level == 'high':
                    # If auth control passed return requested function id.
                    if function_id in self.accessed_functions_text[auth_level]:
                        return function_id, True
                    else:
                        return 'auth_not_passed', False
                if auth_level == 'middle':
                    # If auth control passed return requested function id.
                    if function_id in self.accessed_functions_text[auth_level]:
                        return function_id, True
                    else:
                        return 'auth_not_passed', False
        # USUAL ACCESS LEVEL
        # If auth control passed return requested function id.
        if function_id in self.accessed_functions_text['usual']:
            return function_id, True
        return 'auth_not_passed', False

    def call_function(self, function_id, activation_word, message_object):
        """Calls real function if exist."""
        # Get values from message objects
        from_id = message_object.from_id
        chat_id = message_object.peer_id
        message_text = message_object.text
        # Check user access level to bot functions.
        function_id, result = self.check_access_level(function_id, from_id)
        # If all is OK continue
        if result:
            # Check for function id and associated real function id!
            # Add these new functions!

            if function_id == 'send_help_message':
                # Call send_help_message
                self.bot_functions_obj.Help.run(chat_id)

            elif function_id == 'send_user_message':
                # Call send_user_message
                self.bot_functions_obj.SendUserMessage.run(chat_id, message_text, activation_word)

            elif function_id == 'search_info_in_search_engine':
                # Call search_info_in_search_engine
                self.bot_functions_obj.SearchSomethingInSearchEngine.run(chat_id, message_text, activation_word)
            else:
                # Logging Error
                print("Command Centre module [Call Function Error]: The requested function does not exist! ",
                      "Details: id: ", from_id, "; ", "chat_id: ", chat_id, "; ", "message: ", message_text, ";")
        else:
            # Auth not passed
            pass

    def command_match(self, list_of_synonyms, message):
        """Checks for match command."""
        # Init exception var.
        is_exception = False
        for i in list_of_synonyms:
            # Check for exception commands.
            if i == '_exception_':
                is_exception = True
            # _exception_ isn't command!
            if i != '_exception_':
                if is_exception:
                    pattern = '(?i)^' + str(i)
                else:
                    pattern = '(?i)^' + str(i) + " "
                match = re.match(pattern, message)
                if match:
                    # Match found
                    return i, True
        # Match not found
        return i, False


if __name__ == "__main__":
    # Change for tests module
    _TEST_ = False

    if _TEST_:
        # Init list
        tests_result_c = list()
        tests_result_t = list()
        tests_result_Comm = list()

        # Test config object
        config = Config('config/config.json')
        test = config.get_config_var('Auth', 'group_id')

        tests_result_c.append(test)

        print(tests_result_c)

        # Test text object
        text = Text(config)
        test = text.get_filename('Common Errors', 'empty_message_error')
        test2 = text.get_all_files_block('Common Errors')
        test3 = text.get_text('Common Errors', 'empty_message_error')
        test4 = text.get_text('Main', 'help_message')

        tests_result_t.append(test)
        tests_result_t.append(test2)
        tests_result_t.append(test3)
        tests_result_t.append(test4)

        print(tests_result_t)
