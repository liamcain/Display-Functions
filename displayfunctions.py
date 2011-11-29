# import sublime
# import sublime_plugin
# import re
# import os

# completions = []

# class DisplayFunctionsCommand(sublime_plugin.TextCommand):
    
#     def run(self, edit):

#         sel = self.view.sel()[0]
#         word = self.view.word(sel.end() - 1)
#         string = self.view.substr(word).strip()

#         if not self.is_proceeding_method(word):

#             regions = self.view.find_all('(?<![\\w])' + re.escape(string) + '\\b')

#             self.view.insert(edit, sel.end(), ".")

#             for r in regions:
#                 prev_end = r.begin() - 2
#                 prev_word = self.view.word(prev_end)

#                 if "storage.type" in self.view.scope_name(prev_word.begin()):
#                     print "Class: " + self.view.substr(prev_word)
#                     self.add_functions(self.view.substr(prev_word))

#                     self.view.run_command('auto_complete', {'disable_auto_insert': True})
#                     break
            
#         return

#     def get_package_dir(self):
#         return os.path.join(sublime.packages_path(), "Display-Functions")


#     def prev(self, word):
#         return self.view.word(word.begin() - 2)
#     def next(self, word):
#         return self.view.word(word.end() + 2)

#     def get_type(self, current_word):
#         string = self.view.substr(current_word)
#         regions = self.view.find_all('(?<![\\w])' + re.escape(string) + '\\b')
#         for r in regions:
#             prev_word = self.prev(r)
#             print self.view.substr(prev_word)

#             if "storage.type" in self.view.scope_name(prev_word.begin()):
#                 return self.view.substr(prev_word)
        

    
#     def is_proceeding_method(self, word):
#         prev_word = self.prev(word)
#         while "storage.type" in self.view.scope_name(prev_word.begin()):
#             prev_word = self.view.word(prev_word.begin() - 2)
#         current_word = prev_word
        
#         word_type = self.get_type(current_word)
#         regions = self.view.find_all('(?<![\\w])' + re.escape(word_type) + '\\b')


#         for r in regions:
#             prev_word = self.prev(r)
#             print self.view.substr(prev_word)

#             if "storage.type" in self.view.scope_name(prev_word.begin()):
#                 print "method"
#                 with open(filename, 'r') as f:
#                     read_data = f.read()
#                 current_word = self.next(current_word)
#                 return_type = self.prev(re.find(current_word))
#                 print return_type
#                 return True
                

#     def check_str(self, classname, check_name):
#         if classname == check_name:
#             check_path = os.path.join(self.get_package_dir(), check_name)
#             check_path += '.txt'
#             print check_path
            
#             with open(check_path, 'r') as f:
#                 str_fun = f.read().splitlines()
#             return str_fun

#     #This function will take a classname and return a list of all the class methods
#     #Will use find_by_selector(selector)
#     def add_functions(self, classname):

#         methods = self.check_str(classname, "String")

#         if not methods:
#             this_file = self.view.file_name()

#             dir_len = this_file.rfind('/') #(for OSX)

#             if not dir_len > 0:
#                 dir_len = this_file.rfind('\\') #(for Windows)

#             this_dir = this_file[:(dir_len + 1)] # + 1 for the '/'
#             filename = this_dir + classname + ".java"

#             with open(filename, 'r') as f:
#                read_data = f.read()
#             methods = re.findall("(\w+)\s*\(", read_data) #Regex taken from Java.tmLanguage

#         methods = list(set(methods)) #to remove duplicates

#         del completions[:]

#         for m in methods:
#             m.strip('h')
#             completions.append(m + "()")
    

# class FillAutoComplete(sublime_plugin.EventListener):
#     def on_query_completions(self, view, prefix, locations):
#         return [(x, x) for x in completions]