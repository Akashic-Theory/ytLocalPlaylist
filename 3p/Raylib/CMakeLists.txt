if (NOT DEFINED YTLP-USE_BUNDLED_RAYLIB)
    find_package(raylib 4 QUIET)
    option(YTLP-USE_BUNDLED_RAYLIB "Use bundled Raylib" OFF)
    if (NOT raylib_FOUND)
        set(3P-EXIT "${3P-EXIT}\n- Raylib" CACHE INTERNAL "")
        set(YTLP-USE_BUNDLED_RAYLIB ON CACHE BOOL "Use bundled Raylib" FORCE)
        return()
    endif ()
endif ()

if (YTLP-USE_BUNDLED_RAYLIB)
    include(FetchContent)
    set(FETCHCONTENT_QUIET OFF)
    FetchContent_Declare(
            raylib
            GIT_REPOSITORY https://github.com/raysan5/raylib.git
            GIT_TAG        4.0.0
    )
    FetchContent_MakeAvailable(raylib)
endif ()
