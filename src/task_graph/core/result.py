class TaskResult:
    def __init__(self, result_id: int, get_task_by_id: callable):
        """
        init
        :param result_id: id to self task
        :param get_task_by_id: api to get other tasks from graph
        """

        self.id = result_id
        self.get_task_by_id = get_task_by_id

    def compute(self) -> any:
        """
        call correspond TaskNode to compute the actual result

        :return: any
        """
        return self.get_task_by_id(self.id).compute()

    def print(self):
        """
        print the result of self task
        :return: None
        """
        print(self.compute())
