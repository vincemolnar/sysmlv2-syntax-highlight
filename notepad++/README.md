# Notepad++

User Defined Language files for Notepad++:

| File | Language | Colours |
|---|---|---|
| `SysML-v2.udl.xml` | SysML v2 (`*.sysml`) | light themes |
| `SysML-v2.dark.udl.xml` | SysML v2 (`*.sysml`) | dark mode |
| `KerML.udl.xml` | KerML (`*.kerml`) | light themes |
| `KerML.dark.udl.xml` | KerML (`*.kerml`) | dark mode |

To install, copy one file per language into the `userDefineLangs` folder
(**Language > User Defined Language > Open User Defined Language folder...**)
and restart Notepad++, or use **Import...** in the **Define your language**
dialog. Install either the light or the dark file of a language, not both, as
they claim the same file extension.

The light files use the colours of the Eclipse editor of the SysML v2 Pilot
Implementation, the dark ones the colours of Notepad++'s dark theme. Default text
and the background follow the active theme.

The files are generated from the keyword lists in [`../spec`](../spec) by
`build.py`; edit that script, not the XML.
