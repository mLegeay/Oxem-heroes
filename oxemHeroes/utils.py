def check_param_type(param_type, parameter):
    try:
        if param_type == "str":
            str(parameter)
        elif param_type == "int":
            int(parameter)
        return True

    except ValueError:
        return False
