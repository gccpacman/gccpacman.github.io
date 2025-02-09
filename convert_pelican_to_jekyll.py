import os
import re
import shutil
from datetime import datetime

# 定义 Pelican 格式的正则表达式
pelican_metadata_pattern = {
    'Title': re.compile(r'^Title:\s*(.*)$'),
    'Date': re.compile(r'^Date:\s*(.*)$'),
    'Category': re.compile(r'^Category:\s*(.*)$'),
    'Tags': re.compile(r'^Tags:\s*(.*)$'),
    'Slug': re.compile(r'^Slug:\s*(.*)$'),
    'Summary': re.compile(r'^Summary:\s*(.*)$')
}

# 读取和转换每个Markdown文件
def convert_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    metadata = {}
    content = []
    is_metadata_section = True

    # 读取文件内容并提取元数据
    for line in lines:
        if is_metadata_section:
            # 处理元数据
            match_found = False
            for key, pattern in pelican_metadata_pattern.items():
                match = pattern.match(line.strip())
                if match:
                    metadata[key] = match.group(1).strip()
                    match_found = True
                    break

            if not match_found and line.strip() == "":
                is_metadata_section = False
        else:
            content.append(line)

    # 构建 Jekyll 的 Front Matter
    jekyll_front_matter = "---\n"
    jekyll_front_matter += f"title: {metadata.get('Title', '')}\n"

    # 处理 Date 格式
    date_str = metadata.get('Date', '')
    if date_str:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            jekyll_front_matter += f"date: {date_obj.strftime('%Y-%m-%d %H:%M:%S %z')}\n"
        except ValueError:
            print(f"Error: Could not parse date for file {input_file_path}")
            jekyll_front_matter += "date: unknown\n"
    
    # 处理其他字段
    if 'Category' in metadata:
        jekyll_front_matter += f"categories: {metadata['Category']}\n"
    if 'Tags' in metadata:
        jekyll_front_matter += f"tags: [{metadata['Tags']}]\n"
    if 'Slug' in metadata:
        jekyll_front_matter += f"slug: {metadata['Slug']}\n"
    if 'Summary' in metadata:
        jekyll_front_matter += f"summary: {metadata['Summary']}\n"
    
    jekyll_front_matter += "---\n"

    # 合并 Front Matter 和内容
    new_content = jekyll_front_matter + ''.join(content)

    # 写回转换后的内容到新的文件路径
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Converted {input_file_path} -> {output_file_path}")

# 批量转换指定目录下的所有 Markdown 文件
def convert_directory(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        input_file_path = os.path.join(input_directory, filename)

        if os.path.isfile(input_file_path) and filename.endswith(".md"):
            # 解析出文件的标题部分（假设文件名格式为 `YYYY-MM-DD-title.md`）
            output_file_path = os.path.join(output_directory, filename)
            # 转换文件
            convert_file(input_file_path, output_file_path)

# 执行脚本
if __name__ == "__main__":
    # 修改为你的目标文件夹路径
    input_directory = "./content"  # 输入文件夹路径（Pelican 格式的文件）
    output_directory = "/_posts"  # 输出文件夹路径（Jekyll 格式的文件）
    convert_directory(input_directory, output_directory)
