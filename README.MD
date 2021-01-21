<h2 align="center">单词救星</h2>

### 一、各个文件的作用
- ContentToDatabase文件中包含DatabaseOperate类，通过实例化此类，实现数据库的增删改查。
- GetTranslation文件中包含get_translation函数，通过调用此函数实现输入的单词直接插入数据库中。
- GetResult文件中包含了get_result函数，通过调用此函数，实现数据库的查询动作。
- create_database_with_table.sql文件中包含了创建数据库表的代码，可直接创建。
