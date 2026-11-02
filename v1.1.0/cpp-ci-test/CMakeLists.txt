cmake_minimum_required(VERSION 3.10)
project(cpp-ci-test)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include directories
include_directories(include)

# Create a library from the sources
add_library(greeter src/greeter.cpp)
add_library(geometry src/geometry.c)

# Specify include directories for the targets
target_include_directories(greeter PUBLIC include)
target_include_directories(geometry PUBLIC include)