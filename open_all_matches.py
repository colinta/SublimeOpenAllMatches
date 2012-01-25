import sublime
import sublime_plugin
import os
import re
import codecs
from fnmatch import fnmatch


class OpenAllMatchesCommand(sublime_plugin.TextCommand):
    def run(self, edit, **kwargs):
        e = self.view.begin_edit('open_all_matches')
        regions = [region for region in self.view.sel()]

        # any edits that are performed will happen in reverse; this makes it
        # easy to keep region.a and region.b pointing to the correct locations
        def compare(region_a, region_b):
            return cmp(region_b.end(), region_a.end())
        regions.sort(compare)

        for region in regions:
            error = self.run_each(edit, region, **kwargs)
            if error:
                sublime.status_message(error)
        self.view.end_edit(e)

    def run_each(self, edit, region, regex=False):
        def on_done(search):
            folders = self.view.window().folders()
            files = self.find_files(folders, search, regex)

            for file in files:
                self.view.window().open_file(file)
        if regex:
            prompt = 'Regex search'
        else:
            prompt = 'Search'
        self.view.window().show_input_panel(prompt, '', on_done, None, None)

    def find_files(self, folders, search, regex):
        # Cannot access these settings!!  WHY!?
        # folder_exclude_patterns = self.view.settings().get('folder_exclude_patterns')
        # file_exclude_patterns = self.view.settings().get('file_exclude_patterns')
        folder_exclude_patterns = [".svn", ".git", ".hg", "CVS"]
        file_exclude_patterns = ["*.pyc", "*.pyo", "*.exe", "*.dll", "*.obj", "*.o", "*.a", "*.lib", "*.so", "*.dylib", "*.ncb", "*.sdf", "*.suo", "*.pdb", "*.idb", ".DS_Store", "*.class", "*.psd", "*.db"]

        ret = []
        for folder in folders:
            for file in os.listdir(folder):
                fullpath = os.path.join(folder, file)
                if os.path.isdir(fullpath):
                    # excluded folder?
                    if not len([True for pattern in folder_exclude_patterns if fnmatch(file, pattern)]):
                        ret += self.find_files([fullpath], search, regex)
                else:
                    # excluded file?
                    if not len([True for pattern in file_exclude_patterns if fnmatch(file, pattern)]):
                        # do my search
                        with codecs.open(fullpath, mode='U', encoding='utf-8') as f:
                            from_content = f.read()

                        if not regex and search in from_content:
                            ret.append(fullpath)
                        elif regex and re.search(search, from_content):
                            ret.append(fullpath)
        return ret
