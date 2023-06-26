# Examples of using multiple dispatch in python
This project provides a small example of using multiple dispatch in Python via the [plum](https://beartype.github.io/plum) library.

## Running tests
```sh
cd $REPO
virtualenv fooenv
source fooenv/bin/activate
pip install --editable .
pytest .
```

## Investigating performance
```
$ pytest --durations=10 .
=================================================================================== test session starts ====================================================================================
platform linux -- Python 3.10.6, pytest-7.3.2, pluggy-1.0.0
rootdir: /home/ggoretkin/repos/bdai/projects/example_py_multiple_dispatch
plugins: anyio-3.7.0, libtmux-0.21.1
collected 8 items                                                                                                                                                                          

test/test_foo.py .x..                                                                                                                                                                [ 50%]
test/test_zoo.py ....                                                                                                                                                                [100%]

=================================================================================== slowest 10 durations ===================================================================================
1.22s call     test/test_zoo.py::test_workload_functional_equivalence
1.15s call     test/test_zoo.py::test_perf_multiple_dispatch
0.03s call     test/test_zoo.py::test_perf_elif_chain

(7 durations < 0.005s hidden.  Use -vv to show these durations.)
=============================================================================== 7 passed, 1 xfailed in 2.45s ===============================================================================
```

## Investigating performance, continued

```bash
python -m cProfile -o mult-disp.prof ./test/profile_zoo.py
snakeviz mult-disp.prof
```

or

```bash
py-spy record -o profile.svg -- python  test/profile_zoo.py
```

reveal that plum's [`is_type`](https://github.com/beartype/plum/blob/b38a1625c30a235d4e7a20d8a5828280fdb0fba7/plum/parametric.py#L282) is the culprit.
It is being called with `plum.parametric.Val[example_py_multiple_dispatch.zoo.ROS_Pose]()` and always returns `false`.
See https://github.com/beartype/plum/issues/86
