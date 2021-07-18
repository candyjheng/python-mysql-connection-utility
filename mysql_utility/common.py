

import time
import random
import logging

from MySQLdb.connections import OperationalError as db_OperationalError

_log = logging.getLogger(__name__)

ATTEMPT_MAX = 8
STOER_RUN_WARN = 6

def store_impl_guard(store_func):
	def _store_impl_guard(dbinstance, *args, **kwds):
		""" 資料儲存函數，呼叫時期防護
		Args:
			store_func - 被呼叫的資料儲存函數，第一個參數需要為資料庫連線物件
			dbconn - 資料庫連線物件
			*args, **kwds - 要傳給 store_func 的其他參數
		Return:
			store_func 的傳回值
		"""
		for attempt in range(ATTEMPT_MAX):
			try:
				aux = store_func(dbinstance, *args, **kwds)
				return aux
			except db_OperationalError as db_e:
				log_args = ("failed on store function [%r]: %r (attempt=%r)", store_func, db_e, attempt)
				if attempt < STOER_RUN_WARN:
					_log.warning(*log_args)
				else:
					_log.exception(*log_args)
			# }}} end except db_OperationalError
			try:
				time.sleep(1 + random.randint(0, attempt + 1))
			except Exception as e:
				_log.warning("have exception on stops between attempts: %r", e)
		# }}} end for
		# 嘗試次數用盡無法正常寫入資料庫
		raise RuntimeError("failed on store function [%r]" % (store_func,))
	return _store_impl_guard