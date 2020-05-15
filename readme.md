# Task-Graph

Build a dynamic task graph for your project with Task-Graph!

## Introduction 

When facing a complex task, it's often necessary to recalculate the entire task when user wants to get one of the intermediate results, or to adjust one of the parameters or methods, but once you have Task-Graph,

1. If you need to get a result, Task-Graph will only compute all the upstream tasks of the result, and each task will cache  for later use.

2. If one of the task's parameters or method is adjusted, Task-Graph will automatically check all the downstream tasks and clear their cached results.

**In short, Task-Graph will make the computer lazy and just fulfill your needs without doing repetitive tasks, no more or less.**

## Usage

No doc available now, here is an minimal example.

```python
# import
from task_graph import TaskGraph

# init a TaskGraph
tg = TaskGraph()

# user task methods
def add(a, b):
    print("add", a, b)
    return a + b


def sub(a, b):
    print("sub", a, b)
    return a - b

# describe the task graph(much like dask.delayed)
ret1 = tg.add_task(add)(1, 2)
ret2 = tg.add_task(add)(3, ret1)
ret3 = tg.add_task(add)(4, ret2)
ret4 = tg.add_task(sub)(ret2, ret3)
final = tg.add_task('to_list')(ret1, ret2, ret3, ret4)

# trigger the computation and print
print(final.compute())

# when I want to update a task
tg.update_task(ret3)(add)(5, ret2)

# Because ret3 is change, rest3, rest4 and final will be recalculated
print(final.compute())

```

Or, a lazy way:

```python
from task_graph import TaskGraph


tg = TaskGraph()

def add(a, b):
    print("add", a, b)
    return a + b


def sub(a, b):
    print("sub", a, b)
    return a - b

# omit add_task
ret1 = tg(add)(1, 2)
ret2 = tg(add)(3, ret1)
ret3 = tg(add)(4, ret2)
ret4 = tg(sub)(ret2, ret3)
final = tg('to_list')(ret1, ret2, ret3, ret4)

# auto compute and print
final.print()

# omit update_task
tg(ret3)(add)(5, ret2)

# auto compute and print
final.print()


```
## TODO
Task-Graph is at the very beginning, so many todos in the codes. Here are a few general ones:

- [ ] add parallel scheduler
- [ ] add decorator that can auto transfer function to task
- [ ] add graphviz-based visualization
- [ ] add unit test
- [ ] add doc
- [ ] add examples


## Pattern: Task Graph

The main task of many python projects can be considered as a static collection of atomic tasks with dependencies between input and output, which can be thought of as forming the vertices of a directed acyclic graph, while the directed edges of the graph show the dependencies between tasks.

We can solve the problems with the following techniques:

 - **Up-Propagate**: If some data item is accessed, we need to do the up-propagate and find all upstream tasks and do the correspond tasks. The result of an upstream task may be passed to downstream tasks on completion of the upstream. Data does not stream to downstream task during execution, the upstream task completes its work, terminates, and then its result is passed to the downstream task. The final result of the graph is returned when the last downstream task(s) complete.
 - **Cache**: when a task been computed once(Usually triggered by Up-Propagate), it will automatically cache the result.
 - **Down-Propagate** : If one task is changed, we need to do the down-propagate and find all downstream tasks and clear the correspond task caches. The result of an upstream task is much likely to have effect on all of its’ downstream tasks, so the recomputation is necessary. But Down-Propagate will not trigger the recomputation but only clear the result caches, recomputation will happened when this task has been ‘Up-Propagated’ or accessed.

## Zen

**I am lazy, so I build this to let computer be also lazy.**

One of the biggest differences in Python from other languages is that the methods (like all other objects) are mutable, Task-Graph is designed to accommodate that.

Task-Graph was designed to speed up python project, and want to make it the simplest solution to avoid any recalculation.

I have referred to the Dask.delayed API in many places. The difference between Task-Graph and Dask is to try to adapt to the dynamics of the python and python projects, and **make computer not only delayed but also lazy**.

See more information in [Loopy-tech-blog](https://blog.loopy.tech/2020/05/14/task-graph/)






