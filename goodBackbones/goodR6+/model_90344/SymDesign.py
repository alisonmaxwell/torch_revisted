# python SymDesign.py ~/rosetta/ model_90344.pdb sym_fr_noLayers.xml resfileHand.txt constraints.txt handOutLayers/
#better sym_fr_noLayers.xml

### python SymDesign.py ~/rosetta/ model_90344.pdb sym_fr.xml resfileHand.txt constraints.txt handOutputs/
 

# 1) path 2 rosetta main
# 2) path to input structure file
# 3) path to XML script for protocol
# 4) resfile
# 5) constraint file for backbone atom minimization
import sys, os, subprocess as sp, re


################## MAIN #######################
# Non-variable args
rosetta_database_path   = os.path.join( sys.argv[1] , 'database/' )
rosetta_scriptsEXE_path = os.path.join( sys.argv[1], 'source/bin/rosetta_scripts.macosclangrelease' )
design_script_path      = sys.argv[3]
struc_path 				= sys.argv[2]
resfile_path			= sys.argv[4]
cst_path				= sys.argv[5]

# Variable args

output_prefix			= sys.argv[6]
try:
	output_suffix 			= '_out%s' % (str(  os.environ["SGE_TASK_ID"]) )
except KeyError:
	output_suffix                      = '_out%s' % ( 'Local' )

cmd = [
		rosetta_scriptsEXE_path,
		'-database', rosetta_database_path,
		'-parser:protocol', design_script_path,
		'-in:file:s', struc_path,
		'-out:prefix', output_prefix,   
		'-out:suffix', output_suffix,                               
		'-out:no_nstruct_label',
		'-out:overwrite',
		'-out:nstruct', '10',
		'-use_input_sc', '-ignore_zero_occupancy', 'false',
        '-packing:resfile', resfile_path,
		'-parser:script_vars', 'cst_file=%s' % ( cst_path )
]

print
print ' '.join(cmd)
print

sp.call( cmd )
