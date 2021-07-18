# 系統需求

* MySQL 5.7+ - 對於字串查詢在處理大小寫的方法不太一樣，舊的版本可能會有預期之外的反應。

# 相依套件

* PyYAML
* MySQLClient

# 使用方式

1. 新增一個物件，此物件繼承 mysql_utility.mysqlbase 的 MySQLBaseInstance 物件
2. 為新物件撰寫相關資料庫存取函式

# 範例程式使用方式

1. 撰寫 `etc/db_config.yaml` 設定
2. 執行

```
./example.py etc/db_config.yaml
```