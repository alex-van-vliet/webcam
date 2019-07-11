# %Tag(FULLTEXT)%
cmake_minimum_required(VERSION 2.8.3)
project(webcamcpp)

## Find catkin and any catkin packages
find_package(catkin REQUIRED COMPONENTS roscpp rospy sensor_msgs std_msgs cv_bridge)
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_Include_DIRS})

## Declare a catkin package
catkin_package()

## Build talker and listener
include_directories(include ${catkin_INCLUDE_DIRS})

add_executable(webcamcpp src/main.cpp)
target_link_libraries(webcamcpp ${catkin_LIBRARIES} ${OpenCV_LIBRARIES})

# %EndTag(FULLTEXT)%
