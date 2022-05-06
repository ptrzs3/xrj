# Intro.

这是一个秀人集爬虫，可以根据关键词爬取指定模特的所有专辑

具备下载、更新、文件夹查空功能



# Instr.

运行XRJ.py（可能需要安装依赖）

输入模特关键词，然后按提示选择下一步操作

该文件的输出为父目录下按专辑名字分类的url.txt，里面包含这张专辑所有图片的链接



使用download.py，更改要下载的目录，然后运行，即下载该模特目录下所有专辑

下载采用wget，需要将其加入环境变量

该文件的输出为专辑图片，与url.txt同目录



# Hints

秀人集经常更改图片真实路径的前缀网址，如果遇到不能爬取的情况，需要检查该前缀是否被更改（在common.py中）

粗制滥造的代码，以实用为主，如不满意可以自行改进



# Results

![image-20220506225756188](C:\Users\ptrzs\AppData\Roaming\Typora\typora-user-images\image-20220506225756188.png)

![image-20220506225842119](C:\Users\ptrzs\AppData\Roaming\Typora\typora-user-images\image-20220506225842119.png)

# 健康生活，从我做起