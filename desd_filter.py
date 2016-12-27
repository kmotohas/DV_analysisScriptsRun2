#!/usr/bin/env python

import sys
import re
from datetime import date

#try:
import ROOT
import AtlasStyle
#except ImportError:
#    # on my laptop
#    sys.path.append('/usr/local/root/latest/lib')
#    sys.path.append(BasicConfig.workdir + 'DV_analysisScriptsRun2/')
#    import ROOT
#    import AtlasStyle

import BasicConfig
import utils
import mc


def superpose_tocs(passed_list, total, parameters):
    print('')
    print('*** start create_toc_plot')

    #if len(passed_list) != len(total_list):
    #    print('lengths of passed_list and total_list are different.')
    #    print('aborted.')
    #    sys.exit()

    canvas = ROOT.TCanvas("c", "c", 1000, 600)

    legend = ROOT.TLegend(0.6, 0.20, 0.85, 0.60)
    tgs = []
    for index, passed in enumerate(passed_list):
        if 'rebin' in parameters:
            passed.Rebin(parameters['rebin'])
            if index == 0:  # only once
                if passed.GetNbinsX() != total.GetNbinsX():
                    total.Rebin(parameters['rebin'])
        tg = ROOT.TGraphAsymmErrors(passed, total)
        utils.decorate_histogram(tg, BasicConfig.colors[index])
        if index == 0:
            tg.SetMaximum(1.09)
            tg.GetXaxis().SetRangeUser(0, 400)
            tg.GetYaxis().SetTitle('Efficiency')
            if 'x_title' in parameters:
                tg.GetXaxis().SetTitle(parameters['x_title'])
            tg.Draw('AP')
        else:
            tg.Draw('P,same')
        legend.AddEntry(tg, parameters['legend'][index], 'pl')
        tgs.append(tg)  # stored temporarily

    utils.decorate_legend(legend)
    legend.Draw()

    AtlasStyle.ATLASLabel(0.19, 0.85, 'Work in Progress')
    AtlasStyle.myText(0.20, 0.79, ROOT.kBlack, parameters['label'], 0.035)
    if 'label2' in parameters:
        AtlasStyle.myText(0.20, 0.74, ROOT.kBlack, parameters['label2'], 0.035)

    utils.save_as(canvas, BasicConfig.plotdir + parameters['plot_name'] + '_' + str(date.today()))


def get_met_filter_acceptance(passed_list, total, parameters):
    print('')
    print('*** start get_met_filter_acceptance')

    canvas = ROOT.TCanvas("c", "c", 1000, 600)
    canvas.SetLogy()

    n_bins = len(parameters['from_to'])
    bin_width = (parameters['from_to'][-1] - parameters['from_to'][0]) / n_bins
    histo = [ROOT.TH1F('histo' + str(x), ';MET_LocHadTopo Threshold [GeV];Acceptance', n_bins,
                       parameters['from_to'][0] - bin_width / 2.,
                       parameters['from_to'][-1] + bin_width / 2.) for x in range(len(passed_list))]

    legend = ROOT.TLegend(0.6, 0.50, 0.85, 0.85)
    denominator = total.Integral(0, -1)
    for (ii, passed) in enumerate(passed_list):
        utils.decorate_histogram(histo[ii], BasicConfig.colors[ii])
        for threshold in parameters['from_to']:
            numerator = passed.Integral(passed.FindBin(threshold), -1)
            acceptance, error = utils.division_error_propagation(numerator, denominator)
            histo[ii].SetBinContent(histo[ii].FindBin(threshold), acceptance)
            histo[ii].SetBinError(histo[ii].FindBin(threshold), error)
            if ii == 0:
                if 'max_min' in parameters:
                    histo[ii].SetMaximum(parameters['max_min'][0])
                    histo[ii].SetMinimum(parameters['max_min'][1])
                histo[ii].Draw('e1')
            else:
                histo[ii].Draw('same,e1')
        legend.AddEntry(histo[ii], parameters['legend'][ii], 'ple')

    if 'reference' in parameters:
        ref_acceptance = parameters['reference'].Integral(0, -1) / denominator
        print ref_acceptance
        canvas.Update()
        tl = ROOT.TLine(canvas.GetUxmin(), ref_acceptance, canvas.GetUxmax(), ref_acceptance)
        tl.SetLineColor(ROOT.kGray+1)
        tl.SetLineStyle(2)
        tl.Draw()

    utils.decorate_legend(legend)
    legend.Draw()

    AtlasStyle.ATLASLabel(0.19, 0.85, 'Work in Progress')
    AtlasStyle.myText(0.20, 0.79, ROOT.kBlack, parameters['label'], 0.035)
    if 'label2' in parameters:
        AtlasStyle.myText(0.20, 0.74, ROOT.kBlack, parameters['label2'], 0.035)

    utils.save_as(canvas, BasicConfig.plotdir + parameters['plot_name'] + '_' + str(date.today()))


def compare_signal_efficiencies_2d(passed, ref, total, dsids, parameters):
    print('')
    print('*** start compare_signal_efficiencies')

    canvas = ROOT.TCanvas("c", "c", 1000, 600)
    canvas.SetLogz()

    y_labels = ['30', '50', '80', '130', 'M_{#tilde{g}} - 100']
    histo = ROOT.TH2F('histo', ';M_{#tilde{g}} [GeV];#DeltaM [GeV]', 8, 500, 2100, 5, 0, 5)
    histo_ref = ROOT.TH2F('histo_ref', ';M_{#tilde{g}} [GeV];#Delta M', 8, 500, 2100, 5, 0, 5)
    for ii, y_label in enumerate(y_labels):
        histo.GetYaxis().SetBinLabel(ii+1, y_label)
        histo_ref.GetYaxis().SetBinLabel(ii+1, y_label)

    for ii, (met, trackless, all, dsid) in enumerate(zip(passed, ref, total, dsids)):
        numerator = met[8].Integral(met[8].FindBin(250), -1)
        reference = trackless[0].Integral(trackless[0].FindBin(220), -1)
        denominator = all[0].Integral(0, -1)
        print(numerator, reference, denominator)
        m_g = mc.parameters[dsid]['g']
        m_chi0 = mc.parameters[dsid]['chi0']
        dM = m_g - m_chi0 if m_chi0 != 100 else 'M_{#tilde{g}} - 100'
        histo.Fill(mc.parameters[dsid]['g'], str(dM), numerator / denominator)
        histo_ref.Fill(mc.parameters[dsid]['g'], str(dM), reference / denominator)

    histo.Draw('colz,TEXT45')
    utils.save_as(canvas, BasicConfig.plotdir + parameters['plot_name'] + '_' + str(date.today()))

    canvas_ref = ROOT.TCanvas("c_ref", "c_ref", 1000, 600)
    canvas_ref.SetLogz()
    histo_ref.Draw('colz,TEXT45')
    utils.save_as(canvas_ref, BasicConfig.plotdir + parameters['plot_name_ref'] + '_' + str(date.today()))

    canvas_ratio = ROOT.TCanvas("c_ratio", "c_ratio", 1000, 600)
    canvas_ratio.SetLogz()
    histo.Divide(histo_ref)
    histo.Draw('colz,TEXT45')
    utils.save_as(canvas_ratio, BasicConfig.plotdir + parameters['plot_name_ratio'] + '_' + str(date.today()))

    #AtlasStyle.ATLASLabel(0.19, 0.85, 'Work in Progress')
    #AtlasStyle.myText(0.20, 0.79, ROOT.kBlack, parameters['label'], 0.035)
    #if 'label2' in parameters:
    #    AtlasStyle.myText(0.20, 0.74, ROOT.kBlack, parameters['label2'], 0.035)



if __name__ == '__main__':
    AtlasStyle.SetAtlasStyle()

    # data
    path_to_root_file = [
        # 2016 Period F Full AOD
        'user.kmotohas.data16_13TeV.304494_AOD.SysUnc_MET.v3_histograms.root/'
        + 'all_data16_13TeV.304494_AOD.SysUnc_MET.v3_histograms.root',
        # 2016 Period F DAOD_JETM2
        'user.kmotohas.data16_13TeV.304337_DAOD_JETM2.SysUnc_MET.v3_histograms.root/'
        + 'all_data16_13TeV.304337_DAOD_JETM2.SysUnc_MET.v3_histograms.root',
        # 2015 Period D DAOD_JETM2
        'all_JETM2_2015_PeriodD.root',
        # 2016 Period C DAOD_JETM2
        'all_JETM2_2016_PeriodC.root',
        # 2016 Period C DAOD_JETM1
        'all_data16_13TeV.PeriodC.DAOD_JETM1.SysUnc_MET.root',
        # 2016 Period F DAOD_JETM1
        'all_data16_13TeV.PeriodF.DAOD_JETM1.SysUnc_MET.root',
        # 2015 Period J DAOD_JETM1
        'all_data15_13TeV.PeriodJ.DAOD_JETM1.SysUnc_MET.root'
    ]

    tf = [utils.open_tfile(BasicConfig.histodir + x) for x in path_to_root_file]

    # mc
    mc_file_list = open(BasicConfig.workdir + 'DV_analysisScriptsRun2/mc_SysUnc_MET.list', 'r')
    tf_mc = [utils.open_tfile(x.rstrip()) for x in mc_file_list]

    mc_file_list = open(BasicConfig.workdir + 'DV_analysisScriptsRun2/mc_SysUnc_MET.list', 'r')
    dsid = [int(re.sub('.*hist_run', '', x)[:6]) for x in mc_file_list]
    # for x in mc_file_list:
    #     tf_mc.append(utils.open_tfile(x.rstrip()))
    #     dsid.append(int(re.sub('.*hist_run', '', x)[:6]))

    #legend_trigger = ['HLT_xe100_tc_lcw', 'HLT_xe100_tc_lcw_wEFMu',
    #                  'HLT_xe100_mht_L1XE50', 'HLT_xe110_mht_L1XE50', 'HLT_xe120_mht_L1XE50']
    legend_trigger = ['HLT_xe110_mht_L1XE50']

    key_list_passed_trigger = ['calibMET_' + x + '_SysUnc_MET' for x in legend_trigger]
    key_list_passed_lht = ['calibMET_passed_MET_LHT_' + str(x) + '_SysUnc_MET' for x in range(100, 200, 10)]
    key_list_passed_xe100_lht = ['calibMET_passed_xe100_MET_LHT_' + str(x) + '_SysUnc_MET' for x in range(100, 200, 10)]
    key_list_total = ['calibMET_SysUnc_MET', 'MET_LocHadTopo_SysUnc_MET']

    # legend_trigger_2 = ['HLT_xe100_mht_L1XE50', 'HLT_xe110_mht_L1XE50', 'HLT_xe120_mht_L1XE50', 'Any in the MET Filter']
    legend_trigger_2 = ['HLT_xe100_mht_L1XE50', 'HLT_xe110_mht_L1XE50', 'HLT_xe120_mht_L1XE50']

    # key_list_lht_passed_trigger = ['MET_LocHadTopo_xe100_SysUnc_MET', 'MET_LocHadTopo_xe110_SysUnc_MET',
    #                               'MET_LocHadTopo_xe120_SysUnc_MET', 'MET_LocHadTopo_xeAny_SysUnc_MET']

    key_list_lht_passed_trigger = ['MET_LocHadTopo_xe100_SysUnc_MET', 'MET_LocHadTopo_xe110_SysUnc_MET',
                                   'MET_LocHadTopo_xe120_SysUnc_MET']

    key_list_trackless = ['calibMET_passed_trackless_filter_SysUnc_MET']

    # prepare cases for TH1F histograms
    passed_trigger_list = [
        [ROOT.TH1F() for _ in range(len(key_list_passed_trigger))] for __ in range(len(path_to_root_file))
        ]
    passed_lht_list = [
        [ROOT.TH1F() for _ in range(len(key_list_passed_lht))] for __ in range(len(path_to_root_file))
        ]
    lht_passed_trigger_list = [
        [ROOT.TH1F() for _ in range(len(key_list_lht_passed_trigger))] for __ in range(len(path_to_root_file))
        ]
    total_list = [
        [ROOT.TH1F() for _ in range(len(key_list_total))] for __ in range(len(path_to_root_file))
        ]
    trackless_list = [
        [ROOT.TH1F() for _ in range(len(key_list_trackless))] for __ in range(len(path_to_root_file))
        ]
    # MC
    mc_passed_xe100_lht_list = [
        [ROOT.TH1F() for _ in range(len(key_list_passed_xe100_lht))] for __ in range(len(dsid))
        ]
    mc_trackless_list = [
        [ROOT.TH1F() for _ in range(len(key_list_trackless))] for __ in range(len(dsid))
        ]
    mc_total_list = [
        [ROOT.TH1F() for _ in range(len(key_list_total))] for __ in range(len(dsid))
        ]

    for (ii, xx) in enumerate(passed_trigger_list):
        for (passed, key) in zip(xx, key_list_passed_trigger):
            tf[ii].GetObject(key, passed)
    for (ii, xx) in enumerate(passed_lht_list):
        for (passed, key) in zip(xx, key_list_passed_lht):
            tf[ii].GetObject(key, passed)
    for (ii, xx) in enumerate(lht_passed_trigger_list):
        for (passed, key) in zip(xx, key_list_lht_passed_trigger):
            tf[ii].GetObject(key, passed)
    for (ii, xx) in enumerate(total_list):
        for (total, key) in zip(xx, key_list_total):
            tf[ii].GetObject(key, total)
    for (ii, xx) in enumerate(trackless_list):
        for (passed, key) in zip(xx, key_list_trackless):
            tf[ii].GetObject(key, passed)
    # MC
    for (ii, xx) in enumerate(mc_passed_xe100_lht_list):
        for (passed, key) in zip(xx, key_list_passed_xe100_lht):
            tf_mc[ii].GetObject(key, passed)
    for (ii, xx) in enumerate(mc_trackless_list):
        for (passed, key) in zip(xx, key_list_trackless):
            tf_mc[ii].GetObject(key, passed)
    for (ii, xx) in enumerate(mc_total_list):
        for (total, key) in zip(xx, key_list_total):
            tf_mc[ii].GetObject(key, total)


    # legend_trigger = ['HLT_xe' + str(x) + '_mht_L1XE50' for x in range(110, 121, 10)]

    parameters_trigger = [
        {'rebin': 2, 'plot_name': 'Trigger_TOC_2016_run304494', 'x_title': "Missing E_{T} [GeV]",
         'label': 'data16_13TeV PeriodF', 'label2':'run 304494 Full AOD', 'legend': legend_trigger},
        {'rebin': 2, 'plot_name': 'Trigger_TOC_2016_run304337', 'x_title': "Missing E_{T} [GeV]",
         'label': 'data16_13TeV PeriodF', 'label2':'run 304337 DAOD_JETM2', 'legend': legend_trigger},
        {'rebin': 2, 'plot_name': 'Trigger_TOC_2015_PeriodD', 'x_title': "Missing E_{T} [GeV]",
         'label': 'data15_13TeV PeriodD', 'label2':'DAOD_JETM2', 'legend': legend_trigger},
        {'rebin': 2, 'plot_name': 'Trigger_TOC_2016_PeriodC_DAOD_JETM2', 'x_title': "Missing E_{T} [GeV]",
         'label': 'data16_13TeV PeriodC', 'label2':'DAOD_JETM2', 'legend': legend_trigger},
        {'rebin': 2, 'plot_name': 'Trigger_TOC_2016_PeriodC_DAOD_JETM1', 'x_title': "Missing E_{T} [GeV]",
         'label': 'data16_13TeV PeriodC', 'label2':'DAOD_JETM1', 'legend': legend_trigger},
        {'rebin': 2, 'plot_name': 'Trigger_TOC_2016_PeriodF_DAOD_JETM1', 'x_title': "Missing E_{T} [GeV]",
         'label': 'data16_13TeV PeriodF', 'label2':'DAOD_JETM1', 'legend': legend_trigger},
        {'rebin': 2, 'plot_name': 'Trigger_TOC_2015_PeriodJ_DAOD_JETM1', 'x_title': "Missing E_{T} [GeV]",
         'label': 'data15_13TeV PeriodJ', 'label2':'DAOD_JETM1', 'legend': legend_trigger}
    ]

    # superpose_tocs(passed_trigger_list[0], total_list[0][0], parameters_trigger[0])
    # superpose_tocs(passed_trigger_list[1], total_list[1][0], parameters_trigger[1])
    # superpose_tocs(passed_trigger_list[2], total_list[2][0], parameters_trigger[2])
    # superpose_tocs(passed_trigger_list[3], total_list[3][0], parameters_trigger[3])
    # superpose_tocs(passed_trigger_list[4], total_list[4][0], parameters_trigger[4])
    # superpose_tocs(passed_trigger_list[5], total_list[5][0], parameters_trigger[5])
    # superpose_tocs(passed_trigger_list[6], total_list[6][0], parameters_trigger[6])

    legend_lht = ['MET_LocHadTopo > ' + str(x) + ' [GeV]' for x in range(100, 200, 10)]

    parameters_lht = [
        {'rebin': 2, 'plot_name': 'MET_LHT_TOC_2016_run304494', 'x_title': "Missing E_{T} [GeV]",
         'label': 'data16_13TeV PeriodF', 'label2':'run 304494 Full AOD', 'legend': legend_lht},
        {'rebin': 2, 'plot_name': 'MET_LHT_TOC_2016_run304337', 'x_title': "Missing E_{T} [GeV]",
         'label': 'data16_13TeV PeriodF', 'label2':'run 304337 DAOD_JETM2', 'legend': legend_lht},
        {'rebin': 2, 'plot_name': 'MET_LHT_TOC_2015_PeriodD', 'x_title': "Missing E_{T} [GeV]",
         'label': 'data15_13TeV PeriodD', 'label2':'DAOD_JETM2', 'legend': legend_lht},
        {'rebin': 2, 'plot_name': 'MET_LHT_TOC_2016_PeriodC_DAOD_JETM2', 'x_title': "Missing E_{T} [GeV]",
         'label': 'data16_13TeV PeriodC', 'label2':'DAOD_JETM2', 'legend': legend_lht},
        {'rebin': 2, 'plot_name': 'MET_LHT_TOC_2016_PeriodC_DAOD_JETM1', 'x_title': "Missing E_{T} [GeV]",
         'label': 'data16_13TeV PeriodC', 'label2':'DAOD_JETM1', 'legend': legend_lht},
        {'rebin': 2, 'plot_name': 'MET_LHT_TOC_2016_PeriodF_DAOD_JETM1', 'x_title': "Missing E_{T} [GeV]",
         'label': 'data16_13TeV PeriodF', 'label2':'DAOD_JETM1', 'legend': legend_lht},
        {'rebin': 2, 'plot_name': 'MET_LHT_TOC_2015_PeriodJ_DAOD_JETM1', 'x_title': "Missing E_{T} [GeV]",
         'label': 'data15_13TeV PeriodJ', 'label2':'DAOD_JETM1', 'legend': legend_lht},
    ]

    # superpose_tocs(passed_lht_list[0], total_list[0][0], parameters_lht[0])
    # superpose_tocs(passed_lht_list[1], total_list[1][0], parameters_lht[1])
    # superpose_tocs(passed_lht_list[2], total_list[2][0], parameters_lht[2])
    # superpose_tocs(passed_lht_list[3], total_list[3][0], parameters_lht[3])
    # superpose_tocs(passed_lht_list[4], total_list[4][0], parameters_lht[4])
    superpose_tocs(passed_lht_list[5], total_list[5][0], parameters_lht[5])
    # superpose_tocs(passed_lht_list[6], total_list[6][0], parameters_lht[6])

    parameters_met_acc = {'plot_name': 'met_acceptance_2016_run304494',
                          'label': 'data16_13TeV PeriodF',
                          'label2': 'run 304494 Full AOD',
                          'from_to': range(100, 200, 10), 'reference': trackless_list[0][0],
                          'max_min': [5.9e-1, 1.1e-3], 'legend': legend_trigger_2}

    # get_met_filter_acceptance(lht_passed_trigger_list[0], total_list[0][1], parameters_met_acc)

    parameters_signal_efficiencies = {'plot_name': 'signal_efficiencies_mc',
                                      'plot_name_ref': 'signal_efficiencies_mc_trackless',
                                      'plot_name_ratio': 'signal_efficiencies_mc_ratio'}

    #compare_signal_efficiencies_2d(mc_passed_xe100_lht_list, mc_trackless_list, mc_total_list, dsid, parameters_signal_efficiencies)
