import traceback

from task_graph.core.result import TaskResult
from task_graph.utils.error import TaskRuntimeError


class TaskNode:
    def __init__(
            self,
            node_id: int,
            get_task_by_id: callable,
        func: callable,
        args: tuple,
        kwargs: dict,
    ):
        """
        Init a task node

        :param func:  The function that the task executes
        :param args:  The args pass to the function (may contains TaskResult)
        :param kwargs: The kwargs pass to the function (may contains TaskResult in values)
        """

        # api to get other tasks from graph
        self.get_task_by_id = get_task_by_id

        # store self.result unless upstream task is changed
        self.cache = None

        # always get task from TaskGraph with id, each TaskNode must belong to a TaskGraph
        self.id: int = node_id

        # the downstream tasks which depend on us
        self.downstream: list[int] = []

        # the function that the task executes
        self.method: callable = func

        # the args & kwargs pass to the function (may contains TaskResult)
        self.args: tuple = args
        self.kwargs: dict = kwargs

        # analyse the args and kwargs to find all upstream tasks, add self id to the upstream tasks
        self.analyse_upstream()

    def analyse_upstream(self):
        """
        Analyse the args and kwargs to find all upstream tasks, add self id to the upstream tasks

        :return: None
        """
        # analyse the upstream tasks
        upstream = [arg.id for arg in self.args if isinstance(arg, TaskResult)] + [
            arg.id for k, arg in self.kwargs if isinstance(arg, TaskResult)
        ]

        # save self id to upstream tasks
        for task_id in upstream:
            self.get_task_by_id(task_id).add_downstream(self.id)

    def add_downstream(self, downstream_task_id):
        """
        Let the downstream tasks add their id in self. downstream

        :param downstream_task_id:  the id of downstream tasks
        :return: None
        """
        self.downstream.append(downstream_task_id)

    def up_propagate(self) -> (tuple, dict):
        """
        Require upstream tasks to perform calculations

        :note: 'arg.compute()' triggers the propagation of the next layer
        :return: the args and kwargs (without TaskResult) for self function
        """
        args = tuple(
            arg.compute() if isinstance(arg, TaskResult) else arg for arg in self.args
        )
        kwargs = {
            key: (arg.compute() if isinstance(arg, TaskResult) else arg)
            for key, arg in self.kwargs
        }
        return args, kwargs

    def down_propagate(self):
        """
        Require downstream tasks to empty their cache

        :note: 'task.clear()' triggers the propagation of the next layer
        :return: None
        """
        for task_id in self.downstream:
            self.get_task_by_id(task_id).clear()

    def compute(self) -> any:
        """
        Do the computation

        return self.cache if result have been cached

        :return: actually task result
        """
        if self.cache is not None:
            return self.cache
        else:
            args, kwargs = self.up_propagate()
            try:
                res = self.method(*args, *kwargs)
            except Exception as _:
                raise TaskRuntimeError(
                    self.method.__name__, args, kwargs, traceback.format_exc()
                )
            self.cache = res
            return res

    def clear(self):
        """
        Empty self cache and do down_propagate

        :note: this usually happened when upstream task is changed or self is changed
        :return: None
        """
        self.cache = None
        self.down_propagate()

    def print(self):
        """
        print the result of self task
        :return: None
        """
        print(self.compute())
