import PySimpleGUI as sg


def framed(elem: sg.Element, *args: object, **kwargs: object) -> sg.Frame:
    return sg.Frame(*args, layout=[[elem]], **kwargs)
