#!/bin/env python

from ROOT import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--inputFiles', type=str, help='comma separated input files')
parser.add_argument('-o', '--outputFile', type=str, help='output file name')
args = parser.parse_args()

import mc

#input_files = args.inputFiles.split(',')
#print('*** input files: ')
#print(input_files)

#print('*** output file: ')
#print(args.outputFile)
#output_root = TFile(args.outputFile, 'recreate')


def pass_event_cut(tree, cut_level):
    # [1: Trigger, 2: Filter, 3: Cleaning, 4: GRL,
    #  5: PV, 6: MET, 7: DV Selection]
    event_cuts = [tree.PassCut1, tree.PassCut2, tree.PassCut3, tree.PassCut4,
                  tree.PassCut5, tree.PassCut6, tree.PassCut7]
    passed_or_not = True
    for cut in event_cuts[:cut_level]:
        passed_or_not &= cut
    return passed_or_not


def basic_event_selection(tree):
    # [1: Trigger, 2: Filter, 3: Cleaning, 4: GRL,
    #  5: PV, 6: MET, 7: DV Selection]
    return tree.PassCut3 and tree.PassCut4 and tree.PassCut5


def basic_dv_selection(tree, idv):
    #return tree.DV_passFidCuts[idv] and tree.DV_passChisqCut[idv] and tree.DV_passDistCut[idv]
    return tree.DV_passFidCuts[idv] and tree.DV_passChisqCut[idv] and tree.DV_passDistCut[idv] and tree.DV_passMatVeto[idv]


def get_lifetime_weight(tree, ctau, ctau_MC):
    if len(tree.Rhadron_properdecaytime) != 2:
        #print('vector size of Rhadron_properdecaytime is not 2. return weight=0.')
        return 0
    dt1 = tree.Rhadron_properdecaytime[0] * 1e-3  # [ms]->[s]
    dt2 = tree.Rhadron_properdecaytime[1] * 1e-3  # [ms]->[s]
    tau = ctau / TMath.C()
    tau_MC = ctau_MC / TMath.C()
    weight_rhad1 = tau_MC/tau * TMath.Exp(dt1/tau_MC - dt1/tau)
    weight_rhad2 = tau_MC/tau * TMath.Exp(dt2/tau_MC - dt2/tau)
    return weight_rhad1 * weight_rhad2


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

    #isMC = True
    
    # histogram bins
    cut_flow_ev = ['Initial', 'Trigger', 'Filter', 'Cleaning', 'GRL', 'PV', 'MET', 'DV Selection']
    cut_flow_dv = ['Reco DVs', 'Event Selection', 'Fiducial Volume', 'Chi2/ndof', 'Displacement', 'Material Veto', 'N Tracks', 'DV Mass']
    # define histograms
    h_cut_flow_ev = TH1F('cut_flow_event', ';;Number of Events', len(cut_flow_ev), 0, len(cut_flow_ev))
    h_cut_flow_dv = TH1F('cut_flow_dv', ';;Number of Vertices', len(cut_flow_dv), 0, len(cut_flow_dv))
    h_DVmass_Ntrk = TH2F('DVmass_Ntrk', ';Number of Tracks;DV Mass [GeV]', 50, 0, 50, 500, 0, 100)
    h_Ntrk_loMET = TH1F('Ntrk_loMET', ';Number of Tracks', 50, 0, 50)
    h_Ntrk_loMET_gt100GeV = TH1F('Ntrk_loMET_gt100GeV', ';Number of Tracks', 50, 0, 50)
    h_Ntrk_hiMET = TH1F('Ntrk_hiMET', ';Number of Tracks', 50, 0, 50)
    h_MET_loNtrk = TH1F('MET_loNtrk', ';MET [GeV]', 100, 0, 500)
    h_MET_2trk = TH1F('MET_2Ntrk', ';MET [GeV]', 100, 0, 500)
    h_MET_3trk = TH1F('MET_3Ntrk', ';MET [GeV]', 100, 0, 500)
    h_MET_4trk = TH1F('MET_4Ntrk', ';MET [GeV]', 100, 0, 500)
    h_MET_hiNtrk = TH1F('MET_hiNtrk', ';MET [GeV]', 100, 0, 500)
    h_DVmass_Ntrk_MatVeto = TH2F('DVmass_Ntrk_MatVeto', ';Number of Tracks;DV Mass [GeV]', 50, 0, 50, 500, 0, 100)
    h_DVmass_Ntrk_MatVeto_MET220 = TH2F('DVmass_Ntrk_MatVeto_MET220', ';Number of Tracks;DV Mass [GeV]', 50, 0, 50, 500, 0, 100)
    h_DVmass_Ntrk_MatVeto_MET250 = TH2F('DVmass_Ntrk_MatVeto_MET250', ';Number of Tracks;DV Mass [GeV]', 50, 0, 50, 500, 0, 100)
    h_DVmass_Ntrk_Region = [[TH1F() for _ in range(12)] for __ in range(8)]
    h_DVmass_Ntrk_Sum = [TH1F() for __ in range(8)]
    h_DVmass_Ntrk_Region_loMET = [[TH1F() for _ in range(12)] for __ in range(8)]
    h_DVmass_Ntrk_Region_hiMET = [[TH1F() for _ in range(12)] for __ in range(8)]
    h_DVxy = TH2F('DVxy', ';x [mm];y [mm]', 600, -300, 300, 600, -300, 300)
    h_DVxy_matVeto = TH2F('DVxy_matVeto', ';x [mm];y [mm]', 600, -300, 300, 600, -300, 300)
    h_DVxy_matVeto_10GeV = TH2F('DVxy_matVeto_10GeV', ';x [mm];y [mm]', 600, -300, 300, 600, -300, 300)
    h_DVxy_matVeto_10GeV_no2Trk = TH2F('DVxy_matVeto_10GeV_no2Trk', ';x [mm];y [mm]', 600, -300, 300, 600, -300, 300)
    h_DVrz_matVeto_10GeV = TH2F('DVrz_matVeto_10GeV', ';z [mm];r [mm]', 150, -300, 300, 300, 0, 300)
    h_DVrz_matVeto_10GeV_no2Trk = TH2F('DVrz_matVeto_10GeV_no2Trk', ';z [mm];r [mm]', 150, -300, 300, 300, 0, 300)
    h_DVrphi_matVeto_10GeV = TH2F('DVrphi_matVeto_10GeV', ';#phi [rad];r [mm]', 836, -TMath.Pi(), TMath.Pi(), 300, 0, 300)
    h_DVrphi_matVeto_10GeV_no2Trk = TH2F('DVrphi_matVeto_10GeV_no2Trk', ';#phi [rad];r [mm]', 836, -TMath.Pi(), TMath.Pi(), 300, 0, 300)
    h_mu = TH1F('mu', ';Mean Number of Interactions per Crossing', 50, 0, 50)
    h_mu_pileupWeight = TH1F('mu_pileupWeight', ';Mean Number of Interactions per Crossing', 50, 0, 50)
    for ntrk in range(2, 8):
        h_DVmass_Ntrk_Sum[ntrk] = TH1F('BkgEst_data_{0}Trk'.format(ntrk), ';Invariant Mass [GeV]', 500, 0, 100)
        for reg in range(12):
            h_DVmass_Ntrk_Region[ntrk][reg] = TH1F('BkgEst_data_{0}Trk_Region{1}'.format(ntrk, reg), ';Invariant Mass [GeV]', 500, 0, 100)
            h_DVmass_Ntrk_Region_loMET[ntrk][reg] = TH1F('BkgEst_data_{0}Trk_Region{1}_loMET'.format(ntrk, reg), ';Invariant Mass [GeV]', 500, 0, 100)
            h_DVmass_Ntrk_Region_hiMET[ntrk][reg] = TH1F('BkgEst_data_{0}Trk_Region{1}_hiMET'.format(ntrk, reg), ';Invariant Mass [GeV]', 500, 0, 100)
    for bin, cut in enumerate(cut_flow_ev):
        h_cut_flow_ev.GetXaxis().SetBinLabel(bin+1, cut)
    for bin, cut in enumerate(cut_flow_dv):
        h_cut_flow_dv.GetXaxis().SetBinLabel(bin+1, cut)
    #
    m_MET_min = 250
    
    n_reweight_steps = 50
    xmin = 1.
    xmax = 10000.
    ratio = xmax/xmin
    bins = []
    for ii in range(n_reweight_steps):
        bins.append(xmax * 10**(ii*TMath.Log10(ratio)/n_reweight_steps-TMath.Log10(ratio)))
    #n_passed_w1 = [0. for _ in range(n_reweight_steps)]
    #n_passed = [0. for _ in range(n_reweight_steps)]
    from array import array
    limitsLifetime = array('d', bins)
    n_passed = TH1F('n_passed', ';c#tau [mm]; Event-level efficiency', len(limitsLifetime)-1, limitsLifetime)
    #n_total_w1 = [0. for _ in range(n_reweight_steps)]
    #n_total = [0. for _ in range(n_reweight_steps)]
    n_total = TH1F('n_total', ';c#tau [mm]; Event-level efficiency', len(limitsLifetime)-1, limitsLifetime)

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
            if chain.EventNumber == 752668466:
                continue
            event_weight = chain.McEventWeight * chain.PileupWeight * chain.ISRWeight
            h_mu.Fill(chain.CorrectedMu, event_weight)
            h_mu_pileupWeight.Fill(chain.CorrectedMu, chain.PileupWeight)

            # lifetime reweighting
            if chain.McChannelNumber > 400000:
                pass_all = pass_event_cut(chain, 7)
                ctau_MC = TMath.C() * mc.parameters[chain.McChannelNumber]['t'] * 1e-9  # [nm]->[m]
                for step in range(n_reweight_steps):
                    #target_ctau = TMath.Power(300., step/float(n_reweight_steps-1)) * 1e-3  # [mm]->[m]
                    target_ctau = xmax * 10**(step*TMath.Log10(ratio)/n_reweight_steps-TMath.Log10(ratio)) * 1e-3 # [mm]->[m]
                    #print(target_ctau*1e3)
                    lifetime_weight = get_lifetime_weight(chain, target_ctau, ctau_MC)
                    if pass_all:
                        #n_passed_w1[step] += 1.
                        #n_passed[step] += event_weight * lifetime_weight
                        n_passed.Fill(target_ctau*1e3, event_weight * lifetime_weight)
                    #n_total_w1[step] += 1.
                    #n_total[step] += event_weight * lifetime_weight
                    n_total.Fill(target_ctau*1e3, event_weight * lifetime_weight)

            max_ntrk = 0
            if basic_event_selection(chain):
                for idv in range(len(chain.DV_x)):
                    fill_DVmass_Ntrk(chain, h_DVmass_Ntrk, idv, event_weight)
                    fill_DVmass_Ntrk(chain, h_DVmass_Ntrk_MatVeto, idv, event_weight, doMatVeto=True)
                    if chain.MET > 220:
                        fill_DVmass_Ntrk(chain, h_DVmass_Ntrk_MatVeto_MET220, idv, event_weight, doMatVeto=True)
                    if chain.MET > 250:
                        fill_DVmass_Ntrk(chain, h_DVmass_Ntrk_MatVeto_MET250, idv, event_weight, doMatVeto=True)
                    #if basic_dv_selection(chain, idv) and chain.DV_nTracks[idv] < 7 and chain.DV_Region[idv] >= 0:
                    if basic_dv_selection(chain, idv) and chain.DV_Region[idv] >= 0:
                        ntrk = chain.DV_nTracks[idv] if chain.DV_nTracks[idv] < 7 else 7
                        max_ntrk = ntrk if ntrk > max_ntrk else max_ntrk
                        #if chain.DV_Region[idv] in [0, 2, 4, 6, 8, 10, 11]:
                        if chain.DV_Region[idv] >= 0:
                            h_DVmass_Ntrk_Sum[ntrk].Fill(chain.DV_m[idv], event_weight)
                        h_DVmass_Ntrk_Region[ntrk][chain.DV_Region[idv]].Fill(chain.DV_m[idv], event_weight)
                        if chain.MET < m_MET_min:
                            h_DVmass_Ntrk_Region_loMET[ntrk][chain.DV_Region[idv]].Fill(chain.DV_m[idv], event_weight)
                            h_Ntrk_loMET.Fill(chain.DV_nTracks[idv], event_weight)
                            if chain.MET > 100:
                                h_Ntrk_loMET_gt100GeV.Fill(chain.DV_nTracks[idv], event_weight)
                        else:
                            h_DVmass_Ntrk_Region_hiMET[ntrk][chain.DV_Region[idv]].Fill(chain.DV_m[idv], event_weight)
                            h_Ntrk_hiMET.Fill(chain.DV_nTracks[idv], event_weight)
                    if basic_dv_selection(chain, idv):
                        h_DVxy.Fill(chain.DV_x[idv], chain.DV_y[idv])
                        if chain.DV_passMatVeto[idv]:
                            h_DVxy_matVeto.Fill(chain.DV_x[idv], chain.DV_y[idv])
                            if chain.DV_m[idv] > 10:
                                h_DVxy_matVeto_10GeV.Fill(chain.DV_x[idv], chain.DV_y[idv])
                                h_DVrz_matVeto_10GeV.Fill(chain.DV_z[idv], chain.DV_r[idv])
                                h_DVrphi_matVeto_10GeV.Fill(TMath.ATan2(chain.DV_y[idv], chain.DV_x[idv]), chain.DV_r[idv])
                                if chain.DV_nTracks[idv] > 2:
                                    h_DVxy_matVeto_10GeV_no2Trk.Fill(chain.DV_x[idv], chain.DV_y[idv])
                                    h_DVrz_matVeto_10GeV_no2Trk.Fill(chain.DV_z[idv], chain.DV_r[idv])
                                    h_DVrphi_matVeto_10GeV_no2Trk.Fill(TMath.ATan2(chain.DV_y[idv], chain.DV_x[idv]), chain.DV_r[idv])
            if max_ntrk < 5:
                h_MET_loNtrk.Fill(chain.MET, event_weight)
                if max_ntrk == 4:
                    h_MET_4trk.Fill(chain.MET, event_weight)
                elif max_ntrk == 3:
                    h_MET_3trk.Fill(chain.MET, event_weight)
                elif max_ntrk == 2:
                    h_MET_2trk.Fill(chain.MET, event_weight)
            else:
                h_MET_hiNtrk.Fill(chain.MET, event_weight)

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
            #if chain.RandomRunNumber < 309000:
            #    if not (chain.PassCut2):
            #        continue
            #else:
            #    if not (chain.MET_LHT > 180.):
            #        continue
            if not chain.PassCut2:
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
            #if chain.RunNumber < 309000:
            #    if not (chain.MET > 250):
            #        continue
            #else: 
            #    if not (chain.MET > 250):
            #        continue
            if chain.MET < 250:
                continue
            h_cut_flow_ev.Fill('MET', event_weight)
            h_cut_flow_dv.Fill('Event Selection', len(chain.DV_x)*event_weight)
            ############ 
            # dv loop
            ############ 
            have_signal_like_dv = False
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
                have_signal_like_dv = True
            if have_signal_like_dv:
                h_cut_flow_ev.Fill('DV Selection', event_weight)
    except KeyboardInterrupt:
        pass

    #for step in range(n_reweight_steps):
    #    sf =  n_total_w1[step] / n_total[step]
    #    n_passed[step] *= sf
    #    n_total[step] *= sf
 
    output_root.cd()
    h_cut_flow_ev.Write()
    h_cut_flow_dv.Write()
    h_DVmass_Ntrk.Write()
    h_DVmass_Ntrk_MatVeto.Write()
    h_DVmass_Ntrk_MatVeto_MET220.Write()
    h_DVmass_Ntrk_MatVeto_MET250.Write()
    h_Ntrk_loMET.Write()
    h_Ntrk_hiMET.Write()
    h_Ntrk_loMET_gt100GeV.Write()
    h_MET_loNtrk.Write()
    h_MET_hiNtrk.Write()
    h_MET_2trk.Write()
    h_MET_3trk.Write()
    h_MET_4trk.Write()
    for ntrk in range(2, 8):
        h_DVmass_Ntrk_Sum[ntrk].Write()
        for reg in range(12):
            h_DVmass_Ntrk_Region[ntrk][reg].Write()
            h_DVmass_Ntrk_Region_loMET[ntrk][reg].Write()
            h_DVmass_Ntrk_Region_hiMET[ntrk][reg].Write()
    h_DVxy.Write()
    h_DVxy_matVeto.Write()
    h_DVxy_matVeto_10GeV.Write()
    h_DVrz_matVeto_10GeV.Write()
    h_DVrphi_matVeto_10GeV.Write()
    h_DVxy_matVeto_10GeV_no2Trk.Write()
    h_DVrz_matVeto_10GeV_no2Trk.Write()
    h_DVrphi_matVeto_10GeV_no2Trk.Write()
    h_mu.Write()
    h_mu_pileupWeight.Write()
    n_passed.Write()
    n_total.Write()
    tg = TGraphAsymmErrors(n_passed, n_total)
    tg.SetName('efficiency')
    tg.GetXaxis().SetTitle('c#tau [mm]')
    tg.GetYaxis().SetTitle('Event-level efficiency')
    tg.Write()
    output_root.Close()
