import os
import shutil
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

class FileMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件移动工具")
        self.root.geometry("600x400")

        # 创建界面组件
        self.create_widgets()

    def create_widgets(self):
        # 输入框框架
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X)

        # 文件后缀输入
        ttk.Label(input_frame, text="文件后缀名:").grid(row=0, column=0, sticky=tk.W)
        self.extension_entry = ttk.Entry(input_frame, width=10)
        self.extension_entry.grid(row=0, column=1, sticky=tk.W)
        self.extension_entry.insert(0, "png")  # 默认值

        # 执行按钮
        self.execute_button = ttk.Button(
            input_frame,
            text="执行移动",
            command=self.execute_move
        )
        self.execute_button.grid(row=0, column=2, padx=10)

        # 进度显示文本框
        self.progress_text = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=70,
            height=20,
            state='normal'
        )
        self.progress_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # 清空按钮
        clear_button = ttk.Button(
            self.root,
            text="清空日志",
            command=self.clear_log
        )
        clear_button.pack(pady=5)

    def execute_move(self):
        """执行文件移动操作"""
        # 获取用户输入的后缀名
        extension = self.extension_entry.get().strip().lower()
        if not extension:
            messagebox.showerror("错误", "请输入文件后缀名")
            return

        # 禁用按钮防止重复点击
        self.execute_button.config(state=tk.DISABLED)

        try:
            # 清空进度文本框
            self.progress_text.delete(1.0, tk.END)

            # 获取当前目录
            current_directory = os.getcwd()
            self.log_message(f"当前目录: {current_directory}")
            self.log_message(f"开始移动 .{extension} 文件...\n")

            # 用于记录文件名及其出现次数
            file_count = {}
            moved_files = 0

            # 遍历当前目录下的所有子目录
            for root, dirs, files in os.walk(current_directory):
                for file in files:
                    if file.lower().endswith(f'.{extension}'):
                        # 构造文件的完整路径
                        file_path = os.path.join(root, file)

                        # 获取文件名和扩展名
                        file_name, file_extension = os.path.splitext(file)

                        # 如果文件名已经存在，则在文件名后拼接自增数字
                        new_file_name = file
                        while os.path.exists(os.path.join(current_directory, new_file_name)):
                            file_count[file_name] = file_count.get(file_name, 0) + 1
                            new_file_name = f"{file_name}_{file_count[file_name]}{file_extension}"

                        try:
                            # 移动文件到当前目录
                            shutil.move(file_path, os.path.join(current_directory, new_file_name))
                            self.log_message(f"已移动: {file_path} -> {new_file_name}")
                            moved_files += 1
                        except Exception as e:
                            self.log_message(f"移动失败 {file_path}: {str(e)}")

            self.log_message(f"\n操作完成! 共移动了 {moved_files} 个文件")

        except Exception as e:
            self.log_message(f"发生错误: {str(e)}")
            messagebox.showerror("错误", f"发生错误: {str(e)}")
        finally:
            # 重新启用按钮
            self.execute_button.config(state=tk.NORMAL)

    def log_message(self, message):
        """在进度文本框中添加消息"""
        self.progress_text.insert(tk.END, message + "\n")
        self.progress_text.see(tk.END)  # 自动滚动到底部
        self.progress_text.update()  # 立即更新UI

    def clear_log(self):
        """清空进度文本框"""
        self.progress_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileMoverApp(root)
    root.mainloop()