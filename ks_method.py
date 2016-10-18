from ROOT import *

import BasicConfig
import utils


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
    h_mass_2 = TH1F('mass_2', ';DV Mass [GeV]; Number of Vertices', 10000, 0, 10)
    h_mass_2_in_3 = TH1F('mass_2_in_3', ';DV Mass [GeV]; Number of Vertices', 10000, 0, 10)
    input_tfile = utils.open_tfile(BasicConfig.rootcoredir + 'systTree.root')
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
            if nTracks == 2:
                h_mass_2.Fill(tree.DV_m[idv])
            elif nTracks == 3:
                get_2track_mass_from_3track_dv(tree, idv, h_mass_2_in_3)
            else:
                continue
            #print('3-track mass = ' + str(tree.DV_m[idv]))
    output_tfile = TFile('output_tfile.root', 'recreate')
    h_mass_2.Write()
    h_mass_2_in_3.Write()
    output_tfile.Close()
