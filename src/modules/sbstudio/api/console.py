import sys

if sys.platform[:3] != 'win':
    class ConsoleWindow:
        def __enter__(self):
            pass
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
else:
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    user32.GetClassNameW.argtypes = [wintypes.HWND, ctypes.c_wchar_p, ctypes.c_int]
    user32.IsWindowVisible.argtypes = [wintypes.HWND]
    user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
    user32.SetForegroundWindow.argtypes = [wintypes.HWND]
    user32.GetWindowTextW.argtypes = [wintypes.HWND, ctypes.c_wchar_p, ctypes.c_int]
    user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
    user32.GetDesktopWindow.argtypes = []
    user32.IsIconic.argtypes = [wintypes.HWND]
    user32.EnumChildWindows.argtypes = [wintypes.HWND, ctypes.CFUNCTYPE(ctypes.c_bool, wintypes.HWND, ctypes.py_object), ctypes.py_object]

    SW_HIDE = 0
    SW_SHOW = 5
    SW_RESTORE = 9

    def show_console_window(visible=True, pid=ctypes.windll.kernel32.GetCurrentProcessId()):
        def check_window_info(hwnd):
            class_name = ctypes.create_unicode_buffer(256)
            user32.GetClassNameW(hwnd, class_name, 256)

            title_length = user32.GetWindowTextLengthW(hwnd)
            title = ctypes.create_unicode_buffer(title_length + 1)
            user32.GetWindowTextW(hwnd, title, title_length + 1)

            return "ConsoleWindowClass" in class_name.value and "blender.exe" in title.value.lower()

        def enum_windows_callback(hwnd, ctx):
            window_pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(window_pid))
            if window_pid.value == pid:
                if not check_window_info(hwnd):
                    return True
                if not visible:
                    user32.ShowWindow(hwnd, SW_HIDE)
                else:
                    if not user32.IsWindowVisible(hwnd):
                        user32.ShowWindow(hwnd, SW_SHOW)
                    if user32.IsIconic(hwnd):
                        user32.ShowWindow(hwnd, SW_RESTORE)
                    user32.SetForegroundWindow(hwnd)
                return False
            return True

        if sys.platform[:3] == "win":
            callback = ctypes.CFUNCTYPE(ctypes.c_bool, wintypes.HWND, ctypes.py_object)(enum_windows_callback)
            user32.EnumChildWindows(user32.GetDesktopWindow(), callback, None)

    class ConsoleWindow:
        def __enter__(self):
            show_console_window(True)
        def __exit__(self, exc_type, exc_val, exc_tb):
            show_console_window(False)

    if __name__ == '__main__':
        # 显示窗口
        show_console_window(True)
        # 隐藏窗口
        show_console_window(False)
