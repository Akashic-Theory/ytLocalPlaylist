if (NOT DEFINED YTLP-USE_BUNDLED_TINYPROCESS)
    find_package(tiny-process-library QUIET)
    option(YTLP-USE_BUNDLED_TINYPROCESS "Use bundled Tiny-Process-Library" OFF)
    if (NOT tiny-process-library_FOUND)
        set(3P-EXIT "${3P-EXIT}\n- Tiny-Process-Library" CACHE INTERNAL "")
        set(YTLP-USE_BUNDLED_TINYPROCESS ON CACHE BOOL "Use bundled Tiny-Process-Library" FORCE)
        return()
    endif ()
endif ()

if (YTLP-USE_BUNDLED_TINYPROCESS)
    include(FetchContent)
    set(FETCHCONTENT_QUIET OFF)
    FetchContent_Declare(
            tiny-process-library
            GIT_REPOSITORY https://gitlab.com/eidheim/tiny-process-library.git
            GIT_TAG v2.0.4
    )
    FetchContent_MakeAvailable(tiny-process-library)
else()
    find_package(tiny-process-library REQUIRED)
endif ()
