#include <iostream>
#include "raylib.h"
#include "ui/Button.hpp"

int main () {
    InitWindow(800, 600, "YouTube Playlist Manager");
    SetTargetFPS(60);

    Button button("Click Me", {350, 280}, {100, 40}, 20);
    button.action([]() -> void {
        std::cout << GetTime() << std::endl;
    });

    button();
    while (!WindowShouldClose()) {
        BeginDrawing();
        {
            ClearBackground(DARKPURPLE);
            button.process().draw();
        }
        EndDrawing();
    }
}