import argparse

from ROOT import *

import BasicConfig
import utils

p = argparse.ArgumentParser()
p.add_argument('-f', '--inputFile', help='input TTree file name')
args = p.parse_args()
input_file_name = args.inputFile

def get_2track_mass_from_3track_dv(tree, idv, hist):
    mass_pion = 139.57*0.001  # [GeV]

    combinations = [(0, 1), (1, 2), (2, 0)]
    for combination in combinations:
        tlv0 = TLorentzVector()
        tlv1 = TLorentzVector()
        tlv2 = TLorentzVector()
        tlv0.SetPtEtaPhiM(tree.DV_track_pt_wrtSV[idv][combination[0]],
                          tree.DV_track_eta_wrtSV[idv][combination[0]],
                          tree.DV_track_phi_wrtSV[idv][combination[0]],
                          mass_pion)
        tlv1.SetPtEtaPhiM(tree.DV_track_pt_wrtSV[idv][combination[1]],
                          tree.DV_track_eta_wrtSV[idv][combination[1]],
                          tree.DV_track_phi_wrtSV[idv][combination[1]],
                          mass_pion)
        tlv2 = tlv0 + tlv1
        #print tlv2.M()
        hist.Fill(tlv2.M())


if __name__ == '__main__':
    h_mass_2 = [
        TH1F('mass_2_region'+str(region), ';DV Mass [GeV]; Number of Vertices', 10000, 0, 10)
        for region in range(12)
        ]
    h_mass_2_in_3 = [
        TH1F('mass_2_in_3_region'+str(region),';DV Mass [GeV]; Number of Vertices', 10000, 0, 10)
        for region in range(12)
    ]
    input_tfile = utils.open_tfile(input_file_name)
    tree = input_tfile.Get('Nominal')
    entries = tree.GetEntries()
    for entry in range(entries):
        if entry % 10000 == 0:
            print('*** processed {0} out of {1}'.format(entry, entries))
        # get the next tree in the chain and verify
        ientry = tree.LoadTree(entry)
        if ientry < 0:
            break
        # copy next entry into memory and verify
        nb = tree.GetEntry(entry)
        if nb <= 0:
            continue

        for idv, nTracks in enumerate(tree.DV_nTracks):
            rIndex = utils.get_region(tree, idv)
            if rIndex < 0:
                continue
            if not tree.DV_passFidCuts[idv] or not tree.DV_passChisqCut[idv] or not tree.DV_passDistCut[idv]:
                continue
            if nTracks == 2:
                h_mass_2[rIndex].Fill(tree.DV_m[idv])
            elif nTracks == 3:
                get_2track_mass_from_3track_dv(tree, idv, h_mass_2_in_3[rIndex])
            else:
                continue
            #print('3-track mass = ' + str(tree.DV_m[idv]))
    output_tfile = TFile('output_ks_method.root', 'recreate')
    for region in range(12):
        h_mass_2[region].Write()
        h_mass_2_in_3[region].Write()
    output_tfile.Close()
