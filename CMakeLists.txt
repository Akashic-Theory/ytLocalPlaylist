cmake_minimum_required(VERSION 3.21)
project(ytlp)
set(CMAKE_CXX_STANDARD 17)

set_property(DIRECTORY PROPERTY EP_BASE ${CMAKE_BINARY_DIR}/subprojects)
set(YTLP_STAGING_PREFIX ${CMAKE_BINARY_DIR}/staging CACHE PATH "Path to staging area for dependencies")

set(YTLP-BUILD_TESTS OFF CACHE BOOL "Build tests")

add_subdirectory(3p)
add_subdirectory(src)

if (YTLP-BUILD_TESTS)
    add_subdirectory(tests)
endif ()

