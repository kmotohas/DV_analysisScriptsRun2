#!/usr/bin/env python

import BasicConfig
import sys
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

    canvas.SaveAs(BasicConfig.plotdir + plot_name + '_' + str(date.today()) + '.pdf')

if __name__ == '__main__':
    AtlasStyle.SetAtlasStyle()
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