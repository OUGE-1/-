import tkinter as tk
from tkinter import ttk, messagebox
import json
import pyperclip

class MinecraftCommandEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft 指令编辑器 1.21.4")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 创建样式
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.create_widgets()
    
    def create_widgets(self):
        # 创建选项卡
        tab_control = ttk.Notebook(self.root)
        
        # 标题选项卡
        self.title_frame = ttk.Frame(tab_control)
        tab_control.add(self.title_frame, text='屏幕标题')
        
        # 聊天框选项卡
        self.chat_frame = ttk.Frame(tab_control)
        tab_control.add(self.chat_frame, text='聊天框文字')
        
        tab_control.pack(expand=1, fill='both')
        
        # 填充标题选项卡
        self.setup_title_tab()
        
        # 填充聊天框选项卡
        self.setup_chat_tab()
        
        # 底部按钮
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="复制指令", command=self.copy_command).pack(side='right', padx=5)
        ttk.Button(button_frame, text="生成指令", command=self.generate_command).pack(side='right', padx=5)
        ttk.Button(button_frame, text="清空", command=self.clear_all).pack(side='right', padx=5)
        
        # 指令显示区域
        self.command_display = tk.Text(self.root, height=6, wrap='word')
        self.command_display.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 初始生成指令
        self.generate_command()
    
    def setup_title_tab(self):
        # 标题类型选择
        type_frame = ttk.LabelFrame(self.title_frame, text="标题类型", padding=10)
        type_frame.pack(fill='x', padx=10, pady=5)
        
        self.title_type = tk.StringVar(value="title")
        ttk.Radiobutton(type_frame, text="主标题", variable=self.title_type, value="title").pack(anchor='w')
        ttk.Radiobutton(type_frame, text="副标题", variable=self.title_type, value="subtitle").pack(anchor='w')
        ttk.Radiobutton(type_frame, text="动作栏", variable=self.title_type, value="actionbar").pack(anchor='w')
        
        # 文本输入
        text_frame = ttk.LabelFrame(self.title_frame, text="文本内容", padding=10)
        text_frame.pack(fill='x', padx=10, pady=5)
        
        self.title_text = tk.StringVar(value="欢迎来到服务器")
        ttk.Entry(text_frame, textvariable=self.title_text, width=50).pack(fill='x')
        
        # 颜色选择
        color_frame = ttk.LabelFrame(self.title_frame, text="颜色", padding=10)
        color_frame.pack(fill='x', padx=10, pady=5)
        
        colors = [
            ("黑色", "black"), ("深蓝色", "dark_blue"), ("深绿色", "dark_green"),
            ("深青色", "dark_aqua"), ("深红色", "dark_red"), ("深紫色", "dark_purple"),
            ("金色", "gold"), ("灰色", "gray"), ("深灰色", "dark_gray"),
            ("蓝色", "blue"), ("绿色", "green"), ("青色", "aqua"),
            ("红色", "red"), ("浅紫色", "light_purple"), ("黄色", "yellow"),
            ("白色", "white")
        ]
        
        self.title_color = tk.StringVar(value="gold")
        
        color_row = ttk.Frame(color_frame)
        color_row.pack(fill='x')
        
        for i, (name, value) in enumerate(colors):
            if i % 4 == 0 and i > 0:
                color_row = ttk.Frame(color_frame)
                color_row.pack(fill='x')
            
            ttk.Radiobutton(color_row, text=name, variable=self.title_color, value=value).pack(side='left', padx=5)
        
        # 格式选项
        format_frame = ttk.LabelFrame(self.title_frame, text="格式", padding=10)
        format_frame.pack(fill='x', padx=10, pady=5)
        
        self.title_bold = tk.BooleanVar()
        self.title_italic = tk.BooleanVar()
        self.title_underlined = tk.BooleanVar()
        self.title_strikethrough = tk.BooleanVar()
        self.title_obfuscated = tk.BooleanVar()
        
        ttk.Checkbutton(format_frame, text="粗体", variable=self.title_bold).pack(side='left', padx=5)
        ttk.Checkbutton(format_frame, text="斜体", variable=self.title_italic).pack(side='left', padx=5)
        ttk.Checkbutton(format_frame, text="下划线", variable=self.title_underlined).pack(side='left', padx=5)
        ttk.Checkbutton(format_frame, text="删除线", variable=self.title_strikethrough).pack(side='left', padx=5)
        ttk.Checkbutton(format_frame, text="随机字符", variable=self.title_obfuscated).pack(side='left', padx=5)
        
        # 目标选择器
        target_frame = ttk.LabelFrame(self.title_frame, text="目标", padding=10)
        target_frame.pack(fill='x', padx=10, pady=5)
        
        self.title_target = tk.StringVar(value="@a")
        ttk.Entry(target_frame, textvariable=self.title_target, width=50).pack(fill='x')
        ttk.Label(target_frame, text="例如: @a (所有玩家), @p (最近玩家), @s (自己)").pack(anchor='w')
    
    def setup_chat_tab(self):
        # 文本输入
        text_frame = ttk.LabelFrame(self.chat_frame, text="文本内容", padding=10)
        text_frame.pack(fill='x', padx=10, pady=5)
        
        self.chat_text = tk.StringVar(value="这是一条重要消息")
        ttk.Entry(text_frame, textvariable=self.chat_text, width=50).pack(fill='x')
        
        # 颜色选择
        color_frame = ttk.LabelFrame(self.chat_frame, text="颜色", padding=10)
        color_frame.pack(fill='x', padx=10, pady=5)
        
        colors = [
            ("黑色", "black"), ("深蓝色", "dark_blue"), ("深绿色", "dark_green"),
            ("深青色", "dark_aqua"), ("深红色", "dark_red"), ("深紫色", "dark_purple"),
            ("金色", "gold"), ("灰色", "gray"), ("深灰色", "dark_gray"),
            ("蓝色", "blue"), ("绿色", "green"), ("青色", "aqua"),
            ("红色", "red"), ("浅紫色", "light_purple"), ("黄色", "yellow"),
            ("白色", "white")
        ]
        
        self.chat_color = tk.StringVar(value="aqua")
        
        color_row = ttk.Frame(color_frame)
        color_row.pack(fill='x')
        
        for i, (name, value) in enumerate(colors):
            if i % 4 == 0 and i > 0:
                color_row = ttk.Frame(color_frame)
                color_row.pack(fill='x')
            
            ttk.Radiobutton(color_row, text=name, variable=self.chat_color, value=value).pack(side='left', padx=5)
        
        # 格式选项
        format_frame = ttk.LabelFrame(self.chat_frame, text="格式", padding=10)
        format_frame.pack(fill='x', padx=10, pady=5)
        
        self.chat_bold = tk.BooleanVar()
        self.chat_italic = tk.BooleanVar()
        self.chat_underlined = tk.BooleanVar()
        self.chat_strikethrough = tk.BooleanVar()
        self.chat_obfuscated = tk.BooleanVar()
        
        ttk.Checkbutton(format_frame, text="粗体", variable=self.chat_bold).pack(side='left', padx=5)
        ttk.Checkbutton(format_frame, text="斜体", variable=self.chat_italic).pack(side='left', padx=5)
        ttk.Checkbutton(format_frame, text="下划线", variable=self.chat_underlined).pack(side='left', padx=5)
        ttk.Checkbutton(format_frame, text="删除线", variable=self.chat_strikethrough).pack(side='left', padx=5)
        ttk.Checkbutton(format_frame, text="随机字符", variable=self.chat_obfuscated).pack(side='left', padx=5)
        
        # 目标选择器
        target_frame = ttk.LabelFrame(self.chat_frame, text="目标", padding=10)
        target_frame.pack(fill='x', padx=10, pady=5)
        
        self.chat_target = tk.StringVar(value="@a")
        ttk.Entry(target_frame, textvariable=self.chat_target, width=50).pack(fill='x')
        ttk.Label(target_frame, text="例如: @a (所有玩家), @p (最近玩家), @s (自己)").pack(anchor='w')
    
    def generate_command(self):
        # 获取当前选中的选项卡
        notebook = self.root.winfo_children()[0]
        current_tab = notebook.index(notebook.select())
        
        if current_tab == 0:  # 标题选项卡
            self.generate_title_command()
        else:  # 聊天框选项卡
            self.generate_chat_command()
    
    def generate_title_command(self):
        # 构建JSON文本组件
        text_component = {
            "text": self.title_text.get(),
            "color": self.title_color.get()
        }
        
        # 添加格式选项
        if self.title_bold.get():
            text_component["bold"] = True
        if self.title_italic.get():
            text_component["italic"] = True
        if self.title_underlined.get():
            text_component["underlined"] = True
        if self.title_strikethrough.get():
            text_component["strikethrough"] = True
        if self.title_obfuscated.get():
            text_component["obfuscated"] = True
        
        # 构建完整指令 - 使用ensure_ascii=False避免Unicode转义
        json_str = json.dumps(text_component, ensure_ascii=False, separators=(',', ':'))
        command = f'/title {self.title_target.get()} {self.title_type.get()} {json_str}'
        
        # 显示指令
        self.command_display.delete(1.0, tk.END)
        self.command_display.insert(1.0, command)
    
    def generate_chat_command(self):
        # 构建JSON文本组件
        text_component = {
            "text": self.chat_text.get(),
            "color": self.chat_color.get()
        }
        
        # 添加格式选项
        if self.chat_bold.get():
            text_component["bold"] = True
        if self.chat_italic.get():
            text_component["italic"] = True
        if self.chat_underlined.get():
            text_component["underlined"] = True
        if self.chat_strikethrough.get():
            text_component["strikethrough"] = True
        if self.chat_obfuscated.get():
            text_component["obfuscated"] = True
        
        # 构建完整指令 - 使用ensure_ascii=False避免Unicode转义
        json_str = json.dumps(text_component, ensure_ascii=False, separators=(',', ':'))
        command = f'/tellraw {self.chat_target.get()} {json_str}'
        
        # 显示指令
        self.command_display.delete(1.0, tk.END)
        self.command_display.insert(1.0, command)
    
    def copy_command(self):
        command = self.command_display.get(1.0, tk.END).strip()
        if command:
            pyperclip.copy(command)
            messagebox.showinfo("成功", "指令已复制到剪贴板！")
        else:
            messagebox.showwarning("警告", "没有可复制的指令！")
    
    def clear_all(self):
        self.title_text.set("")
        self.chat_text.set("")
        self.command_display.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftCommandEditor(root)
    root.mainloop()