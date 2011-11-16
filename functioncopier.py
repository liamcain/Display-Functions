import sublime
import sublime_plugin
import re

completions = []

class CopyFunctionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sel = self.view.sel()[0]
        word = self.view.word(sel)
        string = self.view.substr(word).strip()
        regions = self.view.find_all('(?<![\\w])' + re.escape(string) + '\\b')

        self.view.insert(edit, sel.end(), ".")

        for r in regions:
            sel_begin = self.view.word(r).begin()
            prev_end = sel_begin - 2
            prev_word = self.view.substr(self.view.word(prev_end))

            if "storage.type" in self.view.scope_name(r.begin() - 2):
                for method in get_methods(prev_word):
                    completions.append(method)
        self.view.run_command('auto_complete', {'disable_auto_insert': True})
    
    def get_methods(prev_word):
        

class FillAutoComplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        id = view.id()
        if id in completions:
            _completions = completions[id]
            del completions[id]
            return _completions
        return []