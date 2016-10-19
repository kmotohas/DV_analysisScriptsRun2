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


def GetRegion(tree, idv):
    rDV = tree.DV_r[idv]
    nonMaterial = tree.DV_passMatVeto[idv]
    rIndex = -1

    if     (rDV<22.  and nonMaterial):
        rIndex = 0   # inside beampipe
    elif(rDV<25.  and not nonMaterial):
        rIndex = 1   # on beampipe
    elif(rDV<29.  and nonMaterial):
        rIndex = 2   # inside IBL
    elif(rDV<38.  and not nonMaterial):
        rIndex = 3   # around IBL
    elif(rDV<46.  and nonMaterial):
        rIndex = 4   # inside B-Layer
    elif(rDV<73.  and not nonMaterial):
        rIndex = 5   # around B-Layer
    elif(rDV<84.  and nonMaterial):
        rIndex = 6   # inside Layer-1
    elif(rDV<111. and not nonMaterial):
        rIndex = 7   # around Layer-1
    elif(rDV<120. and nonMaterial):
        rIndex = 8   # inside Layer-2
    elif(rDV<145. and not nonMaterial):
        rIndex = 9   # around Layer-2
    elif(rDV<180. and nonMaterial):
        rIndex = 10  # inside octagonal support
    elif(rDV<300. and nonMaterial):
        rIndex = 11  # inside/around 1st SCT Layer

    return rIndex


if __name__ == '__main__':
    h_mass_2 = [
        TH1F('mass_2_region'+str(region), ';DV Mass [GeV]; Number of Vertices', 10000, 0, 10)
        for region in range(12)
        ]
    h_mass_2_in_3 = [
        TH1F('mass_2_in_3_region'+str(region),';DV Mass [GeV]; Number of Vertices', 10000, 0, 10)
        for region in range(12)
    ]
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
            rIndex = GetRegion(tree, idv)
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
    output_tfile = TFile('output_tfile.root', 'recreate')
    for region in range(12):
        h_mass_2[region].Write()
        h_mass_2_in_3[region].Write()
    output_tfile.Close()
