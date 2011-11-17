import sublime
import sublime_plugin
import re

completions = []

class CopyFunctionCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        sel = self.view.sel()[0]
        word = self.view.word(sel.end() - 1)
        string = self.view.substr(word).strip()
        regions = self.view.find_all('(?<![\\w])' + re.escape(string) + '\\b')

        #self.view.insert(edit, sel.end(), ".") # this is for when the plugin is eventually mapped to "."

        for r in regions:
            prev_end = r.begin() - 2
            prev_word = self.view.word(prev_end)

            print self.view.substr(prev_word)
            if "storage.type" in self.view.scope_name(prev_word.begin()):
                print "Class: " + self.view.substr(prev_word)
                self.add_functions(prev_word)

                break
        
        self.view.run_command('auto_complete', {'disable_auto_insert': True})
        return

    #This function will take a classname and return a list of all the class methods
    #Will use find_by_selector(selector)
    def add_functions(self, classname):
        completions.append("")
    

class FillAutoComplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        return [(x, x) for x in completions]