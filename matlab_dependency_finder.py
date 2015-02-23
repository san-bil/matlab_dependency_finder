import os
import sys
import shutil
import subprocess
import graphviz as gv
import argparse

def plot_2tuples_as_graph(graph, file_name):
    g1 = gv.Digraph(format='svg')
    for edge in graph:
        g1.node(edge[0])
        g1.node(edge[1])
        g1.edge(edge[0], edge[1])
    g1.render(filename=file_name)

def top_level_dirname(path):
    return path.split("/")[0]


if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Graph dependencies for a matlab project. Requires graphviz package (sudo apt-get install graphviz) and graphviz-python wrapper (pip install graphviz)')
    parser.add_argument('-f','--callers_folder', help='folder containing caller functions')
    parser.add_argument('-t','--callees_folder', help='folder containing callee functions')
    parser.add_argument('-g','--graph_path',help='path to plot dependency graph image to', default='')
    parser.add_argument('-d','--caller_details',default='',help='caller packages to print individual dependencies for (use option last due to indefinite size)', nargs=argparse.REMAINDER)        

    args = parser.parse_args()
    arg_dict = vars(args)
    callers_tld = arg_dict['callers_folder']
    callees_tld = arg_dict['callees_folder']    
    output_graph_path = arg_dict['graph_path']
    caller_details = arg_dict['caller_details']
    
    
    all_files = subprocess.check_output("find %s -type f -not -iwholename '*.git' " % callees_tld, shell=True)
    all_files_array = all_files.split('\n')
    func_names = [ os.path.splitext(os.path.split(func)[1])[0] for func in all_files_array ] 
    
    file_delimiter = '----------------'
    cmd_string = './mda_finder.sh ' + callers_tld
    f_calls = subprocess.check_output(cmd_string, shell=True).split(file_delimiter)
    file_dep_graph = set([])
    
    for idx,used_f in enumerate(func_names):
        if not used_f == '':
            for idx3,caller_file in enumerate(f_calls):
                caller_file_lines = caller_file.split("\n")
                if len(caller_file_lines)>1:
                    caller_file_path = caller_file_lines[1]
                    for idx2,f_call in enumerate(caller_file_lines[2:]):
                        if ((used_f+'(') in f_call) or ((used_f+'( ') in f_call) or ((used_f+'(  ') in f_call):
                            file_dep_graph.add((caller_file_path, all_files_array[idx], f_call))

    
    f_d_g = list(file_dep_graph)
    package_dep_graph=set([])
    for fdg_node in f_d_g:
        tmp_caller = top_level_dirname(os.path.relpath(fdg_node[0],callers_tld))
        tmp_callee = top_level_dirname(os.path.relpath(fdg_node[1],callees_tld))

        if not tmp_callee==tmp_caller:
            if tmp_caller in sys.argv[4:]:
                print os.path.relpath(fdg_node[0],callees_tld)+'   ---->   '+os.path.relpath(fdg_node[1],callers_tld)            
            package_dep_graph.add((tmp_caller,tmp_callee))
        
        
    pdg = list(package_dep_graph)
    
    if not output_graph_path=='':
        plot_2tuples_as_graph(pdg, output_graph_path)

