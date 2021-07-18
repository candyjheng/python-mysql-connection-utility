""" 使用範例，安裝時不會進行安裝 """
import os
import sys
import yaml
import logging

from mysql_utility.cfgloader import load_configure
from mysql_utility.mysqlbase import MySQLBaseInstance

class SampleMySQLInstance(MySQLBaseInstance):
	""" 使用者自行定義需要進行資料庫連線操作的 SQL 相關函式，繼承自本 lib 的包裝 """
	def get_now(self):
		""" 範例 SQL 函式 """
		try:
			with self.connect() as c:
				c.execute("""SELECT NOW()""")
				return c.rowcount
		except Exception as e:
			print("Caught an exception on get_now: %r" % e)

	def get_secondtime(self):
		return self.get_now()

def main():
	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
	# 範例給定資料庫連線設定, 例如範例的 etc/db_config.yaml.sample
	if len(sys.argv) != 2:
		print("Argument: [db_config_path]")
		return

	db_cfg_path = sys.argv[1]
	# 先自行開檔，讀取設定檔內容
	with open(db_cfg_path) as fp:
		cmap = yaml.safe_load(fp)
	dbcfgs = load_configure("TestSection", cmap)
	# load_configure包裝範例設定檔讀取函式
	# TestSection 為範例設計定檔中指定連線的 Section name
	dbinstance = SampleMySQLInstance(dbcfgs)
	rowcount = dbinstance.get_now()
	print("rowcount:", rowcount)
	rowcount = dbinstance.get_secondtime()
	print("second time rowcount:", rowcount)
	
if __name__ == "__main__":
	main()