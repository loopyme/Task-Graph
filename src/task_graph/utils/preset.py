def preset_method(method_name: str) -> callable:
    """
    some special methods are preset

    :param method_name:
    :return: method
    """
    dispatcher = {
        "to_list": lambda *args: list(args),
        "to_tuple": lambda *args: tuple(args),
        "to_set": lambda *args: set(args),
        "__getitem__": lambda obj, index: obj[index],
    }
    if method_name in dispatcher.keys():
        return dispatcher[method_name]
    else:
        raise NotImplementedError(f"'{method_name}' is not a preset task method")
