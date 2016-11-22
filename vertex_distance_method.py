import argparse
#import numpy

from ROOT import *

import BasicConfig
import utils

p = argparse.ArgumentParser()
p.add_argument('-f', '--inputFile', help='input TTree file name')
args = p.parse_args()
input_file_name = args.inputFile

if __name__ == '__main__':
    tfile1 = utils.open_tfile(input_file_name)
    tfile2 = utils.open_tfile(input_file_name)
    tree1 = tfile1.Get('Nominal')
    tree2 = tfile2.Get('Nominal')
    entries = tree1.GetEntries()
    print('Number of Entries = {}'.format(entries))

    flavors = ['data', 'model']
    data = 0
    model = 1
    combs = ['22', '23', '33']
    h_xy = [[TH1F(flavor+'_xy_'+comb, ';Vertex Pair Distance [mm]; Number of Vertices / mm', 250, 0, 250)
             for comb in combs] for flavor in flavors]
    h_z = [[TH1F(flavor+'_z_'+comb, ';Vertex Pair Distance [mm]; Number of Vertices / mm', 250, 0, 250)
             for comb in combs] for flavor in flavors]
    h_3d = [[TH1F(flavor+'_3d_'+comb, ';Vertex Pair Distance [mm]; Number of Vertices / mm', 250, 0, 250)
             for comb in combs] for flavor in flavors]
    #h_model_xy_22 = TH1F('model_xy_22', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 50, 0, 50)
    #h_model_z_22 = TH1F('model_z_22', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 250, 0, 250)
    #h_model_3d_22 = TH1F('model_3d_22', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 250, 0, 250)

    #h_model_xy_23 = TH1F('model_xy_23', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 50, 0, 50)
    #h_model_z_23 = TH1F('model_z_23', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 250, 0, 250)
    #h_model_3d_23 = TH1F('model_3d_23', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 250, 0, 250)

    #h_model_xy_33 = TH1F('model_xy_33', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 50, 0, 50)
    #h_model_z_33 = TH1F('model_z_33', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 250, 0, 250)
    #h_model_3d_33 = TH1F('model_3d_33', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 250, 0, 250)

    for entry in xrange(entries):
        if entry % 100000 == 0:
            print('*****************************')
            print('***** processed ' + str(entry) + ' events')
        # get the next tree in the chain and verify
        ientry = tree1.LoadTree(entry)
        if ientry < 0:
            break
        # copy next entry into memory and verify
        nb = tree1.GetEntry(entry)
        if nb <= 0:
            continue
        for idv, nTracks in enumerate(tree1.DV_nTracks):
            if len(tree1.DV_nTracks) != len(tree1.DV_r):
                print('##########################################')
                print("len(tree1.DV_nTracks) and len(tree1.DV_r) are different for some reason!!!")
                print(entry, len(tree1.DV_nTracks), len(tree1.DV_r))
                continue
            rIndex = utils.get_region(tree1, idv)
            # interested in only vertices of nTracks == 2 or 3
            if nTracks > 3 or not rIndex == 0:
                continue
            vec1 = TVector3(tree1.DV_x[idv], tree1.DV_y[idv], tree1.DV_z[idv])
            # model construction
            for entry2 in xrange(entry+1, entries):
                utils.show_progress(entry2, entries-entry)
                # get the next tree in the chain and verify
                ientry2 = tree2.LoadTree(entry2)
                if ientry2 < 0:
                    break
                # copy next entry into memory and verify
                nb2 = tree2.GetEntry(entry2)
                if nb2 <= 0:
                    continue
                for idv2, nTracks2 in enumerate(tree2.DV_nTracks):
                    if len(tree2.DV_nTracks) != len(tree2.DV_r):
                        print('##########################################')
                        print("len(tree2.DV_nTracks) and len(tree2.DV_r) are different for some reason!!!")
                        print(entry2, len(tree2.DV_nTracks), len(tree2.DV_r))
                        continue
                    rIndex = utils.get_region(tree2, idv2)
                    # interested in only vertices of nTracks == 2 or 3
                    if nTracks2 > 3 or not rIndex == 0:
                        continue
                    vec2 = TVector3(tree2.DV_x[idv2], tree2.DV_y[idv2], tree2.DV_z[idv2])
                    dist_3d = (vec1-vec2).Mag()
                    dist_xy = (vec1-vec2).Perp()
                    dist_z = TMath.Abs((vec1-vec2).Z())
                    sum_nTracks = nTracks + nTracks2
                    h_xy[model][sum_nTracks-4].Fill(dist_xy)
                    h_z[model][sum_nTracks-4].Fill(dist_z)
                    h_3d[model][sum_nTracks-4].Fill(dist_3d)
            # fill data
            nDVs = len(tree1.DV_nTracks)
            if nDVs < 2:
                continue
            for idv2 in range(idv+1, nDVs):
                rIndex = utils.get_region(tree1, idv2)
                nTracks2 = tree1.DV_nTracks[idv2]
                # interested in only vertices of nTracks == 2 or 3
                if nTracks2 > 3 or not rIndex == 0:
                    continue
                vec2 = TVector3(tree1.DV_x[idv2], tree1.DV_y[idv2], tree1.DV_z[idv2])
                dist_3d = (vec1-vec2).Mag()
                dist_xy = (vec1-vec2).Perp()
                dist_z = TMath.Abs((vec1-vec2).Z())
                sum_nTracks = nTracks + nTracks2
                h_xy[data][sum_nTracks-4].Fill(dist_xy)
                h_z[data][sum_nTracks-4].Fill(dist_z)
                h_3d[data][sum_nTracks-4].Fill(dist_3d)
    output_tfile = TFile('output_vertex_distance_method.root', 'recreate')
    for ii in range(len(flavors)):
        for jj in range(len(combs)):
            h_xy[ii][jj].Write()
            h_z[ii][jj].Write()
            h_3d[ii][jj].Write()
    output_tfile.Close()
