//
// Created by Mayank on 3/24/2022.
//

#include "raylib-cpp.hpp"

int main () {
    int screen[] = {800, 600};
    raylib::Color textCol = raylib::Color::Pink();
    raylib::Window window(screen[0], screen[1], "Raylib Test");
    SetTargetFPS(60);

    while (!window.ShouldClose()) {
        window.BeginDrawing()
              .ClearBackground(raylib::Color::LightGray());
        raylib::DrawText("Test", 300, 200, 10, textCol);
        window.EndDrawing();
    }
}