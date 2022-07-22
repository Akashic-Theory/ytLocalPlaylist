if (NOT DEFINED YTLP-USE_BUNDLED_RAYLIB_CPP)
    find_package(raylib_cpp QUIET)
    option(YTLP-USE_BUNDLED_RAYLIB_CPP "Use bundled Raylib-CPP" OFF)
    if (NOT raylib_cpp_FOUND)
        set(3P-EXIT "${3P-EXIT}\n- Raylib-CPP" CACHE INTERNAL "")
        set(YTLP-USE_BUNDLED_RAYLIB_CPP ON CACHE BOOL "Use bundled Raylib-CPP" FORCE)
        return()
    endif ()
endif ()

if (YTLP-USE_BUNDLED_RAYLIB_CPP)
    include(FetchContent)
    set(FETCHCONTENT_QUIET OFF)
    FetchContent_Declare(
            raylib_cpp
            GIT_REPOSITORY https://github.com/RobLoach/raylib-cpp.git
            GIT_TAG v4.2.3
    )
    FetchContent_MakeAvailable(raylib_cpp)
endif ()
