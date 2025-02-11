---
title: "从 Pelican 到 Hugo：博客静态网站框架切换（一）"
date: 2025-02-11T03:21:00
categories:
  - "Linux"
tags:
  - "linux"
draft: false
---

很久以前就用jekyll搞过博客，jekyll是github page文档默认的例子，但是是基于ruby的，因为我最主要学的是python，那时候找了一个python的静态网站生成框架叫pelican。但几年下来感觉不如一个go的静态网站框架hugo发展的好，pelican 大概是 12k 的 star，而 hugo 有 77k 多，所以想尝试一下看看能不能切换到hugo。

这次打算写两篇，第一篇关于初始化了hugo框架并且用python脚本将pelican的markdown文件转换成hugo的，并且在本地运行起来，第二片写如何用部github action部署到Github Pages，也对主题，中英文多语言等进行调整和优化。

除了github上的受欢迎程度，我也大致问了以下chatgpt——hugo和pelican对比的主要优缺点，这里简单赘述：
- 构建速度极快（go的性能优势？）
- 社区活跃，主题和插件都较为丰富
- 多语言支持
- 配置简单，只需要yaml和toml文件，不需要实际写go代码（相比较pelican需要写python代码）

我现在使用的环境是**windows的wsl2的ubuntu**，所以具体代码以此为例：

#### 一：备份 Pelican 分支

确保备份 Pelican 的分支，避免意外丢失数据或者需要快速重新上线pelican的blog时候，可随时恢复到原先的状态。

```bash
git clone https://github.com/gccpacman/gccpacman.github.io
git checkout -b pelican
git push -u origin pelican
```

#### 二：安装 Go语言

浏览器到go官网下载并安装golang：
```
cd Downloads
sudo su -
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.23.6.linux-amd64.tar.gz
```
编辑`.zprofile`加入环境变量 (因为我用的zsh）：
```
# golang
export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin
```
#### 三：安装hugo

ubuntu其实可以用apt或者snap安装，但我想要用最新的版本，就用go来安装了：

```bash
go install github.com/gohugoio/hugo@latest
```

安装完成后验证：

```bash
hugo version
```

#### 四：创建hugo必要的文件

如果是一个新项目，按照[Hugo官方文档](https://gohugo.io/getting-started/quick-start/#explanation-of-commands)安装完成 Hugo 后应该执行：

```bash
hugo new site my-new-blog
```

但因为我是把已有的pelican项目改成hugo，所以我又查了下chatgpt，结果是可以直接在git目录执行`hugo new site .` 但是需要考虑一些目录可能会重名的问题，比如 `content/`、`themes/`、`config.toml` 等。
我检查了以下`content`这个目录pelican和hugo确实是重名的，因此暂时重命名成了`content-pelican`然后再执行：
```
hugo new site .
```

#### 五：安装 Hugo 主题

Hugo 提供了多种主题，这里我搜到了一个看着比较好的主题 **ananke** ，然后就简单的在`hugo.toml`指定主题，并且作为**git submodule**加入到项目里即可：

```bash
echo "theme = 'ananke'" >> hugo.toml
 git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke
```

#### 六：迁移Markdown内容

内容迁移是整个过程的最核心也是最麻烦的部分。由于 Pelican 和 Hugo 的**Markdown文件结构不同**，所以需要一些改动，我大概有30多篇博客，不太可能手动修改，因此想通过 **Python 脚本来转换markdown文件**，这个脚本我大部分**交给chatgpt帮我写**，我自己来验证和修改。一开始chatgpt会有一些时间格式和漏掉hugo的`draft`值等错误，经过几次指正，chatgpt生成的代码基本上没有大的问题，以下是我给ChatGpt的最终版本的Prompt：

```

Pelican和hugo是两个静态网站生成框架， 我需要将一个Pelican框架的Posts的markdown转换成Hugo框架的格式。
- 考虑date, tags, categories格式和大小写的不同
- 并加上draft=false
- hugo按 "yaml"而不是"toml"的格式编写
- pelican的post文件夹目录为./content-pelican, hugo的为./content/posts
- 考虑文件名的差别, 重命名markdown文件

```

最终GPT生成的代码主要完成了以下两个功能：

##### 6.1 处理markdown文件内容
Pelican 的 Markdown 文件使用 YAML 格式的元数据，而 Hugo 也使用 YAML 格式，但两者在格式上存在一些差异，例如：

- Pelican 使用 `Category` 来表示分类，而 Hugo 使用 `categories`。
- Pelican 的 `Date` 字段格式为 `YYYY-MM-DD HH:MM`，而 Hugo 使用 `YYYY-MM-DDTHH:MM:SS+ZZ:ZZ` 格式。
- Hugo 需要 `draft: false` 来标记发布的文章。

``` bash
# Pelican 格式
Title: Linux将Socks代理转换成Http代理
Date: 2015-05-14 10:20
Modified: 2015-05-14 19:30
Category: Linux
Tags: linux, proxy
Authors: r341h

# Hugo 格式
---
title: "Linux将Socks代理转换成Http代理"
date: 2015-05-14T10:20:00
categories:
  - "Linux"
tags:
  - "linux"
  - "proxy"
draft: false
---
```


该脚本会：
- 从 Pelican 文件中提取标题、日期、分类、标签等元数据。
- 格式化这些数据为 Hugo的格式，并增加 `draft: false` 来标记该文章为发布状态。

```python
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
```



##### 6.2 处理文件名

Pelican 中的 Markdown 文件通常是以 `title.md` 的格式命名，而 Hugo 需要使用 `YYYY-MM-DD-title.md` 格式。以下是文件名改变的关键代码：

```python
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
```

#### 七：测试与部署

在本地环境中运行 Hugo，命令行运行：

```bash
hugo server
# 命令行输出
                   | CN  | EN
-------------------+-----+-----
  Pages            | 138 |  8
  Paginator pages  |   9 |  0
  Non-page files   |   0 |  0
  Static files     |   2 |  2
  Processed images |   0 |  0
  Aliases          |   2 |  0
  Cleaned          |   0 |  0

Built in 162 ms
Environment: "development"
Serving pages from disk
Running in Fast Render Mode. For full rebuilds on change: hugo server --disableFastRender
Web Server is available at http://localhost:1313/ (bind address 127.0.0.1)
```

然而我访问` http://localhost:1313/`无效，原因我理解应该是wsl2不能使用那么小的端口号，于是我改成了9090：
```
hugo server -p 9090
```

本地运行效果正常

#### 结论

到此已经初始化了hugo框架并且转换了所有的posts文件，并且在本地运行起来，但**依旧没有部署到Github Pages，也没有对主题，中英文多语言这些进行优化**，如果都写在这一篇篇幅太长，暂时写道这里。改天再补上。
