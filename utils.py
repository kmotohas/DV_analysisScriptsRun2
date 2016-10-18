#!/usr/bin/env python

import BasicConfig
import sys
import os
from datetime import date

try:
    import ROOT
    import AtlasStyle
except ImportError:
    # on my laptop
    sys.path.append('/usr/local/root/latest/lib')
    sys.path.append(BasicConfig.workdir + 'DV_analysisScriptsRun2/')
    import ROOT
    import AtlasStyle


def open_tfile(filepath):
    tfile = ROOT.TFile(filepath, 'open')
    if tfile.IsOpen():
        print(filepath + ' is opened successfully!')
    else:
        print(filepath + ' failed to be opened!')
        sys.exit()
    return tfile


def save_as(canvas, file_name):
    canvas.SaveAs(file_name + '.pdf')
    canvas.SaveAs(file_name + '.png')


def division_error_propagation(numerator, denominator):
    error = ROOT.TMath.Sqrt(
        ROOT.TMath.Power(1 / denominator * ROOT.TMath.Sqrt(numerator), 2)
        + ROOT.TMath.Power(numerator / denominator / denominator
                           * ROOT.TMath.Sqrt(denominator), 2))
    return numerator/denominator, error


def binomial_ratio_and_error(numerator, denominator):
    ratio = numerator / denominator
    error = ROOT.TMath.Sqrt(ratio * (1 - ratio) / denominator)
    return ratio, error


def configure_pave_text(pave_text, align=11, font=82):
    pave_text.SetTextAlign(int(align))  # 11: Left adjusted and bottom adjusted
    pave_text.SetTextFont(int(font))    # 82: courier-medium-r-normal
    pave_text.SetBorderSize(0)
    pave_text.SetFillStyle(0)


def double_gaussian_fit(histo, parameters):
    print('')
    print('*** start double_gaussian_fit on {}'.format(parameters['plot_name']))

    # Get some parameters from a dictionary of the argument
    x_min = parameters['x_min']
    x_max = parameters['x_max']
    width_high = parameters['width_high']
    width_low = parameters['width_low']
    plot_name = parameters['plot_name']

    canvas = ROOT.TCanvas("c", "c", 1000, 600)

    # Gaussian High
    gaus1 = ROOT.TF1('gaus1', 'gaus', x_min, x_max)
    gaus1.SetLineStyle(2)
    gaus1.SetLineColor(ROOT.kAzure)

    # Gaussian Low
    gaus2 = ROOT.TF1('gaus2', 'gaus', x_min, x_max)
    gaus2.SetLineStyle(2)
    gaus2.SetLineColor(ROOT.kGreen + 1)

    double_gaus = ROOT.TF1('double_gaus', 'gaus(0)+gaus(3)', x_min, x_max)
    double_gaus.SetLineColor(ROOT.kRed + 1)

    histo.Scale(1./histo.Integral())
    histo.GetYaxis().SetTitle('Arbitrary Unit')
    histo.GetXaxis().SetRangeUser(x_min * 1.2, x_max * 3)

    y_max = histo.GetBinContent(histo.GetMaximumBin())
    double_gaus.SetParameter(0, y_max)
    double_gaus.SetParLimits(0, y_max * 0.5, y_max)
    double_gaus.SetParameter(2, width_high)
    double_gaus.SetParameter(3, y_max * 0.05)
    double_gaus.SetParLimits(3, y_max * 0.01, y_max * 0.5)
    double_gaus.SetParameter(5, width_low)
    par_names = ['Height_high', 'Mean_high', 'Width_high',
                 'Height_low' , 'Mean_low' , 'Width_low']
    double_gaus.SetParNames(par_names[0], par_names[1], par_names[2],
                            par_names[3], par_names[4], par_names[5])

    # do fit
    histo.Fit(double_gaus,'R')

    # Get fit parameters to draw each component of double gaussian
    for ii in range(3):
        gaus1.SetParameter(ii, double_gaus.GetParameter(ii))
        gaus2.SetParameter(ii, double_gaus.GetParameter(ii + 3))

    histo.Draw()
    double_gaus.Draw('same')
    gaus1.Draw('same')
    gaus2.Draw('same')

    # text box for fit parameters
    pave_text = ROOT.TPaveText(0.5, 0.45, 0.80, 0.82, 'NDC')
    configure_pave_text(pave_text, align=11, font=82)
    for (ii, fit_parameter) in enumerate(par_names):
        pave_text.AddText('{0:<12}: {1:.3f}'.format(fit_parameter, double_gaus.GetParameter(ii)))
        if ii == 2:
            pave_text.AddText('')
    pave_text.Draw()

    save_as(canvas, BasicConfig.plotdir + plot_name + '_' + str(date.today()))


def create_toc_plot(passed, total, parameters):
    print('')
    print('*** start create_toc_plot')

    canvas = ROOT.TCanvas("c", "c", 1000, 600)

    if 'rebin' in parameters:
        passed.Rebin(parameters['rebin'])
        total.Rebin(parameters['rebin'])
    tg = ROOT.TGraphAsymmErrors(passed, total)
    tg.GetXaxis().SetRangeUser(0, 400)
    tg.GetYaxis().SetTitle('Efficiency')
    if 'x_title' in parameters:
        tg.GetXaxis().SetTitle(parameters['x_title'])
    tg.Draw('AP')

    AtlasStyle.ATLASLabel(0.50, 0.4, 'Work in Progress')
    AtlasStyle.myText(0.55, 0.32, ROOT.kBlack, parameters['label'], 0.038)
    if 'label2' in parameters:
        AtlasStyle.myText(0.55, 0.24, ROOT.kBlack, parameters['label2'], 0.038)

    save_as(canvas, BasicConfig.plotdir + parameters['plot_name'] + '_' + str(date.today()))


def overlay_histograms(histograms, legends, parameters):
    print('')
    print('*** start overlay_histograms')

    canvas = ROOT.TCanvas("c", "c", 1000, 600)
    y_max = histograms[0].GetMaximum() * 2
    y_min = 0.8
    leg = ROOT.TLegend(0.6, 0.78, 0.88, 0.90)
    for ii, (histogram, legend) in enumerate(zip(histograms, legends)):
        print(ii)
        decorate_histogram(histogram, BasicConfig.colors[ii])
        if ii == 0:
            histograms[0].SetMinimum(y_min)
            histogram.Draw()
        else:
            if histogram.GetMaximum() > y_max:
                y_max = histogram.GetMaximum()
                histograms[0].SetMaximum(y_max * 15)
                histogram.Draw('same')
            histogram.Draw('same')
        leg.AddEntry(histogram, legend, 'l')
    canvas.Update()
    canvas.SetLogy()
    decorate_legend(leg)
    leg.Draw()

    AtlasStyle.ATLASLabel(0.20, 0.85, 'Work in Progress')
    AtlasStyle.myText(0.22, 0.80, ROOT.kBlack, parameters['label'], 0.038)
    if 'label2' in parameters:
        AtlasStyle.myText(0.25, 0.76, ROOT.kBlack, parameters['label2'], 0.038)

    save_as(canvas, BasicConfig.plotdir + parameters['plot_name'] + '_' + str(date.today()))


def decorate_histogram(histogram, color, marker_style=20, line_style=1, fill_style=0):
    histogram.SetLineColor(color)
    histogram.SetMarkerColor(color)
    histogram.SetFillColor(color)
    histogram.SetMarkerStyle(marker_style)
    histogram.SetLineStyle(line_style)
    histogram.SetFillStyle(fill_style)


def decorate_legend(legend):
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)


def decorate_line(line, color, style):
    line.SetLineStyle(color)
    line.SetLineStyle(style)


def decorate_ratio_plot(h_ratio, y_min, y_max):
    h_ratio.SetMinimum(y_min)
    h_ratio.SetMaximum(y_max)
    h_ratio.SetFillColor(ROOT.kGray)
    h_ratio.SetFillStyle(3144)
    h_ratio.SetTitle('')  # // Remove the ratio title
    h_ratio.GetYaxis().SetTitle('Ratio')
    h_ratio.GetYaxis().SetNdivisions(505)
    h_ratio.GetYaxis().SetTitleSize(30)
    h_ratio.GetYaxis().SetTitleFont(43)
    h_ratio.GetYaxis().SetTitleOffset(1.50)
    h_ratio.GetYaxis().SetLabelFont(43)  # Absolute font size in pixel (precision 3)
    h_ratio.GetYaxis().SetLabelSize(35)
    h_ratio.GetXaxis().SetTitleSize(35)
    h_ratio.GetXaxis().SetTitleFont(43)
    h_ratio.GetXaxis().SetTitleOffset(4.5)
    h_ratio.GetXaxis().SetLabelFont(43)  # Absolute font size in pixel (precision 3)
    h_ratio.GetXaxis().SetLabelSize(35)


def prepare_pads(canvas, pad1, pad2):
    canvas.cd()
    # upper
    pad1.SetBottomMargin(0)  # Upper and lower plot are joined
    pad1.Draw()  # Draw the upper pad: pad1
    pad1.SetLogy()
    # lower
    canvas.cd()
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.25)
    pad2.Draw()
    pad2.SetGridy()


def draw_distributions_and_ratio(h_data, h_model, parameters):
    canvas2 = ROOT.TCanvas('canvas2', 'canvas2', 1000, 750)
    # mass distributions
    pad1 = ROOT.TPad('pad1', 'pad1', 0, 0.3, 1, 1.0)
    pad2 = ROOT.TPad('pad2', 'pad2', 0, 0.05, 1, 0.3)
    prepare_pads(canvas2, pad1, pad2)

    pad1.cd()
    decorate_histogram(h_data, ROOT.kGray+3)
    h_data.Sumw2()
    h_data.Scale(1./h_data.GetEntries())
    h_data.SetMaximum(h_data.GetMaximum() * 10)
    h_data.Draw('e')
    #h_model.SetLineWidth(2)
    decorate_histogram(h_model, ROOT.kRed+1)
    h_model.Sumw2()
    h_model.Scale(1./h_model.GetEntries())
    h_model.Draw('same,e')
    # list_diff3[ipad-1].SetLineWidth(2)
    AtlasStyle.ATLASLabel(0.2, 0.85, 'Work in Progress')
    #AtlasStyle.myText(0, self.ty, ROOT.kBlack, self.beam_condition, 0.038)
    leg = ROOT.TLegend(0.55, 0.6, 0.85, 0.85)
    leg.AddEntry(h_data, parameters['legend1'], 'lep')
    leg.AddEntry(h_model, parameters['legend2'], 'lep')
    decorate_legend(leg)
    leg.Draw()

    #line = ROOT.TLine(self.m_cut, h_data.GetMinimum(), self.m_cut, h_data.GetMaximum() * 0.1)
    #decorate_line(line, ROOT.kGray + 1, 5)
    #line.Draw()

    # Ratio plot
    pad2.cd()
    h_ratio = h_data.Clone('ratio')
    h_ratio.Sumw2()
    h_ratio.Divide(h_model)
    decorate_ratio_plot(h_ratio, 0.1, 1.9)
    h_ratio.Draw('e2p')
    #line2 = ROOT.TLine(self.m_cut, h_ratio.GetMinimum(), self.m_cut, h_ratio.GetMaximum())
    #decorate_line(line2, ROOT.kGray + 1, 5)
    #line2.Draw()

    directory = BasicConfig.plotdir + 'validation/' + str(date.today())
    os.system('mkdir -p ' + directory)
    save_as(canvas2, directory + '/' + parameters['file_name'])
    canvas2.Close()


def compare_two_ntuples(tree0, tree1, branch, nbin, xmin, xmax, cut, legend1, legend2, hname=''):
    c = ROOT.TCanvas('c', 'c', 1000, 800)
    if hname == '':
        hname = 'h_' + branch
    tree0.Draw("{0}>>h_{4}0({1},{2},{3})".format(branch, nbin, xmin, xmax, hname), cut)
    hist = [ROOT.TH1F(), ROOT.TH1F()]
    hist[0] = c.GetPrimitive('h_'+hname+'0').Clone('hist0')
    hist[0].SetLineColor(ROOT.kGray+3)
    tree1.Draw("{0}>>h_{4}1({1},{2},{3})".format(branch, nbin, xmin, xmax, hname), cut)
    hist[1] = c.GetPrimitive('h_'+hname+'1').Clone('hist1')
    hist[1].SetLineColor(ROOT.kPink-1)
    parameters = {'file_name': hname, 'legend1': legend1, 'legend2': legend2}

    hist[0].Sumw2()
    hist[1].Sumw2()

    draw_distributions_and_ratio(hist[0], hist[1], parameters)


if __name__ == '__main__':
    AtlasStyle.SetAtlasStyle()

    do_resolution = False
    if do_resolution:
        filename = 'histograms_1200_1150.root'
        tf = open_tfile(BasicConfig.rootcoredir + filename)
        # R
        histo_R = ROOT.TH1D()
        tf.GetObject('diffVertPosR_DVPlusMETEff', histo_R)
        parameters_R = {'x_min': -1.5, 'x_max': 1.5, 'width_high': 0.1, 'width_low': 0.3,
                        'plot_name': 'diffVertPosR'}
        double_gaussian_fit(histo_R, parameters_R)
        # Phi
        histo_Phi = ROOT.TH1D()
        tf.GetObject('diffVertPosPhi_DVPlusMETEff', histo_Phi)
        parameters_Phi = {'x_min': -1.5, 'x_max': 1.5, 'width_high': 0.1, 'width_low': 0.3,
                          'plot_name': 'diffVertPos_Phi'}
        double_gaussian_fit(histo_Phi, parameters_Phi)
        # Z
        histo_Z = ROOT.TH1D()
        tf.GetObject('diffVertPosZ_DVPlusMETEff', histo_Z)
        parameters_Z = {'x_min': -1.5, 'x_max': 1.5, 'width_high': 0.1, 'width_low': 0.5,
                        'plot_name': 'diffVertPos_Z'}
        double_gaussian_fit(histo_Z, parameters_Z)

    do_toc = False
    if do_toc:
        # turn-on curve
        sys_filename_2015 = 'all_2015_PeriodD.root'
        sys_filename_2016 = 'all_2016_PeriodC.root'
        passed_2015 = ROOT.TH1F()
        passed_2016 = ROOT.TH1F()
        total_2015 = ROOT.TH1F()
        total_2016 = ROOT.TH1F()
        tf_sys_2015 = open_tfile(BasicConfig.workdir + sys_filename_2015)
        tf_sys_2016 = open_tfile(BasicConfig.workdir + sys_filename_2016)
        tf_sys_2015.GetObject('calibMET_xe_SysUnc_MET', passed_2015)
        tf_sys_2015.GetObject('calibMET_SysUnc_MET', total_2015)
        tf_sys_2016.GetObject('calibMET_xe_SysUnc_MET', passed_2016)
        tf_sys_2016.GetObject('calibMET_SysUnc_MET', total_2016)
        parameters_2015 = {'plot_name': 'HLT_xe100_tc_lcw_wEFMu_TOC_2015', 'x_title': 'Missing E_{T} [GeV]',
                           'label': 'data15_13TeV PeriodD DAOD_JETM2',
                           'label2': 'HLT_xe100_tc_lcw_wEFMu', 'rebin': 2}
        parameters_2016 = {'plot_name': 'HLT_xe100_mht_L1XE50_TOC_2016', 'x_title': 'Missing E_{T} [GeV]',
                           'label': 'data16_13TeV PeriodC DAOD_JETM2',
                           'label2': 'HLT_xe100_mht_L1XE50', 'rebin': 2}
        create_toc_plot(passed_2015, total_2015, parameters_2015)
        create_toc_plot(passed_2016, total_2016, parameters_2016)

    do_met_phi = False
    if do_met_phi:
        tfile = open_tfile('/Users/kmotohas/afs-work/DisplacedVertex/DV_xAODAnalysis/histograms_00304494_01_40.root')
        key_list = ['MET_phi_met_lht_DVPlusMET',
                    'MET_phi_trackless_DVPlusMET', 'MET_phi_NOtrackless_DVPlusMET',
                    'MET_phi_calibMET_DVPlusMET']
        h = [ROOT.TH1F() for _ in key_list]
        for ii, key in enumerate(key_list):
            tfile.GetObject(key, h[ii])
        legends = ['MET_LHT > 180 GeV', '1/2 Trackless Jets',
                   'No Trackless Jet', 'Offline MET > 250 GeV']
        parameters = {'plot_name': 'MET_phi', 'label': 'data16_13TeV run 304494 AOD'}
        overlay_histograms(h, legends, parameters)

    tfile_group = open_tfile('/Users/kmotohas/ATLAS/sw/projects/DV_xAODAnalysis/histograms_302137_VrtSecInclusive_BasicPlots.root')
    #tfile_central = open_tfile('/Users/kmotohas/ATLAS/sw/projects/DV_xAODAnalysis/histograms_307732_VrtSecInclusive_BasicPlots.root')
    tfile_central = open_tfile('/Users/kmotohas/ATLAS/sw/projects/DV_xAODAnalysis/histograms_302137_VrtSecInclusive_BasicPlots_v2.root')
    key_list = ['trkD0_all_BasicPlots', 'trkZ0_all_BasicPlots',
                'trkD0_LargeD0_BasicPlots', 'trkZ0_LargeD0_BasicPlots',
                'DVr_BasicPlots', 'DVmass_BasicPlots']
    h_group = [ROOT.TH1F() for _ in key_list]
    h_central = [ROOT.TH1F() for _ in key_list]
    for ii, key in enumerate(key_list):
        tfile_group.GetObject(key, h_group[ii])
        h_group[ii].SetName(key+'group')
        tfile_central.GetObject(key, h_central[ii])
        h_central[ii].SetName(key+'central')
    legend1 = 'run302137 (group-susy)'
    legend2 = 'run302137 (central)'
    #'run307732 (central)'
    for ii, key in enumerate(key_list):
        parameters = {'file_name': key, 'legend1': legend1, 'legend2': legend2}
        draw_distributions_and_ratio(h_group[ii], h_central[ii], parameters)
    #parameters = {'file_name': key_list[1], 'legend1': legend1, 'legend2': legend2}
    #draw_distributions_and_ratio(h_group[1], h_central[1], parameters)
    #parameters = {'file_name': key_list[2], 'legend1': legend1, 'legend2': legend2}
    #draw_distributions_and_ratio(h_group[2], h_central[2], parameters)
    #parameters = {'file_name': key_list[3], 'legend1': legend1, 'legend2': legend2}
    #draw_distributions_and_ratio(h_group[3], h_central[3], parameters)

