import os
import re
from datetime import datetime

# 定义 Pelican 元数据的正则表达式模式
pelican_metadata_pattern = {
    'Title': re.compile(r'^Title:\s*(.*)$', re.IGNORECASE),
    'Date': re.compile(r'^Date:\s*(.*)$', re.IGNORECASE),
    'Category': re.compile(r'^Category:\s*(.*)$', re.IGNORECASE),
    'Tags': re.compile(r'^Tags:\s*(.*)$', re.IGNORECASE),
    'Slug': re.compile(r'^Slug:\s*(.*)$', re.IGNORECASE),
    'Summary': re.compile(r'^Summary:\s*(.*)$', re.IGNORECASE)
}

# 将 Pelican 元数据转换为 Hugo 前置格式
def convert_metadata_to_hugo(metadata):
    hugo_front_matter = '---\n'
    if 'Title' in metadata:
        hugo_front_matter += f'title: "{metadata["Title"]}"\n'
    if 'Date' in metadata:
        try:
            date_obj = datetime.strptime(metadata['Date'], '%Y-%m-%d %H:%M')
            hugo_front_matter += f'date: {date_obj.strftime("%Y-%m-%dT%H:%M:%S%z")}\n'
        except ValueError:
            print(f"Error: Invalid date format '{metadata['Date']}'")
    if 'Category' in metadata:
        categories = [cat.strip() for cat in metadata['Category'].split(',')]
        hugo_front_matter += 'categories:\n'
        for category in categories:
            hugo_front_matter += f'  - "{category}"\n'
    if 'Tags' in metadata:
        tags = [tag.strip() for tag in metadata['Tags'].split(',')]
        hugo_front_matter += 'tags:\n'
        for tag in tags:
            hugo_front_matter += f'  - "{tag}"\n'
    if 'Slug' in metadata:
        hugo_front_matter += f'slug: "{metadata["Slug"]}"\n'
    if 'Summary' in metadata:
        hugo_front_matter += f'summary: "{metadata["Summary"]}"\n'
    hugo_front_matter += 'draft: false\n'
    hugo_front_matter += '---\n'
    return hugo_front_matter

# 处理单个文件的转换
def convert_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    metadata = {}
    content = []
    is_metadata_section = True

    for line in lines:
        if is_metadata_section:
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

    hugo_front_matter = convert_metadata_to_hugo(metadata)
    new_content = hugo_front_matter + ''.join(content)

    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Converted {input_file_path} -> {output_file_path}")

# 批量转换目录中的所有 Markdown 文件
def convert_directory(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for root, _, files in os.walk(input_directory):
        for filename in files:
            if filename.endswith('.md'):
                input_file_path = os.path.join(root, filename)
                with open(input_file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    date_str = None
                    for line in lines:
                        match = pelican_metadata_pattern['Date'].match(line.strip())
                        if match:
                            date_str = match.group(1).strip()
                            break
                if date_str:
                    try:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
                        new_filename = f"{date_obj.strftime('%Y-%m-%d')}-{filename}"
                    except ValueError:
                        print(f"Error: Invalid date format in file {input_file_path}. Skipping...")
                        continue
                else:
                    new_filename = filename

                relative_path = os.path.relpath(root, input_directory)
                output_dir = os.path.join(output_directory, relative_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                output_file_path = os.path.join(output_dir, new_filename)
                convert_file(input_file_path, output_file_path)

# 主函数
if __name__ == "__main__":
    input_directory = "./content-pelican"  # Pelican 的内容目录
    output_directory = "./hugocontent/cn/posts"  # Hugo 的内容目录

    convert_directory(input_directory, output_directory)
