# QQMessageStatistics

简单的QQ消息记录统计脚本

## 功能

可以统计你的QQ聊天记录里的词频，并且制作一个简单的云图。

统计很粗糙，仅供娱乐，不要用于专业用途哦。

## 用法

1. 导出纯文本的聊天记录。方法是去 PC qq 的消息查看器，找到“导出聊天记录”。在选择目标文件的时候，可以在下面选择文件类型。选择txt类型导出纯文本聊天记录。
2. 用 pip 安装 3 个依赖库：pyyaml、jieba（中文分词）以及 wordcloud（生成云图）。因为库很少就不写 requirements 文件了， 不过 wordcloud 依赖项有点多，推荐你还是用 venv 配置运行。
3. 配置 'configs.yaml' 文件，填写你的聊天记录文件的路径以及你的用户名。
4. 运行脚本 'main.py' ，然后得到你的结果！
5. 结果会放在同目录下的 'result.png' 文件和 'result.txt' 文件。

## 配置

所有配置都通过写配置文件设置

- file_path ：聊天记录文件的位置
- user_name ：想分析的用户名
- start_time ：分析范围的起始时间
- end_time ：分析范围的终止时间
- mode ：分析模式

下表是可选的分析模式：

- frequency ：频率模式，仅统计出现最多的词
- feature ：特征模式，挑选最有你特色的词

## 使用例

下图是我 2022 年的年度词汇统计：

![](./example_frequency.png)

可以看到其实都是汉语中的常用词，比较有意思的词得仔细看才能看见。

这个是特征词统计：

![](./example_feature.png)

特征词比较有意思，233。
