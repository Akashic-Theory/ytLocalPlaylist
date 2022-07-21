find_package(Catch2 3.1 REQUIRED)
set(TEST_SRCS SongMetaDataTest.cpp)

add_executable(run_tests ${TEST_SRCS})
target_link_libraries(run_tests PRIVATE ytlp-lib Catch2::Catch2WithMain)
target_compile_options(ytlp-lib PRIVATE --coverage)
target_link_options(run_tests PRIVATE --coverage)
