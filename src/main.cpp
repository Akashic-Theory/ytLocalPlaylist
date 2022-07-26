#include <iostream>
#include "raylib.h"
#include "ui/Button.h"
#include "process.hpp"
#include "nlohmann/json.hpp"

namespace tinyproc = TinyProcessLib;
using json = nlohmann::json;

int main () {
    SetTraceLogLevel(LOG_NONE);
    InitWindow(800, 600, "YouTube Playlist Manager");
    SetTargetFPS(60);

    Button button("Click Me", {350, 280}, {100, 40}, 20);
    button.action([]() -> void {
        std::cout << GetTime() << std::endl;
    });
    tinyproc::Process process("yt-dlp --version");
    if (process.get_exit_status()) {
        std::cout << "Not Found on path" << std::endl;
    }

    while (!WindowShouldClose()) {
        BeginDrawing();
        {
            ClearBackground(DARKPURPLE);
            button.process().draw();
        }
        EndDrawing();
    }
}