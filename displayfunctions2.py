import sublime
import sublime_plugin
import re
import os

completions = []

class DisplayFunctionsCommand(sublime_plugin.TextCommand):

    # while previous word is a method
    # go back && count ++

    # now have root word

    # get type of root
    #while less than count
    #   open up file
    #   get return type of next method

    #open up file and get methods...
    #

    def run(self, edit):

        sel = self.view.sel()[0]
        word = self.view.word(sel.end() - 1)
        #string = self.view.substr(word).strip()
        count = 0

        prev_word = self.prev(word)

        print self.view.substr(prev_word)

        return

        while "meta.method" in self.view.scope_name(prev_word.begin()):
            prev_word = self.prev(prev_word)
            count = count + 1
        
        root = prev_word

        return

        return_type = self.get_type(root)

        i = 0
        while i < count:
            filename = self.make_filename(return_type)
            with open(filename, 'r') as f:
                read_data = f.read()
            return_type = re.search('(\w+)\W+\w+$', read_data)
            print return_type

        self.add_functions(return_type)

    def make_filename(self, classname):
        this_file = self.view.file_name()

        dir_len = this_file.rfind('/') #(for OSX)

        if not dir_len > 0:
            dir_len = this_file.rfind('\\') #(for Windows)

        this_dir = this_file[:(dir_len + 1)] # + 1 for the '/'
        return this_dir + classname + ".java"

    def get_package_dir(self):
        return os.path.join(sublime.packages_path(), "Display-Functions")

    def prev(self, word):
        return self.view.word(word.begin() - 2)

    def next(self, word):
        return self.view.word(word.end() + 2)

    def get_type(self, current_word):
        string = self.view.substr(current_word)
        regions = self.view.find_all('(?<![\\w])' + re.escape(string) + '\\b')
        for r in regions:
            prev_word = self.prev(r)
            print self.view.substr(prev_word)

            if "storage.type" in self.view.scope_name(prev_word.begin()):
                return self.view.substr(prev_word)

    def check_str(self, classname, check_name):
        if classname == check_name:
            check_path = os.path.join(self.get_package_dir(), check_name)
            check_path += '.txt'
            print check_path
            
            with open(check_path, 'r') as f:
                str_fun = f.read().splitlines()
            return str_fun

    #This function will take a classname and return a list of all the class methods
    #Will use find_by_selector(selector)
    def add_functions(self, classname):

        methods = self.check_str(classname, "String")

        if not methods:

            filename = self.make_filename(classname)

            with open(filename, 'r') as f:
                read_data = f.read()
            methods = re.findall("(\w+)\s*\(", read_data) #Regex taken from Java.tmLanguage

        methods = list(set(methods)) #to remove duplicates

        del completions[:]

        for m in methods:
            m.strip('h')
            completions.append(m + "()")
    

class FillAutoComplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        return [(x, x) for x in completions]