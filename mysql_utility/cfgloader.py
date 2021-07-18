# -*- coding: utf-8 -*-
""" MySQL 資料庫設定讀取函式 """

import logging
from collections import namedtuple

_log = logging.getLogger(__name__)

DataBaseConfigure = namedtuple("DataBaseConfigure", ("host", "schema", "user", "passwd", "socket", "port",))

def _get_socket_from_cmap(cmap):
	for socket_key in ('socket', 'socket-path', 'socket_path', 'Socket', 'SocketPath'):
		r = cmap.get(socket_key)
		if r:
			return r
	return None

def _parser_configure(cmap):
	host = cmap['host']
	schema = cmap.get('schema')
	user = cmap['user']
	passwd = cmap.get('passwd', None)
	socket = _get_socket_from_cmap(cmap)
	port = cmap.get('port') if not socket else None
	return DataBaseConfigure(host, schema, user, passwd, socket, port)

def load_configure(section: str, cmap: dict):
	""" 讀取資料庫設定檔函式
	Args:
		section - 資料庫設定區塊標頭文字
		cmap - 從設定檔讀出之字典物件，其中 key 為 section 內容
	"""
	cmap = cmap.get(section)
	if cmap is None:
		_log.error("Can't get db-confugre, name: %r, from configure struct: %r", section, cmap)
		return None
	try:
		cfgs = []
		if isinstance(cmap, list):
			for c in cmap:
				cfgs.append(_parser_configure(c))
			return cfgs
		if isinstance(cmap, dict):
			cfgs.append(_parser_configure(cmap))
			return cfgs
	except Exception as e:
		_log.error("Configure format not fit: %r", e)
	return None
	