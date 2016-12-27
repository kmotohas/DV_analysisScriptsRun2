#!/usr/bin/env python

import BasicConfig
import sys
import os

import ROOT
import AtlasStyle
#except ImportError:
#    # on my laptop
#    sys.path.append('/usr/local/root/latest/lib')
#    sys.path.append(BasicConfig.workdir + 'Macro/')
#    import ROOT
#    import AtlasStyle

import MaterialVolume
from datetime import date
from array import array
import utils
#import AtlasLabels

mat = MaterialVolume.MaterialVolume()
bins = array('f', [0] + mat.region_list)
h_factor = ROOT.TH1F('h_factor', ';R [mm]; Crossing Factor', len(mat.region_list), bins)
h_factor_large = ROOT.TH1F('h_factor_large', ';R [mm]; Crossing Factor', len(mat.region_list), bins)

import array

rebins = [round(x * 0.1, 1) for x in range(0, 40, 2)]
for x in range(40, 81, 4):
    rebins.append(round(x * 0.1, 1))
rebins.append(9.)
rebins.append(10.)
rebins.append(12.)
rebins.append(15.)
rebins.append(20.)
rebins.append(30.)
rebins.append(40.)
rebins.append(50.)
rebins.append(70.)
rebins.append(100.)
bins_array = array.array('d', rebins)

class MassFit:
    def __init__(self, year):
        self.lumi = 3.2 if year == 2015 else '33.1'
        # label
        self.beam_condition = '#sqrt{s} = 13 TeV, L = ' + str(self.lumi) + ' fb^{-1}'
        # legend
        self.x_min = 0.5
        self.x_max = 0.85
        self.y_min = 0.60
        self.y_max = 0.80
        # normalisation region mDV > 6 GeV
        self.m_cut = 10
        # 2nd control region
        self.m_cut2 = 8
        # signal region
        self.sr = 10  # SR: mDV > 10 GeV
        # atlas label
        self.ax = 0.45
        self.ay = 0.86
        # mytext
        self.tx = 0.52
        self.ty = 0.80
        #
        self.rebin = 2
        #
        # name: BkgEst_CrossDeltaDeltaR_3Trk_Region0_DVMultiTrkBkg
        #self.model_prefix = 'BkgEst_CrossDeltaDeltaR_'
        #self.model_prefix = 'BkgEst_CrossDeltaDeltaR_NoLargeAngle_'
        #self.model_prefix = 'BkgEst_Cross_'
        #self.model_prefix = 'BkgEst_Cross_NoLargeAngle_'
        #self.nolarge_prefix = 'BkgEst_CrossDeltaPhi_NoLargeAngle_'
        #self.nolarge_prefix = 'BkgEst_CrossDeltaPhi_NoLargeAngle_'
        #self.nolarge_prefix = 'BkgEst_CrossDeltaPhiDeltaEta_'
        #self.nolarge_prefix = 'BkgEst_CrossDeltaPhi_'
        #self.nolarge_prefix = 'BkgEst_CrossDeltaPhiDeltaR_loMET_'
        #self.nolarge_prefix = 'BkgEst_CrossDeltaPhiDeltaR_'
        #self.nolarge_prefix = 'BkgEst_Cross_DeltaR_'
        #self.nolarge_prefix = 'BkgEst_CrossDeltaPhiDeltaR_th10_'
        self.nolarge_prefix = ['BkgEst_CrossDeltaPhiDeltaR_th10_',  # 0
                               'BkgEst_CrossDeltaPhiDeltaR_th10_',  # 1
                               'BkgEst_CrossDeltaPhiDeltaR_th10_',  # 2
                               'BkgEst_CrossDeltaPhiDeltaR_th10_',  # 3
                               'BkgEst_CrossDeltaPhiDeltaR_th10_',  # 4
                               'BkgEst_CrossDeltaPhiDeltaR_th10_',  # 5
                               'BkgEst_CrossDeltaPhiDeltaR_th10_',  # 6
                               'BkgEst_CrossDeltaPhiDeltaR_th10_',  # 7
                               'BkgEst_CrossDeltaPhiDeltaR_th10_',  # 8
                               'BkgEst_CrossDeltaPhiDeltaR_th10_',  # 9
                               'BkgEst_CrossDeltaPhiDeltaR_th10_',  # 10
                               'BkgEst_CrossDeltaPhiDeltaR_th10_',  # 11
                              ]
        #self.nolarge_middle_prefix = 'BkgEst_CrossDeltaPhiDeltaEta_'
        #self.nolarge_middle_prefix = 'BkgEst_CrossDeltaPhiDeltaR_loMET_'
        #self.nolarge_middle_prefix = 'BkgEst_CrossDeltaPhiDeltaR_'
        #self.nolarge_middle_prefix = 'BkgEst_CrossDeltaPhiDeltaR_'
        #self.nolarge_middle_prefix = 'BkgEst_Cross_DeltaR_'
        #self.nolarge_middle_prefix = 'BkgEst_CrossDeltaPhiDeltaR_th10_'
        #self.nolarge_outer_prefix = 'BkgEst_CrossDeltaPhiDeltaR_pt10_'
        #self.nolarge_outer_prefix = 'BkgEst_CrossDeltaPhiDeltaR_pt5_'
        #self.nolarge_outer_prefix = 'BkgEst_CrossDeltaPhiDeltaR_loMET_'
        #self.nolarge_outer_prefix = 'BkgEst_CrossDeltaPhiDeltaR_'
        #self.nolarge_outer_prefix = 'BkgEst_Cross_DeltaR_'
        #self.nolarge_outer_prefix = 'BkgEst_CrossDeltaPhiDeltaR_th10_'
        self.large_prefix = ['BkgEst_CrossDeltaPhi_',  # 0
                             'BkgEst_CrossDeltaPhi_',  # 1
                             'BkgEst_CrossDeltaPhi_',  # 2
                             'BkgEst_CrossDeltaPhi_',  # 3
                             'BkgEst_CrossDeltaPhi_',  # 4
                             'BkgEst_CrossDeltaPhi_',  # 5
                             'BkgEst_CrossDeltaPhi_',  # 6
                             'BkgEst_CrossDeltaPhi_',  # 7
                             'BkgEst_CrossDeltaPhi_',  # 8
                             'BkgEst_CrossDeltaPhi_',  # 9
                             'BkgEst_CrossDeltaPhi_',  # 10
                             'BkgEst_CrossDeltaPhi_',  # 11
                            ]
        #self.nolarge_outer_prefix = 'BkgEst_CrossDeltaPhiDeltaR_dR10_'
        #self.nolarge_prefix = 'BkgEst_CrossDeltaPhi_'
        #self.nolarge_prefix = 'BkgEst_CrossDeltaDeltaR_'
        #self.large_prefix = 'BkgEst_CrossDeltaPhi_LargeAngle_'
        #self.large_middle_prefix = 'BkgEst_CrossDeltaPhi_LargeAngle_'
        #self.large_outer_prefix = 'BkgEst_CrossDeltaPhi_LargeAngle_'
        #self.large_prefix = 'BkgEst_CrossDeltaPhi_'
        #self.large_middle_prefix = 'BkgEst_CrossDeltaPhi_'
        #self.large_outer_prefix = 'BkgEst_CrossDeltaPhi_'
        # name: BkgEst_data_3Trk_Region0_DVMultiTrkBkg
        #self.data_prefix = 'BkgEst_data_loMET_'
        self.data_prefix = 'BkgEst_data_'
        self.middle_name = 'Trk_Region'
        #self.module_name = '_DVMultiTrkBkg'
        self.module_name = ''
        self.show_collimated = False
        #self.module_name = ''
        #
        #self.non_vetoed_region = [0, 2, 4, 6, 8, 10, 11]
        self.non_vetoed_region = [x for x in range(12)]
        #self.vetoed_region = [1, 3, 5, 7, 9]
        self.vetoed_region = []
        self.crossfactor_list = []
        #self.error_list = []
        self.est_list = {}
        self.est_list_8to10 = {}
        self.est_err_list = {}
        self.est_err_list_8to10 = {}
        self.obs_list = {}
        self.obs_list_8to10 = {}
        #
        #self.h_factor = ROOT.TH1F()
        #
        #print(bins)
        mode_list = {'3', '4', '5', '6'}
        self.h_obs = {mode: ROOT.TH1F('h_obs_' + mode, ';R [mm]; Number of Vertices', len(mat.region_list), bins)
                      for mode in mode_list}
        self.h_est = {mode: ROOT.TH1F('h_est_' + mode, ';R [mm]; Number of Vertices', len(mat.region_list), bins)
                      for mode in mode_list}
        self.h_est_large = {mode: ROOT.TH1F('h_est_large_' + mode, ';R [mm]; Number of Vertices', len(mat.region_list), bins)
                            for mode in mode_list}
        self.h_obs_8to10 = {mode: ROOT.TH1F('h_obs_8to10_' + mode, ';R [mm]; Number of Vertices', len(mat.region_list), bins)
                            for mode in mode_list}
        self.h_est_8to10 = {mode: ROOT.TH1F('h_est_8to10_' + mode, ';R [mm]; Number of Vertices', len(mat.region_list), bins)
                            for mode in mode_list}
        self.h_est_large_8to10 = {mode: ROOT.TH1F('h_est_large_8to10_' + mode, ';R [mm]; Number of Vertices', len(mat.region_list), bins)
                                  for mode in mode_list}

    def print_value_and_error(self, value, label):
        print(label + ': ' + str(value) + ' +- ' + str(ROOT.TMath.Sqrt(value)))

    def configure_data_histogram(self, histo):
        #histo.SetBins(len(rebins)-1, bins_array)
        #histo.GetXaxis().SetRangeUser(0, 100)
        histo.SetMinimum(2e-3)
        histo.GetXaxis().SetRangeUser(0, 100)
        #histo.GetYaxis().SetTitle('Number of Vertices / ' + str(0.2 * self.rebin) + ' GeV')
        histo.GetYaxis().SetTitle('Number of Vertices / ' + str(0.2) + ' GeV')
        histo.GetYaxis().SetTitleSize(30)
        histo.GetYaxis().SetTitleFont(43)
        histo.GetYaxis().SetTitleOffset(1.50)
        histo.SetLineColor(ROOT.kGray + 3)
        histo.SetMarkerColor(ROOT.kGray + 3)
        histo.SetMarkerStyle(20)

    def configure_model_histogram(self, histo):
        #histo.SetBins(len(rebins)-1, bins_array)
        #histo.GetXaxis().SetRangeUser(0, 100)
        histo.GetXaxis().SetRangeUser(0, 100)
        histo.SetFillStyle(3001)
        histo.SetFillColor(ROOT.kOrange + 1)
        histo.SetLineColor(ROOT.kOrange + 1)

    def fit_3trk(self, tfile, use_multiple_models=True):
        print('*******************************')
        print('Running MassFit.fit_3trk')
        ntrk = 3
        #tfile2 = utils.open_tfile('../MassTemplates_systTree_PeriodA-I.root')
        h_nolarge = [ROOT.TH1F() for _ in mat.region_list]
        h_large = [ROOT.TH1F() for _ in mat.region_list]
        h_data = [ROOT.TH1F() for _ in mat.region_list]
        h_data_collimated = [ROOT.TH1F() for _ in mat.region_list]
        self.obs_list[ntrk] = []
        self.est_list[ntrk] = []
        self.est_err_list[ntrk] = []
        self.obs_list_8to10[ntrk] = []
        self.est_list_8to10[ntrk] = []
        self.est_err_list_8to10[ntrk] = []
        for (region, region_border) in enumerate(mat.region_list):
            tfile.GetObject(self.nolarge_prefix[region] + str(ntrk) + self.middle_name
            + str(region), h_nolarge[region])
            tfile.GetObject(self.large_prefix[region] + str(ntrk) + self.middle_name
            + str(region), h_large[region])
            #if region < 4:
            #    tfile.GetObject(self.nolarge_prefix + str(ntrk) + self.middle_name
            #    + str(region), h_nolarge[region])
            #    tfile.GetObject(self.large_prefix + str(ntrk) + self.middle_name
            #    + str(region), h_large[region])
            #elif 4 <= region <= 8:
            #    tfile.GetObject(self.nolarge_middle_prefix + str(ntrk) + self.middle_name
            #                    + str(region), h_nolarge[region])
            #    tfile.GetObject(self.large_middle_prefix + str(ntrk) + self.middle_name
            #                    + str(region), h_large[region])
            #elif region > 8:
            #    tfile.GetObject(self.nolarge_outer_prefix + str(ntrk) + self.middle_name
            #                    + str(region), h_nolarge[region])
            #    tfile.GetObject(self.large_outer_prefix + str(ntrk) + self.middle_name
            #                    + str(region), h_large[region])
            #tfile.GetObject(self.data_prefix + str(ntrk) + self.middle_name
            #                + str(region) + self.module_name, h_data[region])
            tfile.GetObject(self.data_prefix + str(ntrk) + self.middle_name
                            + str(region) + self.module_name, h_data[region])
            noCross_prefix = 'BkgEst_data_NoCross_'
            if self.show_collimated:
                tfile.GetObject(noCross_prefix + str(ntrk) + self.middle_name
                                #+ str(region) + self.module_name, h_data_collimated_original)
                + str(region) + self.module_name, h_data_collimated[region])
            #numerator = float(h_data[region].Integral(self.m_cut * 5 / self.rebin + 1, -1))
            #denominator = float(h_cross[region].Integral(self.m_cut * 5 / self.rebin + 1, -1))
            bin_vr = h_nolarge[region].FindBin(self.m_cut2)
            bin_sr = h_nolarge[region].FindBin(self.sr)
            bin_fit = h_nolarge[region].FindBin(self.m_cut)
            bin_max = h_nolarge[region].GetNbinsX()
            ## the least chi2 method
            #chisq_list = []
            #if use_multiple_models:
            #    for tmp_p1 in range(1, 300, 5):
            #        for tmp_p2 in range(1, tmp_p1*20, 8):
            #            p1 = round(tmp_p1 * 0.0001, 5)
            #            p2 = round(tmp_p2 * 0.00001, 5)
            #            sum_chisq = 0
            #            if region > 9:
            #                bin_fit = h_nolarge[region].FindBin(3)
            #            for ii in range(bin_fit, int(bin_max/2)+1):
            #                h1 = h_nolarge[region].GetBinContent(ii)
            #                h2 = h_large[region].GetBinContent(ii)
            #                d = h_data[region].GetBinContent(ii)
            #                d = 1 if d == 0 else d
            #                chisq = (p1*h1 + p2*h2 - d)**2 / d
            #                sum_chisq+=chisq
            #            chisq_list.append([round(sum_chisq, 3), p1, p2])
            #else:
            #    for tmp_p1 in range(1, 300, 1):
            #        p1 = round(tmp_p1 * 0.00001, 5)
            #        sum_chisq = 0
            #        for ii in range(bin_fit, bin_max+1):
            #            h1 = h_nolarge[region].GetBinContent(ii)
            #            d = h_data[region].GetBinContent(ii)
            #            d = 1 if d == 0 else d
            #            chisq = (p1*h1 - d)**2 / d
            #            sum_chisq+=chisq
            #        chisq_list.append([round(sum_chisq, 3), p1, 0])
            #min_chisq_index = chisq_list.index(min(chisq_list))
            ##min_chisq_p1 = int(min_chisq_index) / (200-1)
            ##print(min_chisq_index, min(chisq_lROOT.ist))
            ##print(min(chisq_list), chisq_list[min_chisq_index])
            #min_chisq_list = min(chisq_list)
            #fit_prob = ROOT.TMath.Prob(min_chisq_list[0], bin_max-bin_fit)
            #print(region, min_chisq_list, fit_prob)
            #h_factor.SetBinContent(region+1, min_chisq_list[1])
            #if region in self.vetoed_region:
            #    #h_factor.SetBinContent(region+1, 1.)
            #
            #    continue
            ##h_factor.SetBinError(region+1, min_chisq_list[1]*(1-fit_prob))
            #relative_error = h_data[region].Integral(bin_sr, -1) ** (-0.5)
            #denom = h_nolarge[region].Integral(bin_fit, bin_sr-1)
            #denom = denom if denom > 0 else 1
            #division, relative_error = utils.division_error_propagation(
            #    h_data[region].Integral(bin_fit, bin_sr-1), denom)
            #denom = h_large[region].Integral(bin_fit, bin_sr-1)
            #denom = denom if denom > 0 else 1
            #division, relative_error_large = utils.division_error_propagation(
            #    h_data[region].Integral(bin_sr, -1), denom)
            ##h_factor.SetBinError(region+1, min_chisq_list[1] * relative_error)
            #h_factor.SetBinError(region+1, relative_error)
            #h_factor_large.SetBinContent(region+1, min_chisq_list[2])
            ##h_factor_large.SetBinError(region+1, min_chisq_list[2]*(1-fit_prob))
            ##h_factor.SetBinError(region+1, min_chisq_list[2] * relative_error)
            #h_factor_large.SetBinError(region+1, relative_error_large)
            #h_nolarge[region].Sumw2()
            #h_nolarge[region].Scale(min_chisq_list[1])
            #h_large[region].Sumw2()
            #h_large[region].Scale(min_chisq_list[2])
            ## the least chi2 method end

            ## nVertices-based normalization
            if region in self.vetoed_region:
                continue
            data_sr = float(h_data[region].Integral(bin_sr, -1))
            model_sr = float(h_nolarge[region].Integral(bin_sr, -1))
            try:
                cross_factor, cross_factor_error = utils.division_error_propagation(data_sr, model_sr)
            except ZeroDivisionError:
                cross_factor, cross_factor_error = 0, 1
            print('data_sr, model_sr, cross_factor')
            print(data_sr, model_sr, cross_factor)
            h_factor.SetBinContent(region+1, cross_factor)
            h_factor.SetBinError(region+1, cross_factor_error)
            h_nolarge[region].Sumw2()
            h_nolarge[region].Scale(cross_factor)
            #h_large[region].Sumw2()
            #h_large[region].Scale(min_chisq_list[2])

        #    #
        for (region, region_border) in enumerate(mat.region_list):
            print('Region ' + str(region) + ':')
            # before scaling
            bin_sr = h_nolarge[region].FindBin(self.sr)
        #    obs_sr = float(h_data[region].Integral(self.sr * 5 / self.rebin + 1, -1))
        #    est_sr = float(h_cross[region].Integral(self.sr * 5 / self.rebin + 1, -1))
        #    obs_vr = float(h_data[region].Integral(self.m_cut2 * 5 / self.rebin + 1, self.sr * 5 / self.rebin))
        #    est_vr = float(h_cross[region].Integral(self.m_cut2 * 5 / self.rebin + 1, self.sr * 5 / self.rebin))
            obs_sr = float(h_data[region].Integral(bin_sr, -1))
            obs_vr = float(h_data[region].Integral(bin_vr, bin_sr-1))
        #    self.h_obs[str(ntrk)].SetBinContent(region+1, obs_sr)
        #    self.h_est[str(ntrk)].SetBinContent(region+1, est_sr)
            # scaling
        #    h_cross[region].Sumw2()
        #    h_cross[region].Scale(h_factor.GetBinContent(region+1))
            # adding
            #h_nolarge[region].Add(h_large[region])
            # after scaling
            est_err_sr = ROOT.Double()
            est_err_vr = ROOT.Double()
        #    est_sr = float(h_cross[region].IntegralAndError(self.sr * 5 / self.rebin + 1, -1, est_err_sr))
        #    est_vr = float(h_cross[region].IntegralAndError(self.m_cut2 * 5 / self.rebin + 1, self.sr * 5 / self.rebin, est_err_vr))
            #est_sr = float(h_nolarge[region].Integral(bin_sr, -1))
            #est_vr = float(h_nolarge[region].Integral(bin_vr, bin_sr-1))
            est_sr = float(h_nolarge[region].IntegralAndError(bin_sr, -1, est_err_sr))
            est_vr = float(h_nolarge[region].IntegralAndError(bin_vr, bin_sr-1, est_err_vr))
            #print(est_err_sr, est_err_vr)
            if region not in self.vetoed_region:
                if region in self.vetoed_region:
                    self.h_obs[str(ntrk)].SetBinContent(ii+1, 0)
                    self.h_obs[str(ntrk)].SetBinError(ii+1, 0)
                    self.h_est[str(ntrk)].SetBinContent(ii+1, 0)
                    self.h_est[str(ntrk)].SetBinError(ii+1, 0)
                    self.h_est_large[str(ntrk)].SetBinContent(ii+1, 0)
                    self.h_est_large[str(ntrk)].SetBinError(ii+1, 0)
                    # 8to10
                    self.h_obs_8to10[str(ntrk)].SetBinContent(ii+1, 0)
                    self.h_obs_8to10[str(ntrk)].SetBinError(ii+1, 0)
                    self.h_est_8to10[str(ntrk)].SetBinContent(ii+1, 0)
                    self.h_est_8to10[str(ntrk)].SetBinError(ii+1, 0)
                    self.h_est_large_8to10[str(ntrk)].SetBinContent(ii+1, 0)
                    self.h_est_large_8to10[str(ntrk)].SetBinError(ii+1, 0)
                else:
                    self.obs_list[ntrk].append(obs_sr)
                    self.obs_list_8to10[ntrk].append(obs_vr)
                    self.est_list[ntrk].append(est_sr)
                    self.est_list_8to10[ntrk].append(est_vr)
                    self.est_err_list[ntrk].append(est_err_sr)
                    self.est_err_list_8to10[ntrk].append(est_err_vr)
                    #
                    tmp_obs = float(h_data[region].Integral(bin_sr, -1))
                    tmp_est = float(h_nolarge[region].Integral(bin_sr, -1))
                    tmp_est_large = float(h_large[region].Integral(bin_sr, -1))
                    self.h_obs[str(ntrk)].SetBinContent(region+1, tmp_obs)
                    self.h_est[str(ntrk)].SetBinContent(region+1, tmp_est)
                    self.h_est_large[str(ntrk)].SetBinContent(region+1, tmp_est_large)
                    #
                    tmp_obs = float(h_data[region].Integral(bin_vr, bin_sr-1))
                    tmp_est = float(h_nolarge[region].Integral(bin_vr, bin_sr-1))
                    tmp_est_large = float(h_large[region].Integral(bin_vr, bin_sr-1))
                    self.h_obs_8to10[str(ntrk)].SetBinContent(region+1, tmp_obs)
                    self.h_est_8to10[str(ntrk)].SetBinContent(region+1, tmp_est)
                    self.h_est_large_8to10[str(ntrk)].SetBinContent(region+1, tmp_est_large)
                #self.draw_mass_distributions_and_ratio(ntrk, region, h_data[region], h_cross[region])
                self.draw_mass_distributions_and_ratio(ntrk, region, h_data[region], h_nolarge[region], h_data_collimated[region])
                #self.draw_mass_distributions_and_ratio(ntrk, region, h_data[region], h_nolarge[region])

        #rto = [15.226784809010558, 2.7543289934387376, 36.09739368998628, 3.702930752856273, 23.136884888953404,
        # 3.5915703073818004, 62.3418701522551, 3.0377784344440526, 18.22623196271174, 4.764991311794014,
        # 18.404410427304487, 12.474650962482222]
        #rto = [13.9798, 14.8443, 1.0, 8.6998, 1.0, 5.3456, 6.6107, 6.0631, 5.9471, 2.7072, 2.5752, 1.6157]
        #rto = [12.8703, 10.8239, 1.0, 10.9029, 1.0, 7.5371, 10.7423, 7.8206, 14.8677, 4.4452, 2.4864, 1.2265]
        #rto = [3.552, 9.201, 9.678, 6.551, 3.53, 5.391, 6.308, 4.305, 6.79, 3.121, 2.189, 3.419]
        #rto = [3.04, 12.888, 28.43, 10.736, 2.956, 8.169, 11.801, 5.618, 8.911, 3.613, 2.616, 3.935]
        #rto = [2.182, 13.106, 30.807, 10.962, 5.086, 8.045, 8.581, 5.713, 7.032, 3.912, 2.854, 3.861]
        rto = [1 for _ in range(0, 12)]
        for region in range(0, 12):
            h_factor.SetBinContent(region+1, h_factor.GetBinContent(region+1)*rto[region])
            h_factor_large.SetBinContent(region+1, h_factor_large.GetBinContent(region+1)*rto[region])

        mode = {'mode': 'cross_factor', 'y_axis': 'Crossing Factor'}
        self.draw_breakdown(mode, use_multiple_models)
        ##return h_factor

    def prepare_pads(self, canvas, pad1, pad2):
        canvas.cd()
        # upper
        pad1.SetBottomMargin(0)  # Upper and lower plot are joined
        pad1.Draw()  # Draw the upper pad: pad1
        pad1.SetLogy()
        # lower
        canvas.cd()
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(0.3)
        pad2.Draw()
        pad2.SetGridy()

    def draw_mass_distributions_and_ratio(self, ntrk, region, h_data, h_model, h_coll):
    #def draw_mass_distributions_and_ratio(self, ntrk, region, h_data, h_model):
        canvas2 = ROOT.TCanvas('canvas2', 'canvas2', 1000, 750)
        # mass distributions
        pad1 = ROOT.TPad('pad1', 'pad1', 0, 0.35, 1, 1.0)
        pad2 = ROOT.TPad('pad2', 'pad2', 0, 0.05, 1, 0.35)
        self.prepare_pads(canvas2, pad1, pad2)

        pad1.cd()

        if self.rebin > 1:
            # h_nocross.Rebin(rebin)
            #h_nolarge[region].Rebin(self.rebin)
            #h_large[region].Rebin(self.rebin)
            #h_data[region].Rebin(self.rebin)
            #h_data_collimated[region].Rebin(self.rebin)
            h_model = utils.rebin(h_model, bins_array)
            h_data = utils.rebin(h_data, bins_array)
            h_coll = utils.rebin(h_coll, bins_array)
        self.configure_data_histogram(h_data)
        h_data.SetMaximum(h_data.GetMaximum() * 8)
        self.configure_model_histogram(h_model)
        for bin in range(h_data.GetNbinsX()):
            if h_data.GetBinContent(bin+1) == 0:
                h_data.SetBinError(bin+1, 1.)
        h_data.Draw('e')
        if self.show_collimated:
            self.configure_model_histogram(h_coll)
            h_coll.SetFillStyle(3013)
            h_coll.SetLineWidth(0)
            h_coll.SetFillColor(ROOT.kAzure)
            h_coll.Draw('same,hist')
        h_model.SetLineWidth(2)
        h_model.Draw('same,hist')
        h_data.Draw('same,e')
        # list_diff3[ipad-1].SetLineWidth(2)
        AtlasStyle.ATLASLabel(self.ax, self.ay, 'Work in Progress')
        AtlasStyle.myText(self.tx, self.ty, ROOT.kBlack, self.beam_condition, 0.038)
        leg = ROOT.TLegend(self.x_min, self.y_min, self.x_max, self.y_max)
        leg.AddEntry(h_data, str(ntrk) + '-trk vertices Region' + str(region), 'lep')
        leg.AddEntry(h_model, str(ntrk-1) + '-trk vert + 1 random track', 'f')
        utils.decorate_legend(leg)
        leg.Draw()

        line = ROOT.TLine(self.m_cut, h_data.GetMinimum(), self.m_cut, h_data.GetMaximum() * 0.1)
        utils.decorate_line(line, ROOT.kGray+1, 5)
        line.Draw()

        # Ratio plot
        pad2.cd()
        h_ratio = h_data.Clone(str(ntrk) + 'trk_ratio' + str(region))
        h_ratio.Sumw2()
        h_ratio.Divide(h_model)
        self.decorate_ratio_plot(h_ratio, 0.1, 1.9)
        h_ratio.Draw('e2p')
        line2 = ROOT.TLine(self.m_cut, h_ratio.GetMinimum(), self.m_cut, h_ratio.GetMaximum())
        utils.decorate_line(line2, ROOT.kGray+1, 5)
        line2.Draw()

        directory = BasicConfig.plotdir + 'bg_est/' + str(date.today())
        os.system('mkdir -p ' + directory)
        utils.save_as(canvas2, directory + '/dv_mass_fitter_' + str(ntrk) + 'Trk_Region' + str(region))
        canvas2.Close()

    def decorate_ratio_plot(self, h_ratio, y_min, y_max):
        h_ratio.SetMinimum(y_min)
        h_ratio.SetMaximum(y_max)
        h_ratio.SetFillColor(ROOT.kGray+1)
        #h_ratio.SetFillStyle(3144)
        h_ratio.SetFillStyle(3001)
        h_ratio.SetTitle('')  # // Remove the ratio title
        h_ratio.GetXaxis().SetTitle('Invariant Mass [GeV]')
        h_ratio.GetYaxis().SetTitle('Data/Model')
        h_ratio.GetYaxis().SetNdivisions(505)
        h_ratio.GetYaxis().SetTitleSize(30)
        h_ratio.GetYaxis().SetTitleFont(43)
        h_ratio.GetYaxis().SetTitleOffset(1.50)
        h_ratio.GetYaxis().SetLabelFont(43)  # Absolute font size in pixel (precision 3)
        h_ratio.GetYaxis().SetLabelSize(25)
        h_ratio.GetXaxis().SetTitleSize(30)
        h_ratio.GetXaxis().SetTitleFont(43)
        h_ratio.GetXaxis().SetTitleOffset(3.5)
        h_ratio.GetXaxis().SetLabelFont(43)  # Absolute font size in pixel (precision 3)
        h_ratio.GetXaxis().SetLabelSize(25)

    def draw_breakdown(self, mode, use_multiple_models=True):
        print('***********************')
        print('draw_breakdown')
        print(mode)
        canvas3 = ROOT.TCanvas('canvas3_' + mode['mode'], 'canvas3', 1000, 800)
        canvas3.SetLeftMargin(0.15)
        #canvas3.SetLogy()

        #mat = MaterialVolume.MaterialVolume()
        #bins = array('f', [0] + mat.region_list)
        #h_factor = mode['h_factor']
        #if mode['mode'] == 'cross_factor':
        #    self.h_factor = ROOT.TH1F('h_value_' + mode['mode'], ';R [mm];' + mode['y_axis'],
        #                              len(mat.region_list), bins)
        #h_value = ROOT.TH1F('h_value_' + mode['mode'], ';R [mm];' + mode['y_axis'],
        #                    len(mat.region_list), bins)
        #h_est = ROOT.TH1F('h_est_' + mode['mode'], '', len(mat.region_list), bins)
        h_fill = ROOT.TH1F('h_fill_' + mode['mode'], '', len(mat.region_list), bins)
        for ii in range(len(mat.region_list)):
            if ii in self.vetoed_region:
                h_fill.SetBinContent(ii + 1, 99999.)
                h_fill.SetBinError(ii + 1, 0.)
                h_factor.SetBinContent(ii+1, 0)
                h_factor.SetBinError(ii+1, 0)
                h_factor_large.SetBinContent(ii+1, 0)
                h_factor_large.SetBinError(ii+1, 0)
                if not mode['mode'] == 'cross_factor':
                    self.h_obs[mode['mode']].SetBinContent(ii+1, 0)
                    self.h_obs[mode['mode']].SetBinError(ii+1, 0)
                    self.h_est[mode['mode']].SetBinContent(ii+1, 0)
                    self.h_est[mode['mode']].SetBinError(ii+1, 0)
                    self.h_est_large[mode['mode']].SetBinContent(ii+1, 0)
                    self.h_est_large[mode['mode']].SetBinError(ii+1, 0)
                    # 8to10
                    self.h_obs_8to10[mode['mode']].SetBinContent(ii+1, 0)
                    self.h_obs_8to10[mode['mode']].SetBinError(ii+1, 0)
                    self.h_est_8to10[mode['mode']].SetBinContent(ii+1, 0)
                    self.h_est_8to10[mode['mode']].SetBinError(ii+1, 0)
                    self.h_est_large_8to10[mode['mode']].SetBinContent(ii+1, 0)
                    self.h_est_large_8to10[mode['mode']].SetBinError(ii+1, 0)
            else:
                pass
                #h_fill.SetBinContent(ii + 1, -99999.)
                #h_fill.SetBinError(ii + 1, 0.)
                #if mode['mode'] == 'cross_factor':
                    #pass
                    #self.h_factor.SetBinContent(ii + 1, self.crossfactor_list[ii])
                    #self.h_factor.SetBinError(ii + 1, self.error_list[ii])
                    #self.h_factor.Sumw2()
                #elif mode['mode'] == '4':
                    ##print(ii, self.obs_list[4][ii])
                    #h_value.SetBinContent(ii + 1, self.obs_list[4][ii])
                    #h_value.SetBinError(ii + 1, ROOT.TMath.Sqrt(self.obs_list[4][ii]))
                    ##print(ii, self.est_list[4][ii])
                    #h_est.SetBinContent(ii + 1, self.est_list[4][ii])
                    #h_est.SetBinError(ii + 1, ROOT.TMath.Sqrt(self.est_list[4][ii]))
                #elif mode['mode'] == '5' or mode['mode'] == '6':
                #    h_value.SetBinContent(ii + 1, self.obs_list[5][ii])
                #    h_value.SetBinError(ii + 1, ROOT.TMath.Sqrt(self.obs_list[5][ii]))
                #else:
                #    print('invalid mode')
        h_fill.SetLineWidth(0)
        h_fill.SetFillColor(ROOT.kPink)
        h_fill.SetFillStyle(3001)
        if mode['mode'] == 'cross_factor':
            #h_factor.SetMaximum(0.0105)
            #h_factor.SetMaximum(0.0305)
            #h_factor.SetMaximum(0.905)
            #h_factor.SetMaximum(90.5)
            h_factor.SetMaximum(0.004)
            h_factor.GetYaxis().SetTitleOffset(1.80)
            h_factor.SetMinimum(0)
            #h_factor.SetMinimum(0.00002)
            #h_factor.SetMinimum(0.00002)
            h_factor.SetLineWidth(2)
            h_factor.SetLineColor(ROOT.kBlack)
            h_factor.SetMarkerColor(ROOT.kBlack)
            h_factor.SetMarkerStyle(20)
            h_factor.Draw('e')
            if use_multiple_models:
                h_factor_large.SetLineWidth(2)
                h_factor_large.SetLineColor(ROOT.kBlue+1)
                h_factor_large.SetMarkerColor(ROOT.kBlue+1)
                h_factor_large.SetMarkerStyle(20)
                h_factor_large.Draw('e,same')
            output_factor = ROOT.TFile('output_factor_{}.root'.format(self.m_cut), 'recreate')
            h_factor.Write()
            h_fill.Write()
        else:
            utils.decorate_histogram(self.h_obs[mode['mode']], ROOT.kGray+3)
            #self.h_obs[mode['mode']].SetMaximum(self.h_obs[mode['mode']].GetMaximum() * 3.1)
            #self.h_obs[mode['mode']].SetMaximum(self.h_obs[mode['mode']].GetMaximum() * 200)
            #self.h_obs[mode['mode']].SetMinimum(2e-2)
            self.h_obs[mode['mode']].SetMaximum(self.h_obs[mode['mode']].GetMaximum() * 3)
            self.h_obs[mode['mode']].SetMinimum(0)
            self.h_obs[mode['mode']].Draw('e')
            utils.decorate_histogram(self.h_est[mode['mode']], ROOT.kGreen+2, fill_style=3002)
            self.h_est[mode['mode']].Add(self.h_est_large[mode['mode']])
            self.h_est[mode['mode']].SetLineWidth(0)
            self.h_est[mode['mode']].Draw('e2,same')
            ## 8to10
            #utils.decorate_histogram(self.h_obs_8to10[mode['mode']], ROOT.kGray+3)
            #self.h_obs_8to10[mode['mode']].SetMaximum(self.h_obs_8to10[mode['mode']].GetMaximum() * 200)
            #self.h_obs_8to10[mode['mode']].Draw('e')
            #utils.decorate_histogram(self.h_est_8to10[mode['mode']], ROOT.kGreen+2, fill_style=3002)
            self.h_est_8to10[mode['mode']].Add(self.h_est_large_8to10[mode['mode']])
            #self.h_est[mode['mode']].SetLineWidth(0)
            #self.h_est[mode['mode']].Draw('e2,same')
        h_fill.Draw('same')
        AtlasStyle.ATLASLabel(self.ax, self.ay, 'Work in Progress')
        AtlasStyle.myText(self.tx, self.ty, ROOT.kBlack, self.beam_condition, 0.038)
        leg3 = ROOT.TLegend(self.x_min, self.y_min, self.x_max, self.y_max)
        if mode['mode'] == 'cross_factor':
            if use_multiple_models:
                leg3.AddEntry(h_factor, 'Crossing Factor (NoLarge)', 'lep')
                leg3.AddEntry(h_factor_large, 'Crossing Factor (Large)', 'lep')
            else:
                leg3.AddEntry(h_factor, 'Crossing Factor', 'lep')
        elif mode['mode'] == '4':
            leg3.AddEntry(self.h_obs[mode['mode']], 'Observed', 'lep')
            leg3.AddEntry(self.h_est[mode['mode']], 'Predicted', 'epf')
        elif mode['mode'] == '5' or mode['mode'] == 6:
            leg3.AddEntry(self.h_obs[mode['mode']], 'Observed (Blinded)', 'lep')
            leg3.AddEntry(self.h_est[mode['mode']], 'Predicted', 'epf')
        utils.decorate_legend(leg3)
        leg3.Draw()
        directory = BasicConfig.plotdir + 'bg_est/' + str(date.today())
        utils.save_as(canvas3, directory + '/dv_mass_fitter_summary_' + mode['mode'])
        canvas3.Close()

    def apply_crossing_factor(self, tfile,  ntrk):
        print('***************************************')
        print('apply_crossing_factor with ntrk = ' + str(ntrk))
        #mat = MaterialVolume.MaterialVolume()
        #h_cross = [ROOT.TH1F() for _ in mat.region_list]
        #tfile2 = utils.open_tfile('../output_systTree_PeriodA-I.root')
        #tfile2 = utils.open_tfile('../MassTemplates_systTree_PeriodA-I.root')
        h_nolarge = [ROOT.TH1F() for _ in mat.region_list]
        h_large = [ROOT.TH1F() for _ in mat.region_list]
        h_data = [ROOT.TH1F() for _ in mat.region_list]
        h_data_collimated = [ROOT.TH1F() for _ in mat.region_list]
        h_ratio = [ROOT.TH1F() for _ in mat.region_list]
        self.obs_list[ntrk] = []
        self.est_list[ntrk] = []
        self.obs_list_8to10[ntrk] = []
        self.est_list_8to10[ntrk] = []
        self.est_err_list[ntrk] = []
        self.est_err_list_8to10[ntrk] = []
        #bins = array('f', [0] + mat.region_list)
        #self.h_obs[str(ntrk)] = ROOT.TH1F('h_obs_' + str(ntrk), ';R [mm]; Number of Vertices', len(mat.region_list), bins)
        #self.h_est[str(ntrk)] = ROOT.TH1F('h_est_' + str(ntrk), ';R [mm]; Number of Vertices', len(mat.region_list), bins)
        #self.h_est_large[str(ntrk)] = ROOT.TH1F('h_est_large_' + str(ntrk), ';R [mm]; Number of Vertices', len(mat.region_list), bins)
        ## 8to10
        #self.h_obs_8to10[str(ntrk)] = ROOT.TH1F('h_obs_8to10_' + str(ntrk), ';R [mm]; Number of Vertices', len(mat.region_list), bins)
        #self.h_est_8to10[str(ntrk)] = ROOT.TH1F('h_est_8to10_' + str(ntrk), ';R [mm]; Number of Vertices', len(mat.region_list), bins)
        #self.h_est_large_8to10[str(ntrk)] = ROOT.TH1F('h_est_large_8to10_' + str(ntrk), ';R [mm]; Number of Vertices', len(mat.region_list), bins)
        for (region, region_border) in enumerate(mat.region_list):
            #model_prefix = 'BkgEst_Cross_' if region < 7 else 'BkgEst_Cross_NoLargeAngle_'
            #nolarge_prefix = 'BkgEst_Cross_NoLargeAngle_'
            #nolarge_prefix = 'BkgEst_CrossDeltaDeltaR_'
            #nolarge_prefix = 'BkgEst_CrossDeltaPhiDeltaR_'
            #large_prefix = 'BkgEst_Cross_LargeAngle_'
            #tfile.GetObject(model_prefix + str(ntrk) + self.middle_name
            #                + str(region) + self.module_name, h_cross[region])
            #tfile.GetObject(nolarge_prefix + str(ntrk) + self.middle_name
            #                + str(region) + self.module_name, h_nolarge[region])
            #tfile.GetObject(large_prefix + str(ntrk) + self.middle_name
            #                + str(region) + self.module_name, h_large[region])
            h_nolarge_original = ROOT.TH1F()
            h_large_original = ROOT.TH1F()
            h_data_original = ROOT.TH1F()
            h_data_collimated_original = ROOT.TH1F()
            tfile.GetObject(self.nolarge_prefix[region] + str(ntrk) + self.middle_name
                            + str(region), h_nolarge[region])
            tfile.GetObject(self.large_prefix[region] + str(ntrk) + self.middle_name
                            + str(region), h_large[region])
            #if region < 4:
            #    tfile.GetObject(self.nolarge_prefix + str(ntrk) + self.middle_name
            #                    + str(region), h_nolarge[region])
            #    tfile.GetObject(self.large_prefix + str(ntrk) + self.middle_name
            #                    + str(region), h_large[region])
            #elif 4 <= region <= 8:
            #    tfile.GetObject(self.nolarge_middle_prefix + str(ntrk) + self.middle_name
            #                    + str(region), h_nolarge[region])
            #    tfile.GetObject(self.large_prefix + str(ntrk) + self.middle_name
            #                    + str(region), h_large[region])
            #elif 8 < region:
            #    tfile.GetObject(self.nolarge_outer_prefix + str(ntrk) + self.middle_name
            #                    + str(region), h_nolarge[region])
            #    tfile.GetObject(self.large_prefix + str(ntrk) + self.middle_name
            #                    + str(region), h_large[region])
            #tfile.GetObject(self.data_prefix + str(ntrk) + self.middle_name
            #                + str(region) + self.module_name, h_data[region])
            tfile.GetObject(self.data_prefix + str(ntrk) + self.middle_name
                            #+ str(region) + self.module_name, h_data_original)
                            + str(region) + self.module_name, h_data[region])
            noCross_prefix = 'BkgEst_data_NoCross_'
            if self.show_collimated:
                tfile.GetObject(noCross_prefix + str(ntrk) + self.middle_name
                                 #+ str(region) + self.module_name, h_data_collimated_original)
                                 + str(region) + self.module_name, h_data_collimated[region])
            ##if self.rebin > 1:
            #h_nolarge[region] = ROOT.TH1F('h_nolarge_'+str(region), ';Invariant Mass [GeV]; Number of Vertices', len(rebins)-1, bins_array)
            #h_large[region] = ROOT.TH1F('h_large_'+str(region), ';Invariant Mass [GeV]; Number of Vertices', len(rebins)-1, bins_array)
            #h_data[region] = ROOT.TH1F('h_data_'+str(region), ';Invariant Mass [GeV]; Number of Vertices', len(rebins)-1, bins_array)
            #for ii in range(h_nolarge_original.GetNbinsX()+1):
            #    h_nolarge[region].Fill(h_nolarge_original.GetBinLowEdge(ii+1),
            #                           h_nolarge_original.GetBinContent(ii+1))
            #    h_large[region].Fill(h_large_original.GetBinLowEdge(ii+1),
            #                         h_large_original.GetBinContent(ii+1))
            #    h_data[region].Fill(h_data_original.GetBinLowEdge(ii+1),
            #                        h_data_original.GetBinContent(ii+1))
            ##h_nolarge[region].SetBins(len(rebins)-1, bins_array)
            ##h_large[region].SetBins(len(rebins)-1, bins_array)
            ##h_data[region].SetBins(len(rebins)-1, bins_array)
            #if self.show_collimated:
            #    for ii in range(h_nolarge_original.GetNbinsX()+1):
            #        h_data_collimated[region].Fill(h_data_collimated_original.GetBinLowEdge(ii+1),
            #                                       h_data_collimated_original.GetBinContent(ii+1))
            #    #h_data_collimated[region].SetBins(len(rebins)-1, bins_array)
                # h_nocross.Rebin(rebin)
            #h_nolarge[region].Sumw2()
            #h_nolarge[region].Scale(h_factor.GetBinContent(region+1))
            #h_large[region].Sumw2()
            #h_large[region].Scale(h_factor_large.GetBinContent(region+1))
            bin_vr = h_nolarge[region].FindBin(self.m_cut2)
            bin_sr = h_nolarge[region].FindBin(self.sr)
            bin_fit = h_nolarge[region].FindBin(self.m_cut)
            bin_max = h_nolarge[region].GetNbinsX()

            tmp_obs = float(h_data[region].Integral(bin_sr, -1))
            tmp_est = float(h_nolarge[region].Integral(bin_sr, -1))
            tmp_est_large = float(h_large[region].Integral(bin_sr, -1))
            self.h_obs[str(ntrk)].SetBinContent(region+1, tmp_obs)
            self.h_est[str(ntrk)].SetBinContent(region+1, tmp_est)
            self.h_est_large[str(ntrk)].SetBinContent(region+1, tmp_est_large)
            #
            tmp_obs = float(h_data[region].Integral(bin_vr, bin_sr-1))
            tmp_est = float(h_nolarge[region].Integral(bin_vr, bin_sr-1))
            tmp_est_large = float(h_large[region].Integral(bin_vr, bin_sr-1))
            self.h_obs_8to10[str(ntrk)].SetBinContent(region+1, tmp_obs)
            self.h_est_8to10[str(ntrk)].SetBinContent(region+1, tmp_est)
            self.h_est_large_8to10[str(ntrk)].SetBinContent(region+1, tmp_est_large)

        #if ntrk == 5:
        #    rto_4_5 = [2.182, 46.634, 109.845, 35.767, 29.256, 25.514, 48.679, 18.587, 27.23, 11.599, 13.07, 24.111]
        #    rto_3_4 = [2.182, 13.106, 30.807, 10.962, 5.086, 8.045, 8.581, 5.713, 7.032, 3.912, 2.854, 3.861]
        #    rto = [x/y for x,y in zip(rto_4_5, rto_3_4)]
        #    for region in range(0, 12):
        #        h_factor.SetBinContent(region+1, h_factor.GetBinContent(region+1)*rto[region])
        #        h_factor_large.SetBinContent(region+1, h_factor_large.GetBinContent(region+1)*rto[region])
        #canvas = ROOT.TCanvas('c', 'c', 1000, 800)
        #canvas.SetLogy()
        #h_data[0].Draw()
        #canvas.SaveAs('test1.png')
        for (region, region_border) in enumerate(mat.region_list):
            print('Region ' + str(region) + ':')
            bin_vr = h_nolarge[region].FindBin(self.m_cut2)
            bin_sr = h_nolarge[region].FindBin(self.sr)
            bin_fit = h_nolarge[region].FindBin(self.m_cut)
            bin_max = h_nolarge[region].GetNbinsX()
            # before scaling
            tmp_obs = float(h_data[region].Integral(bin_sr, -1))
            # scaling
            #h_cross[region].Sumw2()
            #h_cross[region].Scale(h_factor.GetBinContent(region+1))
            #if self.rebin > 1:
            #    #ex = 5
            #    #h_nolarge[region].Rebin(int(ex))
            #    #h_large[region].Rebin(int(ex))
            #    #h_data[region].Rebin(int(ex))
            #    #h_data_collimated[region].Rebin(int(ex))
            #    h_nolarge[region] = utils.rebin(h_nolarge[region], bins_array)
            #    h_large[region] = utils.rebin(h_large[region], bins_array)
            #    h_data[region] = utils.rebin(h_data[region], bins_array)
            #    h_data_collimated[region] = utils.rebin(h_data_collimated[region], bins_array)
            h_nolarge[region].Sumw2()
            h_nolarge[region].Scale(h_factor.GetBinContent(region+1))
            h_large[region].Sumw2()
            h_large[region].Scale(h_factor_large.GetBinContent(region+1))
            h_nolarge[region].Add(h_large[region])
            if region not in self.vetoed_region:
                # after scaling
                est_err_sr = ROOT.Double()
                #est_large_err_sr = ROOT.Double()
                tmp_est = float(h_nolarge[region].IntegralAndError(bin_sr, -1, est_err_sr))
                #tmp_est_large = float(h_nolarge[region].IntegralAndError(bin_sr, -1, est_large_err_sr))
                self.obs_list[ntrk].append(tmp_obs)
                #self.est_list[ntrk].append(tmp_est+tmp_est_large)
                self.est_list[ntrk].append(tmp_est)
                #self.est_err_list[ntrk].append(ROOT.TMath.Sqrt(est_err_sr**2+est_large_err_sr**2))
                self.est_err_list[ntrk].append(est_err_sr)
                #h_cross[region].Scale(self.crossfactor_list[region])
                #if ntrk == 4:
                self.obs_list_8to10[ntrk].append(float(h_data[region].Integral(bin_vr, bin_sr-1)))
                est_err_vr = ROOT.Double()
                #est_large_err_vr = ROOT.Double()
                #self.est_list_8to10[ntrk].append(
                #    float(h_nolarge[region].IntegralAndError(bin_vr, bin_sr-1, est_err_vr))
                #    + float(h_large[region].IntegralAndError(bin_vr, bin_sr-1, est_large_err_vr)))
                self.est_list_8to10[ntrk].append(
                    float(h_nolarge[region].IntegralAndError(bin_vr, bin_sr-1, est_err_vr)))
                #self.est_err_list_8to10[ntrk].append(ROOT.TMath.Sqrt(est_err_vr**2+est_large_err_vr**2))
                self.est_err_list_8to10[ntrk].append(est_err_vr)
                #
                #self.print_value_and_error(self.obs_list[ntrk][region], 'data  ' + str(ntrk) + '(-trk)')
                #self.print_value_and_error(self.est_list[ntrk][region], 'model ' + str(ntrk) + '(-trk)')
            #h_nolarge[region].Add(h_large[region])
            self.draw_mass_distributions_and_ratio(ntrk, region, h_data[region], h_nolarge[region], h_data_collimated[region])
            #self.draw_mass_distributions_and_ratio(ntrk, region, h_data[region], h_nolarge[region])
        self.h_obs[str(ntrk)].Sumw2()
        self.h_est[str(ntrk)].Sumw2()
        self.h_est_large[str(ntrk)].Sumw2()

        self.h_est[str(ntrk)].Multiply(h_factor)
        self.h_est_large[str(ntrk)].Multiply(h_factor_large)
        #
        self.h_obs_8to10[str(ntrk)].Sumw2()
        self.h_est_8to10[str(ntrk)].Sumw2()
        self.h_est_large_8to10[str(ntrk)].Sumw2()
        self.h_est_8to10[str(ntrk)].Multiply(h_factor)
        self.h_est_large_8to10[str(ntrk)].Multiply(h_factor_large)
        mode = {'mode': str(int(ntrk)), 'y_axis': 'Number of Vertices'}
        self.draw_breakdown(mode)


    def create_latex_summary(self):
        obs = {x: int(sum(self.obs_list[x])) for x in range(3, 7)}
        obs_8to10 = {x: int(sum(self.obs_list_8to10[x])) for x in range(3, 7)}
        est = {x: sum(self.est_list[x]) for x in range(3, 7)}
        est_8to10 = {x: sum(self.est_list_8to10[x]) for x in range(3, 7)}
        print(self.h_est.keys())
        print(self.h_est['3'].GetEntries())
        est_err = {x: ROOT.TMath.Sqrt(sum(self.h_est[str(x)].GetBinError(r+1)**2 for r in range(12))) for x in range(3, 7)}
        est_err_8to10 = {x: ROOT.TMath.Sqrt(sum(self.h_est_8to10[str(x)].GetBinError(r+1)**2 for r in range(12))) for x in range(3, 7)}
        #est_err = {3: ROOT.TMath.Sqrt(sum(err*err for err in self.est_err_list[x])) for x in range(3, 3)}
        #est_err_8to10 = {3: ROOT.TMath.Sqrt(sum(err*err for err in self.est_err_list_8to10[x])) for x in range(3, 3)}

        print('\\begin{table}')
        print('\\begin{center}')
        print('  \\caption{Total number of estimated background vertices with a mass $m_DV > '+str(int(self.sr))+'$ GeV'
              + ' in the control, validation and signal regions, from vertices crossed by random tracks,'
              + ' using the full integrated luminosity of ' + self.lumi + ' fb^{-1}.}')
        print('  \\begin{tabular}{ccc} \\hline')
        print('    \multicolumn{3}{c}{Control and Validation Regions} \\\\ \\hline')
        print('     & 3 $(2+1)$ Track DV & 4 $(3+1)$ Track DV \\\\ \\hline')
        print('    Estimation  & $ '
              + '{0:3.3f} \\pm {1:3.3f} $ & $ {2:3.3f} \\pm {3:3.3f} $ \\\\'.format(est[3], est_err[3], est[4], est_err[4]))
        print('    Observation & $ {0} $ & $ {1} $ \\\\'.format(obs[3], obs[4]))
        print('    \\hline')
        print('    \\hline')
        print('    \multicolumn{3}{c}{Additional Control and Validation Regions (' + str(int(self.m_cut2)) + '-' + str(int(self.sr))+' GeV)} \\\\ \\hline')
        print('     & 3 $(2+1)$ Track DV & 4 $(3+1)$ Track DV \\\\ \\hline')
        print('    Estimation  & $ '
              + '{0:3.3f} \\pm {1:3.3f} $ & $ {2:3.3f} \\pm {3:3.3f} $ \\\\'.format(est_8to10[3], est_err_8to10[3],
                                                                                    est_8to10[4], est_err_8to10[4]))
        print('    Observation & $ {0} $ & $ {1} $ \\\\'.format(obs_8to10[3], obs_8to10[4]))
        print('    \\hline')
        print('    \\hline')
        print('    \multicolumn{3}{c}{Additional Control and Validation Regions (' + str(int(self.m_cut2)) + '-' +str(int(self.sr))+' GeV)} \\\\ \\hline')
        print('     & 5 $(4+1)$ Track DV & 6 $(5+1)$ Track DV \\\\ \\hline')
        print('    Estimation  & $ '
              + '{0:3.3f} \\pm {1:3.3f} $ & $ {2:3.3f} \\pm {3:3.3f} $ \\\\'.format(est_8to10[5], est_err_8to10[5],
                                                                                    est_8to10[6], est_err_8to10[6]))
        print('    Observation & $ {0} $ & $ {1} $ \\\\'.format(obs_8to10[5], obs_8to10[6]))
        print('    \\hline')
        print('    \\hline')
        print('    \multicolumn{3}{c}{Signal Region} \\\\ \\hline')
        print('    & 5 $(4+1)$ Track DV & 6 $(5+1)$ Track DV\\\\ \\hline')
        print('    Estimation & $ '
              + '{0:3.3f} \\pm {1:3.3f} $ & $ {2:3.3f} \\pm {3:3.3f} $ \\\\'.format(est[5], est_err[5],
                                                                                    est[6], est_err[6]))
        print('    Observation & Blinded & Blinded \\\\')
        print('    Observation & $ {0} $ & $ {1} $ \\\\'.format(obs[5], obs[6]))
        print('    \\hline')
        print('  \\end{tabular}')
        print('\\end{center}')
        print('\\end{table}')


if __name__ == '__main__':
    AtlasStyle.SetAtlasStyle()
    #mass_fit = MassFit(2015)
    mass_fit = MassFit(2016)
    #tfile = utils.open_tfile('../all.root')
    #tfile = utils.open_tfile('../all_2016_1114.root')
    #tfile = utils.open_tfile('../MassTemplates_systTree_ALL_v21.root')
    tfile = utils.open_tfile('../MassTemplates_systTree_ALL_v30.root')
    #tfile = utils.open_tfile('../test.root')
    mass_fit.fit_3trk(tfile, use_multiple_models=False)
    #mass_fit.fit_3trk(tfile, use_multiple_models=True)
    #print(h_factor)
    mass_fit.apply_crossing_factor(tfile, 4)
    mass_fit.apply_crossing_factor(tfile, 5)
    mass_fit.apply_crossing_factor(tfile, 6)
    mass_fit.create_latex_summary()
