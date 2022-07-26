if (NOT DEFINED YTLP-USE_BUNDLED_JSON)
    find_package(nlohmann_json 3.10 QUIET)
    option(YTLP-USE_BUNDLED_JSON "Use bundled nlohmann json" OFF)
    if (NOT nlohmann_json_FOUND)
        set(3P-EXIT "${3P-EXIT}\n- Nlohmann json" CACHE INTERNAL "")
        set(YTLP-USE_BUNDLED_JSON ON CACHE BOOL "Use bundled nlohmann json" FORCE)
        return()
    endif ()
endif ()

if (YTLP-USE_BUNDLED_JSON)
    include(FetchContent)
    set(FETCHCONTENT_QUIET OFF)
    FetchContent_Declare(
            nlohmann_json
            URL https://github.com/nlohmann/json/releases/download/v3.10.5/json.tar.xz
    )
    FetchContent_MakeAvailable(nlohmann_json)
else()
    find_package(nlohmann_json 3.10 REQUIRED)
endif ()
