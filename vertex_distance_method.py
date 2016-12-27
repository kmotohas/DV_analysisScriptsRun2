#!/bin/env python

import argparse
#import numpy

from ROOT import *

#import BasicConfig
import utils

p = argparse.ArgumentParser()
p.add_argument('-f', '--inputFile', help='input TTree file name')
p.add_argument('-o', '--outputFile', help='output histogram file name')
args = p.parse_args()
input_file_name = args.inputFile
output_file_name = args.outputFile

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
    m_nEvents = TH1F('nEvents', ';;Number of Events', 1, 0, 1)
    vertices = []

    for entry in xrange(entries):
        if entry % 10000 == 0:
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
        if tree1.EventNumber == 752668466:
            continue
        event_weight = tree1.McEventWeight * tree1.PileupWeight * tree1.ISRWeight
        m_nEvents.Fill(0.5, event_weight)
        for idv, nTracks in enumerate(tree1.DV_nTracks):
            if len(tree1.DV_nTracks) != len(tree1.DV_r):
                print('##########################################')
                print("len(tree1.DV_nTracks) and len(tree1.DV_r) are different for some reason!!!")
                print(entry, len(tree1.DV_nTracks), len(tree1.DV_r))
                continue
            if nTracks > 3 or not tree1.DV_Region[idv] == 0:
                continue
            tracks = []
            tracks.append([tree1.DV_track_pt_wrtSV[idv][0], tree1.DV_track_eta_wrtSV[idv][0], tree1.DV_track_phi_wrtSV[idv][0]])
            tracks.append([tree1.DV_track_pt_wrtSV[idv][1], tree1.DV_track_eta_wrtSV[idv][1], tree1.DV_track_phi_wrtSV[idv][1]])
            if nTracks == 3:
                tracks.append([tree1.DV_track_pt_wrtSV[idv][2], tree1.DV_track_eta_wrtSV[idv][2], tree1.DV_track_phi_wrtSV[idv][2]])
            vertices.append([tree1.EventNumber, nTracks, tree1.DV_x[idv], tree1.DV_y[idv], tree1.DV_z[idv], tracks])

    print('=== start construction of model ===')

    # model construction
    for ii in xrange(len(vertices)-1):
        if ii % 100 == 0:
            print('*****************************')
            print('***** processed ' + str(ii) + ' DVs')
        for jj in xrange(ii+1, len(vertices)):
            sum_nTracks = vertices[ii][1]+vertices[jj][1]
            tlv = [TLorentzVector() for _ in range(sum_nTracks)]
            for itrk in range(vertices[ii][1]):
                tlv[itrk].SetPtEtaPhiM(vertices[ii][5][itrk][0], vertices[ii][5][itrk][1], vertices[ii][5][itrk][2], 0.13957)
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
            if vertices[ii][0] != vertices[jj][0]:
                h_xy[model][sum_nTracks-4].Fill(dist_xy)
                h_z[model][sum_nTracks-4].Fill(dist_z)
                h_3d[model][sum_nTracks-4].Fill(dist_3d)
            else:
                h_xy[data][sum_nTracks-4].Fill(dist_xy)
                h_z[data][sum_nTracks-4].Fill(dist_z)
                h_3d[data][sum_nTracks-4].Fill(dist_3d)
    output_tfile = TFile(output_file_name, 'recreate')
    for ii in range(len(flavors)):
        for jj in range(len(combs)):
            h_xy[ii][jj].Write()
            h_z[ii][jj].Write()
            h_3d[ii][jj].Write()
    m_nEvents.Write()
    output_tfile.Close()
