import sys
import os
import urllib.parse
import pyperclip  # 用于复制到剪贴板，需要先安装：pip install pyperclip


def convert_to_file_protocol(file_path):
    """
    将文件绝对路径转换为三种不同格式的file协议地址
    """
    # 移除路径中可能存在的引号
    file_path = file_path.strip("\"'")

    # 确保路径是绝对路径
    abs_path = os.path.abspath(file_path)

    # 检查文件是否存在
    if not os.path.exists(abs_path):
        print(f"错误：文件 '{abs_path}' 不存在")
        return

    # 格式1: 标准格式 file:///path/to/file
    # 在Windows上，需要将反斜杠转换为正斜杠
    standard_path = abs_path.replace("\\", "/")
    standard_url = f"file:///{standard_path}"

    # 格式2: 使用URL编码的格式
    encoded_path = urllib.parse.quote(standard_path)
    encoded_url = f"file:///{encoded_path}"

    # 格式3: 使用主机名的格式 (file://localhost/path/to/file)
    localhost_url = f"file://localhost/{standard_path}"

    # 输出结果
    print("\n文件协议地址转换结果：")
    print("\n1. 标准格式:")
    print(f"{standard_url}")
    print("\n2. URL编码格式:")
    print(f"{encoded_url}")
    print("\n3. 带主机名格式:")
    print(f"{localhost_url}")

    # 询问用户是否需要复制到剪贴板
    try:
        choice = input("\n请选择要复制到剪贴板的格式 (1/2/3)，直接回车跳过: ")
        if choice == "1":
            pyperclip.copy(standard_url)
            print("已复制标准格式URL到剪贴板")
        elif choice == "2":
            pyperclip.copy(encoded_url)
            print("已复制URL编码格式到剪贴板")
        elif choice == "3":
            pyperclip.copy(localhost_url)
            print("已复制带主机名格式到剪贴板")
    except ImportError:
        print("提示：安装 pyperclip 包可以启用复制到剪贴板功能 (pip install pyperclip)")
    except Exception as e:
        print(f"复制到剪贴板时出错: {e}")

    # 返回三种格式的URL，方便其他程序调用
    return standard_url, encoded_url, localhost_url


def main():
    if len(sys.argv) > 1:
        # 从命令行参数获取文件路径
        file_path = sys.argv[1]
        convert_to_file_protocol(file_path)
    else:
        # 从用户输入获取文件路径
        file_path = input("请输入文件的绝对路径: ")
        convert_to_file_protocol(file_path)


if __name__ == "__main__":
    main()
