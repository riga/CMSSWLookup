# -*- coding: utf-8 -*-

# python imports
import os
import re

# sublime imports
import sublime, sublime_plugin


class CmsswLookupCommand(sublime_plugin.TextCommand):

    def __init__(self, *args, **kwargs):
        super(CmsswLookupCommand, self).__init__(*args, **kwargs)

        self._settings = None

    def run(self, edit):
        # load settings
        print(1, dir(sublime.load_settings("CMSSWLookup.sublime-settings")))
        print(2, dir(self.view.settings()))
        print(3, sublime.load_settings("CMSSWLookup.sublime-settings").has("open_cmd"))
        print(4, self.view.settings().has("open_cmd"))

        if self._settings is None:
            self._settings = sublime.load_settings("CMSSWLookup.sublime-settings")

        # load extensions (lists, 0 -> label, 1 -> postfix (e.g. ".py"))
        extensions = self._settings.get("extensions")
        if not len(extensions):
            self.log("no extensions found")
            return

        labels    = [ext[0] for ext in extensions]
        postfixes = [ext[1] for ext in extensions]

        # lookup callback
        def do_lookup(idx):
            if ~idx:
                self.lookup(self.view, postfixes[idx])

        # > 1 extensions => show quick panel
        if len(extensions) == 1:
            do_lookup(0)
        else:
            self.view.window().show_quick_panel(labels, do_lookup)


    def lookup(self, view, postfix):
        for region in view.sel():
            # the region must not be empty
            if region.empty():
                continue

            # get the selected text
            text = view.substr(region)

            # convert the python-style import path to a url-style path
            path = self.convert_path(text, postfix)

            if not path:
                self.log("no valid path to expand")
            else:
                # build and execute the command
                cmd = " ".join([self._settings.get("open_cmd"), path])
                self.log(cmd)
                os.system(cmd)

            # only use the first non-empty region
            break


    def convert_path(self, path, postfix):
        # simple conversion, e.g. "some.python.file" => "some/python/file.py"
        parts = path.strip().replace("/", ".").split(" ")[0].split(".")

        # we lookup python files, the CMSSW folder structur yields a "python" folder
        # after the second part (module.submodule."python".some.path)
        parts.insert(2, "python")

        # create data for formatting
        data = {
            "branch" : self._settings.get("branch"),
            "path"   : "/".join(parts),
            "postfix": postfix
        }

        return self._settings.get("url_format") % data


    @staticmethod
    def log(*msg):
        print("CMSSW Lookup:", *msg)
