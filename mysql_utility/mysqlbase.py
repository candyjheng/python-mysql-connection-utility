# -*- coding: utf-8 -*-
"""
MySQL 資料庫相關函式基礎物件
mysqlclient 背後使用 C API 故在參考 MySQL 官方 API 文件時，讀 https://dev.mysql.com/doc/connectors/en/connector-c.html
mysqlclient 官方文件 https://mysqlclient.readthedocs.io/user_guide.html
"""

import sys
import logging
import MySQLdb

_log = logging.getLogger(__name__)



def _get_mysqldb_coonect(db_cfg):
	connect_variables = {"host": db_cfg.host, "user": db_cfg.user}
	if db_cfg.schema:
		connect_variables['db'] = db_cfg.schema
	if db_cfg.passwd:
		connect_variables['passwd'] = db_cfg.passwd
	if db_cfg.socket:
		connect_variables['unix_socket'] = db_cfg.socket
	else:
		connect_variables['port'] = db_cfg.port
	_log.debug("_get_mysqldb_coonect : %r", connect_variables)
	return MySQLdb.connect(**connect_variables)


def _open_connection_by_cfg(db_cfg):
	""" 依照設定檔資訊打開 MySQL 資料庫連線 """
	try:
		if db_cfg.host is None:
			_log.error("host info not in db config")
			return
		return _get_mysqldb_coonect(db_cfg)
	except Exception as e:
		_log.exception("Error on _open_connection_by_cfg: %r", e)
	return None


class MySQLBaseInstance(object):
	""" 資料庫連線實體物件 """
	__slots__ = ("db_cfgs", "_auto_commit", "_dbconn", "_next_indx", "_use_DictCursor")

	def __init__(self, db_confs, auto_commit=True, use_DictCursor=True):
		""" 建構子
		Argument:
			db_cfgs - 資料庫連線資訊 list
			auto_commit - 是否自動 commit
			_dbconn - MySQL.connect 物件
			_next_indx - 下一個使用之連線資訊索引
		"""
		self.db_cfgs = db_confs
		self._dbconn = None
		self._next_indx = 0
		self._auto_commit = auto_commit
		self._use_DictCursor = use_DictCursor

	def ping(self):
		""" 檢驗資料庫連線是否正常
		MySQLdb.connect.ping() 對應 C API 的 mysql_ping()
		https://dev.mysql.com/doc/refman/8.0/en/mysql-ping.html
		Argument:
		Return:
			True: 連線正常
			False: 連線已失效或中斷
		"""
		if self._dbconn is not None:
			try:
				self._dbconn.ping()
				return True
			except Exception as e:
				sys.stderr.write("WARN: database connection broken: %r [@base-dbroutine~mysql.ping]\n" % (e, ))
		return False

	def _open_connection(self):
		""" 從資料庫連線清單中取得一筆可連線資訊 """
		indx_try = 0
		while indx_try < len(self.db_cfgs):  # 表示 try 完一輪沒有可用連線
			self._dbconn = _open_connection_by_cfg(self.db_cfgs[self._next_indx])
			self._dbconn.autocommit(self._auto_commit)
			self._dbconn.set_character_set('utf8')
			if self._dbconn:
				_log.debug("Use database configure: %r", self.db_cfgs[self._next_indx])
				if self._use_DictCursor:
					return self._dbconn.cursor(MySQLdb.cursors.DictCursor)
				return self._dbconn.cursor()

			self._next_indx += 1
			if (self._next_indx >= len(self.db_cfgs)):
				self._next_indx = 0

			indx_try += 1
		# }}} end while
		self._dbconn = None
		return None

	def connect(self):
		""" (protected) 檢查連線物件是否有效，無效時重新連線
		"""
		if self.ping():
			return self._dbconn.cursor(MySQLdb.cursors.DictCursor)
		self.close()
		self._dbconn = None
		return self._open_connection()

	def close(self):
		try:
			self._dbconn.close()
		except Exception:
			pass
		self._dbconn = None
