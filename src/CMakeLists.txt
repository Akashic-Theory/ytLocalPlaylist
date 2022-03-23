if (DEFINED ENV_WX_CONFIG)
    set (ENV{WX_CONFIG} ${ENV_WX_CONFIG})
endif()

set(SRCS main.cpp)

add_executable(ytlp WIN32 ${SRCS})


target_link_libraries(ytlp PRIVATE wx::core)

set_target_properties(ytlp PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
)

add_custom_command(TARGET ytlp POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_RUNTIME_DLLS:ytlp> $<TARGET_FILE_DIR:ytlp>
    COMMAND_EXPAND_LISTS
)