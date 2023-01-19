import sublime
import sublime_plugin
import os
import re
from fnmatch import fnmatch


class OpenAllMatchesCommand(sublime_plugin.TextCommand):
    def run(self, edit, regex=False):
        callback = lambda search: self.on_done(search, regex)

        if regex:
            prompt = 'Regex search'
        else:
            prompt = 'Search'
        self.view.window().show_input_panel(prompt, '', callback, None, None)

    def on_done(self, search, regex):
        folders = self.view.window().folders()
        files = self.find_files(folders, search, regex)
        window = self.view.window()
        for file in files:
            new_file = window.open_file(file)

            def callback():
                flags = 0
                if not regex:
                    flags |= sublime.LITERAL
                selections = new_file.find_all(search, flags)
                if selections:
                    new_file.sel().clear()
                    for selection in selections:
                        new_file.sel().add(selection)
                    new_file.show(selection)

            sublime.set_timeout(callback, 250)

    def find_files(self, folders, search, regex):
        # Cannot access these settings!!  WHY!?
        # folder_exclude_patterns = self.view.settings().get('folder_exclude_patterns')
        # file_exclude_patterns = self.view.settings().get('file_exclude_patterns')
        folder_exclude_patterns = [".svn", ".git", ".hg", "CVS"]
        file_exclude_patterns = ["*.pyc", "*.pyo", "*.exe", "*.dll", "*.obj", "*.o", "*.a", "*.lib", "*.so", "*.dylib", "*.ncb", "*.sdf", "*.suo", "*.pdb", "*.idb", ".DS_Store", "*.class", "*.psd", "*.db"]

        ret = []
        for folder in folders:
            if not os.path.isdir(folder):
                continue

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
                        try:
                            with open(fullpath, mode='U') as f:
                                from_content = f.read()

                            if not regex and search in from_content:
                                ret.append(fullpath)
                            elif regex and re.search(search, from_content):
                                ret.append(fullpath)
                        except FileNotFoundError:
                            pass
                        except UnicodeDecodeError:
                            sublime.status_message('Could not open "' + fullpath + '"')
        return ret
