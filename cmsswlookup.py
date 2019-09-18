# coding: utf-8

import os

import sublime
import sublime_plugin


class CmsswLookupCommand(sublime_plugin.TextCommand):

    PYTHON, OTHER = range(2)
    labels = ["Python", "Other"]

    def __init__(self, *args, **kwargs):
        super(CmsswLookupCommand, self).__init__(*args, **kwargs)

        # store some settings
        settings = sublime.load_settings("CMSSWLookup.sublime-settings")
        self.branch = settings.get("branch")
        self.url_format = settings.get("url_format")
        self.open_cmd = settings.get("open_cmd")

    def run(self, edit):
        self.view.window().show_quick_panel(self.labels, self.lookup)

    def lookup(self, idx):
        if not (0 <= idx < len(self.labels)):
            return

        # do the lookup for all regions
        for region in self.view.sel():
            # the region must not be empty
            if region.empty():
                continue

            # get the selected text
            text = self.view.substr(region)

            # convert the selected text to a URL based
            url = self.create_url(text, idx)

            # open it
            if not url:
                self.log("no valid path to expand")
            else:
                # build and execute the command
                cmd = " ".join([self.open_cmd, url])
                self.log(cmd)
                os.system(cmd)

            # only use the first non-empty region
            break

    def create_url(self, text, idx):
        # create the path based on idx
        if idx == self.PYTHON:
            # "module.subsystem.file" => "module/subsystem/python/file.py"
            parts = text.strip().replace("/", ".").split(" ")[0].split(".")
            parts.insert(2, "python")
            path = "/".join(parts) + ".py"
        elif idx == self.OTHER:
            path = text
        else:
            raise Exception("unknown choice for index {}".format(idx))

        return self.url_format.format(branch=self.branch, path=path)

    @staticmethod
    def log(*msg):
        print("CMSSWLookup: " + " ".join(str(s) for s in msg))
