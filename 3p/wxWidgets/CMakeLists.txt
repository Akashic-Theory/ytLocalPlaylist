find_package(wxWidgets QUIET)

if (wxWidgets_FOUND)
    set(YTLP-USE_BUNDLED_WX OFF CACHE BOOL "Use bundled wxWidgets")
else()
    set(YTLP-USE_BUNDLED_WX ON CACHE BOOL "Use bundled wxWidgets")
endif ()

if (YTLP-USE_BUNDLED_WX)
    include(FetchContent)
    set(FETCHCONTENT_QUIET OFF)
    FetchContent_Declare(
        wxWidgets
        GIT_REPOSITORY  https://github.com/wxWidgets/wxWidgets
        GIT_TAG         v3.1.5
        GIT_PROGRESS    TRUE
        GIT_SHALLOW     TRUE
    )
    FetchContent_MakeAvailable(wxWidgets)
    add_library(wxWidgets INTERFACE)
else()
    include(${wxWidgets_USE_FILE})
    find_package(wxWidgets REQUIRED)
endif ()
