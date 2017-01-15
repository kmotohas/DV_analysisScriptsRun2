#!/usr/bin/env python

from ROOT import *
import array
import argparse

import utils

#def basic_event_selection(tree):
#    # [1: Trigger, 2: Filter, 3: Cleaning, 4: GRL,
#    #  5: PV, 6: MET, 7: DV Selection]
#    return tree.PassCut3 and tree.PassCut4 and tree.PassCut5
#
#
#def basic_dv_selection(tree, idv):
#    #return tree.DV_passFidCuts[idv] and tree.DV_passChisqCut[idv] and tree.DV_passDistCut[idv]
#    #return tree.DV_passFidCuts[idv] and tree.DV_passChisqCut[idv] and tree.DV_passDistCut[idv] and tree.DV_passMatVeto[idv]
#    #return tree.DV_passFidCuts[idv] and tree.DV_passChisqCut[idv] and tree.DV_passDistCut[idv] and tree.DV_passMatVeto2016[idv]
#    return tree.DV_passFidCuts[idv] and tree.DV_passChisqCut[idv] and tree.DV_passDistCut[idv] and tree.DV_passDisabledModuleVeto[idv] and tree.DV_passMatVeto2p1[idv]


#if __name__ == '__main__':
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--inputFiles', type=str, help='comma separated input files')
    parser.add_argument('-o', '--outputFile', type=str, help='output file name')
    args = parser.parse_args()
    #
    print "Writing a tree"
    #
    #f = TFile("DVtrkTemplate_tree.root", "recreate")
    f = TFile(args.outputFile, "recreate")
    t = TTree("DVtrkTemplate", "track template for DVMultiTrkBkg")
    #
    # create 1 dimensional float arrays (python's float datatype corresponds to c++ doubles)
    # as fill variables
    pt = array.array('f', [0.])
    eta = array.array('f', [0.])
    phi = array.array('f', [0.])
    d_eta = array.array('f', [0.])
    d_phi = array.array('f', [0.])
    dv_r = array.array('f', [0.])
    dv_z = array.array('f', [0.])
    dv_phi = array.array('f', [0.])
    dv_eta = array.array('f', [0.])
    dv_nTracks = array.array('i', [0])
    dv_m = array.array('f', [0.])
    region = array.array('i', [0])
    met = array.array('f', [0.])
    #
    # create the branches and assign the fill-variables to them
    t.Branch('pt', pt, 'pt/F')
    t.Branch('eta', eta, 'eta/F')
    t.Branch('phi', phi, 'phi/F')
    t.Branch('d_eta', d_eta, 'd_eta/F')
    t.Branch('d_phi', d_phi, 'd_phi/F')
    t.Branch('dv_r', dv_r, 'dv_r/F')
    t.Branch('dv_z', dv_z, 'dv_z/F')
    t.Branch('dv_phi', dv_phi, 'dv_phi/F')
    t.Branch('dv_eta', dv_eta, 'dv_eta/F')
    t.Branch('dv_nTracks', dv_nTracks, 'dv_nTracks/I')
    t.Branch('dv_m', dv_m, 'dv_m/F')
    t.Branch('region', region, 'region/I')
    t.Branch('met', met, 'met/F')
    #
    chain = TChain('Nominal', 'Nominal Tree')
    #for input_file in input_files:
    chain.Add(args.inputFiles)
    # create some random numbers, fill them into the fill varibles and call Fill()
    entries = chain.GetEntries()
    #print('* Number of entries = {}'.format(entries))
    try:
        for entry in range(entries):
            #if not entry % 100000:
            #    print('*** processed {0} out of {1} ({2}%)'.format(entry, entries, round(float(entry)/entries*100., 1)))
            utils.show_progress(entry, entries)
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
            if chain.EventNumber == 752668466:
                continue
            if not utils.basic_event_selection(chain):
                continue
            pos_PV = TVector3(chain.PV_x, chain.PV_y, chain.PV_z)
            for idv in range(len(chain.DV_x)):
                if not utils.basic_dv_selection(chain, idv):
                    continue
                region[0] = chain.DV_Region[idv]
                pos_DV = TVector3(chain.DV_x[idv], chain.DV_y[idv], chain.DV_z[idv])
                dv_m[0] = chain.DV_m[idv]
                dv_r[0] = pos_DV.Perp()
                dv_z[0] = pos_DV.Z()
                dv_phi[0] = pos_DV.Phi()
                dv_eta[0] = pos_DV.Eta()
                #if chain.DV_nTracks[idv] < 3 or (chain.DV_Region[idv] in [-1, 1, 3, 5, 7, 9]):
                #if chain.DV_nTracks[idv] < 3 or chain.DV_Region[idv] < 0 or chain.DV_m[idv] < 3:
                if chain.DV_Region[idv] < 0 or chain.DV_m[idv] < 2:
                #if chain.DV_nTracks[idv] < 3 or chain.DV_Region[idv] < 0:
                #if chain.DV_Region[idv] in [-1, 1, 3, 5, 7, 9]:
                    continue
                dv_nTracks[0] = chain.DV_nTracks[idv]
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


if __name__ == '__main__':
    main()
