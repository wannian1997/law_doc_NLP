# data_access
01 process_doc 批量转换doc文件\
02 extract_list 抽取一篇文书（doc或docx都可）中的关键信息。\
（后面考虑doc文件存储方式与03的兼容性，即将生成的docx文件存储在docx文件夹中，这样的话，就可以省去01步骤）\
03 extract_information 批量处理抽取一个文件夹中的docx文件关键信息

# Paper.py
| 标签      | 含义      |
|---------|---------|
| label00 | 文件名     |
| label01 | 法院      |
| label02 | 文书类型    |
| label03 | 案号      |
| label04 | 公诉机关    |
| label05 | 被告人     |
| label06 | 指控      |
| label07 | 法院认定    |
| label08 | 审判人员和日期 |
| label09 | 相关法律    |
label6后面数字含义：审判程序1\t指控2\t辩护意见3\t审理查明4\t证据5\n
