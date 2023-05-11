from array import Array
from key_val import KeyVal
from inline_table import InlineTable
from table import Table
from table_array import TableArray
from key import Key
from value import Value


class TranslatorUnit:
    @classmethod
    def translate(cls, list_):
        """
        Translate a list of nodes resulting from parsing
        :param list_: list of nodes
        """
        pass

    @classmethod
    def key_val(cls, key_val: KeyVal):
        """
        Process a key-value pair
        :param key_val: KeyVal object that contains a list of keys and a value
        """
        pass

    @classmethod
    def key(cls, key: Key):
        """
        Process a key
        :param key: object that contains a key with its type and value
        """
        pass

    @classmethod
    def array(cls, array: Array):
        """
        Process an array
        :param array: object that contains an array with its values
        """
        pass

    @classmethod
    def inline_table(cls, inline_table: InlineTable):
        """
        Process an inline table
        :param inline_table: object that contains an inline table
        """
        pass

    @classmethod
    def table(cls, table: Table):
        """
        Process a table
        :param table: object that contains a table with its keys
        """
        pass

    @classmethod
    def table_array(cls, table_array: TableArray):
        """
        Process a table array
        :param table_array: object that contains a table array with its keys
        """
        pass

    @classmethod
    def value(cls, value: Value):
        """
        Process a value
        :param value: object that contains a value with its type and value
        """
        pass

    @classmethod
    def get_result(cls):
        """
        Get the result of the translation
        """
        pass
