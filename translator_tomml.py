from array import Array
from key_val import KeyVal
from inline_table import InlineTable
from table import Table
from table_array import TableArray
from key import Key
from value import Value


class TranslatorUnit:
    @classmethod
    def key_val(cls, key_val: KeyVal):
        pass

    @classmethod
    def key(cls, key: Key):
        pass

    @classmethod
    def array(cls, array: Array):
        pass

    @classmethod
    def inline_table(cls, inline_table: InlineTable):
        pass

    @classmethod
    def table(cls, table: Table):
        pass

    @classmethod
    def table_array(cls, table_array: TableArray):
        pass

    @classmethod
    def value(cls, value: Value):
        pass
