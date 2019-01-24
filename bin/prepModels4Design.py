interface 	= [10,12,14,16,18,21,23]
chSet		= ['H','G','F','E']
import os,sys, numpy as np
from prody import *
from PDButil import UnNatAA

# run this from current working dir


for pdb in sorted( [x for x in  os.listdir( sys.argv[1] ) if 'pdb' in x] ):

	pdbname = pdb
	workDir = pdbname[:-4]
	if not os.path.exists( workDir ):
		os.mkdir(workDir)

	print pdbname
	# grab 2 closest amyloid chains middle helix (chain Y) to make ASU
	pdb 	= parsePDB( pdb, chain='YEFGH' )

	chY 	= pdb.select('chid Y')
	Nz 		= pdb.select('name NZ')

	# find distance between each Nz and the closest atom on chain Y helix
	dList = [np.min(x) for x in buildDistMatrix(Nz, chY)]
	#return index of number 1 and 2 closest Nz's; assume it is NOT ending index 0 and not 3... 
	min_index1 = dList.index(min(dList))
	if dList[min_index1 + 1] > dList[min_index1 - 1]:
		min_index2 = min_index1 - 1
	else:
		min_index2 = min_index1 +1
	# return chains of these 1st and 2nd closest Nz atoms, as seperate atom groups
	chz = [ chSet[x] for x in sorted( [ min_index1, min_index2 ] ) ]
	ch1, ch2 = pdb.select('chid %s' % chz[0]).copy(), pdb.select('chid %s' % chz[1]).copy()

	# rename these chains E & F
	ch1.setChids( ['E' for a in ch1.getChids() ]  )
	ch2.setChids( ['F' for a in ch2.getChids() ]  )


	# put chains 'em together
	newAtomGroup = ch1 + ch2 + chY.copy()

	# renumber by 
	for n, r in enumerate(newAtomGroup.iterResidues(), 1):
		r.setResnum(n)
	writePDB( os.path.join( workDir, pdbname), newAtomGroup)

	print newAtomGroup.select('ca chid E F '), len(newAtomGroup.select('ca chid E F '))
	# write C-alpha restraints file into this directory.... 
	# copy resfile & design .py & .xml manually
	txt = ''
	for a in newAtomGroup.select('ca chid E F '):

		xyz = '%.4f %.4f %.4f' % (tuple(a.getCoords()) )
		txt += 'CoordinateConstraint CA  %d  N 1 %s HARMONIC 0.0 0.8\n' % (a.getResnum(), xyz)

	cstFile = open( os.path.join( workDir, 'constraints.txt'), 'w')
	cstFile.write(txt)
	cstFile.close()



	