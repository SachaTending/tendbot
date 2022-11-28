import json, loguru

info = loguru.logger.info

class Bundle():
	def __init__(self):
		self.bundledb = json.load(open("bundledb.json"))
		self.cached = {}
	def get(self, servid=0, target=""):
		lang = self.bundledb.get(servid, "en_US")
		l = self.getbundlelang(lang)
		info(l)
		return l.get(target, target)
	def getbundlelang(self, lang):
		if lang in self.cached:
			info(1)
			lng = hash(open(f"bundles/{lang}.bundle").read())
			if self.cached[lang]['hash'] != lng:
				lng = self.parselang(lang)
				info(2)
				self.cached[lang]['hash'] = hash(open(f"bundles/{lang}.bundle").read())
				self.cached[lang]['lang'] = lng
				return self.cached[lang]['lang']
			else:
				return self.cached[lang]['lang']
		else:
			try:
				l = self.parselang(lang)
				self.cached[lang] = {}
				info(3)
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
