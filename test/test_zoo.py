# Copyright (c) 2023 Boston Dynamics AI Institute, Inc.  All rights reserved.
import random

from example_py_multiple_dispatch.zoo import BD_SE3Pose, ROS_Pose, ROS_Transform, SpatialMath_SE3, convert
from plum import Val  # type: ignore
import plum

# https://github.com/beartype/plum/issues/86#issuecomment-1607741292
Val.__faithful__ = True
plum.clear_all_cache()

def test_1() -> None:
    # ultimately, we'd like to avoid the use of `Val here`
    # See https://github.com/beartype/plum/issues/85
    x = convert(Val(BD_SE3Pose), ROS_Pose("args"))
    assert isinstance(x, BD_SE3Pose)
    assert x.data4 == "args"


def workload_multiple_dispatch(work_amount: int = 50_000) -> int:
    use_the_result = 0
    random.seed(1234)
    for i in range(work_amount):
        from_ = random.choice([ROS_Transform("args1"), SpatialMath_SE3("args22")])
        to = convert(Val(ROS_Pose), from_)
        use_the_result += len(to.data1)
    return use_the_result


def convert_to_ros_pose_traditional(from_: ROS_Transform | SpatialMath_SE3) -> ROS_Pose:
    if isinstance(from_, ROS_Transform):
        to = ROS_Pose(from_.data2)
    elif isinstance(from_, SpatialMath_SE3):
        to = ROS_Pose(from_.data5)
    return to


def workload_elif_chain(work_amount: int = 50_000) -> int:
    use_the_result = 0
    random.seed(1234)
    for i in range(work_amount):
        from_ = random.choice([ROS_Transform("args1"), SpatialMath_SE3("args22")])
        to = convert_to_ros_pose_traditional(from_)
        use_the_result += len(to.data1)
    return use_the_result


def test_workload_functional_equivalence() -> None:
    assert workload_multiple_dispatch() == workload_elif_chain()


def test_perf_multiple_dispatch() -> None:
    assert workload_multiple_dispatch() > 0


def test_perf_elif_chain() -> None:
    assert workload_elif_chain() > 0
