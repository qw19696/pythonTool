import tkinter as tk
from tkinter import ttk
import psutil
import logging
import os

# 配置日志
def setup_logger():
    # 创建日志目录（如果不存在）
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 配置日志
    log_file = os.path.join(log_dir, "port_checker.log")
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),  # 输出到文件
            logging.StreamHandler()         # 输出到控制台
        ]
    )

def get_port_info():
    """获取当前系统的 TCP 和 UDP 端口使用情况"""
    tcp_ports = []
    udp_ports = []

    try:
        # 获取 TCP 端口信息
        for conn in psutil.net_connections(kind='tcp'):
            if conn.status == psutil.CONN_LISTEN:
                tcp_ports.append({
                    "类型": "TCP",
                    "端口": conn.laddr.port,
                    "进程ID": conn.pid,
                    "进程名": psutil.Process(conn.pid).name()
                })

        # 获取 UDP 端口信息
        for conn in psutil.net_connections(kind='udp'):
            if conn.laddr:
                udp_ports.append({
                    "类型": "UDP",
                    "端口": conn.laddr.port,
                    "进程ID": conn.pid,
                    "进程名": psutil.Process(conn.pid).name()
                })

    except Exception as e:
        logging.error(f"获取端口信息时发生异常: {e}")

    return tcp_ports + udp_ports

def on_query_button_click():
    """查询按钮点击事件"""
    # 清空表格
    for row in tree.get_children():
        tree.delete(row)

    # 获取端口信息
    ports = get_port_info()

    # 将数据插入表格
    for port in ports:
        tree.insert("", "end", values=(
            port["类型"],
            port["端口"],
            port["进程ID"],
            port["进程名"]
        ))

    logging.info("查询完成，共找到 {} 条记录".format(len(ports)))

def sort_column(tree, col, reverse):
    """按列排序"""
    data = [(tree.set(child, col), child) for child in tree.get_children()]
    data.sort(reverse=reverse)
    for index, (_, child) in enumerate(data):
        tree.move(child, "", index)
    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))

# 创建主窗口
root = tk.Tk()
root.title("端口使用情况查询工具")
root.geometry("800x400")

# 配置日志
setup_logger()

# 创建查询按钮
query_button = tk.Button(root, text="查询", command=on_query_button_click)
query_button.pack(pady=10)

# 创建表格
columns = ("类型", "端口", "进程ID", "进程名")
tree = ttk.Treeview(root, columns=columns, show="headings")

# 设置列标题并绑定排序事件
for col in columns:
    tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))

# 设置列宽
tree.column("类型", width=100, anchor="center")
tree.column("端口", width=100, anchor="center")
tree.column("进程ID", width=100, anchor="center")
tree.column("进程名", width=400, anchor="center")

# 添加滚动条
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# 放置表格
tree.pack(fill="both", expand=True, padx=10, pady=10)

# 运行主循环
root.mainloop()