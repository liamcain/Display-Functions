import sublime
import sublime_plugin
import re

completions = []

class DisplayFunctionsCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        sel = self.view.sel()[0]
        word = self.view.word(sel.end() - 1)
        string = self.view.substr(word).strip()
        regions = self.view.find_all('(?<![\\w])' + re.escape(string) + '\\b')

        self.view.insert(edit, sel.end(), ".") # this is for when the plugin is eventually mapped to "."

        for r in regions:
            prev_end = r.begin() - 2
            prev_word = self.view.word(prev_end)

            if "storage.type" in self.view.scope_name(prev_word.begin()):
                print "Class: " + self.view.substr(prev_word)
                self.add_functions(self.view.substr(prev_word))

                self.view.run_command('auto_complete', {'disable_auto_insert': True})
                break
        
        return

    #This function will take a classname and return a list of all the class methods
    #Will use find_by_selector(selector)
    def add_functions(self, classname):
        
        this_file = self.view.file_name()
        print this_file
        
        dir_len = this_file.rfind('/') #(for OSX)

        if not dir_len > 0:
            dir_len = this_file.rfind('\\') #(for Windows)

        this_dir = this_file[:(dir_len + 1)] # + 1 for the '/'
        filename = this_dir + classname + ".java"

        print filename

        with open(filename, 'r') as f:
            read_data = f.read()
        methods = re.findall("(\w+)\s*\(\)", read_data) #Regex taken from Java.tmLanguage (needs fix)

        methods = list(set(methods)) #to remove duplicates

        print 'methods: '
        print methods

        del completions[:]

        for m in methods:
            completions.append(m + "()")
    

class FillAutoComplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        return [(x, x) for x in completions]