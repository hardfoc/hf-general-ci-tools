# Self-test project for ru-host-ci.yml.
cmake_minimum_required(VERSION 3.21)
project(host_ci_fixture LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
enable_testing()

add_library(calc src/calc.cpp)
target_include_directories(calc PUBLIC include)

# Vendored code: compiled, but excluded from analysis by exclude_paths.
add_library(vendored third_party/vendored.cpp)

add_executable(calc_test test/calc_test.cpp)
target_link_libraries(calc_test PRIVATE calc)
add_test(NAME calc COMMAND calc_test)

# Seeded defects, so the self-test can check that findings are detected.
option(HOST_CI_SEED_FINDINGS "Build a source file with known findings" OFF)
if(HOST_CI_SEED_FINDINGS)
  add_library(seeded src/seeded.cpp)
  target_include_directories(seeded PUBLIC include)
endif()
