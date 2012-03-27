import sublime
import sublime_plugin
import re
import os.path

completions = []

class DisplayFunctionsCommand(sublime_plugin.TextCommand):

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
        if object_type:
            if self.add_functions(object_type):
                self.view.run_command('auto_complete', {
                'disable_auto_insert': True,
                'api_completions_only': True,
                'next_competion_if_showing': False
                })
                

    def make_filename(self, classname):
        this_file = self.view.file_name()

        dir_len = this_file.rfind('/')  # (for OSX)

        if not dir_len > 0:
            dir_len = this_file.rfind('\\')  # (for Windows)

        this_dir = this_file[:(dir_len + 1)]  # + 1 for the '/'
        return this_dir + classname + ".java"

    def get_package_dir(self):
        return os.path.join(sublime.packages_path(), "Display Functions (Java)")

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
        
        if 'super' in self.view.substr(word_region):
            extend = self.view.find('extends', 0)
            return self.view.substr(self.next(extend))

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


    def add_functions_helper(self, classname):
        filename = self.make_filename(classname)
        with open(filename, 'r') as f:
            read_data = f.read()
 
        methods = []
        method_lines = re.findall('public.*|protected.*', read_data)

        for l in method_lines:
            s = re.search('(\w+)\s*\(.*\)(?=.*\{)', l)
            if s:
                methods.append(s.group().strip())

        comments = re.findall("/\*.*", read_data)
        superclass = re.search("extends\s*(\w*)", read_data)

        print filename

        if superclass:
            superclass = superclass.group()
            superclass = superclass[8:]
            for m in self.add_functions_helper(superclass):
                methods.append(m)

        for c in comments:  # remove commented out methods from list
            for m in methods:
                if m in c:
                    methods.remove(m)
        
        return methods


    #Takes a classname and returns a list of all the class methods
    def add_functions(self, classname):
        methods = self.check_str(classname, "String")
        if not methods:
            methods = self.check_str(classname, "Object")

        if not methods:
            methods = self.add_functions_helper(classname)

        for m in methods:
            completions.append(m)

        if methods:
            return True
        return False
    
class FunctionsAutoComplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        _completions = []
            
        for c in list(set(completions)):
            c_snip = c
            params = re.findall('\w+\s+\w+(?=\)|,)',c_snip)
            num = 1
            for p in params:
                c_snip = c_snip.replace(p, '${' + str(num) + ':' + p + '}')
                num = num + 1
            _completions.append((c, c_snip))

        del completions[:]
        # return (x,x) for x in sorted(_completions)
        return sorted(_completions)
