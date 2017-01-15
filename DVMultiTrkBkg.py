#!/bin/env python

from ROOT import *

import argparse
import utils

#m_angleCut = 0.5
m_massPion = 139.57*0.001
m_MET_min = 250

m_dvTrks = []
m_tlvDV = TLorentzVector()
m_posDV = TVector3()
m_posPV = TVector3()
m_Region = 0
m_DVnTrk = 0
m_DVPV = TLorentzVector()

m_nEvents = TH1F()
m_nEvents_MET = TH1F()
m_BkgEst_data_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(8)]
m_BkgEst_data_loMET_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_data_hiMET_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_data_NoCross_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_data_NoCross_maxAngle_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_data_NoCross_maxDeltaR_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_data_NoCross_maxDeltaEta_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_Cross_NoLargeAngle_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_Cross_LargeAngle_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_Cross_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_Cross_Angle_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_Cross_DeltaR_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_NoLargeAngle_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_LargeAngle_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDelta_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDelta_DeltaR_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDelta_Angle_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_DeltaEta_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_Angle_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_DeltaR_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_DeltaR_loMET_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_DeltaR_hiMET_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_DeltaR_th08_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_DeltaR_th10_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_DeltaR_th15_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_DeltaR_pt20_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_DeltaR_pt15_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_DeltaR_pt10_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_DeltaR_pt5_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_DeltaR_dR10_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_DeltaR_dR15_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_DeltaR_dR20_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_DeltaR_dR25_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
#m_AvgAngleDVmass_iTrk = [TH2F() for itrk in range(7)]
m_AvgAngleDVmass_iTrk_Region = [[TH2F() for region in range(12)] for itrk in range(7)]
#m_maxAngleDVmass_iTrk = [TH2F() for itrk in range(7)]
m_maxAngleDVmass_iTrk_Region = [[TH2F() for region in range(12)] for itrk in range(7)]
#m_dRDVmass_iTrk = [TH2F() for itrk in range(7)]
m_dRDVmass_iTrk_Region = [[TH2F() for region in range(12)] for itrk in range(7)]
m_dEtaDVmass_iTrk_Region = [[TH2F() for region in range(12)] for itrk in range(7)]
flavors = ['Cross', 'DeltaPhi', 'Delta']
props = ['EtaPhi', 'EtaDeltaPhi', 'DeltaEtaDeltaPhi']
m_TrkProp_Pt_iTrk_Region = [[[TH1F() for region in range(12)] for itrk in range(7)] for flavor in flavors]
m_TrkProp_Angle_iTrk_Region = [[[TH2F() for region in range(12)] for itrk in range(7)] for prop in props]

#irandom = int(gRandom.Uniform()*nTrkTemplates)
irandom = 0

def book_histograms():
    global m_nEvents
    global m_nEvents_MET
    global m_BkgEst_data_iTrk_Region
    global m_BkgEst_data_loMET_iTrk_Region
    global m_BkgEst_data_hiMET_iTrk_Region
    global m_BkgEst_data_NoCross_iTrk_Region
    global m_BkgEst_data_NoCross_maxAngle_iTrk_Region
    global m_BkgEst_data_NoCross_maxDeltaR_iTrk_Region
    global m_BkgEst_data_NoCross_maxDeltaEta_iTrk_Region
    global m_BkgEst_Cross_iTrk_Region
    global m_BkgEst_Cross_Angle_iTrk_Region
    global m_BkgEst_Cross_DeltaR_iTrk_Region
    global m_BkgEst_Cross_NoLargeAngle_iTrk_Region
    global m_BkgEst_Cross_LargeAngle_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_NoLargeAngle_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_LargeAngle_iTrk_Region
    global m_BkgEst_CrossDelta_iTrk_Region
    global m_BkgEst_CrossDelta_DeltaR_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_DeltaR_pt20_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_DeltaR_pt15_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_DeltaR_pt10_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_DeltaR_pt5_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_DeltaR_dR10_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_DeltaR_dR15_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_DeltaR_dR20_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_DeltaR_dR25_iTrk_Region
    global m_BkgEst_CrossDelta_Angle_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_DeltaR_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_DeltaR_loMET_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_DeltaR_hiMET_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_DeltaR_th08_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_DeltaR_th10_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_DeltaR_th15_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_DeltaEta_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_Angle_iTrk_Region
    global m_TrkProp_Pt_iTrk_Region
    global m_TrkProp_Angle_iTrk_Region
    #global m_AvgAngleDVmass_iTrk
    global m_AvgAngleDVmass_iTrk_Region
    #global m_maxAngleDVmass_iTrk
    global m_maxAngleDVmass_iTrk_Region
    #global m_dRDVmass_iTrk
    global m_dRDVmass_iTrk_Region
    global m_dEtaDVmass_iTrk_Region



    m_nEvents = TH1F('nEvents', ';;Number of Events', 1, 0, 1)
    m_nEvents_MET = TH1F('nEvents_MET', ';;Number of Events', 1, 0, 1)
    nbins = 500
    #x_min = 0
    x_max = 100
    for itrk in range(2, 7):
        for region in range(12):
            labels = ';Invariant Mass [GeV]; Number of Vertices'
            m_BkgEst_data_iTrk_Region[itrk][region] = TH1F('BkgEst_data_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            if itrk == 6:
                m_BkgEst_data_iTrk_Region[7][region] = TH1F('BkgEst_data_7Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_data_loMET_iTrk_Region[itrk][region] = TH1F('BkgEst_data_loMET_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_data_hiMET_iTrk_Region[itrk][region] = TH1F('BkgEst_data_hiMET_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_data_NoCross_iTrk_Region[itrk][region] = TH1F('BkgEst_data_NoCross_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_data_NoCross_maxAngle_iTrk_Region[itrk][region] = TH1F('BkgEst_data_NoCross_maxAngle_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_data_NoCross_maxDeltaR_iTrk_Region[itrk][region] = TH1F('BkgEst_data_NoCross_maxDeltaR_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_data_NoCross_maxDeltaEta_iTrk_Region[itrk][region] = TH1F('BkgEst_data_NoCross_maxDeltaEta_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_Cross_iTrk_Region[itrk][region] = TH1F('BkgEst_Cross_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_Cross_Angle_iTrk_Region[itrk][region] = TH1F('BkgEst_Cross_Angle_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_Cross_DeltaR_iTrk_Region[itrk][region] = TH1F('BkgEst_Cross_DeltaR_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_Cross_NoLargeAngle_iTrk_Region[itrk][region] = TH1F('BkgEst_Cross_NoLargeAngle_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_Cross_LargeAngle_iTrk_Region[itrk][region] = TH1F('BkgEst_Cross_LargeAngle_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_NoLargeAngle_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhi_NoLargeAngle_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_LargeAngle_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhi_LargeAngle_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDelta_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDelta_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDelta_DeltaR_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaDeltaR_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDelta_Angle_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaAngle_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhi_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_DeltaR_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiDeltaR_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_DeltaR_loMET_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiDeltaR_loMET_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_DeltaR_hiMET_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiDeltaR_hiMET_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_DeltaR_th08_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiDeltaR_th08_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_DeltaR_th10_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiDeltaR_th10_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_DeltaR_th15_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiDeltaR_th15_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_DeltaR_pt20_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiDeltaR_pt20_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_DeltaR_pt15_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiDeltaR_pt15_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_DeltaR_pt10_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiDeltaR_pt10_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_DeltaR_pt5_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiDeltaR_pt5_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_DeltaR_dR10_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiDeltaR_dR10_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_DeltaR_dR15_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiDeltaR_dR15_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_DeltaR_dR20_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiDeltaR_dR20_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_DeltaR_dR25_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiDeltaR_dR25_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_DeltaEta_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiDeltaEta_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            m_BkgEst_CrossDeltaPhi_Angle_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiAngle_{0}Trk_Region{1}'.format(itrk, region), labels, nbins, 0, x_max)
            labels = ';Average Angle [rad]; Invariant Mass [GeV]'
            m_AvgAngleDVmass_iTrk_Region[itrk][region] = TH2F('AvgAngleDVmass_{0}Trk_Region{1}'.format(itrk, region), labels, 150, 0, 3.141592, nbins, 0, x_max)
            labels = ';Max Angle [rad]; Invariant Mass [GeV]'
            m_maxAngleDVmass_iTrk_Region[itrk][region] = TH2F('maxAngleDVmass_{0}Trk_Region{1}'.format(itrk, region), labels, 150, 0, 3.141592, nbins, 0, x_max)
            labels = ';#Delta R; Invariant Mass [GeV]'
            m_dRDVmass_iTrk_Region[itrk][region] = TH2F('dRDVmass_{0}Trk_Region{1}'.format(itrk, region), labels, 150, 0, 10, nbins, 0, x_max)
            labels = ';#Delta#eta; Invariant Mass [GeV]'
            m_dEtaDVmass_iTrk_Region[itrk][region] = TH2F('dEtaDVmass_{0}Trk_Region{1}'.format(itrk, region), labels, 150, 0, 5, nbins, 0, x_max)
    #for ii,flavor in enumerate(flavors):
    for jj,(prop,flavor) in enumerate(zip(props, flavors)):
        for itrk in range(2, 7):
            for region in range(12):
                #if jj == 0:
                m_TrkProp_Pt_iTrk_Region[jj][itrk][region] = TH1F('TrkProp_{2}_model_Pt_{0}Trk_Region{1}'.format(itrk, region, flavor), ';Track P_{T} [GeV]', 100, 0, 20)
                #m_TrkProp_Pt_iTrk_Region[jj][itrk][region] = TH1F('TrkProp_model_Pt_{0}Trk_Region{1}'.format(itrk, region, flavor), ';Track P_{T} [GeV]', 100, 0, 20)
                angle_label = ';#eta;#phi'
                if prop == 'EtaDeltaPhi':
                    angle_label = ';#eta;#Delta#phi'
                if prop == 'DeltaEtaDeltaPhi':
                    angle_label = ';#Delta#eta;#Delta#phi'
                m_TrkProp_Angle_iTrk_Region[jj][itrk][region] = TH2F('TrkProp_{2}_model_{3}_{0}Trk_Region{1}'.format(itrk, region, flavor, prop),
                                                                             angle_label, 150, -3.14, 3.14, 150, -3.14, 3.14)


def get_index_of_leading_jet(tree):
    idx_leading = -1
    pt_leading = -1000
    for idx, jet_pt in enumerate(tree.Jet_pT):
        if jet_pt > pt_leading:
            pt_leading = jet_pt
            idx_leading = idx
    return idx_leading


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
#
#
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


def dvInfo(tree, idv):
    global m_dvTrks
    global m_tlvDV
    global m_posDV
    global m_Region
    global m_DVnTrk

    m_dvTrks = []
    #m_tlvDV.SetPtEtaPhiM(0, 0, 0, 0)
    m_tlvDV = TLorentzVector()
    for itrk in range(tree.DV_nTracks[idv]):
        tmp_tlvTrk = TLorentzVector()
        #print(idv, itrk, tree.DV_track_eta_wrtSV[idv][itrk])
        tmp_tlvTrk.SetPtEtaPhiM(tree.DV_track_pt_wrtSV[idv][itrk],
                                tree.DV_track_eta_wrtSV[idv][itrk],
                                tree.DV_track_phi_wrtSV[idv][itrk], m_massPion)
        m_tlvDV += tmp_tlvTrk
        m_dvTrks.append(tmp_tlvTrk)
    #print(m_dvTrks[0].Eta(), m_dvTrks[1].Eta())
    #print('test = {}'.format(m_tlvDV.M()))
    m_posDV.SetXYZ(tree.DV_x[idv], tree.DV_y[idv], tree.DV_z[idv])
    m_Region = tree.DV_Region[idv]
    m_DVnTrk = tree.DV_nTracks[idv]
    #print(m_Region)
    #print('orig_dvTrks_len'+str(len(m_dvTrks)))


def getMaxTrkAngle():
    maxTotalAngleToOtherTracks = 0.
    maxAngleToDVPV = 0.
    maxDeltaRToDVPV = 0.
    maxDeltaEtaToDVPV = 0.
    #print('next_dvTrks_len'+str(len(m_dvTrks)))
    for ii, trk1 in enumerate(m_dvTrks):
        totalAngleToOtherTracks = 0.
        tmp_angleToDVPV = trk1.Angle(m_DVPV.Vect())
        maxAngleToDVPV = tmp_angleToDVPV if tmp_angleToDVPV > maxAngleToDVPV else maxAngleToDVPV
        tmp_DeltaRToDVPV = trk1.DeltaR(m_DVPV)
        maxDeltaRToDVPV = tmp_DeltaRToDVPV if tmp_DeltaRToDVPV > maxDeltaRToDVPV else maxDeltaRToDVPV
        tmp_DeltaEtaToDVPV = TMath.Abs(trk1.Eta() - m_DVPV.Eta())
        maxDeltaEtaToDVPV = tmp_DeltaEtaToDVPV if tmp_DeltaEtaToDVPV > maxDeltaEtaToDVPV else maxDeltaEtaToDVPV
        #print('trk1.Eta() '+str(trk1.Eta()))
        #print(ii)
        for jj in range(len(m_dvTrks)):
            if (ii == jj):
                continue
            #print(jj)
            #print('trk2.Eta() '+str(m_dvTrks[jj].Eta()))
            totalAngleToOtherTracks += trk1.Angle(m_dvTrks[jj].Vect())
            #print(totalAngleToOtherTracks)
        if (totalAngleToOtherTracks > maxTotalAngleToOtherTracks):
            maxTotalAngleToOtherTracks = totalAngleToOtherTracks
    #print('angle: '+str(maxTotalAngleToOtherTracks/(m_DVnTrk-1.)))
    return maxTotalAngleToOtherTracks/(m_DVnTrk-1.), maxAngleToDVPV, maxDeltaRToDVPV, maxDeltaEtaToDVPV


def dvBkgEst(trkTemplate, nTrkTemplates, MET):
    global irandom

    m_angleCut = 1.0
    # data
    DVnTrk = m_DVnTrk
    if m_DVnTrk < 7:
        m_BkgEst_data_iTrk_Region[m_DVnTrk][m_Region].Fill(m_tlvDV.M())
    else:
        m_BkgEst_data_iTrk_Region[7][m_Region].Fill(m_tlvDV.M())
    if m_DVnTrk > 6:
        return
    if MET < m_MET_min:
        m_BkgEst_data_loMET_iTrk_Region[DVnTrk][m_Region].Fill(m_tlvDV.M())
    else:
        m_BkgEst_data_hiMET_iTrk_Region[DVnTrk][m_Region].Fill(m_tlvDV.M())
    max_average_opening_angle, max_angle_DVPV, max_deltaR_DVPV, max_deltaEta_DVPV = getMaxTrkAngle()
    if (max_average_opening_angle < m_angleCut):
        m_BkgEst_data_NoCross_iTrk_Region[DVnTrk][m_Region].Fill(m_tlvDV.M())
    if (max_angle_DVPV < m_angleCut):
        m_BkgEst_data_NoCross_maxAngle_iTrk_Region[DVnTrk][m_Region].Fill(m_tlvDV.M())
    if (max_deltaR_DVPV < m_angleCut):
        m_BkgEst_data_NoCross_maxDeltaR_iTrk_Region[DVnTrk][m_Region].Fill(m_tlvDV.M())
    if (max_deltaEta_DVPV < m_angleCut):
        m_BkgEst_data_NoCross_maxDeltaEta_iTrk_Region[DVnTrk][m_Region].Fill(m_tlvDV.M())
    m_AvgAngleDVmass_iTrk_Region[DVnTrk][m_Region].Fill(max_average_opening_angle, m_tlvDV.M())
    m_maxAngleDVmass_iTrk_Region[DVnTrk][m_Region].Fill(max_angle_DVPV, m_tlvDV.M())
    m_dRDVmass_iTrk_Region[DVnTrk][m_Region].Fill(max_deltaR_DVPV, m_tlvDV.M())
    m_dEtaDVmass_iTrk_Region[DVnTrk][m_Region].Fill(max_deltaEta_DVPV, m_tlvDV.M())

    #if m_DVnTrk >= 6 or m_Region in [1, 3, 5, 7, 9]:
    if m_DVnTrk >= 6 or m_Region < 0:
        return

    # flag to divide templates into collimated and large angle
    construct_multiple_templates = False

    construct_templates_with_angle_cut = True
    use_pt_upper_limit = False
    use_dR_upper_limit = False
    change_dR_lower_threshold = True

    #nLoops = m_DVnTrk-1 + (m_DVnTrk-2) * 2
    nLoops = m_DVnTrk-1
    #nLoops = 1
    for _ in range(nLoops):
        #---------------------
        # DELTA template
        #--------------------
        # nominal template (delta track, delta R > 0.5)
        isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=True, useDeltaPhi=True, fillTrkProp=True, cut='dR')
        if isSampled:
            m_BkgEst_CrossDelta_DeltaR_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
        # delta template (no cut)
        isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=True, useDeltaPhi=True, cut='none')
        if isSampled:
            m_BkgEst_CrossDelta_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
        #---------------------
        # DELTA PHI template
        #--------------------
        # using delta phi template (delta track, delta R > 0.5)
        isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, fillTrkProp=True, cut='dR')
        if isSampled:
            m_BkgEst_CrossDeltaPhi_DeltaR_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
            if MET < m_MET_min:
                m_BkgEst_CrossDeltaPhi_DeltaR_loMET_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
            else:
                m_BkgEst_CrossDeltaPhi_DeltaR_hiMET_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
        # using delta phi template (delta track, delta Eta > 0.5)
        isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, cut='dEta')
        if isSampled:
            m_BkgEst_CrossDeltaPhi_DeltaEta_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
        # using delta phi template (delta track, no cut)
        isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, cut='none')
        if isSampled:
            m_BkgEst_CrossDeltaPhi_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)

        if change_dR_lower_threshold:
            # using delta phi template (delta track, delta R > 0.8)
            isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, threshold=0.8, cut='dR')
            if isSampled:
                m_BkgEst_CrossDeltaPhi_DeltaR_th08_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
            # using delta phi template (delta track, delta R > 1.0)
            isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, threshold=1.0, cut='dR')
            if isSampled:
                m_BkgEst_CrossDeltaPhi_DeltaR_th10_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
            # using delta phi template (delta track, delta R > 1.5)
            isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, threshold=1.5, cut='dR')
            if isSampled:
                m_BkgEst_CrossDeltaPhi_DeltaR_th15_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)

        if use_pt_upper_limit:
            # using delta phi template (delta track, pt < 20)
            isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, pt_max_GeV=20, cut='dR')
            if isSampled:
                m_BkgEst_CrossDeltaPhi_DeltaR_pt20_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
            isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, pt_max_GeV=15, cut='dR')
            if isSampled:
                m_BkgEst_CrossDeltaPhi_DeltaR_pt15_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
            isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, pt_max_GeV=10, cut='dR')
            if isSampled:
                m_BkgEst_CrossDeltaPhi_DeltaR_pt10_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
            isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, pt_max_GeV=5, cut='dR')
            if isSampled:
                m_BkgEst_CrossDeltaPhi_DeltaR_pt5_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
        if use_dR_upper_limit:
            # using delta phi template (delta track, dR < 1.0)
            isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, dR_max=1.0, cut='dR')
            if isSampled:
                m_BkgEst_CrossDeltaPhi_DeltaR_dR10_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
            isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, dR_max=1.5, cut='dR')
            if isSampled:
                m_BkgEst_CrossDeltaPhi_DeltaR_dR15_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
            isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, dR_max=2.0, cut='dR')
            if isSampled:
                m_BkgEst_CrossDeltaPhi_DeltaR_dR20_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
            isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, dR_max=2.5, cut='dR')
            if isSampled:
                m_BkgEst_CrossDeltaPhi_DeltaR_dR25_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
        #---------------------
        # NORMAL template
        #--------------------
        # using absolute template, no cut
        isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=False, cut='none')
        if isSampled:
            m_BkgEst_Cross_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
        # using absolute template, dR > 0.5
        isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=False, fillTrkProp=True, cut='dR')
        if isSampled:
            m_BkgEst_Cross_DeltaR_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
        #
        if construct_templates_with_angle_cut:
            # delta template (angle > 0.5)
            isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=True, useDeltaPhi=True, cut='angle')
            if isSampled:
                m_BkgEst_CrossDelta_Angle_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
            # using delta phi template (delta track, delta R > 0.5)
            isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, cut='angle')
            if isSampled:
                m_BkgEst_CrossDeltaPhi_Angle_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
            # using absolute template, relative angle cut
            isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=False, cut='angle')
            if isSampled:
                m_BkgEst_Cross_Angle_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)

        #
        #
        if construct_multiple_templates:
            # collimated template
            if (max_average_opening_angle < m_angleCut):
                isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates)
                if isSampled:
                    m_BkgEst_Cross_NoLargeAngle_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
                # use Delta Phi
                isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, cut='dR')
                if isSampled:
                    m_BkgEst_CrossDeltaPhi_NoLargeAngle_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
            # large angle template
            else:
                isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates)
                if isSampled:
                    m_BkgEst_Cross_LargeAngle_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
                # use Delta Phi
                isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, cut='dR')
                if isSampled:
                    m_BkgEst_CrossDeltaPhi_LargeAngle_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)


def sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=False, divideZregion=True, fillTrkProp=False,
                        pt_max_GeV=10000, dEta_max=10, dPhi_max=10, dR_max=10, angle_max=10, threshold=0.5, cut='dR'):
    global irandom
    nTries = 0
    random_track = TLorentzVector()
    irandom = int(gRandom.Uniform()*nTrkTemplates)
    isSampled = False
    while (not isSampled and nTries < 1000):
        if TMath.Abs(irandom - nTrkTemplates) < 1:
            irandom = 0
        # get the next tree in the chain and verify
        ientry = trkTemplate.LoadTree(irandom)
        # copy next entry into memory and verify
        nb = trkTemplate.GetEntry(irandom)
        irandom += 1
        if m_Region != trkTemplate.region:
            continue
        nTries += 1
        if divideZregion and m_posDV.Z() * trkTemplate.dv_z < 0:
            continue
        if trkTemplate.pt > pt_max_GeV:
            continue
        random_track_eta = trkTemplate.eta
        random_track_phi = trkTemplate.phi
        if useDeltaEta:
            random_track_eta = m_DVPV.Eta() + trkTemplate.d_eta
        if useDeltaPhi:
            random_track_phi = m_DVPV.Phi() + trkTemplate.d_phi
        random_track.SetPtEtaPhiM(trkTemplate.pt, random_track_eta, random_track_phi, m_massPion)
        if cut == 'dR' and (random_track.DeltaR(m_DVPV) > threshold):
            isSampled = True
        elif cut == 'dEta' and (abs(random_track.Eta() - m_DVPV.Eta()) > threshold):
            isSampled = True
        elif cut == 'angle' and (random_track.Angle(m_DVPV.Vect()) > threshold):
            isSampled = True
        elif cut == 'none':
            isSampled = True
    if isSampled:
        #if irandom < 10000:
        #if m_Region >= 10:
        #    print(irandom, m_Region, random_track.Eta(), random_track.Phi(), nTrkTemplates)
        if fillTrkProp and (m_tlvDV+random_track).M() > 3:
            #print('before')
            #print(random_track.Eta(), random_track.Phi())
            #print(m_DVPV.Eta(), m_DVPV.Phi())
            fill_TrkProp(useDeltaEta, useDeltaPhi, m_Region, random_track)
        return True, m_tlvDV+random_track
    if not isSampled:
        print('Warning! A track was not sampled!')
        return False, m_tlvDV

    #print(entry, irandom, trkTemplate.pt, trkTemplate.eta, trkTemplate.phi)


def fill_TrkProp(useDeltaEta, useDeltaPhi, region, random_track):
    ii = -1
    if (not useDeltaEta) and (not useDeltaPhi):
        ii = 0
    elif (not useDeltaEta) and useDeltaPhi:
        ii = 1
    elif useDeltaEta and useDeltaPhi:
        ii = 2
    if ii < 0:
        return
    dvTrks = [trk for trk in m_dvTrks]
    #dvTrks = []
    dvTrks.append(random_track)
    #print('after')
    #print(random_track.Eta(), random_track.Phi())
    #print(m_DVPV.Eta(), m_DVPV.Phi())
    for dvTrk in dvTrks:
        m_TrkProp_Pt_iTrk_Region[ii][m_DVnTrk+1][region].Fill(dvTrk.Pt())
        if ii == 0:
            # EtaPhi
            m_TrkProp_Angle_iTrk_Region[ii][m_DVnTrk+1][region].Fill(dvTrk.Eta(), dvTrk.Phi())
        elif ii == 1:
            # EtaDeltaPhi
            m_TrkProp_Angle_iTrk_Region[ii][m_DVnTrk+1][region].Fill(dvTrk.Eta(), dvTrk.Phi() - m_DVPV.Phi())
        elif ii == 2:
            # DeltaEtaDeltaPhi
            m_TrkProp_Angle_iTrk_Region[ii][m_DVnTrk+1][region].Fill(dvTrk.Eta() - m_DVPV.Eta(), dvTrk.Phi() - m_DVPV.Phi())


def main():
    global irandom
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--inputFiles', type=str, help='comma separated input files')
    parser.add_argument('-o', '--outputFile', type=str, help='output file name')
    args = parser.parse_args()
    #input_files = args.inputFiles
    #print(args.inputFiles)
    input_files = args.inputFiles.split(',')
    print('*** input files: ')
    print(input_files)
    
    print('*** output file: ')
    print(args.outputFile)
    output_root = TFile(args.outputFile, 'recreate')
    
    book_histograms()

    chain = TChain('Nominal', 'Nominal Tree')
    for input_file in input_files:
        chain.Add(input_file)

    #f = TFile('~/data/data16_13TeV/DVPlusMETSys/DVtrkTemplate_v3.root', 'open')
    #f = TFile('~/data/data16_13TeV/DVPlusMETSys/DVtrkTemplate_no2trk_NonVetoOnly_v3.root', 'open')
    # 3 GeV mass cut
    #f = TFile('~/data/data16_13TeV/DVPlusMETSys/DVtrkTemplate_no2trk_massCut_v06-00-00.root', 'open')
    #f = TFile('~/data/data16_13TeV/DVPlusMETSys/DVtrkTemplate_no2trk_v06-00-00.root', 'open')
    #f = TFile('~/data/data16_13TeV/DVPlusMETSys/DVtrkTemplate_no2trk_v06-00-01.root', 'open')
    #f = TFile('~/data/data16_13TeV/DVPlusMETSys/DVtrkTemplate_no2trk_massCut_v06-00-01.root', 'open')
    f = TFile('~/data/data16_13TeV/DVPlusMETSys/DVtrkTemplate_no2trk_massCut_v06-00-03.root', 'open')
    trkTemplate = f.Get('DVtrkTemplate')
    nTrkTemplates = trkTemplate.GetEntries()
    
    entries = chain.GetEntries()
    print('* Number of entries = {}'.format(entries))

    irandom = int(gRandom.Uniform()*nTrkTemplates)

    try:
        for entry in range(entries):
            #if not entry % 10000:
            #    print('*** processed {0} out of {1} ({2}%)'.format(entry, entries, round(float(entry)/entries*100., 1)))
            utils.show_progress(entry, entries)
                #irandom = int(gRandom.Uniform()*nTrkTemplates)
                #print(irandom)
            #if entry == 1000:
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
            m_nEvents.Fill(0.5, event_weight)
            #if chain.MET > 200:
            #    continue
            m_nEvents_MET.Fill(0.5, event_weight)
            if utils.basic_event_selection(chain):
                m_posPV.SetXYZ(chain.PV_x, chain.PV_y, chain.PV_z)
                for idv in range(len(chain.DV_x)):
                    #if basic_dv_selection(chain, idv) and chain.DV_nTracks[idv] < 7 and chain.DV_Region[idv] >= 0:
                    if utils.basic_dv_selection(chain, idv) and chain.DV_Region[idv] >= 0:
                        dvInfo(chain, idv)
                        #print('orig'+str(m_tlvDV.M()))
                        m_DVPV.SetVect(m_posDV - m_posPV)
                        
                        dvBkgEst(trkTemplate, nTrkTemplates, chain.MET)
                        irandom += 1
    except KeyboardInterrupt:
        pass
        
    output_root.cd()
    m_nEvents.Write()
    m_nEvents_MET.Write()
    for itrk in range(2, 7):
        for region in range(12):
            m_BkgEst_data_iTrk_Region[itrk][region].Write()
            if itrk == 6:
                m_BkgEst_data_iTrk_Region[7][region].Write()
            m_BkgEst_data_loMET_iTrk_Region[itrk][region].Write()
            m_BkgEst_data_hiMET_iTrk_Region[itrk][region].Write()
            m_BkgEst_data_NoCross_iTrk_Region[itrk][region].Write()
            m_BkgEst_data_NoCross_maxAngle_iTrk_Region[itrk][region].Write()
            m_BkgEst_data_NoCross_maxDeltaR_iTrk_Region[itrk][region].Write()
            m_BkgEst_data_NoCross_maxDeltaEta_iTrk_Region[itrk][region].Write()
            #
            m_AvgAngleDVmass_iTrk_Region[itrk][region].Write() 
            m_maxAngleDVmass_iTrk_Region[itrk][region].Write() 
            m_dRDVmass_iTrk_Region[itrk][region].Write() 
            m_dEtaDVmass_iTrk_Region[itrk][region].Write() 
            if itrk == 2:
                continue
            m_BkgEst_Cross_iTrk_Region[itrk][region].Write()
            m_BkgEst_Cross_Angle_iTrk_Region[itrk][region].Write()
            m_BkgEst_Cross_DeltaR_iTrk_Region[itrk][region].Write()
            m_BkgEst_Cross_NoLargeAngle_iTrk_Region[itrk][region].Write()
            m_BkgEst_Cross_LargeAngle_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_NoLargeAngle_iTrk_Region[itrk][region].Write()
            #m_BkgEst_CrossDeltaPhi_LargeAngle_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDelta_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDelta_DeltaR_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDelta_Angle_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_DeltaR_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_DeltaR_loMET_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_DeltaR_hiMET_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_DeltaR_th08_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_DeltaR_th10_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_DeltaR_th15_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_DeltaR_pt20_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_DeltaR_pt15_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_DeltaR_pt10_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_DeltaR_pt5_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_DeltaR_dR10_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_DeltaR_dR15_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_DeltaR_dR20_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_DeltaR_dR25_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_DeltaEta_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_Angle_iTrk_Region[itrk][region].Write() 
    #for ii,flavor in enumerate(flavors):
    for jj,prop in enumerate(props):
            for itrk in range(3, 7):
                for region in range(12):
                    #if jj == 0:
                    m_TrkProp_Pt_iTrk_Region[jj][itrk][region].Write()
                    m_TrkProp_Angle_iTrk_Region[jj][itrk][region].Write()
    #h_cut_flow_dv.Write()
    #h_DVmass_Ntrk.Write()
    #h_DVmass_Ntrk_MatVeto.Write()
    #h_DVmass_Ntrk_MatVeto_MET220.Write()
    #h_DVmass_Ntrk_MatVeto_MET250.Write()
    #for ntrk in range(2, 7):
    #    for reg in range(12):
    #        h_DVmass_Ntrk_Region[ntrk][reg].Write()
    output_root.Close()


if __name__ == '__main__':
    main()
