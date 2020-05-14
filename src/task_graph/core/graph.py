from typing import Union

from task_graph.core.node import TaskNode
from task_graph.core.result import TaskResult
from task_graph.utils.preset import preset_method


class TaskGraph:
    def __init__(self):
        """
        Init a task graph
        """

        # All of the task nodes
        self.tasks: list[TaskNode] = []

        # some buffers to help perform function-multiple-calls
        self._method_buffer: Union[callable, None] = None
        self._update_task_id_buffer: Union[int, None] = None

    @property
    def method_buffer(self) -> callable:
        """
        return _method_buffer and set it to None
        :return: _method_buffer
        """
        res = self._method_buffer
        self._method_buffer = None
        return res

    @method_buffer.setter
    def method_buffer(self, method: callable):
        """
        set _method_buffer and raise an error when it's not None before
        :param method:
        :return: None
        """
        if self._method_buffer is not None:
            raise AttributeError(
                "method_buffer was set without access, this is probably due to "
                "the wrong way to call the function."
            )
        self._method_buffer = method

    @property
    def update_task_id_buffer(self) -> int:
        """
        return _update_task_id_buffer and set it to None
        :return: _update_task_id_buffer
        """
        res = self._update_task_id_buffer
        self._update_task_id_buffer = None
        return res

    @update_task_id_buffer.setter
    def update_task_id_buffer(self, update_task_id: int):
        """
        set _update_task_id_buffer and raise an error when it's not None before
        :param update_task_id:
        :return: None
        """
        if self._update_task_id_buffer is not None:
            raise AttributeError(
                "update_task_id_buffer was set without access, this is probably due to "
                "the wrong way to call the function."
            )
        self._update_task_id_buffer = update_task_id

    def get_task_by_id(self, task_id: int) -> TaskNode:
        """
        api for TaskNode and TaskResult to get other tasks

        :note: pass to TaskNode and TaskResult in their init function
        :param task_id:
        :return: task with than given id
        """
        return self.tasks[task_id]

    def add_task(self, method: Union[callable, str]) -> callable:
        """
        add a task

        :note: use like this:`res = add_task(method)(args)`
        :param method: the function that the task executes
        :return: inner function _add_task1, to allow function-multiple-calls
        """
        if isinstance(method, str):
            method = preset_method(method)
        self.method_buffer = method
        return self._add_task1

    def _add_task1(self, *args, **kwargs) -> callable:
        """
        inner function of add_task

        :param args:
        :param kwargs:
        :return: a TaskResult(A hyperlink with task id)
        """
        id = self.update_task_id_buffer
        if id is None:
            id = len(self.tasks)
            self.tasks.append(
                TaskNode(id, self.get_task_by_id, self.method_buffer, args, kwargs)
            )
        else:
            self.tasks[id] = TaskNode(
                id, self.get_task_by_id, self.method_buffer, args, kwargs
            )
        return TaskResult(id, self.get_task_by_id)

    def update_task(self, task_result: TaskResult) -> callable:
        """
        update a task

        :note: use like this:`update_task(task_result)(method)(args)`
        :param task_result: The result user assigned before
        :return: inner function _add_task1, to allow function-multiple-calls
        """
        self.update_task_id_buffer = task_result.id

        self.get_task_by_id(task_result.id).clear()
        # TODO: check task dependence loop
        return self.add_task

    def add_task_node(self, task: TaskNode):
        """
        direct add a TaskNode into a graph

        :param task: TaskNode
        :return: a TaskResult(A hyperlink with task id)
        """
        task.id = len(self.tasks)
        self.tasks.append(task)
        return TaskResult(task.id, self.get_task_by_id)

    def __call__(self, arg):
        if isinstance(arg, TaskResult):
            return self.update_task(arg)
        else:
            return self.add_task(arg)
