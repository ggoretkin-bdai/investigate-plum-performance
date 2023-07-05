from typing import Any, Type

from plum import Val, dispatch, conversion_method  # type: ignore
import plum

# Val is kind of like `typing.Literal`, but not literally equivalent
# See https://github.com/beartype/plum/issues/85
# from typing import Literal

# Make mock representative types that may be used in a robotics code base
# Notes about this example:
# - it is trivial to extend any of these classes with methods, because they are all defined here.
# - it is trivial to make all of the fields `data`, with the same semantics

# In the real world, we do not define these types.
# The OOP-traditional way to add new functionality to existing types is to use subclassing and implementation
# inheritance.
# This makes the zoo worse. Now you have "MyRosPose", etc.
# We give each class different fieldnames to make it clear that the functionality of each method is different.

# Onward to the mock types


# Some types exist for the purposes of serialization and communication, like these ROS and ProtoBuf types
# `geometry_msgs.msg.Pose`
class ROS_Pose:
    def __init__(self, data: Any) -> None:
        self.data1 = data


# `geometry_msgs.msg.Transform`
class ROS_Transform:
    def __init__(self, data: Any) -> None:
        self.data2 = data


# `geometry_pb2.SE3Pose`
class BD_ProtoBuf_SE3Pose:
    def __init__(self, data: Any) -> None:
        self.data3 = data


# Other types exists for purposes of computation, like these `bosdyn` and `spatialmath` types
# `bosdyn.client.math_helpers.SE3Pose`
class BD_SE3Pose:
    def __init__(self, data: Any) -> None:
        self.data4 = data


# `spatialmath.SE3`
class SpatialMath_SE3:
    def __init__(self, data: Any) -> None:
        self.data5 = data

def conversion_method_from_signature(f):
    """Decorator to add a conversion method to convert an object from one
    type to another.

    Like `plum.conversion_method` but the arguments:
        type_from (type): Type to convert from.
        type_to (type): Type to convert to.
    are extracted from the type annotations
    """
    signature = plum.extract_signature(f)
    [type_from] = signature.types
    type_to = signature.return_type
    plum.promotion.add_conversion_method(type_from, type_to, f)
    # do not return anything, because we do not want to define a function (e.g. `convert_whatever`)


# `convert_whatever` is an arbitrary, inconsequential name.

# functionality of def _ros_pose_to_se3_pose(pose: Pose) -> SE3Pose:
@conversion_method_from_signature # type: ignore[no-redef]
def convert_whatever(from_: ROS_Pose) -> BD_SE3Pose: # noqa: F811
    return BD_SE3Pose(from_.data1)


# functionality of def se3pose_to_bd_se3pose(transform: SE3Pose) -> BD_SE3Pose:
@conversion_method_from_signature # type: ignore[no-redef]
def convert_whatever(from_: SpatialMath_SE3) -> BD_SE3Pose: # noqa: F811
    return BD_SE3Pose(from_.data5)


# functionality of def to_ros_pose(pose: Transform | SE3Pose) -> Pose:
# notice the absence of `if isinstance(pose, Pose)` elif chain (switch/case statement).
@conversion_method_from_signature # type: ignore[no-redef]
def convert_whatever(from_: ROS_Transform) -> ROS_Pose: # noqa: F811
    return ROS_Pose(from_.data2)


@conversion_method_from_signature # type: ignore[no-redef]
def convert_whatever(from_: SpatialMath_SE3) -> ROS_Pose: # noqa: F811
    return ROS_Pose(from_.data5)

# at this point, `convert_whatever` is None, because the decorator does not return anything.

# ---- 
# try recommendation from https://github.com/beartype/plum/issues/85#issuecomment-1615339947
# note this is NOT `plum.convert`

@dispatch # type: ignore[no-redef]
def convert(from_ : ROS_Pose, to : Type[BD_SE3Pose]) -> BD_SE3Pose: # noqa: F811
    return BD_SE3Pose(from_.data1)

@dispatch # type: ignore[no-redef]
def convert(from_: SpatialMath_SE3, to : Type[BD_SE3Pose]) -> BD_SE3Pose: # noqa: F811
    return BD_SE3Pose(from_.data5)

@dispatch # type: ignore[no-redef]
def convert(from_: ROS_Transform, to : Type[ROS_Pose]) -> ROS_Pose: # noqa: F811
    return ROS_Pose(from_.data2)

@dispatch # type: ignore[no-redef]
def convert(from_: SpatialMath_SE3, to : Type[ROS_Pose]) -> ROS_Pose: # noqa: F811
    return ROS_Pose(from_.data5)
