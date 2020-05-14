class TaskRuntimeError(Exception):
    def __init__(
            self, method_name: str, task_args: tuple, task_kwargs: dict, traceback_info: str
    ):
        self.method_name = method_name
        self.traceback_info = traceback_info
        self.parameters = [
                              str(arg) if not isinstance(arg, str) else f'"{arg}"' for arg in task_args
                          ] + [
                              f"{key}={arg}" if not isinstance(arg, str) else f'{key}="{arg}"'
                              for key, arg in task_kwargs
                          ]

    def __str__(self):
        # simulate function call
        parameter_string = ", ".join(self.parameters)
        call = f"\n{self.method_name}({parameter_string})\n"
        if len(call) > 79:
            # manual black it!
            call = (
                "\n{method_name}(\n"
                "    {parameters}\n"
                ")\n".format(
                    method_name=self.method_name,
                    parameters=", \n    ".join(self.parameters),
                )
            )

        div_line_len = max(
            [len(line) for line in call.split("\n") + self.traceback_info.split("\n")]
        )
        call = (
                "=" * div_line_len
                + call
                + "-" * div_line_len
                + "\n"
                + self.traceback_info
                + "=" * div_line_len
        )

        # main message
        message = (
                f"An error was raised when trying to do the task with method '{self.method_name}'\n"
                + f"{call}"
        )
        return message
