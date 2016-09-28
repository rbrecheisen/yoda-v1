SUPPORTED_TYPE_NAMES = [
    'bool', 'bool_list', 'bool_tuple', 'bool_set', 'int', 'int_list', 'int_tuple', 'int_set',
    'long', 'long_list', 'long_tuple', 'long_set', 'complex', 'complex_list', 'complex_tuple', 'complex_set',
    'float', 'float_list', 'float_tuple', 'float_set', 'str', 'str_list', 'str_tuple', 'str_set',
    'unicode', 'unicode_list', 'unicode_tuple', 'unicode_set',
]


def to_str(value, sep=','):
    if isinstance(value, bool) or isinstance(value, float):
        return str(value)
    if isinstance(value, int) or isinstance(value, long) or isinstance(value, complex):
        return str(value)
    if isinstance(value, str) or isinstance(value, unicode):
        return str(value)
    if isinstance(value, list) or isinstance(value, tuple) or isinstance(value, set):
        return sep.join([str(x) for x in value])
    return None


def to_unicode(value, sep=','):
    return unicode(to_str(value, sep))


def to_value(type_name, str_value, sep=','):
    if type_name not in SUPPORTED_TYPE_NAMES:
        return None

    if type_name == 'bool':
        return bool(str_value)
    if type_name == 'bool_list':
        return to_bool_list(str_value, sep)
    if type_name == 'bool_tuple':
        return tuple(to_bool_list(str_value, sep))
    if type_name == 'bool_set':
        return set(to_bool_list(str_value, sep))

    if type_name == 'int':
        return int(str_value)
    if type_name == 'int_list':
        return to_int_list(str_value, sep)
    if type_name == 'int_tuple':
        return tuple(to_int_list(str_value, sep))
    if type_name == 'int_set':
        return set(to_int_list(str_value, sep))

    if type_name == 'long':
        return long(str_value)
    if type_name == 'long_list':
        return to_long_list(str_value, sep)
    if type_name == 'long_tuple':
        return tuple(to_long_list(str_value, sep))
    if type_name == 'long_set':
        return set(to_long_list(str_value, sep))

    if type_name == 'complex':
        return complex(str_value)
    if type_name == 'complex_list':
        return to_complex_list(str_value, sep)
    if type_name == 'complex_tuple':
        return tuple(to_complex_list(str_value, sep))
    if type_name == 'complex_set':
        return set(to_complex_list(str_value, sep))

    if type_name == 'float':
        return float(str_value)
    if type_name == 'float_list':
        return to_float_list(str_value, sep)
    if type_name == 'float_tuple':
        return tuple(to_float_list(str_value, sep))
    if type_name == 'float_set':
        return set(to_float_list(str_value, sep))

    if type_name == 'str':
        return str(str_value)
    if type_name == 'str_list':
        return to_str_list(str_value, sep)
    if type_name == 'str_tuple':
        return tuple(to_str_list(str_value, sep))
    if type_name == 'str_set':
        return set(to_str_list(str_value, sep))

    if type_name == 'unicode':
        return unicode(str_value)
    if type_name == 'unicode_list':
        return to_unicode_list(str_value, sep)
    if type_name == 'unicode_tuple':
        return tuple(to_unicode_list(str_value, sep))
    if type_name == 'unicode_set':
        return set(to_unicode_list(str_value, sep))

    return None


def to_bool_list(str_value, sep=','):
    return [bool(x.strip()) for x in str_value.split(sep)]


def to_int_list(str_value, sep=','):
    return [int(x.strip()) for x in str_value.split(sep)]


def to_long_list(str_value, sep=','):
    return [long(x.strip()) for x in str_value.split(sep)]


def to_complex_list(str_value, sep=','):
    return [complex(x.strip()) for x in str_value.split(sep)]


def to_float_list(str_value, sep=','):
    return [float(x.strip()) for x in str_value.split(sep)]


def to_str_list(str_value, sep=','):
    return [str(x.strip()) for x in str_value.split(sep)]


def to_unicode_list(str_value, sep=','):
    return [unicode(x.strip()) for x in str_value.split(sep)]


def str_rep(item_type, list_type=None):
    if item_type is bool:
        if list_type is list:
            return 'bool_list'
        if list_type is tuple:
            return 'bool_tuple'
        if list_type is set:
            return 'bool_set'
        return 'bool'

    if item_type is int:
        if list_type is list:
            return 'int_list'
        if list_type is tuple:
            return 'int_tuple'
        if list_type is set:
            return 'int_set'
        return 'int'

    if item_type is long:
        if list_type is list:
            return 'long_list'
        if list_type is tuple:
            return 'long_tuple'
        if list_type is set:
            return 'long_set'
        return 'long'

    if item_type is complex:
        if list_type is list:
            return 'complex_list'
        if list_type is tuple:
            return 'complex_tuple'
        if list_type is set:
            return 'complex_set'
        return 'complex'

    if item_type is float:
        if list_type is list:
            return 'float_list'
        if list_type is tuple:
            return 'float_tuple'
        if list_type is set:
            return 'float_set'
        return 'float'

    if item_type is str:
        if list_type is list:
            return 'str_list'
        if list_type is tuple:
            return 'str_tuple'
        if list_type is set:
            return 'str_set'
        return 'str'

    if item_type is unicode:
        if list_type is list:
            return 'unicode_list'
        if list_type is tuple:
            return 'unicode_tuple'
        if list_type is set:
            return 'unicode_set'
        return 'unicode'

    if item_type is list:
        return 'list'

    if item_type is tuple:
        return 'tuple'

    if item_type is set:
        return 'set'

    return None
