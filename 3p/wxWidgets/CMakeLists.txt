find_package(wxWidgets QUIET)

if (NOT DEFINED YTLP-USE_BUNDLED_WX)
    option(YTLP-USE_BUNDLED_WX "Use bundled wxWidgets" OFF)
    if (NOT wxWidgets_FOUND)
        set(3P-EXIT "${3P-EXIT}\n- WxWidgets" CACHE INTERNAL "")
        set(YTLP-USE_BUNDLED_WX ON CACHE BOOL "Use bundled wxWidgets" FORCE)
        return()
    endif ()
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
