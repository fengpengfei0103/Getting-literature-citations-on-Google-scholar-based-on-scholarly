# -coding: utf-8
# -Author: fengpengpei
# -Email: fpf0103@163.com
# readme:基于scholarly获取Google scholar上文献引用内容；
# 下面内容包括两种方式：1、通过关键词获取2、通过作者名字获取
# 其中第一种通过关键词获取生成 BibTeX 格式的文献引用；
# 第二种通过作者名字获取，是通过自定义format_cms_style函数提取文献信息并转换为Chicago Manual of Style格式

from scholarly import scholarly
from scholarly import ProxyGenerator


# 提取文献信息并转换为Chicago Manual of Style格式
def format_cms_style(publication, style="Notes and Bibliography"):
    # 获取完整的文献信息
    publication_filled = scholarly.fill(publication)

    # 提取文献信息
    # search_query = scholarly.search_pubs(publication['bib']['title'])
    # pub = next(search_query)
    title = publication_filled.get('bib', {}).get('title', 'Unknown Title')
    authors = publication_filled.get('bib', {}).get('author', 'Unknown Author')
    year = publication_filled.get('bib', {}).get('pub_year', 'Unknown Year')
    journal = publication_filled.get('bib', {}).get('journal', 'Unknown Journal')

    # 处理多个作者
    author_list = authors.split('and') if authors != 'Unknown Author' else ['Unknown Author']
    # 全部作者方式
    # authors_formatted = ', '.join(author_list)
    # 格式化为 "Mei, Xiaoguang, et al."方式
    if len(author_list) > 1:
        authors_formatted = f"{author_list[0]}, et al"
    else:
        authors_formatted = author_list[0]

    # 根据样式生成引用
    if style == "Notes and Bibliography":
        # 格式：脚注
        citation_note = f"{authors_formatted}. {title}. {journal}, {year}."
        # 格式：书目
        citation_bibliography = f"{authors_formatted}. {title}. {journal}, {year}."
        return citation_note, citation_bibliography

    elif style == "Author-Date":
        # 格式：正文引用
        citation_text = f"({author_list[0]} {year})"
        # 格式：参考文献
        citation_reference = f"{authors_formatted}. {year}. {title}. {journal}."
        return citation_text, citation_reference

    else:
        raise ValueError("Unsupported style. Choose 'Notes and Bibliography' or 'Author-Date'.")


pg = ProxyGenerator()

# # 创建 HTTP 客户端并配置代理
success = pg.SingleProxy("127.0.0.1:7890")
 

# 第二个参数ProxyGenerator()代表强制使用代理
scholarly.use_proxy(pg, ProxyGenerator())


# ---------------------2、通过作者名字获取-------------------------------
# 调用 search_pubs 方法搜索标题中包含“attention is all you need”的文献
search_query = scholarly.search_pubs('Window-based Channel Attention')

for i in range(20):
    # 使用 next() 方法从生成器中获取第一篇文献的详细信息，并存储在 pub 变量中
    pub = next(search_query)

    # 从 pub 的 bib 字典中提取标题（title），并打印
    print("第", i+1, "篇文章：")
    print(pub['bib']['title'])

    # 使用 scholarly.bibtex 方法生成 BibTeX 格式的文献引用，并打印
    print("\nCitation (BibTeX):")
    print(scholarly.bibtex(pub))

# ---------------------1、通过关键词获取-------------------------------
# 搜索作者
author_name = 'Xiaoguang Mei'  # 修改为你要搜索的作者名字
search_author = scholarly.search_author(author_name)

# 获取作者详细信息
author = next(search_author)

# 填充作者的详细信息，包括出版物
scholarly.fill(author)

# 打印作者信息
print(f"Author: {author['name']}")
print(f"Affiliation: {author.get('affiliation', 'N/A')}")

# 获取该作者的前20篇出版物
publications = author.get('publications', [])


# 打印该作者的前20篇文献
if publications:
    for i, pub in enumerate(publications):
        if i >= 20:  # 限制输出20篇文献
            break

        # 打印文献标题
        print("第", i+1, "篇文章：")
        print(pub['bib']['title'])

        # 检查并生成 BibTeX 格式的文献引用，处理缺少必要字段的情况
        try:
            # 格式化为Chicago Manual of Style
            # citation_note, citation_bibliography = format_cms_style(pub, style="Notes and Bibliography")
            # print("脚注格式:", citation_note)
            # print("书目格式:", citation_bibliography)

            citation_text, citation_reference = format_cms_style(pub, style="Author-Date")
            print("正文引用格式:", citation_text)
            print("参考文献格式:", citation_reference)
            print("\n" + "-" * 50)
        except KeyError as e:
            print(f"Error generating BibTeX for publication {i + 1}: Missing required fields.")
else:
    print("没有找到该作者的出版物。")


