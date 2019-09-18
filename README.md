# CMSSW Lookup Sublime Text 2/3 Plugin

This ST2/3 plugin lets you easily lookup python based CMSSW code from within your config files.


## Usage

1.  (Text-) Select an import path of a CMSSW module, i.e. the path passed to the `process.load` call or the module path of a real python `import`.

2.  Execute the _CMSSW Lookup_ command, e.g. via the command palette.

3.  If a quick panel shows up, select the _lookup type_: you either may want to open a python file or a directory. By default, your webbrowser will open the desired resource on [github.com](https://github.com/cms-sw/cmssw).

![cmsswlookup usage](https://raw.githubusercontent.com/riga/CMSSWLookup/master/img/sh.png)

With the default configuration, the example above opens https://github.com/cms-sw/cmssw/blob/CMSSW_5_3_19/RecoJets/JetProducers/python/ak5GenJets_cfi.py.


## Configuration

This plugin comes with a small number of package settings to guarantee proper results on your OS.

  - `branch`: the branch to want to lookup, defaults to `master`
  - `url_format`: the url format you like to use, defaults to `https://github.com/cms-sw/cmssw/blob/{branch}/{path}`
  - `open_cmd`: the command your OS uses to open websites


## Development

- Source hosted at [GitHub](https://github.com/riga/CMSSWLookup)
- Report issues, questions, feature requests on
[GitHub Issues](https://github.com/riga/CMSSWLookup/issues)
