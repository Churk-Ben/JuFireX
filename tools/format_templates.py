import os
import subprocess
import sys
import re


def fix_template_indentation(directory):
    """修复Django模板中的缩进问题"""
    # 获取目录下所有HTML文件
    html_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))

    print(f"找到 {len(html_files)} 个HTML文件需要修复模板缩进")

    # 修复每个文件中的模板变量缩进
    success_count = 0
    for file_path in html_files:
        try:
            if manual_fix_template_indentation(file_path):
                success_count += 1
        except Exception as e:
            print(f"修复模板缩进失败: {file_path}")
            print(f"错误信息: {str(e)}")

    print(f"成功修复模板缩进 {success_count}/{len(html_files)} 个文件")


def fix_css_indentation(lines, start_index, end_index, base_indent):
    """修复CSS代码的缩进问题"""
    modified = False

    # 首先确定CSS代码的基础缩进级别
    css_base_indent = " " * (base_indent + 2)  # <style>标签后的内容缩进2个空格

    for i in range(start_index + 1, end_index):  # 跳过<style>和</style>标签
        line = lines[i]
        if not line.strip():
            continue  # 跳过空行

        content = line.strip()

        # 根据CSS内容类型确定缩进级别
        if "{" in content:  # 选择器行
            new_line = css_base_indent + content
        elif "}" in content:  # 闭合括号行
            new_line = css_base_indent + content
        else:  # 属性行
            new_line = css_base_indent + "  " + content  # 属性行多缩进2个空格

        if new_line != line:
            lines[i] = new_line
            modified = True

    return modified


def manual_fix_template_indentation(file_path):
    """手动修复单个文件中的模板变量缩进问题"""
    try:
        print(f"正在修复模板缩进: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # 查找并修复模板变量的缩进问题
        lines = content.split("\n")
        modified = False

        # 查找所有<style>标签块
        i = 0
        while i < len(lines):
            # 检查是否是<style>标签开始
            if "<style>" in lines[i]:
                style_start = i
                base_indent = len(lines[i]) - len(lines[i].lstrip())

                # 查找对应的</style>标签
                style_end = -1
                for j in range(style_start + 1, len(lines)):
                    if "</style>" in lines[j]:
                        style_end = j
                        break

                if style_end > style_start:
                    # 修复<style>标签内的CSS缩进
                    if fix_css_indentation(lines, style_start, style_end, base_indent):
                        modified = True
                    i = style_end  # 跳过已处理的<style>块

            # 检查是否是模板变量行，且前后都是缩进的HTML
            elif (
                "{{" in lines[i]
                and "}}" in lines[i]
                and lines[i].strip().startswith("{{")
                and lines[i].strip().endswith("}}")
            ):
                # 检查前一行和后一行是否有缩进
                if i > 0 and i < len(lines) - 1:
                    prev_line = lines[i - 1]
                    next_line = lines[i + 1]

                    # 如果前后行都有缩进，但当前行没有正确缩进
                    if (
                        prev_line.strip()
                        and next_line.strip()
                        and len(prev_line) - len(prev_line.lstrip()) > 0
                    ):
                        indent = " " * (len(prev_line) - len(prev_line.lstrip()))
                        # 获取变量内容并添加缩进
                        var_content = lines[i].strip()
                        lines[i] = indent + "  " + var_content
                        modified = True

            # 检查是否是纯文本行，且前后都是缩进的HTML
            elif lines[i].strip() and not any(
                tag in lines[i] for tag in ["<", ">", "{%", "%}", "{{", "}}"]
            ):
                # 检查前一行和后一行是否有缩进
                if i > 0 and i < len(lines) - 1:
                    prev_line = lines[i - 1]
                    next_line = lines[i + 1]

                    # 如果前后行都有缩进，但当前行没有正确缩进
                    if (
                        prev_line.strip()
                        and next_line.strip()
                        and len(prev_line) - len(prev_line.lstrip()) > 0
                    ):
                        indent = " " * (len(prev_line) - len(prev_line.lstrip()))
                        # 获取文本内容并添加缩进
                        text_content = lines[i].strip()
                        lines[i] = indent + "  " + text_content
                        modified = True

            # 检查标签内的文本缩进问题
            elif "<" in lines[i] and ">" in lines[i]:
                # 查找标签内的文本
                tag_content_match = re.search(r">\s*(.*?)\s*<", lines[i])
                if (
                    tag_content_match
                    and tag_content_match.group(1).strip()
                    and not any(
                        tag in tag_content_match.group(1)
                        for tag in ["{%", "%}", "{{", "}}"]
                    )
                ):
                    # 获取标签前的缩进
                    indent = " " * (len(lines[i]) - len(lines[i].lstrip()))
                    # 修复标签内文本的缩进
                    original = lines[i]
                    lines[i] = re.sub(
                        r">\s*(.*?)\s*<",
                        lambda m: "> " + m.group(1).strip() + " <",
                        lines[i],
                    )
                    if lines[i] != original:
                        modified = True

            i += 1

        # 如果有修改，写回文件
        if modified:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("\n".join(lines))
            return True
        else:
            return False
    except Exception as e:
        print(f"修复模板缩进失败: {file_path}")
        print(f"错误信息: {str(e)}")
        return False


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # 没有参数，处理整个templates目录
        templates_dir = "templates"

        if not os.path.isdir(templates_dir):
            print(f"错误: {templates_dir} 不是一个有效的目录")
            sys.exit(1)

        # 修复模板缩进问题
        fix_template_indentation(templates_dir)

        print("所有HTML文件格式化完成！")
    else:
        # 有参数，处理单个文件
        file_path = sys.argv[1]

        if not os.path.isfile(file_path):
            print(f"错误: {file_path} 不是一个有效的文件")
            sys.exit(1)

        # 手动修复单个文件的模板缩进
        if manual_fix_template_indentation(file_path):
            print(f"成功修复文件: {file_path}")
        else:
            print(f"文件无需修复: {file_path}")

        print("文件格式化完成！")
