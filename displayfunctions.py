import sublime
import sublime_plugin
import re
import os

completions = []
#
#
#  HAS PROBLEM DEALING WITH ' (). '
#  Add fix to 'prev' and 'next' (if prev is '.' - 2)
#
class DisplayFunctionsCommand(sublime_plugin.TextCommand):


    # start at last word.  Get object type, return completions
    # Get object type: if word is not an object (if it's a method), get object type of prev word.  Then set object type as the return type of the current word (method)


    def is_method(self, word):
        word_checker = self.view.substr(word)
        word_prev = self.view.substr(word.begin() - 1)

        if ' ' in word_prev:
            return False
        if ')' in word_checker:
            return True
        if '.' in word_checker:
            return True
        if ')' in word_prev:
            return True
        if '.' in word_prev:
            return True
        return False

    def run(self, edit):

        sel = self.view.sel()[0]
        word = self.view.word(sel.end() - 1)

        self.view.insert(edit, sel.end(), ".")

        if ')' in self.view.substr(sel.begin() - 1):
            word = self.prev(word)
        object_type = self.get_obj_type(word)
        if not 'void' in object_type:
            if self.add_functions(object_type):
                self.view.run_command('auto_complete', {'disable_auto_insert': True})

        return

    def make_filename(self, classname):
        this_file = self.view.file_name()

        dir_len = this_file.rfind('/')  # (for OSX)

        if not dir_len > 0:
            dir_len = this_file.rfind('\\')  # (for Windows)

        this_dir = this_file[:(dir_len + 1)]  # + 1 for the '/'
        return this_dir + classname + ".java"

    def get_package_dir(self):
        return os.path.join(sublime.packages_path(), "Display-Functions")

    def prev(self, word):

        if '.' in self.view.substr(word.begin() - 1):
            num = 3
        else:
            num = 1

        return self.view.word(word.begin() - num)

    def next(self, word):
        return self.view.word(word.end() + 1)

    def get_return_type(self, current_word, method_region):
        method = self.view.substr(method_region)
        filename = self.make_filename(current_word)

        with open(filename, 'r') as f:
            read_data = f.read()
        return_type = re.search('([\w]+)(?=(?![\n\r]+)\s*' + re.escape(method) + ')', read_data)
        return_type = return_type.group()

        return return_type

    def get_obj_type(self, word_region):
        obj_type = None
        prev_word = self.prev(word_region)
        
        #recursive case
        if self.is_method(word_region):
            prev_obj_type = self.get_obj_type(prev_word)
            obj_type = self.get_return_type(prev_obj_type, word_region)
            return obj_type

         # else:
        string = self.view.substr(word_region)
        regions = self.view.find_all('(?<![\\w])' + re.escape(string) + '\\b')
        for r in regions:
            prev_word = self.prev(r)

            if "storage.type" in self.view.scope_name(prev_word.begin()):
                return self.view.substr(prev_word)

    def check_str(self, classname, check_name):
        if classname == check_name:
            check_path = os.path.join(self.get_package_dir(), check_name)
            check_path += '.txt'
            
            with open(check_path, 'r') as f:
                str_fun = f.read().splitlines()
            return str_fun

    #This function will take a classname and return a list of all the class methods
    #Will use find_by_selector(selector)
    def add_functions(self, classname):

        methods = self.check_str(classname, "String")
        methods = self.check_str(classname, "Object")

        if not methods:

            filename = self.make_filename(classname)

            with open(filename, 'r') as f:
                read_data = f.read()
            methods = re.findall("(\w+)\s*\(.*\){", read_data)  # Regex taken from Java.tmLanguage
            comments = re.findall("/\*.*", read_data)

            for c in comments:
                for m in methods:
                    if m in c:
                        methods.remove(m)
        methods = list(set(methods))  # to remove duplicates

        del completions[:]

        for m in methods:
            completions.append(m + "()")

        if methods:
            return True
        return False
    

class FillAutoComplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        return [(x, x) for x in completions]