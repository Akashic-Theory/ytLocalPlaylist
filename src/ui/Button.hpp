// TODO: UNIT TESTS
#ifndef YTLP_BUTTON_HPP
#define YTLP_BUTTON_HPP

#include <string>
#include <utility>
#include <functional>
#include "raylib.h"

class Button {
private:
    enum State { BASE, HOVER, PRESS };
    std::string _text;
    Vector2 _pos;
    Vector2 _size;
    Color _textCol, _baseCol, _hoverCol, _pressCol;
    Font _font;
    float _fontSize;

    State _state;
    std::function<void(void)> _action;
public:

    explicit Button(std::string text = "", Vector2 pos = {0.0f, 0.0f}, Vector2 size = {30.0f, 30.0f},
                    float fontSize = 10.0f, Font font = GetFontDefault(),
                    Color textCol = DARKPURPLE, Color baseCol = LIGHTGRAY, Color hoverCol = GRAY, Color pressCol = DARKGRAY)
            : _text(std::move(text)), _pos(pos), _size(size),
              _textCol(textCol), _baseCol(baseCol), _hoverCol(hoverCol), _pressCol(pressCol),
              _font(font), _fontSize(fontSize), _state(BASE), _action(nullptr) {}

    [[nodiscard]] Vector2 getCenter() const {
        return {_pos.x + 0.5f * _size.x, _pos.y + 0.5f * _size.y };
    }

    Button& process() {
        bool mouseOver = CheckCollisionPointRec(GetMousePosition(), {_pos.x, _pos.y, _size.x, _size.y});
        switch (_state) {
            case BASE: {
                _state = mouseOver ? HOVER : BASE;
            } break;
            case HOVER: {
                _state = mouseOver
                         ? (IsMouseButtonPressed(MOUSE_BUTTON_LEFT) ? PRESS : HOVER)
                         : BASE;
            } break;
            case PRESS: {
                _state = mouseOver
                         ? (IsMouseButtonReleased(MOUSE_BUTTON_LEFT) ? (_action(), BASE) : PRESS )
                         : BASE;
            } break;
        }
        return *this;
    }

    Button& draw() const { // NOLINT(modernize-use-nodiscard)
        DrawRectangleV(_pos, _size, (&_baseCol)[_state]);
        Vector2 textSize = MeasureTextEx(_font, _text.c_str(), _fontSize, 1.0f);
        DrawTextEx(_font, _text.c_str(), { _pos.x + 0.5f * (_size.x - textSize.x), _pos.y + 0.5f * (_size.y - textSize.y) }, _fontSize, 1.0f, _textCol);
        return const_cast<Button &>(*this);
    }

    // Getters/Setters
    Button& text(const std::string& text) { _text = text; return *this; }
    Button& position(const Vector2& position) { _pos = position; return *this; }
    Button& size(const Vector2& size) { _size = size; return *this; }
    Button& textColor(const Color& textColor) { _textCol = textColor; return *this; }
    Button& baseColor(const Color& baseColor) { _baseCol = baseColor; return *this; }
    Button& hoverColor(const Color& hoverColor) { _hoverCol = hoverColor; return *this; }
    Button& pressColor(const Color& pressColor) { _pressCol = pressColor; return *this; }
    Button& font(const Font& font) { _font = font; return *this; }
    Button& fontSize(const float& fontSize) { _fontSize = fontSize; return *this; }
    Button& action(const std::function<void(void)>& action) { _action = action; return *this; }

    [[nodiscard]] const std::string& text() const { return _text; }
    [[nodiscard]] const Vector2& position() const { return _pos; }
    [[nodiscard]] const Vector2& size() const { return _size; }
    [[nodiscard]] const Color& textColor() const { return _textCol; }
    [[nodiscard]] const Color& baseColor() const { return _baseCol; }
    [[nodiscard]] const Color& hoverColor() const { return _hoverCol; }
    [[nodiscard]] const Color& pressColor() const { return _pressCol; }
    [[nodiscard]] const Font& font() const { return _font; }
    [[nodiscard]] const float& fontSize() const { return _fontSize; }

    // Ops
    void operator()() {
        if(_action)
            _action();
    }
};


#endif //YTLP_BUTTON_HPP
