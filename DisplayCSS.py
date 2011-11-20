import sublime
import sublime_plugin
import re
import os

completions = []

class DisplayCssCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.add_classes_ids()
        self.view.run_command('auto_complete', {'disable_auto_insert': True})
        return

    def add_classes_ids(self):
        
        this_file = self.view.file_name()
        dir_len = this_file.rfind('/') #(for OSX)

        if not dir_len > 0:
            dir_len = this_file.rfind('\\') #(for Windows)

        this_dir = this_file[:(dir_len + 1)] # + 1 for the '/'
        dir_files = os.listdir(this_dir)

        for f in dir_files:
            if ".css" in f:
                filename = this_dir + f
                break

        with open(filename, 'r') as f:
            read_data = f.read()

        classes_ids = re.findall("\.-?[_a-zA-Z]+[_a-zA-Z0-9-]*\s*|\#-?[_a-zA-Z]+[_a-zA-Z0-9-]*\s*", read_data)

        del completions[:]

        for c in classes_ids:
            completions.append(c)
    

class FillAutoComplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        return [(x, x) for x in completions]