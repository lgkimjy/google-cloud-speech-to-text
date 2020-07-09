cmake_minimum_required(VERSION 2.8.3)
project(pino_msgs)

add_compile_options(-std=c++11)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  message_generation
)

add_message_files(
   FILES
   PinoAnswer.msg
   PinoInit.msg
)

generate_messages(
   DEPENDENCIES
   std_msgs
)

catkin_package(
#  INCLUDE_DIRS include
# LIBRARIES pino_msgs
  CATKIN_DEPENDS roscpp std_msgs message_runtime
# DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
