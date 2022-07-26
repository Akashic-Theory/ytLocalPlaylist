if (YTLP-USE_BUNDLED_RAYLIB)
    FetchContent_MakeAvailable(raylib)
else()
    find_package(raylib 4 REQUIRED)
endif ()
set(SRCS SongMetaData.cpp SongMetaData.h ui/Button.h ui/Button.cpp)
set(LIBS raylib nlohmann_json::nlohmann_json)

add_executable(ytlp main.cpp ${SRCS})

target_compile_options(ytlp PRIVATE -g -Wall -Wextra)
target_link_libraries(ytlp PUBLIC ${LIBS})

set_target_properties(ytlp PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
)

if (YTLP-BUILD_TESTS)
    add_library(ytlp-lib ${SRCS})
    target_include_directories(ytlp-lib PUBLIC ${raylib_INCLUDE_DIR})
endif ()

add_custom_command(TARGET ytlp POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_RUNTIME_DLLS:ytlp> $<TARGET_FILE_DIR:ytlp>
    COMMAND_EXPAND_LISTS
)
