#!/bin/env python

from ROOT import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--inputFiles', type=str, help='comma separated input files')
parser.add_argument('-o', '--outputFile', type=str, help='output file name')
args = parser.parse_args()


def basic_event_selection(tree):
    # [1: Trigger, 2: Filter, 3: Cleaning, 4: GRL,
    #  5: PV, 6: MET, 7: DV Selection]
    return tree.PassCut3 and tree.PassCut4 and tree.PassCut5


def basic_dv_selection(tree, idv):
    return tree.DV_passFidCuts[idv] and tree.DV_passChisqCut[idv] and tree.DV_passDistCut[idv]


def fill_DVmass_Ntrk(tree, histogram, idv, ew, doMatVeto=False):
    #for idv in range(len(tree.DV_x)):
    if basic_dv_selection(tree, idv):
        if doMatVeto and not tree.DV_passMatVeto[idv]:
            return
        histogram.Fill(tree.DV_nTracks[idv], tree.DV_m[idv], ew)


if __name__ == '__main__':
    #input_files = args.inputFiles
    #print(args.inputFiles)
    input_files = args.inputFiles.split(',')
    print('*** input files: ')
    print(input_files)
    
    print('*** output file: ')
    print(args.outputFile)
    output_root = TFile(args.outputFile, 'recreate')
    
    chain = TChain('Nominal', 'Nominal Tree')
    for input_file in input_files:
        chain.Add(input_file)
    
    # histogram bins
    cut_flow_ev = ['Initial', 'Trigger', 'Filter', 'Cleaning', 'GRL', 'PV', 'MET', 'DV Selection']
    cut_flow_dv = ['Reco DVs', 'Event Selection', 'Fiducial Volume', 'Chi2/ndof', 'Displacement', 'Material Veto', 'N Tracks', 'DV Mass']
    # define histograms
    h_cut_flow_ev = TH1F('cut_flow_event', ';;Number of Events', len(cut_flow_ev), 0, len(cut_flow_ev))
    h_cut_flow_dv = TH1F('cut_flow_dv', ';;Number of Vertices', len(cut_flow_dv), 0, len(cut_flow_dv))
    h_DVmass_Ntrk = TH2F('DVmass_Ntrk', ';Number of Tracks;DV Mass [GeV]', 50, 0, 50, 500, 0, 100)
    h_DVmass_Ntrk_MatVeto = TH2F('DVmass_Ntrk_MatVeto', ';Number of Tracks;DV Mass [GeV]', 50, 0, 50, 500, 0, 100)
    h_DVmass_Ntrk_MatVeto_MET220 = TH2F('DVmass_Ntrk_MatVeto_MET220', ';Number of Tracks;DV Mass [GeV]', 50, 0, 50, 500, 0, 100)
    h_DVmass_Ntrk_MatVeto_MET250 = TH2F('DVmass_Ntrk_MatVeto_MET250', ';Number of Tracks;DV Mass [GeV]', 50, 0, 50, 500, 0, 100)
    h_DVmass_Ntrk_Region = [[TH1F() for _ in range(12)] for __ in range(7)]
    h_DVxy = TH2F('DVxy', ';x [mm];y [mm]', 600, -300, 300, 600, -300, 300)
    h_DVxy_matVeto = TH2F('DVxy_matVeto', ';x [mm];y [mm]', 600, -300, 300, 600, -300, 300)
    h_mu = TH1F('mu', ';Mean Number of Interactions per Crossing', 50, 0, 50)
    h_mu_pileupWeight = TH1F('mu_pileupWeight', ';Mean Number of Interactions per Crossing', 50, 0, 50)
    for ntrk in range(2, 7):
        for reg in range(12):
            h_DVmass_Ntrk_Region[ntrk][reg] = TH1F('BkgEst_data_{0}Trk_Region{1}_DVMultiTrkBkg'.format(ntrk, reg), ';Invariant Mass [GeV]', 500, 0, 100)
    for bin, cut in enumerate(cut_flow_ev):
        h_cut_flow_ev.GetXaxis().SetBinLabel(bin+1, cut)
    for bin, cut in enumerate(cut_flow_dv):
        h_cut_flow_dv.GetXaxis().SetBinLabel(bin+1, cut)
    #
    
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
            event_weight = chain.McEventWeight * chain.PileupWeight * chain.ISRWeight
            h_mu.Fill(chain.CorrectedMu, event_weight)
            h_mu_pileupWeight.Fill(chain.CorrectedMu, chain.PileupWeight)
            if basic_event_selection(chain):
                for idv in range(len(chain.DV_x)):
                    fill_DVmass_Ntrk(chain, h_DVmass_Ntrk, idv, event_weight)
                    fill_DVmass_Ntrk(chain, h_DVmass_Ntrk_MatVeto, idv, event_weight, doMatVeto=True)
                    if chain.MET > 220:
                        fill_DVmass_Ntrk(chain, h_DVmass_Ntrk_MatVeto_MET220, idv, event_weight, doMatVeto=True)
                    if chain.MET > 250:
                        fill_DVmass_Ntrk(chain, h_DVmass_Ntrk_MatVeto_MET250, idv, event_weight, doMatVeto=True)
                    if basic_dv_selection(chain, idv) and chain.DV_nTracks[idv] < 7 and chain.DV_Region[idv] >= 0:
                        h_DVmass_Ntrk_Region[chain.DV_nTracks[idv]][chain.DV_Region[idv]].Fill(chain.DV_m[idv], event_weight)
                    if basic_dv_selection(chain, idv):
                        h_DVxy.Fill(chain.DV_x[idv], chain.DV_y[idv])
                        if chain.DV_passMatVeto[idv]:
                            h_DVxy_matVeto.Fill(chain.DV_x[idv], chain.DV_y[idv])

            ##############
            # Cut Flow
            ##############
            # initial number of events and dvs
            h_cut_flow_ev.Fill('Initial', event_weight)
            h_cut_flow_dv.Fill('Reco DVs', len(chain.DV_x) * event_weight)
            # trigger
            if not (chain.Passed_HLT_xe100_mht_L1XE50 or chain.Passed_HLT_xe110_mht_L1XE50):
                continue
            h_cut_flow_ev.Fill('Trigger', event_weight)
            # filter
            if chain.RunNumber < 309000:
                if not (chain.PassCut2):
                    continue
            else:
                if not (chain.MET_LHT > 180.):
                    continue
            h_cut_flow_ev.Fill('Filter', event_weight)
            # cleaning
            if not chain.PassCut3:
                continue
            h_cut_flow_ev.Fill('Cleaning', event_weight)
            # GRL
            if not chain.PassCut4:
                continue
            h_cut_flow_ev.Fill('GRL', event_weight)
            # PV
            if not chain.PassCut5:
                continue
            h_cut_flow_ev.Fill('PV', event_weight)
            # MET
            if chain.RunNumber < 309000:
                if not (chain.MET > 220):
                    continue
            else: 
                if not (chain.MET > 250):
                    continue
            h_cut_flow_ev.Fill('MET', event_weight)
            h_cut_flow_dv.Fill('Event Selection', len(chain.DV_x)*event_weight)
            ############ 
            # dv loop
            ############ 
            for idv in range(len(chain.DV_x)):
                # Fidducial Volume
                if not chain.DV_passFidCuts[idv]:
                    continue
                h_cut_flow_dv.Fill('Fiducial Volume', event_weight)
                # Chi2/ndof
                if not chain.DV_passChisqCut[idv]:
                    continue
                h_cut_flow_dv.Fill('Chi2/ndof', event_weight)
                # displacement
                if not chain.DV_passDistCut[idv]:
                    continue
                h_cut_flow_dv.Fill('Displacement', event_weight)
                # Material veto
                if not chain.DV_passMatVeto[idv]:
                    continue
                h_cut_flow_dv.Fill('Material Veto', event_weight)
                # N tracks
                if not chain.DV_passNtrkCut[idv]:
                    continue
                h_cut_flow_dv.Fill('N Tracks', event_weight)
                # DV Mass
                if not chain.DV_passMassCut[idv]:
                    continue
                h_cut_flow_dv.Fill('DV Mass', event_weight)
    except KeyboardInterrupt:
        pass
        
    output_root.cd()
    h_cut_flow_ev.Write()
    h_cut_flow_dv.Write()
    h_DVmass_Ntrk.Write()
    h_DVmass_Ntrk_MatVeto.Write()
    h_DVmass_Ntrk_MatVeto_MET220.Write()
    h_DVmass_Ntrk_MatVeto_MET250.Write()
    for ntrk in range(2, 7):
        for reg in range(12):
            h_DVmass_Ntrk_Region[ntrk][reg].Write()
    h_DVxy.Write()
    h_DVxy_matVeto.Write()
    h_mu.Write()
    h_mu_pileupWeight.Write()
    output_root.Close()
