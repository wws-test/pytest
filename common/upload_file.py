import win32gui
import win32con


def upload(filePath, browser_type="chrome"):
    '''
    通过pywin32模块实现文件上传的操作
    :param filePath: 文件的绝对路径
    :param browser_type: 浏览器类型（默认值为chrome）
    :return:
    '''
    if browser_type.lower() == "chrome":
        title = "打开"
    elif browser_type.lower() == "firefox":
        title = "文件上传"
    elif browser_type.lower() == "ie":
        title = "选择要加载的文件"
    else:
        title = ""  # 这里根据其它不同浏览器类型来修改

    # 找元素
    # 一级窗口"#32770","打开"
    dialog = win32gui.FindWindow("#32770", title)
    # 向下传递
    ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)  # 二级
    comboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, "ComboBox", None)   # 三级
    # 编辑按钮
    edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)  # 四级
    # 打开按钮
    button = win32gui.FindWindowEx(dialog, 0, 'Button', "打开(&O)")  # 二级

    # 输入文件的绝对路径，点击“打开”按钮
    win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filePath)  # 发送文件路径
    win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮