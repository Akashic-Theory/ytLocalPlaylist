find_package(Catch2 3.1 QUIET)

if (NOT DEFINED YTLP-USE_BUNDLED_CATCH)
    option(YTLP-USE_BUNDLED_CATCH "Use bundled Catch" OFF)
    if (NOT Catch2_FOUND)
        set(3P-EXIT "${3P-EXIT}\n- Catch" CACHE INTERNAL "")
        set(YTLP-USE_BUNDLED_CATCH ON CACHE BOOL "Use bundled Catch" FORCE)
        return()
    endif ()
endif ()

if (YTLP-USE_BUNDLED_CATCH)
    include(FetchContent)
    set(FETCHCONTENT_QUIET OFF)
    FetchContent_Declare(
        Catch2
        GIT_REPOSITORY https://github.com/catchorg/Catch2.git
        GIT_TAG        v3.1.0
    )
    FetchContent_MakeAvailable(Catch2)
    list(APPEND CMAKE_MODULE_PATH ${catch2_SOURCE_DIR}/extras)
else()
    find_package(Catch2 3.1 REQUIRED)
endif ()
