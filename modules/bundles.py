import json, loguru

info = loguru.logger.info

class Bundle():
	def __init__(self):
		self.bundledb = json.load(open("bundledb.json"))
		self.cached = {}
	def get(self, servid=0, target=""):
		lang = self.bundledb.get(servid, "en_US")
		l = self.getbundlelang(lang)
		return l.get(target, target)
	def setlang(self, servid: int=0, lang: str="ru_RU"):
		self.bundledb[servid] = lang
		json.dump(self.bundledb, open("bundledb.json", "w"))
	def getbundlelang(self, lang):
		if lang in self.cached:
			lng = hash(open(f"bundles/{lang}.bundle").read())
			if self.cached[lang]['hash'] != lng:
				lng = self.parselang(lang)
				self.cached[lang]['hash'] = hash(open(f"bundles/{lang}.bundle").read())
				self.cached[lang]['lang'] = lng
				return self.cached[lang]['lang']
			else:
				return self.cached[lang]['lang']
		else:
			try:
				l = self.parselang(lang)
				self.cached[lang] = {}
				self.cached[lang]['hash'] = hash(open(f"bundles/{lang}.bundle").read())
				self.cached[lang]['lang'] = l
				return self.cached[lang]['lang']
			except:
				return {}
	def parselang(self, lang):
		ret = {}
		l = open(f"bundles/{lang}.bundle").read()
		for i in l.split("\n"):
			info(i, l, l.split("\n"))
			ret[i.split(":", maxsplit=1)[0]] = i.split(":", maxsplit=1)[1]
		info(ret)
		return ret
