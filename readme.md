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


## Zen

**I am lazy, so I build this to let computer be also lazy.**

One of the biggest differences in Python from other languages is that the methods (like all other objects) are mutable, Task-Graph is designed to accommodate that.

Task-Graph was designed to speed up python project, and want to make it the simplest solution to avoid any recalculation.

I have referred to the Dask.delayed API in many places. The difference between Task-Graph and Dask is to try to adapt to the dynamics of the python and python projects, and **make computer not only delayed but also lazy**.







