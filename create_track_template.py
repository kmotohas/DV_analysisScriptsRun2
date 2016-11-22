#!/bin/env python

from ROOT import *
import array
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--inputFiles', type=str, help='comma separated input files')
parser.add_argument('-o', '--outputFile', type=str, help='output file name')
args = parser.parse_args()

chain = TChain('Nominal', 'Nominal Tree')
#for input_file in input_files:
chain.Add(args.inputFiles)

print "Writing a tree"

#f = TFile("DVtrkTemplate_tree.root", "recreate")
f = TFile(args.outputFile, "recreate")
t = TTree("DVtrkTemplate", "track template for DVMultiTrkBkg")

# create 1 dimensional float arrays (python's float datatype corresponds to c++ doubles)
# as fill variables
pt = array.array('f', [0.])
eta = array.array('f', [0.])
phi = array.array('f', [0.])
d_eta = array.array('f', [0.])
d_phi = array.array('f', [0.])
region = array.array('i', [0])

# create the branches and assign the fill-variables to them
t.Branch('pt', pt, 'pt/F')
t.Branch('eta', eta, 'eta/F')
t.Branch('phi', phi, 'phi/F')
t.Branch('d_eta', d_eta, 'd_eta/F')
t.Branch('d_phi', d_phi, 'd_phi/F')
t.Branch('region', region, 'region/I')

# create some random numbers, fill them into the fill varibles and call Fill()
entries = chain.GetEntries()
print('* Number of entries = {}'.format(entries))
try:
    for entry in range(entries):
        if not entry % 100000:
            print('*** processed {0} out of {1} ({2}%)'.format(entry, entries, round(float(entry)/entries*100., 1)))
        #if entry == 100000:
        #    break
        # get the next tree in the chain and verify
        ientry = chain.LoadTree(entry)
        if ientry < 0:
            break
        # copy next entry into memory and verify
        nb = chain.GetEntry(entry)
        if nb <= 0:
            continue
        pos_PV = TVector3(chain.PV_x, chain.PV_y, chain.PV_z)
        for idv in range(len(chain.DV_x)):
            region[0] = chain.DV_Region[idv]
            pos_DV = TVector3(chain.DV_x[idv], chain.DV_y[idv], chain.DV_z[idv])
            tlv_DVPV = TLorentzVector()
            tlv_DVPV.SetVect(pos_DV - pos_PV)
            for itrk in range(chain.DV_nTracks[idv]):
                #tlv = TLorentzVector()
                pt[0] = chain.DV_track_pt_wrtSV[idv][itrk]
                eta[0] = chain.DV_track_eta_wrtSV[idv][itrk]
                phi[0] = chain.DV_track_phi_wrtSV[idv][itrk]
                #tlv.SetPtEtaPhiM(pt[0], eta[0], phi[0], 139.57/1e3)
                d_eta[0] = eta[0] - tlv_DVPV.Eta()
                d_phi[0] = phi[0] - tlv_DVPV.Phi()
                t.Fill()
except KeyboardInterrupt:
    pass

# write the tree into the output file and close the file
f.Write()
f.Close()
