import logging, json

logger = logging.getLogger("ConfMan")

info = logger.info

class DB:
	def __init__(self, dbname):
		info("Loading database...")
		self.db = json.load(open(dbname))
		self.dbname = dbname
		info(f"Database {dbname} has been loaded!")
	def get(self, var: str):
		try: return self.db[var]
		except KeyError: return None
	def set(self, var: str, data):
		self.db[var] = data
		json.dump(self.db, open(self.dbname, "w"))
	def search(self, data):
		out = None
		for i in self.db:
			info(i)
			info(self.db[i])
			if self.db[i] == data:
				out = self.db[i]
		return out