import json
from translator_tomml import TranslatorUnit
from array import Array
from key_val import KeyVal
from inline_table import InlineTable
from table import Table
from table_array import TableArray
from key import Key
from value import Value


def get_dict(key_list, dict):
    """
    Returns the dictionary at the end of the key_list
    Initializes the dictionary if it doesn't exist along the way
    :param key_list: list of keys
    :param dict: dictionary to start from
    :return: dictionary at the end of the key_list
    """
    current_dict = dict
    for key in key_list:
        if key not in current_dict:
            current_dict[key] = {}
        current_dict = current_dict[key]
    return current_dict


def get_dict_as_array(dict):
    """
    Returns the dictionary's values as an array
    :param dict: dictionary to convert
    :return: modified dictionary
    """
    for key, value in dict.items():
        dict[key] = [v for v in value]


def escape_newlines(ml_string):
    chunks = ml_string.split('\n')
    if len(chunks) > 1:
        return ''.join([chunk + '\n' for chunk in chunks])
    return ml_string


class JSONTranslator(TranslatorUnit):
    def __init__(self):
        super().__init__()

        self.tables = {}
        self.current_dict = self.tables

        self.table_arrays = {}
        self.current_table_array = self.table_arrays
        self.current_array = None

        self.array = False

    def translate(self, list_):
        for node in list_:
            if isinstance(node, KeyVal):
                self.key_val(node)
            elif isinstance(node, Table):
                self.table(node)
            elif isinstance(node, TableArray):
                self.table_array(node)

    def key_val(self, key_val: KeyVal):
        """
        Adds a key-value pair to the current dictionary
        :param key_val: KeyVal object that contains a list of keys and a value
        """
        translated_keys = [self.translate_key(key) for key in key_val.key_list]
        translated_value = self.translate_value(key_val.value)
        last_key = translated_keys[-1]
        key_path = translated_keys[:-1]

        current_dict = get_dict(key_path, self.current_dict)
        current_dict[last_key] = translated_value

    def table(self, table: Table):
        translated_keys = [self.translate_key(key) for key in table.key_list]
        self.current_dict = get_dict(translated_keys, self.tables)
        self.array = False

    def translate_key(self, key: Key):
        return self.translate_value(key.value)

    def translate_value(self, value: Value):
        if value.type == 'boolean':
            return True if value.value == 'true' else False
        elif value.type == 'integer':
            return int(value.value, 0)
        elif value.type == 'float':
            return float(value.value)
        elif value.type == 'array':
            return self.translate_array(value.value)
        elif value.type == 'ml_string':
            return escape_newlines(value.value)
        elif value.type == 'inline_table':
            return self.inline_table(value.value)
        else:
            return value.value

    def translate_array(self, array: Array):
        return [self.translate_value(value) for value in array.value_list]

    def inline_table(self, table: InlineTable):
        # save current dict
        old_dict = self.current_dict
        # set current dict to empty
        self.current_dict = {}

        # translate inline table into current dict
        self.translate(table.expression_list)

        # save inline table
        inline = self.current_dict
        # restore old dict
        self.current_dict = old_dict

        return inline

    def table_array(self, table_array: TableArray):
        translated_keys = [self.translate_key(key) for key in table_array.key_list]
        self.current_table_array = get_dict(translated_keys[:-1], self.table_arrays)

        if translated_keys[-1] not in self.current_table_array:
            self.current_table_array[translated_keys[-1]] = []
        self.current_dict = {}
        self.current_array = self.current_table_array[translated_keys[-1]]
        self.current_array.append(self.current_dict)
        self.array = True

    def get_result(self):
        # get_dict_as_array(self.table_arrays)
        return json.dumps({**self.tables, **self.table_arrays}, indent=4, ensure_ascii=False)
