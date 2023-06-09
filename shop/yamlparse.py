import dataclasses
import typing


def is_parsable(data, obj_type):
    # If primitive
    if type(data) is not dict:
        return type(data) is obj_type
    # If dict
    fields = dataclasses.fields(obj_type)
    minimum = set(
        field.name
        for field in fields
        if field.default == dataclasses.MISSING
        and field.default_factory == dataclasses.MISSING
    )
    maximum = set(field.name for field in fields)
    data_names = set(data.keys())
    if not maximum.issuperset(data_names):
        raise Exception(
            f"Excess fields {data_names - maximum} for type {obj_type} in data {data}"
        )
    if not minimum.issubset(data_names):
        raise Exception(
            f"Missing fields {minimum - data_names} for type {obj_type} in data {data}"
        )
    return True


def is_parsable_list(data, list_type):
    if not type(data) is list:
        return False
    # Parse list
    return all(is_parsable(item, typing.get_args(list_type)[0]) for item in data)


def dict_zip(d1, d2):
    # Zip together values where keys match
    keys = set(d1).intersection(set(d2))
    return {k: (d1[k], d2[k]) for k in keys}


def parse_dict_to_dataclasses(data, obj_type):
    print("Parse", type(data), obj_type, type(data) is obj_type)

    if typing.get_origin(obj_type) is list:
        # Parse List
        if is_parsable_list(data, obj_type):
            child_type = typing.get_args(obj_type)[0]
            return [parse_dict_to_dataclasses(item, child_type) for item in data]
        raise Exception(f"List data `{data}` is unparsable to {obj_type}")
    else:
        if type(data) is not dict and type(data) is obj_type:
            # Parse 'primitive'
            return obj_type(data)
        if is_parsable(data, obj_type):
            # Parse class
            types = {field.name: field.type for field in dataclasses.fields(obj_type)}
            d_t = dict_zip(data, types)
            args = {k: parse_dict_to_dataclasses(d, t) for k, (d, t) in d_t.items()}
            return obj_type(**args)
    raise Exception(f"Data `{data}` is unparsable to {obj_type}")
