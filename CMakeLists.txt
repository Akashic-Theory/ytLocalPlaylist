cmake_minimum_required(VERSION 3.21)
project(ytlp)
set(CMAKE_CXX_STANDARD 17)

set(YTLP-BUILD_TESTS OFF CACHE BOOL "Build tests")

add_subdirectory(3p)
add_subdirectory(src)

if (YTLP-BUILD_TESTS)
    add_subdirectory(tests)
endif ()

