# matlab_dependency_finder

Finds dependencies between "packages" in a Matlab project (structured in a certain way) and render to a graph. A package is assumed to be a directory **directly** underneath the callers_folder or the callees_folder. I.E. it only outputs dependencies one directory deep from the root folder specified.

Example usage:
A project structured as:

  - src/
    + component_1/
    + component_2/
  - deps/
    + dep_1/
    + dep_2/
    + dep_3/
    + dep_4/
    
where e.g. component_2 uses {dep_1, dep_2, dep_4}, and component_1 uses dep_2.

python matlab_dependency_finder -f /path/to/src -t /path/to/deps -g /path/to/dep_graph.svg -d component_2

will draw a graph with the listed dependencies, and will also print every outgoing dependency of component_2 at the file-level to stdout (e.g "src/component_1/fubar.m -------> deps/dep_2/foo.m" )


Requires the graphviz package and the python wrapper, which can be installed using (on Ubuntu) apt-get and pip, respectively.
No guarantee that it catches all dependencies, as it's just using grepping instances of "foo\(|foo\( |foo\(  " in the callers_folder, and matching them to filenames in the callees_folder. No proper grammar parsing, though I'm not sure how easy that'd be considering Matlab syntax.
