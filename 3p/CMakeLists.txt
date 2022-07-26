add_subdirectory(Raylib)
add_subdirectory(json)
add_subdirectory(tiny-process)

if (YTLP-BUILD_TESTS)
    add_subdirectory(Catch2)
endif ()

if (DEFINED 3P-EXIT)
    message(WARNING "Failed to find some dependencies:"
        "${3P-EXIT}"
        "\nSetting missing dependencies to automatically be fetched on next configure."
        "\nThis is NOT an error unless you wish to use local installs of the libraries"
        "\nSimply re-configure to fetch missing dependencies")
    unset(3P-EXIT CACHE)
    message(FATAL_ERROR "Confirm options and re-configure to continue...")
endif ()