if (YTLP-USE_BUNDLED_RAYLIB)
    FetchContent_MakeAvailable(raylib)
else()
    find_package(raylib 4 REQUIRED)
endif ()
if (YTLP-USE_BUNDLED_RAYLIB_CPP)
    FetchContent_MakeAvailable(raylib_cpp)
else()
    find_package(raylib_cpp REQUIRED)
endif ()
set(SRCS SongMetaData.cpp SongMetaData.h)
set(LIBS raylib raylib_cpp)

add_executable(ytlp main.cpp ${SRCS})

target_compile_options(ytlp PRIVATE -g -Wall -Wextra)
target_link_libraries(ytlp PUBLIC ${LIBS})

set_target_properties(ytlp PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
)

if (YTLP-BUILD_TESTS)
    add_library(ytlp-lib ${SRCS})
    target_link_libraries(ytlp-lib ${LIBS})
endif ()

add_custom_command(TARGET ytlp POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_RUNTIME_DLLS:ytlp> $<TARGET_FILE_DIR:ytlp>
    COMMAND_EXPAND_LISTS
)
