add_subdirectory(Raylib)
add_subdirectory(raylib-cpp)

if (YTLP-BUILD_TESTS)
    add_subdirectory(Catch2)
endif ()

if (DEFINED 3P-EXIT)
    message(WARNING "Failed to find some dependencies:"
        "${3P-EXIT}"
        "\nSet missing dependencies to automatically be fetched on next configure.")
    unset(3P-EXIT CACHE)
    message(FATAL_ERROR "Confirm options and re-configure to continue...")
endif ()