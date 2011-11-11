import sublime, sublime_plugin
import re 

class CopyFunctionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sel = self.view.sel()[0]
		word = self.view.word(sel)
		string = self.view.substr(word).strip()		
		regions = self.view.find_all('(?<![\\w])'+re.escape(string)+'\\b')

		for r in regions:
			sel_begin = self.view.word(r).begin()
			prev_end = sel_begin - 2
			prev_word = self.view.substr(self.view.word(prev_end)) + "@"

			if "storage.type" in self.view.scope_name(r.begin() - 2):
				self.view.window().run_command("show_overlay", {"overlay": "goto", "text": prev_word})
				return
		self.view.window().run_command("show_overlay", {"overlay": "goto", "text": "@"})