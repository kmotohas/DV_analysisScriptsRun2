#!/usr/bin/env python
import re
#import os
from glob import glob
from array import array
import numpy as np

# ROOT
from ROOT import gROOT
from ROOT import gDirectory
from ROOT import gStyle

from ROOT import TFile
from ROOT import TTree
from ROOT import TChain
from ROOT import TH1F
#from ROOT import TH2F
from ROOT import TCanvas
from ROOT import TLegend
from ROOT import TMath
from ROOT import kPink

import AtlasStyle

# DV_analysisScriptsRun2
import BasicConfig
import utils
import mc


def pass_event_cut(tree, cut_level):
    # [1: Trigger, 2: Filter, 3: Cleaning, 4: GRL,
    #  5: PV, 6: MET, 7: DV Selection]
    #event_cuts = [tree.PassCut1, tree.PassCut2, tree.PassCut3, tree.PassCut4,
    #              tree.PassCut5, tree.PassCut6]
    event_cuts = [tree.PassCut1, True, tree.PassCut3, tree.PassCut4,
                  tree.PassCut5, tree.PassCut6]
                  #tree.PassCut5, tree.PassCut6, tree.PassCut7]  # TODO
    passed_or_not = True
    for cut in event_cuts[:cut_level]:
        passed_or_not &= cut
    return passed_or_not


def pass_dv_cut(tree, cut_level):
    DV_cuts = [tree.DV_PassFidCuts, tree.DV_PassChisqCut, tree.DV_PassDistCut, tree.DV_PassMatVeto,
               tree.DV_PassNtrkCut, tree.DV_PassMassCut]
    passed_or_not = True
    for cut in DV_cuts[:cut_level]:
        passed_or_not &= cut
    return passed_or_not


def root_sum_squares(histogram, axis):
    sum_squares_up = 0.
    sum_squares_down = 0.
    if axis == 'x':
        for bin in range(1, histogram.GetNbinsX()):
            if histogram.GetBinContent(bin) > 0:
                sum_squares_up += histogram.GetBinContent(bin) * histogram.GetBinContent(bin)
            else:
                sum_squares_down += histogram.GetBinContent(bin) * histogram.GetBinContent(bin)
        return TMath.Sqrt(sum_squares_up), TMath.Sqrt(sum_squares_down)


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


def pass_base_event_selection(tree):
    base_cuts = [tree.PassCut3, tree.PassCut4, tree.PassCut4]
    passed_or_not = True
    for cut in base_cuts:
        passed_or_not &= cut
    return passed_or_not


def pass_base_dv_selection(tree, dv_index):
    dv_base_cuts = [tree.DV_passFidCuts, tree.DV_passChisqCut, tree.DV_passDistCut, tree.DV_passMatVeto]
    passed_or_not = True
    for cut in dv_base_cuts:
        passed_or_not = passed_or_not and cut[dv_index]
    return passed_or_not


def check_n_vertices_vs_met_threshold():
    AtlasStyle.SetAtlasStyle()

    input_tfile = utils.open_tfile(BasicConfig.workdir + 'DVTree_NTuple_data15_13TeV.root')
    tree = input_tfile.Get('DVTree_NTuple')

    bin_name = ['Base', 'Trigger', 'Filter', 'MET200', 'MET220', 'MET250']
    h_nevents_cut = TH1F('nevents_cut', ';;Double Ratio', len(bin_name), 0, len(bin_name))
    h_nevents_all = TH1F('nevents_all', ';;Double Ratio', len(bin_name), 0, len(bin_name))
    h_ndvs_cut = {ntracks: TH1F('ndvs_cut_'+str(ntracks), ';;Double Ratio', len(bin_name), 0, len(bin_name))
                  for ntracks in range(2, 30)}
    h_ndvs_all = {ntracks: TH1F('ndvs_all_'+str(ntracks), ';;Double Ratio', len(bin_name), 0, len(bin_name))
                  for ntracks in range(2, 30)}
    for bin, name in enumerate(bin_name):
        h_nevents_cut.GetXaxis().SetBinLabel(bin+1, name)
        h_nevents_all.GetXaxis().SetBinLabel(bin+1, name)
        for ntracks in range(2, 30):
            h_ndvs_cut[ntracks].GetXaxis().SetBinLabel(bin+1, name)
            h_ndvs_all[ntracks].GetXaxis().SetBinLabel(bin+1, name)
    entries = tree.GetEntries()
    for entry in range(entries):
        if entry % 10000 == 0:
            print('*** processed {0} out of {1}'.format(entry, entries))
        #if entry == 1000000:
        #    break
        # get the next tree in the chain and verify
        ientry = tree.LoadTree(entry)
        if ientry < 0:
            break
        # copy next entry into memory and verify
        nb = tree.GetEntry(entry)
        if nb <= 0:
            continue
        #if not pass_base_event_selection(tree):
        #    continue
        # fill all
        for name in bin_name:
            h_nevents_all.Fill(name, 1.)
            for dv_index, DV_nTracks in enumerate(tree.DV_nTracks):
                if pass_base_dv_selection(tree, dv_index):
                    h_ndvs_all[DV_nTracks].Fill(name, 1.)
        #
        h_nevents_cut.Fill('Base', 1.)
        for dv_index, DV_nTracks in enumerate(tree.DV_nTracks):
            if pass_base_dv_selection(tree, dv_index):
                h_ndvs_cut[DV_nTracks].Fill('Base', 1.)
        #
        if not tree.PassCut1:
            continue
        h_nevents_cut.Fill('Trigger', 1.)
        for dv_index, DV_nTracks in enumerate(tree.DV_nTracks):
            if pass_base_dv_selection(tree, dv_index):
                h_ndvs_cut[DV_nTracks].Fill('Trigger', 1.)
        #
        if not tree.PassCut2:
            continue
        h_nevents_cut.Fill('Filter', 1.)
        for dv_index, DV_nTracks in enumerate(tree.DV_nTracks):
            if pass_base_dv_selection(tree, dv_index):
                h_ndvs_cut[DV_nTracks].Fill('Filter', 1.)
        #
        if not tree.MET > 200:
            continue
        h_nevents_cut.Fill('MET200', 1.)
        for dv_index, DV_nTracks in enumerate(tree.DV_nTracks):
            if pass_base_dv_selection(tree, dv_index):
                h_ndvs_cut[DV_nTracks].Fill('MET200', 1.)
        #
        if not tree.MET > 220:
            continue
        h_nevents_cut.Fill('MET220', 1.)
        for dv_index, DV_nTracks in enumerate(tree.DV_nTracks):
            if pass_base_dv_selection(tree, dv_index):
                h_ndvs_cut[DV_nTracks].Fill('MET220', 1.)
        #
        if not tree.MET > 250:
            continue
        h_nevents_cut.Fill('MET250', 1.)
        for dv_index, DV_nTracks in enumerate(tree.DV_nTracks):
            if pass_base_dv_selection(tree, dv_index):
                h_ndvs_cut[DV_nTracks].Fill('MET250', 1.)
    #
    canvas = TCanvas('canvas', 'canvas', 1200, 800)
    h_ndvs_all_clone = h_ndvs_all[2].Clone('unit')
    h_ndvs_all_clone.Divide(h_ndvs_all[2])
    h_ndvs_all_clone.SetMaximum(3)
    h_ndvs_all_clone.SetMinimum(0)
    h_ndvs_all_clone.Draw()
    legend = TLegend(0.5, 0.6, 0.85, 0.85)
    for DV_nTracks in range(2, 6):
        h_ndvs_cut[DV_nTracks].Sumw2()
        h_ndvs_cut[DV_nTracks].Divide(h_ndvs_all[DV_nTracks])
        h_ndvs_cut[DV_nTracks].Divide(h_nevents_cut)
        h_ndvs_cut[DV_nTracks].Multiply(h_nevents_all)
        utils.decorate_histogram(h_ndvs_cut[DV_nTracks], BasicConfig.colors[DV_nTracks])
        h_ndvs_cut[DV_nTracks].Draw('same,hist')
        legend.AddEntry(h_ndvs_cut[DV_nTracks],
                        '('+str(DV_nTracks)+'trk-DVs(cut)/2trk-DVs(all))/(Events(cut)/Events(all))', 'l')
    utils.decorate_legend(legend)
    legend.Draw()
    utils.save_as(canvas, BasicConfig.plotdir + 'nVerts_met_dependency')
    output = TFile('test.root', 'recreate')
    canvas.Write()
    output.Close()


def create_cut_flow():
    AtlasStyle.SetAtlasStyle()

    input_tfile = utils.open_tfile(BasicConfig.workdir + 'DVTree_NTuple_data15_13TeV.root')
    tree = input_tfile.Get('DVTree_NTuple')

    cut_flow = ['Initial', 'Trigger', 'Filter', 'Cleaning', 'GRL', 'PV', 'MET', 'DV Selection']
    h_cut_flow = TH1F('cut_flow', ';;Number of Events', len(cut_flow), 0, len(cut_flow))
    for bin, cut in enumerate(cut_flow):
        h_cut_flow.GetXaxis().SetBinLabel(bin+1, cut)
    #
    entries = tree.GetEntries()
    for entry in range(entries):
        if entry % 10000 == 0:
            print('*** processed {0} out of {1}'.format(entry, entries))
        if entry == 100000:
            break
        # get the next tree in the chain and verify
        ientry = tree.LoadTree(entry)
        if ientry < 0:
            break
        # copy next entry into memory and verify
        nb = tree.GetEntry(entry)
        if nb <= 0:
            continue
        for step, cut in enumerate(cut_flow):
            if step == 0:
                h_cut_flow.Fill(cut, 1.)
            elif step == 6:
                if pass_event_cut(tree, 5) and tree.MET > 220:
                    h_cut_flow.Fill(cut, 1.)
            elif step == 7:
                have_signal_like_dv = False
                for dv_index in range(len(tree.DV_passVtxCuts)):
                    have_signal_like_dv = have_signal_like_dv or tree.DV_passVtxCuts[dv_index]
                if pass_event_cut(tree, 5) and tree.MET > 220 and have_signal_like_dv:
                    h_cut_flow.Fill(cut, 1.)
            elif pass_event_cut(tree, step):
                h_cut_flow.Fill(cut, 1.)
    output = TFile('cut_flow.root', 'recreate')
    h_cut_flow.Write()
    output.Close()


def fill_ntuple():
    AtlasStyle.SetAtlasStyle()

#    # get key list
#    tfile = TFile(BasicConfig.workdir + 'systTree.root')
#    key_list_all = [key.GetName() for key in gDirectory.GetListOfKeys()]
#    regex = re.compile('PRW|JET|MET.*')
#    key_list = [key for key in key_list_all if re.match(regex, key)]
#    tfile.Close()

    # start making ttree
    output_tfile = TFile('rhadron_SimpleMETFilter.root', 'recreate')

    # initialize TTree
    tree = TTree('rhadron', 'tree of rhadron properties for limit setting')
    # leaf variables
    mass_gluino = array('f', [0])
    delta_mass = array('f', [0])
    ctau = array('f', [0])
    eff = array('f', [0])
    eff_stat_error = array('f', [0])
    eff_syst_error = array('f', [0])
    # set branch
    tree.Branch("mGluino", mass_gluino, 'mGluino/F')
    tree.Branch("deltaM", delta_mass, 'deltaM/F')
    tree.Branch("ctau", ctau, 'ctau/F')
    tree.Branch("eff", eff, 'eff/F')
    tree.Branch("effRelStatErr", eff_stat_error, 'effRelStatErr/F')
    tree.Branch("effRelSystErr", eff_syst_error, 'effRelSystErr/F')

    #directory = '/afs/cern.ch/work/k/kmotohas/DisplacedVertex/DV_xAODAnalysis/submitDir_LSF/mc/hist_DVPlusMETSys/'
    directory = BasicConfig.workdir + 'hist_DVPlusMETSys/'

    #c = 299792458.  # [m/s]
    tchains = [[dsid, TChain('Nominal', str(dsid))] for dsid in range(402700, 402740)]

    systematic_tables = TFile('systematic_summary_SimpleMETFilter.root', 'open')
    table = TH1F()

    n_reweight_steps = 10

    for dsid, tchain in tchains:
        print('')
        print(dsid)
        #index = 0
        for input in glob(directory + 'systTree_' + str(dsid) + '_*.root'):
            print(input)
            tchain.Add(input)
        mass_gluino[0] = mc.parameters[dsid]['g']
        delta_mass[0] = mass_gluino[0] - mc.parameters[dsid]['chi0']
        #print(mass_gluino[0], delta_mass[0], ctau[0])
        entries = tchain.GetEntries()
        n_passed_w1 = [0. for _ in range(n_reweight_steps)]
        n_passed = [0. for _ in range(n_reweight_steps)]
        n_total_w1 = [0. for _ in range(n_reweight_steps)]
        n_total = [0. for _ in range(n_reweight_steps)]
        if entries == 0:
            continue
        for entry in range(entries):
            # get the next tree in the chain and verify
            ientry = tchain.LoadTree(entry)
            if ientry < 0:
                break
            # copy next entry into memory and verify
            nb = tchain.GetEntry(entry)
            if nb <= 0:
                continue
            ctau_MC = TMath.C() * mc.parameters[dsid]['t'] * 1e-9  # [pm]->[m]
            for step in range(n_reweight_steps):
                target_ctau = TMath.Power(300., step/float(n_reweight_steps-1)) * 1e-3  # [mm]->[m]
                lifetime_weight = get_lifetime_weight(tchain, target_ctau, ctau_MC)
                if pass_event_cut(tchain, 5) and tchain.MET > 220 and tchain.PassCut7:  # TODO
                #if pass_event_cut(tchain, 5) and tchain.MET > 250 and tchain.PassCut7:  # TODO
                    #print(lifetime_weight)
                    n_passed_w1[step] += 1.
                    n_passed[step] += tchain.McEventWeight * tchain.PileupWeight * tchain.ISRWeight * lifetime_weight
                n_total_w1[step] += 1.
                n_total[step] += tchain.McEventWeight * tchain.PileupWeight * tchain.ISRWeight * lifetime_weight
        systematic_tables.GetObject('systematic_table_'+str(dsid), table)
        syst_up, syst_down = root_sum_squares(table, 'x')
        eff_syst_error[0] = max(syst_up, syst_down)  # TODO
        if eff_syst_error[0] > 1:
            print('eff_syst_error[0] = ' + str(eff_syst_error[0]))
            eff_syst_error[0] = 1.
        for step in range(n_reweight_steps):
            #print(n_total_w1[step], n_total[step])
            sf =  n_total_w1[step] / n_total[step]
            n_passed[step] *= sf
            n_total[step] *= sf
            #eff_no_weight, stat_error_no_weight = utils.division_error_propagation(n_passed_w1[step], n_total_w1[step])
            ctau[0] = TMath.Power(300, step/float(n_reweight_steps-1)) * 1e-3  # [mm]->[m]
            eff[0], abs_stat_error = utils.binomial_ratio_and_error(n_passed[step], n_total[step])
            if eff[0] < 1e-4:
                eff_stat_error[0] = 1  # avoid zero division error and divergence
                continue  # not fill values in tree if efficiency is too small
            else:
                eff_stat_error[0] = abs_stat_error / eff[0]
            if eff_stat_error[0] > 1:
                print(n_passed[step], n_total[step], abs_stat_error, eff[0], eff_stat_error[0])
                eff_stat_error[0] = 1.
            tree.Fill()
    output_tfile.Write()
    output_tfile.Close()


def make_systematic_table():
    AtlasStyle.SetAtlasStyle()

    #directory = '/afs/cern.ch/work/k/kmotohas/DisplacedVertex/DV_xAODAnalysis/submitDir_LSF/mc/hist_DVPlusMETSys/'
    directory = BasicConfig.workdir + 'hist_DVPlusMETSys/'

    tfile = TFile(BasicConfig.workdir + 'systTree.root')
    key_list_all = [key.GetName() for key in gDirectory.GetListOfKeys()]
    print(len(key_list_all), key_list_all)
    regex = re.compile('Nominal|PRW|JET|MET.*')
    key_list = [key for key in key_list_all if re.match(regex, key)]
    print(len(key_list), key_list)
    tfile.Close()

    output_tfile = TFile('systematic_summary_SimpleMETFilter.root', 'recreate')

    tchains = [[dsid, [TChain(key, key+str(dsid)) for key in key_list]] for dsid in range(402700, 402740)]

    #trees = [gROOT.FindObject(key) for key in key_list]
    #entries_list = [tree.GetEntriesFast() for tree in trees]

    gStyle.SetHistMinimumZero()

    for dsid, each_tchain in tchains:
        print('')
        print(dsid)
        for tchain in each_tchain:
            for input in glob(directory + 'systTree_' + str(dsid) + '_*.root'):
                #print(input)
                tchain.Add(input)

        #h_syst_diff = TH1F('syst_diff', ';Difference from Nominal', 101, -50.5, 50.5, 120, 0, 120)
        h_syst_diff = TH1F('syst_diff', ';;(N_{shifted} - N_{nominal}) / N_{nominal}', len(key_list)+1, 0, len(key_list)+1)
        for ii, key in enumerate(key_list):
            h_syst_diff.GetXaxis().SetBinLabel(ii+1, key)
        h_syst_diff.GetXaxis().SetBinLabel(len(key_list)+1, 'ISR_Py2MG_SF_removed')
        h_syst_diff.SetMinimum(-0.3)
        h_syst_diff.SetMaximum(0.3)

        n_events_nominal = 0.
        for ii, tchain in enumerate(each_tchain):
            #print('')
            print('*** ' + key_list[ii])
            n_events_weighted = 0.
            n_events_weighted_noISR = 0.
            entries = tchain.GetEntries()
            if entries == 0:
                continue
            for entry in xrange(entries):
                ## get the next tree in the chain and verify
                #ientry = tree.LoadTree(entry)
                #if ientry < 0:
                #    break
                ## copy next entry into memory and verify
                nb = tchain.GetEntry(entry)
                if nb <= 0:
                    continue
                #if pass_event_cut(tchain, 7):
                if pass_event_cut(tchain, 5) and tchain.MET > 220 and tchain.PassCut7:  # TODO
                #if pass_event_cut(tchain, 5) and tchain.MET > 250 and tchain.PassCut7:  # TODO
                    #print(tree.McEventWeight, tree.PileupWeight)
                    n_events_weighted += tchain.McEventWeight * tchain.PileupWeight * tchain.ISRWeight
                    n_events_weighted_noISR += tchain.McEventWeight * tchain.PileupWeight
            if ii == 0:
                n_events_nominal = n_events_weighted
                if n_events_nominal < 1e-4:
                    h_syst_diff.SetBinContent(len(key_list)+1, 0)
                else:
                    h_syst_diff.SetBinContent(len(key_list)+1, float((n_events_weighted_noISR-n_events_nominal)/n_events_nominal))
            diff = n_events_weighted - n_events_nominal
            #print(n_events_nominal, n_events_weighted, diff)
            if n_events_nominal < 1e-4:
                h_syst_diff.SetBinContent(ii+1, 0)
            else:
                h_syst_diff.SetBinContent(ii+1, float(diff/n_events_nominal))
            #h_syst_diff.SetBinError(ii+1, n_event_weighted-n_events_nominal)
        utils.decorate_histogram(h_syst_diff, kPink, fill_style=3001)
        h_syst_diff.SetBarWidth(0.9)
        h_syst_diff.GetXaxis().SetLabelSize(0.035)
        output_tfile.cd()
        h_syst_diff.SetName('systematic_table_'+str(dsid))
        h_syst_diff.Write()
        #h_syst_diff.Draw('hbar')

if __name__ == '__main__':
    make_systematic_table()
    fill_ntuple()
    check_n_vertices_vs_met_threshold()
    #create_cut_flow()
