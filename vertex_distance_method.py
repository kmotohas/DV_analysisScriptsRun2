#!/bin/env python

import argparse
#import numpy

from ROOT import *

#import BasicConfig
import utils

p = argparse.ArgumentParser()
p.add_argument('-f', '--inputFile', help='input TTree file name')
p.add_argument('-o', '--outputFile', help='output histogram file name')
p.add_argument('-m', '--doModel', help='construct model', action='store_true')
args = p.parse_args()
input_file_name = args.inputFile
output_file_name = args.outputFile


#def basic_event_selection(tree):
#    # [1: Trigger, 2: Filter, 3: Cleaning, 4: GRL,
#    #  5: PV, 6: MET, 7: DV Selection]
#    #return tree.PassCut3 and tree.PassCut4 and tree.PassCut5
#    return tree.PassCut3 and tree.PassCut4 and tree.PassCut5 and PassNCBVeto(tree)
#
#
#def basic_dv_selection(tree, idv):
#    #return tree.DV_passFidCuts[idv] and tree.DV_passChisqCut[idv] and tree.DV_passDistCut[idv] and tree.DV_passMatVeto[idv]
#    #return tree.DV_passFidCuts[idv] and tree.DV_passChisqCut[idv] and tree.DV_passDistCut[idv] and tree.DV_passMatVeto2016[idv]
#    return tree.DV_passFidCuts[idv] and tree.DV_passChisqCut[idv] and tree.DV_passDistCut[idv] and tree.DV_passDisabledModuleVeto[idv] and tree.DV_passMatVeto2p1[idv]
#
#
#def PassNCBVeto(tree):
#    #idx = get_index_of_leading_jet(tree)
#    #if idx < 0:
#    #    return True
#    #else:
#    #    return (tree.Jet_EMFrac[idx] < 0.96 and tree.Jet_FracSamplingMax < 0.8)
#    if tree.Jet_n > 0:
#        return (tree.Jet_EMFrac[0] < 0.96 and tree.Jet_FracSamplingMax[0] < 0.8)
#    else:
#        return True


if __name__ == '__main__':
    tfile1 = utils.open_tfile(input_file_name)
    #tfile2 = utils.open_tfile(input_file_name)
    tree1 = tfile1.Get('Nominal')
    #tree2 = tfile2.Get('Nominal')
    entries = tree1.GetEntries()
    print('Number of Entries = {}'.format(entries))

    flavors = ['data', 'model']
    data = 0
    model = 1
    combs = ['22', '23', '33']
    h_xy = [[TH1F(flavor+'_xy_'+comb, ';Vertex Pair XY Distance [mm]; Number of Vertices / mm', 50, 0, 50)
             for comb in combs] for flavor in flavors]
    h_z = [[TH1F(flavor+'_z_'+comb, ';Vertex Pair Z Distance [mm]; Number of Vertices / mm', 250, 0, 250)
             for comb in combs] for flavor in flavors]
    h_3d = [[TH1F(flavor+'_3d_'+comb, ';Vertex Pair 3D Distance [mm]; Number of Vertices / mm', 250, 0, 250)
             for comb in combs] for flavor in flavors]
    h_xy_weighted = [TH1F('model_xy_weighted_'+comb, ';Vertex Pair XY Distance [mm]; Number of Vertices / mm', 50, 0, 50)
             for comb in combs]
    h_z_weighted = [TH1F('model_z_weighted_'+comb, ';Vertex Pair Z Distance [mm]; Number of Vertices / mm', 250, 0, 250)
             for comb in combs]
    h_3d_weighted = [TH1F('model_3d_weighted_'+comb, ';Vertex Pair 3D Distance [mm]; Number of Vertices / mm', 250, 0, 250)
             for comb in combs]
    h_xy_Zweighted = [TH1F('model_xy_Zweighted_'+comb, ';Vertex Pair XY Distance [mm]; Number of Vertices / mm', 50, 0, 50)
             for comb in combs]
    h_z_Zweighted = [TH1F('model_z_Zweighted_'+comb, ';Vertex Pair Z Distance [mm]; Number of Vertices / mm', 250, 0, 250)
             for comb in combs]
    h_3d_Zweighted = [TH1F('model_3d_Zweighted_'+comb, ';Vertex Pair 3D Distance [mm]; Number of Vertices / mm', 250, 0, 250)
             for comb in combs]
    #h_model_xy_22 = TH1F('model_xy_22', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 50, 0, 50)
    #h_model_z_22 = TH1F('model_z_22', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 250, 0, 250)
    #h_model_3d_22 = TH1F('model_3d_22', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 250, 0, 250)

    #h_model_xy_23 = TH1F('model_xy_23', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 50, 0, 50)
    #h_model_z_23 = TH1F('model_z_23', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 250, 0, 250)
    #h_model_3d_23 = TH1F('model_3d_23', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 250, 0, 250)

    #h_model_xy_33 = TH1F('model_xy_33', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 50, 0, 50)
    #h_model_z_33 = TH1F('model_z_33', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 250, 0, 250)
    #h_model_3d_33 = TH1F('model_3d_33', ';Vertex Pair Distance [mm]; Number of Vertices / mm', 250, 0, 250)
    m_nEvents = TH1F('nEvents', ';;Number of Events', 1, 0, 1)
    vertices = []

    for entry in xrange(entries):
        if entry % 10000 == 0:
            print('*****************************')
            print('***** processed ' + str(entry) + ' events out of ' + str(entries))
        # get the next tree in the chain and verify
        ientry = tree1.LoadTree(entry)
        if ientry < 0:
            break
        # copy next entry into memory and verify
        nb = tree1.GetEntry(entry)
        if nb <= 0:
            continue
        if tree1.EventNumber == 752668466:
            continue
        event_weight = tree1.McEventWeight * tree1.PileupWeight * tree1.ISRWeight
        m_nEvents.Fill(0.5, event_weight)
        if utils.basic_event_selection(tree1):
            for idv, nTracks in enumerate(tree1.DV_nTracks):
                if len(tree1.DV_nTracks) != len(tree1.DV_r):
                    print('##########################################')
                    print("len(tree1.DV_nTracks) and len(tree1.DV_r) are different for some reason!!!")
                    print(entry, len(tree1.DV_nTracks), len(tree1.DV_r))
                    continue
                if (not utils.basic_dv_selection(tree1, idv)) or nTracks > 3 or not tree1.DV_Region[idv] == 0:
                    continue
                tracks = []
                tracks.append([tree1.DV_track_pt_wrtSV[idv][0], tree1.DV_track_eta_wrtSV[idv][0], tree1.DV_track_phi_wrtSV[idv][0]])
                tracks.append([tree1.DV_track_pt_wrtSV[idv][1], tree1.DV_track_eta_wrtSV[idv][1], tree1.DV_track_phi_wrtSV[idv][1]])
                if nTracks == 3:
                    tracks.append([tree1.DV_track_pt_wrtSV[idv][2], tree1.DV_track_eta_wrtSV[idv][2], tree1.DV_track_phi_wrtSV[idv][2]])
                vertices.append([tree1.EventNumber, nTracks, tree1.DV_x[idv], tree1.DV_y[idv], tree1.DV_z[idv], tracks])

    print('=== start construction of model ===')

    #tfile_weight = utils.open_tfile('~/data/data16_13TeV/DVPlusMETSys/merged_weight_v4.root')
    tfile_weight = utils.open_tfile('~/data/data16_13TeV/DVPlusMETSys/merged_weight_v06-00-04.root')
    w_xy = tfile_weight.Get('weight_xy')
    w_z = tfile_weight.Get('weight_z')
    tf1_xy_data = tfile_weight.Get('tf1_xy_data')
    tf1_xy_model = tfile_weight.Get('tf1_xy_model')
    tf1_z_data = tfile_weight.Get('tf1_z_data')
    tf1_z_model = tfile_weight.Get('tf1_z_model')

    # model construction
    try:
        for ii in xrange(len(vertices)-1):
            if ii % 100 == 0:
                print('*****************************')
                print('***** processed ' + str(ii) + ' DVs out of ' + str(len(vertices)))
            for jj in xrange(ii+1, len(vertices)):
                if vertices[ii][0] != vertices[jj][0]:
                    if not args.doModel:
                        continue
                sum_nTracks = vertices[ii][1]+vertices[jj][1]
                tlv = [TLorentzVector() for _ in range(sum_nTracks)]
                for itrk in range(vertices[ii][1]):
                    tlv[itrk].SetPtEtaPhiM(vertices[ii][5][itrk][0], vertices[ii][5][itrk][1], vertices[ii][5][itrk][2], 0.13957)  # pion hypo
                for jtrk in range(vertices[jj][1]):
                    tlv[vertices[ii][1]+jtrk].SetPtEtaPhiM(vertices[jj][5][jtrk][0], vertices[jj][5][jtrk][1], vertices[jj][5][jtrk][2], 0.13957)
                tlv_sum = TLorentzVector()
                for t in tlv:
                    tlv_sum += t
                #print(tlv_sum.M())
                if tlv_sum.M() < 10:
                    continue
                dist_3d = ((vertices[ii][2]-vertices[jj][2])**2 + (vertices[ii][3]-vertices[jj][3])**2 + (vertices[ii][4]-vertices[jj][4])**2)**0.5
                dist_xy = ((vertices[ii][2]-vertices[jj][2])**2 + (vertices[ii][3]-vertices[jj][3])**2)**0.5
                dist_z = TMath.Abs(vertices[ii][4]-vertices[jj][4])
                if vertices[ii][0] != vertices[jj][0]:  # construct model if event number is different
                    h_xy[model][sum_nTracks-4].Fill(dist_xy)
                    h_z[model][sum_nTracks-4].Fill(dist_z)
                    h_3d[model][sum_nTracks-4].Fill(dist_3d)
                    #zweight = w_z.GetBinContent(w_z.FindBin(dist_z))
                    zweight = tf1_z_data(dist_z) / tf1_z_model(dist_z)
                    #weight = w_xy.GetBinContent(w_xy.FindBin(dist_xy)) * zweight
                    weight = tf1_xy_data(dist_xy) / tf1_xy_model(dist_xy) * zweight
                    h_xy_weighted[sum_nTracks-4].Fill(dist_xy, weight)
                    h_z_weighted[sum_nTracks-4].Fill(dist_z, weight)
                    h_3d_weighted[sum_nTracks-4].Fill(dist_3d, weight)
                    h_xy_Zweighted[sum_nTracks-4].Fill(dist_xy, zweight)
                    h_z_Zweighted[sum_nTracks-4].Fill(dist_z, zweight)
                    h_3d_Zweighted[sum_nTracks-4].Fill(dist_3d, zweight)
                else:
                    h_xy[data][sum_nTracks-4].Fill(dist_xy)
                    h_z[data][sum_nTracks-4].Fill(dist_z)
                    h_3d[data][sum_nTracks-4].Fill(dist_3d)
    except KeyboardInterrupt:
        pass
    output_tfile = TFile(output_file_name, 'recreate')
    for ii in range(len(flavors)):
        if (not args.doModel) and ii == 1:
            continue
        for jj in range(len(combs)):
            h_xy[ii][jj].Write()
            h_z[ii][jj].Write()
            h_3d[ii][jj].Write()
            if ii == 1:
                h_xy_weighted[jj].Write()
                h_z_weighted[jj].Write()
                h_3d_weighted[jj].Write()
                h_xy_Zweighted[jj].Write()
                h_z_Zweighted[jj].Write()
                h_3d_Zweighted[jj].Write()
    m_nEvents.Write()
    output_tfile.Close()
