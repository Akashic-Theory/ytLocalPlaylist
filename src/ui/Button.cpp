#include "Button.h"

Button &Button::draw() const {
    DrawRectangleV(_pos, _size, (&_baseCol)[_state]);
    Vector2 textSize = MeasureTextEx(_font, _text.c_str(), _fontSize, 1.0f);
    DrawTextEx(_font, _text.c_str(), { _pos.x + 0.5f * (_size.x - textSize.x), _pos.y + 0.5f * (_size.y - textSize.y) }, _fontSize, 1.0f, _textCol);
    return const_cast<Button &>(*this);
}

Button &Button::process() {
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
