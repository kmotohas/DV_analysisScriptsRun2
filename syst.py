#!/usr/bin/env python
import re
#import os
from glob import glob
from array import array
#import numpy as np

# ROOT
from ROOT import gROOT
from ROOT import gDirectory
from ROOT import gStyle

from ROOT import TFile
from ROOT import TTree
from ROOT import TChain
from ROOT import TH1F
from ROOT import TEfficiency
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

import argparse
parser = argparse.ArgumentParser()
#parser.add_argument('-f', '--inputFiles', type=str, help='comma separated input files')
parser.add_argument('-f', '--inputFile', type=str, help='input file')
parser.add_argument('-o', '--outputFile', type=str, help='output file name')
parser.add_argument('-r', '--referenceFile', type=str, help='reference file name')
parser.add_argument('-d', '--DSID', type=int, help='DSID')
args = parser.parse_args()

#input_files = args.inputFiles.split(',')
print('*** input files: ')
print(args.inputFile)
print('*** output files: ')
print(args.outputFile)
print('*** reference files: ')
print(args.referenceFile)
print('*** DSID: ')
print(args.DSID)

#print('*** output file: ')
#print(args.outputFile)
#output_root = TFile(args.outputFile, 'recreate')


def pass_event_cut(tree, cut_level):
    # [1: Trigger, 2: Filter, 3: Cleaning, 4: GRL,
    #  5: PV, 6: MET, 7: DV Selection]
    # from v06-00-05
    # [1: Trigger, 2: Filter, 3: Cleaning, 4: GRL,
    #  5: PV, 6: NCB, 7: MET, 8: DV Selection]
    event_cuts = [tree.PassCut1, tree.PassCut2, tree.PassCut3, tree.PassCut4,
                  tree.PassCut5, PassNCBVeto(tree), tree.PassCut7, tree.PassCut8]
    #event_cuts = [tree.PassMetTrigger, tree.PassMetFilter, tree.PassGRL, tree.PassEventCleaning,
    #              tree.PassPVCuts, PassNCBCuts, tree.PassMETCut, tree.PassCut8]
    passed_or_not = True
    for cut in event_cuts[:cut_level]:
        passed_or_not &= cut
    return passed_or_not


def PassNCBVeto(tree):
    if tree.Jet_n > 0 and len(tree.Jet_EMFrac) and len(tree.Jet_FracSamplingMax):
        return (tree.Jet_EMFrac[0] < 0.96 and tree.Jet_FracSamplingMax[0] < 0.8)
    else:
        if tree.Jet_n > 0:
            print(tree.Jet_n, len(tree.Jet_EMFrac), len(tree.Jet_FracSamplingMax))
        return True


def match(tree, idv, cut=1.0):
    from math import sqrt
    for irh in range(len(tree.Rhadron_vtx_x)):
        dr = sqrt( (tree.DV_x[idv]-tree.Rhadron_vtx_x[irh])**2.0 
                 + (tree.DV_y[idv]-tree.Rhadron_vtx_y[irh])**2.0 )
        dL = sqrt( dr**2.0 + (tree.DV_z[idv]-tree.Rhadron_vtx_z[irh])**2.0) 
        if dL < cut:
            return True
    return False


def root_sum_squares(histogram, axis):
    sum_squares_up = 0.
    sum_squares_down = 0.
    sum_squares_ISR = 0.
    sum_squares_PRW = 0.
    sum_squares_JET = 0.
    sum_squares_MET = 0.
    if axis == 'x':
        for ibin in range(1, histogram.GetNbinsX()+1):
            print(histogram.GetXaxis().GetBinLabel(ibin))

            if histogram.GetBinContent(ibin) > 0:
                sum_squares_up += histogram.GetBinContent(ibin) ** 2 
            else:
                sum_squares_down += histogram.GetBinContent(ibin) ** 2 
            if 'ISR' in histogram.GetXaxis().GetBinLabel(ibin):
                sum_squares_ISR += histogram.GetBinContent(ibin) ** 2
            elif 'PRW' in histogram.GetXaxis().GetBinLabel(ibin):
                sum_squares_PRW += histogram.GetBinContent(ibin) ** 2
            elif 'JET' in histogram.GetXaxis().GetBinLabel(ibin):
                sum_squares_JET += histogram.GetBinContent(ibin) ** 2
            elif 'MET' in histogram.GetXaxis().GetBinLabel(ibin):
                sum_squares_MET += histogram.GetBinContent(ibin) ** 2
        return [sum_squares_up**0.5,
                sum_squares_down**0.5,
                sum_squares_ISR**0.5,
                sum_squares_PRW**0.5,
                sum_squares_JET**0.5,
                sum_squares_MET**0.5]


def get_lifetime_weight(tree, ctau, ctau_MC):
    if len(tree.Rhadron_properdecaytime) != 2:
        #print('vector size of Rhadron_properdecaytime is not 2. return weight=0.')
        return 0
    dt1 = tree.Rhadron_properdecaytime[0] * 1e-9  # [ns]->[s]
    dt2 = tree.Rhadron_properdecaytime[1] * 1e-9  # [ns]->[s]
    tau = ctau / TMath.C()
    tau_MC = ctau_MC / TMath.C()
    weight_rhad1 = tau_MC/tau * TMath.Exp(dt1/tau_MC - dt1/tau)
    weight_rhad2 = tau_MC/tau * TMath.Exp(dt2/tau_MC - dt2/tau)
    return weight_rhad1 * weight_rhad2


#def pass_base_event_selection(tree):
#    #base_cuts = [tree.PassCut3, tree.PassCut4, tree.PassCut5, PassNCBVeto(tree)]
#    base_cuts = [tree.PassCut3, tree.PassCut4, tree.PassCut5]
#    passed_or_not = True
#    for cut in base_cuts:
#        passed_or_not &= cut
#    return passed_or_not
#
#
#def pass_base_dv_selection(tree, dv_index):
#    #dv_base_cuts = [tree.DV_passFidCuts, tree.DV_passChisqCut, tree.DV_passDistCut, tree.DV_passMatVeto]
#    dv_base_cuts = [tree.DV_passFidCuts, tree.DV_passChisqCut, tree.DV_passDistCut, tree.DV_passMatVeto2p1, tree.DV_passDisabledModuleVeto]
#    passed_or_not = True
#    for cut in dv_base_cuts:
#        passed_or_not = passed_or_not and cut[dv_index]
#    return passed_or_not


def check_n_vertices_vs_met_threshold():
    AtlasStyle.SetAtlasStyle()

    #input_tfile = utils.open_tfile(BasicConfig.workdir + 'DVTree_NTuple_data15_13TeV.root')
    input_tfile = utils.open_tfile(args.inputFile)
    #tree = input_tfile.Get('DVTree_NTuple')
    tree = input_tfile.Get('Nominal')

    #bin_name = ['Base', 'Trigger', 'Filter', 'MET200', 'MET220', 'MET250']
    bin_name = ['Base', 'Trigger', 'Filter', 'MET250']
    h_nevents_cut = TH1F('nevents_cut', ';;Double Ratio', len(bin_name), 0, len(bin_name))
    h_nevents_all = TH1F('nevents_all', ';;Double Ratio', len(bin_name), 0, len(bin_name))
    h_ndvs_cut = {ntracks: TH1F('ndvs_cut_'+str(ntracks), ';;Double Ratio', len(bin_name), 0, len(bin_name))
                  for ntracks in range(2, 6)}
    h_ndvs_all = {ntracks: TH1F('ndvs_all_'+str(ntracks), ';;Double Ratio', len(bin_name), 0, len(bin_name))
                  for ntracks in range(2, 6)}
    for bin, name in enumerate(bin_name):
        h_nevents_cut.GetXaxis().SetBinLabel(bin+1, name)
        h_nevents_all.GetXaxis().SetBinLabel(bin+1, name)
        for ntracks in range(2, 6):
            h_ndvs_cut[ntracks].GetXaxis().SetBinLabel(bin+1, name)
            h_ndvs_all[ntracks].GetXaxis().SetBinLabel(bin+1, name)
    entries = tree.GetEntries()
    for entry in range(entries):
        utils.show_progress(entry, entries)
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
        if not utils.basic_event_selection(tree):
            continue
        # fill all
        for name in bin_name:
            h_nevents_all.Fill(name, 1.)
            for dv_index, DV_nTracks in enumerate(tree.DV_nTracks):
                if utils.basic_dv_selection(tree, dv_index):
                    if DV_nTracks < 6:
                        h_ndvs_all[DV_nTracks].Fill(name, 1.)
                    else:
                        h_ndvs_all[5].Fill(name, 1.)
        #
        h_nevents_cut.Fill('Base', 1.)
        for dv_index, DV_nTracks in enumerate(tree.DV_nTracks):
            if utils.basic_dv_selection(tree, dv_index):
                if DV_nTracks < 6:
                    h_ndvs_cut[DV_nTracks].Fill('Base', 1.)
                else:
                    h_ndvs_cut[5].Fill('Base', 1.)
        # Trigger
        if not tree.PassCut1:
            continue
        h_nevents_cut.Fill('Trigger', 1.)
        for dv_index, DV_nTracks in enumerate(tree.DV_nTracks):
            if utils.basic_dv_selection(tree, dv_index):
                if DV_nTracks < 6:
                    h_ndvs_cut[DV_nTracks].Fill('Trigger', 1.)
                else:
                    h_ndvs_cut[5].Fill('Trigger', 1.)
        # Filter
        if not tree.PassCut2:
            continue
        h_nevents_cut.Fill('Filter', 1.)
        for dv_index, DV_nTracks in enumerate(tree.DV_nTracks):
            if utils.basic_dv_selection(tree, dv_index):
                if DV_nTracks < 6:
                    h_ndvs_cut[DV_nTracks].Fill('Filter', 1.)
                else:
                    h_ndvs_cut[5].Fill('Filter', 1.)
        ##
        #if not tree.MET > 200:
        #    continue
        #h_nevents_cut.Fill('MET200', 1.)
        #for dv_index, DV_nTracks in enumerate(tree.DV_nTracks):
        #    if pass_base_dv_selection(tree, dv_index):
        #        if DV_nTracks < 6:
        #            h_ndvs_cut[DV_nTracks].Fill(name, 1.)
        #        else:
        #            h_ndvs_cut[5].Fill(name, 1.)
        ##
        #if not tree.MET > 220:
        #    continue
        #h_nevents_cut.Fill('MET220', 1.)
        #for dv_index, DV_nTracks in enumerate(tree.DV_nTracks):
        #    if pass_base_dv_selection(tree, dv_index):
        #        if DV_nTracks < 6:
        #            h_ndvs_cut[DV_nTracks].Fill(name, 1.)
        #        else:
        #            h_ndvs_cut[5].Fill(name, 1.)
        #
        if not tree.MET > 250:
            continue
        h_nevents_cut.Fill('MET250', 1.)
        for dv_index, DV_nTracks in enumerate(tree.DV_nTracks):
            if utils.basic_dv_selection(tree, dv_index):
                if DV_nTracks < 6:
                    h_ndvs_cut[DV_nTracks].Fill('MET250', 1.)
                else:
                    h_ndvs_cut[5].Fill('MET250', 1.)
    #
    output_tfile = TFile(args.outputFile, 'recreate')
    #
    #canvas = TCanvas('canvas', 'canvas', 1200, 800) #h_ndvs_all_clone = h_ndvs_all[2].Clone('unit')
    #h_ndvs_all_clone.Divide(h_ndvs_all[2])
    #h_ndvs_all_clone.SetMaximum(3)
    #h_ndvs_all_clone.SetMinimum(0)
    #h_ndvs_all_clone.Draw()
    #legend = TLegend(0.5, 0.6, 0.85, 0.85)
    h_nevents_cut.Write()
    h_nevents_all.Write()
    for DV_nTracks in range(2, 6):
        h_ndvs_cut[DV_nTracks].Write()
        h_ndvs_all[DV_nTracks].Write()
    #
    #    h_ndvs_cut[DV_nTracks].Sumw2()
    #    h_ndvs_cut[DV_nTracks].Divide(h_ndvs_all[DV_nTracks])
    #    h_ndvs_cut[DV_nTracks].Divide(h_nevents_cut)
    #    h_ndvs_cut[DV_nTracks].Multiply(h_nevents_all)
    #    utils.decorate_histogram(h_ndvs_cut[DV_nTracks], BasicConfig.colors[DV_nTracks])
    #    h_ndvs_cut[DV_nTracks].Draw('same,hist')
    #    legend.AddEntry(h_ndvs_cut[DV_nTracks],
    #                    '('+str(DV_nTracks)+'trk-DVs(cut)/2trk-DVs(all))/(Events(cut)/Events(all))', 'l')
    #utils.decorate_legend(legend)
    #legend.Draw()
    #utils.save_as(canvas, BasicConfig.plotdir + 'nVerts_met_dependency')
    #output = TFile('nVerts_met_dependency.root', 'recreate')
    #canvas.Write()
    output_tfile.Close()


def create_cut_flow():
    AtlasStyle.SetAtlasStyle()

    #input_tfile = utils.open_tfile(BasicConfig.workdir + 'DVTree_NTuple_data15_13TeV.root')
    #tree = input_tfile.Get('DVTree_NTuple')
    input_tfile = utils.open_tfile(args.inputFile)
    tree = input_tfile.Get('Nominal')

    cut_flow = ['Initial', 'Trigger', 'Filter', 'Cleaning', 'GRL', 'PV', 
                'NCB veto', 'MET', 'DV Selection']
    h_cut_flow = TH1F('cut_flow', ';;Number of Events', len(cut_flow), 0, len(cut_flow))
    #h_cut_flow2 = TH1F('cut_flow2', ';;Number of Events', len(cut_flow), 0, len(cut_flow))
    for bin, cut in enumerate(cut_flow):
        h_cut_flow.GetXaxis().SetBinLabel(bin+1, cut)
    #
    entries = tree.GetEntries()
    for entry in range(entries):
        #if entry % 10000 == 0:
        #    print('*** processed {0} out of {1}'.format(entry, entries))
        utils.show_progress(entry, entries)
        #if entry == 100000:
        #    break
        # get the next tree in the chain and verify
        ientry = tree.LoadTree(entry)
        if ientry < 0:
            break
        # copy next entry into memory and verify
        nb = tree.GetEntry(entry)
        if nb <= 0:
            continue
        event_weight = tree.McEventWeight * tree.PileupWeight * tree.ISRWeight
        for step, cut in enumerate(cut_flow):
            if step == 0:
                h_cut_flow.Fill(cut, event_weight)
                #h_cut_flow2.Fill(cut, event_weight)
            #elif step == 2:
            #    if tree.RandomRunNumber < 309311 and pass_event_cut(tree, 2):
            #        h_cut_flow.Fill(cut, event_weight)
            #    if tree.RandomRunNumber > 309311 and pass_event_cut(tree, 2):
            #        h_cut_flow2.Fill(cut, event_weight)
            #elif step == 6:
            #    if tree.RandomRunNumber < 309311 and pass_event_cut(tree, 6):
            #        h_cut_flow.Fill(cut, event_weight)
            #    if tree.RandomRunNumber > 309311 and pass_event_cut(tree, 6):
            #        h_cut_flow2.Fill(cut, event_weight)
            #elif step == 7:
            #    #have_signal_like_dv = False
            #    #for dv_index in range(len(tree.DV_passVtxCuts)):
            #    #    have_signal_like_dv = have_signal_like_dv or tree.DV_passVtxCuts[dv_index]
            #    #if pass_event_cut(tree, 7) and tree.MET > 220 and have_signal_like_dv:
            #    if tree.RandomRunNumber < 309311 and pass_event_cut(tree, 7):
            #        h_cut_flow.Fill(cut, event_weight)
            #    if tree.RandomRunNumber > 309311 and pass_event_cut(tree, 7):
            #        h_cut_flow2.Fill(cut, event_weight)
            elif pass_event_cut(tree, step):
                h_cut_flow.Fill(cut, event_weight)
                #h_cut_flow2.Fill(cut, event_weight)
    output = TFile('cut_flow.root', 'recreate')
    h_cut_flow.Write()
    output.Close()


def fill_ntuple():
    print('*** starting fill_ntuple() ')
    AtlasStyle.SetAtlasStyle()

#    # get key list
#    tfile = TFile(BasicConfig.workdir + 'systTree.root')
#    key_list_all = [key.GetName() for key in gDirectory.GetListOfKeys()]
#    regex = re.compile('PRW|JET|MET.*')
#    key_list = [key for key in key_list_all if re.match(regex, key)]
#    tfile.Close()

    # start making ttree
    #output_tfile = TFile('rhadron_v06-00-05.root', 'recreate')
    output_tfile = TFile(args.outputFile, 'recreate')

    # initialize TTree
    tree = TTree('rhadron', 'tree of rhadron properties for limit setting')
    # leaf variables
    from array import array
    mass_gluino = array('f', [0.])
    delta_mass = array('f', [0.])
    ctau = array('f', [0.])
    eff = array('f', [0.])
    eff_stat_error = array('f', [0.])
    eff_syst_error = array('f', [0.])
    eff_syst_error_ISR = array('f', [0.])
    eff_syst_error_PRW = array('f', [0.])
    eff_syst_error_JET = array('f', [0.])
    eff_syst_error_MET = array('f', [0.])
    # set branch
    tree.Branch("mGluino", mass_gluino, 'mGluino/F')
    tree.Branch("deltaM", delta_mass, 'deltaM/F')
    tree.Branch("ctau", ctau, 'ctau/F')
    tree.Branch("eff", eff, 'eff/F')
    tree.Branch("effRelStatErr", eff_stat_error, 'effRelStatErr/F')
    tree.Branch("effRelSystErr", eff_syst_error, 'effRelSystErr/F')
    tree.Branch("effRelSystErrISR", eff_syst_error_ISR, 'effRelSystErrISR/F')
    tree.Branch("effRelSystErrPRW", eff_syst_error_PRW, 'effRelSystErrPRW/F')
    tree.Branch("effRelSystErrJET", eff_syst_error_JET, 'effRelSystErrJET/F')
    tree.Branch("effRelSystErrMET", eff_syst_error_MET, 'effRelSystErrMET/F')

    #directory = '/afs/cern.ch/work/k/kmotohas/DisplacedVertex/DV_xAODAnalysis/submitDir_LSF/mc/hist_DVPlusMETSys/'
    #directory = BasicConfig.workdir + 'hist_DVPlusMETSys/'
    #directory = '/home/motohash/data/mc15_13TeV/DVPlusMETSys/v06-00-05/'

    #tfile = TFile(args.referenceFile)
    tfile = TFile(args.inputFile)
    key_list_all = [key.GetName() for key in gDirectory.GetListOfKeys()]
    print(len(key_list_all), key_list_all)
    regex = re.compile('Nominal|PRW|JET|MET.*')
    key_list = [key for key in key_list_all if re.match(regex, key)]
    print(len(key_list), key_list)
    tfile.Close()
    #c = 299792458.  # [m/s]
    #tchains = [[dsid, TChain('Nominal', str(dsid))] for dsid in range(402700, 402740)]
    #tchains = [[dsid, TChain('Nominal', str(dsid))] for dsid in mc.parameters.keys()]
    #tchains = [[dsid, [TChain(key, key+str(dsid)) for key in key_list]] for dsid in mc.parameters.keys()]
    dsids = [args.DSID]
    tchains = [[dsid, [TChain(key, key+str(dsid)) for key in key_list]] for dsid in dsids]

    cut_flow = ['Initial', 'Trigger', 'Filter', 'Cleaning', 'GRL', 'PV', 
                'NCB veto', 'MET', 'DV Selection']
    #systematic_tables = TFile('systematic_summary_SimpleMETFilter.root', 'open')
    #table = TH1F()

    m_MET_min = 250.

    # loop over dsid
    try:
        for dsid, each_tchain in tchains:
            print('')
            print(dsid)
            #index = 0
            #for input in glob(directory + 'systTree_' + str(dsid) + '_*.root'):
            for tchain in each_tchain:
                #for input_file in glob(directory+'systTree_mc15_13TeV.' + str(dsid) + '*.root'):
                #    print(input_file)
                #    tchain.Add(input_file)
                tchain.Add(args.inputFile)

            mass_gluino[0] = mc.parameters[dsid]['g']
            delta_mass[0] = mass_gluino[0] - mc.parameters[dsid]['chi0']
            n_reweight_steps = 40
            xmin = 1.
            xmax = 10000.
            ratio = xmax/xmin
            bins = []
            for ii in range(n_reweight_steps):
                bins.append(xmax * 10**(ii*TMath.Log10(xmax/xmin)/n_reweight_steps-TMath.Log10(xmax/xmin)))
            #n_passed_w1 = [0. for _ in range(n_reweight_steps)]
            #n_passed = [0. for _ in range(n_reweight_steps)]
            from array import array
            limitsLifetime = array('d', bins)
            #
            tefficiency = [[TEfficiency('tefficiency_{0}_{1}_{2}'.format(key, step, dsid), ';c#tau [mm]; Event-level efficiency', len(limitsLifetime)-1, limitsLifetime)
                            for step in range(n_reweight_steps)] for key in key_list]
            #h_syst_diff = [[TH1F('syst_diff_{0}_{1}_{2}'.format(key, step, dsid), ';;(N_{shifted} - N_{nominal}) / N_{nominal}', len(key_list)+1, 0, len(key_list)+1)
            #                for step in range(n_reweight_steps)] for key in key_list]
            h_syst_diff = [TH1F('syst_diff_{0}_{1}_{2}'.format(key, step, dsid), ';;(N_{shifted} - N_{nominal}) / N_{nominal}', len(key_list)+1, 0, len(key_list)+1)
                           for step in range(n_reweight_steps)]
            
            for step in range(n_reweight_steps):
                for jj, key in enumerate(key_list):
                     h_syst_diff[step].GetXaxis().SetBinLabel(jj+1, key)
                h_syst_diff[step].GetXaxis().SetBinLabel(len(key_list)+1, 'ISR_Py2MG_SF_removed')
            n_events_weighted = [[0. for _ in range(n_reweight_steps)] for key in key_list]
            n_events_weighted_noISR = [[0. for _ in range(n_reweight_steps)] for key in key_list]

            # loop over tchain of each systematic
            for ii, tchain in enumerate(each_tchain):
                entries = tchain.GetEntries()
                print('*** processed systs: {0} / {1}'.format(ii, len(each_tchain)))
                #n_reweight_steps = 50
                #for step in range(n_reweight_steps):
                #    tefficiency.append(TEfficiency('tefficiency_'+str(step), ';c#tau [mm]; Event-level efficiency',
                #                                   len(limitsLifetime)-1, limitsLifetime))
                #    h_syst_diff.append(TH1F('syst_diff_'+str(step), ';;(N_{shifted} - N_{nominal}) / N_{nominal}', len(key_list)+1, 0, len(key_list)+1))
                for step in range(n_reweight_steps):
                    tefficiency[ii][step].SetUseWeightedEvents()
                    #for jj, key in enumerate(key_list):
                    #     h_syst_diff[ii][step].GetXaxis().SetBinLabel(jj+1, key)
                    #h_syst_diff[ii][step].GetXaxis().SetBinLabel(len(key_list)+1, 'ISR_Py2MG_SF_removed')
                #    h_syst_diff[step].SetMinimum(-0.3)
                #    h_syst_diff[step].SetMaximum(0.3)
                if entries == 0:
                    continue
                for entry in range(entries):
                    #if entry % 1000 == 0:
                    #    print('* processed events: {0} / {1}'.format(entry, entries))
                    utils.show_progress(entry, entries)
                    #if entry == 605:
                    #    break
                    # get the next tree in the chain and verify
                    ientry = tchain.LoadTree(entry)
                    if ientry < 0:
                        break
                    # copy next entry into memory and verify
                    nb = tchain.GetEntry(entry)
                    if nb <= 0:
                        continue
                    event_weight = tchain.McEventWeight * tchain.PileupWeight * tchain.ISRWeight
                    ctau_MC = TMath.C() * mc.parameters[dsid]['t'] * 1e-9  # [nm]->[m]
                    for step in range(n_reweight_steps):
                        #print(tchain.GetListOfBranches())
                        pass_all = pass_event_cut(tchain, len(cut_flow)-1)
                        if pass_all:
                            matched = False
                            for idv in range(len(tchain.DV_x)):
                                matched = matched or match(tchain, idv, cut=1.0)
                            #print('pass_all is ', pass_all, ', matched is ', matched)
                            pass_all = pass_all and matched
                        target_ctau = xmax * 10**(step*TMath.Log10(xmax/xmin)/n_reweight_steps
                                                  -TMath.Log10(xmax/xmin)) * 1e-3 # [mm]->[m]
                        #print(target_ctau)
                        lifetime_weight = get_lifetime_weight(tchain, target_ctau, ctau_MC)
                        n_events_weighted[ii][step] += event_weight * lifetime_weight
                        n_events_weighted_noISR[ii][step] += tchain.McEventWeight * tchain.PileupWeight * lifetime_weight
                        #print(event_weight)
                        #print(event_weight*lifetime_weight)
                        #print(pass_all)
                        tefficiency[ii][step].FillWeighted(pass_all, event_weight*lifetime_weight, target_ctau*1e3)
                # end of loop over entries of each TChain
            # end loop over tchain of each systematic
            for step in range(n_reweight_steps):
                n_events_nominal = [0. for _ in range(n_reweight_steps)]
                for ii in range(len(each_tchain)):
                    # if Nominal TTree, set syst diff of ISR as well
                    if ii == 0:
                        n_events_nominal[step] = n_events_weighted[ii][step]
                        if n_events_nominal[step] < 1e-4:
                            #h_syst_diff[ii][step].SetBinContent(len(key_list)+1, 0)
                            h_syst_diff[step].SetBinContent(len(key_list)+1, 0)
                        else:
                            #h_syst_diff[ii][step].SetBinContent(len(key_list)+1,
                            h_syst_diff[step].SetBinContent(len(key_list)+1,
                                    float((n_events_weighted_noISR[ii][step]-n_events_nominal[step])/n_events_nominal[step]))
                                    #float((n_events_weighted[ii][step]-n_events_nominal[step])/n_events_nominal[step]))
                    diff = n_events_weighted[ii][step] - n_events_nominal[step]
                    #print(n_events_nominal, n_events_weighted, diff)
                    if n_events_nominal[step] < 1e-4:
                        #h_syst_diff[ii][step].SetBinContent(ii+1, 0)
                        h_syst_diff[step].SetBinContent(ii+1, 0)
                    else:
                        #h_syst_diff[ii][step].SetBinContent(ii+1, float(diff/n_events_nominal[step]))
                        h_syst_diff[step].SetBinContent(ii+1, float(diff/n_events_nominal[step]))
                    #systematic_tables.GetObject('systematic_table_'+str(dsid), table)
                    #syst_up, syst_down = root_sum_squares(table, 'x')
                #systs = root_sum_squares(h_syst_diff[ii][step], 'x')
                systs = root_sum_squares(h_syst_diff[step], 'x')
                #eff_syst_error[0] = max(syst_up, syst_down)  # TODO
                #eff_syst_error[0] = (syst_up**2 + syst_down**2)**0.5

####    ############################
                eff_syst_error[0] = (systs[0]**2 + systs[1]**2)**0.5
                eff_syst_error_ISR[0] = systs[2]
                eff_syst_error_PRW[0] = systs[3]
                eff_syst_error_JET[0] = systs[4]
                eff_syst_error_MET[0] = systs[5]
                if eff_syst_error[0] > 1:
                    print('eff_syst_error[0] = ' + str(eff_syst_error[0]))
                    #eff_syst_error[0] = 1.
                #for step in range(n_reweight_steps):
                #for ct in bins:
                #    print(len(bins), bins)
                    #print(n_total_w1[step], n_total[step])
                    #sf =  n_total_w1[step] / n_total[step]
                    #n_passed[step] *= sf
                    #n_total[step] *= sf
                    #eff_no_weight, stat_error_no_weight = utils.division_error_propagation(n_passed_w1[step], n_total_w1[step])
                    #ctau[0] = TMath.Power(300, step/float(n_reweight_steps-1)) * 1e-3  # [mm]->[m]
                ct = bins[step]
                #print(ct)
                ctau[0] = ct * 1e-3  # [mm]->[m]
                #print(ctau[0])
                bin_ctau = tefficiency[0][step].GetPassedHistogram().FindBin(ct)
                print(tefficiency[0][step].GetPassedHistogram().GetBinContent(bin_ctau))
                print(tefficiency[0][step].GetTotalHistogram().GetBinContent(bin_ctau))
                #print(bin_ctau)
                #print('ct', ct, 'bin_ctau', bin_ctau)
                eff[0] = tefficiency[0][step].GetEfficiency(bin_ctau)
                print(eff[0])
                abs_stat_error = (tefficiency[0][step].GetEfficiencyErrorLow(bin_ctau)**2
                                + tefficiency[0][step].GetEfficiencyErrorUp(bin_ctau)**2) ** 0.5
                #eff[0], abs_stat_error = utils.binomial_ratio_and_error(n_passed[step], n_total[step])
                #if eff[0] < 1e-4:
                if eff[0] == 0:
                    eff_stat_error[0] = 1.  # avoid zero division error and divergence
                    continue  # not fill values in tree if efficiency is too small
                else:
                    eff_stat_error[0] = abs_stat_error / eff[0]
                #if eff_stat_error[0] > 1:
                #    print(n_passed[step], n_total[step], abs_stat_error, eff[0], eff_stat_error[0])
                #    eff_stat_error[0] = 1.
                tree.Fill()
            # end loop over n_reweight_steps
    except KeyboardInterrupt:
        pass
    output_tfile.Write()
    output_tfile.Close()


def make_systematic_table():
    AtlasStyle.SetAtlasStyle()

    #directory = '/afs/cern.ch/work/k/kmotohas/DisplacedVertex/DV_xAODAnalysis/submitDir_LSF/mc/hist_DVPlusMETSys/'
    #directory = BasicConfig.workdir + 'hist_DVPlusMETSys/'
    directory = '/home/motohash/data/mc15_13TeV/DVPlusMETSys/'

    #tfile = TFile(BasicConfig.workdir + 'systTree.root')
    tfile = TFile(args.inputFile)
    key_list_all = [key.GetName() for key in gDirectory.GetListOfKeys()]
    print(len(key_list_all), key_list_all)
    regex = re.compile('Nominal|PRW|JET|MET.*')
    key_list = [key for key in key_list_all if re.match(regex, key)]
    print(len(key_list), key_list)
    tfile.Close()

    output_tfile = TFile('systematic_summary_SimpleMETFilter.root', 'recreate')

    #tchains = [[dsid, [TChain(key, key+str(dsid)) for key in key_list]] for dsid in range(402700, 402740)]
    tchains = [[dsid, [TChain(key, key+str(dsid)) for key in key_list]] for dsid in mc.parameters.keys()]
    #tchains = [[dsid, [TChain(key, key+str(dsid)) for key in key_list]] for dsid in range(402070, 402080)]
    #tchains = [[dsid, [TChain(key, key+str(dsid)) for key in key_list]] for dsid in range(402070, 402080)]

    #trees = [gROOT.FindObject(key) for key in key_list]
    #entries_list = [tree.GetEntriesFast() for tree in trees]

    gStyle.SetHistMinimumZero()

    for dsid, each_tchain in tchains:
        print('')
        print(dsid)
        #print glob(directory + 'systTree_mc15_13TeV.' + str(dsid) + '*.root')
        for tchain in each_tchain:
            for input in glob(directory + 'systTree_mc15_13TeV.' + str(dsid) + '*.root'):
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
                ientry = tchain.LoadTree(entry)
                if ientry < 0:
                    break
                ## copy next entry into memory and verify
                nb = tchain.GetEntry(entry)
                if nb <= 0:
                    continue
                #if pass_event_cut(tchain, 7):
                #if pass_event_cut(tchain, 5) and tchain.MET > 220 and tchain.PassCut7:  # TODO
                if pass_event_cut(tchain, len(cut_flow)-1):  # TODO
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
    #make_systematic_table()
    #fill_ntuple()
    check_n_vertices_vs_met_threshold()
    #create_cut_flow()
