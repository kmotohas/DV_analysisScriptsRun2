#!/bin/env python

from ROOT import *

import argparse

m_angleCut = 0.5
m_massPion = 139.57*0.001

m_dvTrks = []
m_tlvDV = TLorentzVector()
m_posDV = TVector3()
m_posPV = TVector3()
m_Region = 0
m_DVnTrk = 0
m_DVPV = TLorentzVector()

m_BkgEst_data_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_data_NoCross_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_Cross_NoLargeAngle_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_Cross_LargeAngle_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_NoLargeAngle_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_LargeAngle_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDelta_DeltaR_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_DeltaR_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_DeltaEta_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]
m_BkgEst_CrossDeltaPhi_Angle_iTrk_Region = [[TH1F() for region in range(12)] for itrk in range(7)]

#irandom = int(gRandom.Uniform()*nTrkTemplates)
irandom = 0

def book_histograms():
    global m_BkgEst_data_iTrk_Region
    global m_BkgEst_data_NoCross_iTrk_Region
    global m_BkgEst_Cross_NoLargeAngle_iTrk_Region
    global m_BkgEst_Cross_LargeAngle_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_NoLargeAngle_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_LargeAngle_iTrk_Region
    global m_BkgEst_CrossDelta_DeltaR_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_DeltaR_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_DeltaEta_iTrk_Region
    global m_BkgEst_CrossDeltaPhi_Angle_iTrk_Region
    for itrk in range(2, 7):
        for region in range(12):
            m_BkgEst_Cross_data_iTrk_Region[itrk][region] = TH1F('BkgEst_data_{0}Trk_Region{1}'.format(itrk, region),
                                                                         ';Invariant Mass [GeV]; Number of Vertices', 500, 0, 100)
            m_BkgEst_Cross_data_NoCross_iTrk_Region[itrk][region] = TH1F('BkgEst_data_NoCross_{0}Trk_Region{1}'.format(itrk, region),
                                                                         ';Invariant Mass [GeV]; Number of Vertices', 500, 0, 100)
            m_BkgEst_Cross_NoLargeAngle_iTrk_Region[itrk][region] = TH1F('BkgEst_Cross_NoLargeAngle_{0}Trk_Region{1}'.format(itrk, region),
                                                                         ';Invariant Mass [GeV]; Number of Vertices', 500, 0, 100)
            m_BkgEst_Cross_LargeAngle_iTrk_Region[itrk][region] = TH1F('BkgEst_Cross_LargeAngle_{0}Trk_Region{1}'.format(itrk, region),
                                                                       ';Invariant Mass [GeV]; Number of Vertices', 500, 0, 100)
            m_BkgEst_CrossDeltaPhi_NoLargeAngle_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhi_NoLargeAngle_{0}Trk_Region{1}'.format(itrk, region),
                                                                         ';Invariant Mass [GeV]; Number of Vertices', 500, 0, 100)
            m_BkgEst_CrossDeltaPhi_LargeAngle_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhi_LargeAngle_{0}Trk_Region{1}'.format(itrk, region),
                                                                       ';Invariant Mass [GeV]; Number of Vertices', 500, 0, 100)
            m_BkgEst_CrossDelta_DeltaR_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaDeltaR_{0}Trk_Region{1}'.format(itrk, region),
                                                                       ';Invariant Mass [GeV]; Number of Vertices', 500, 0, 100)
            m_BkgEst_CrossDeltaPhi_DeltaR_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiDeltaR_{0}Trk_Region{1}'.format(itrk, region),
                                                                       ';Invariant Mass [GeV]; Number of Vertices', 500, 0, 100)
            m_BkgEst_CrossDeltaPhi_DeltaEta_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiDeltaEta_{0}Trk_Region{1}'.format(itrk, region),
                                                                       ';Invariant Mass [GeV]; Number of Vertices', 500, 0, 100)
            m_BkgEst_CrossDeltaPhi_Angle_iTrk_Region[itrk][region] = TH1F('BkgEst_CrossDeltaPhiAngle_{0}Trk_Region{1}'.format(itrk, region),
                                                                       ';Invariant Mass [GeV]; Number of Vertices', 500, 0, 100)


def basic_event_selection(tree):
    # [1: Trigger, 2: Filter, 3: Cleaning, 4: GRL,
    #  5: PV, 6: MET, 7: DV Selection]
    return tree.PassCut3 and tree.PassCut4 and tree.PassCut5


def basic_dv_selection(tree, idv):
    return tree.DV_passFidCuts[idv] and tree.DV_passChisqCut[idv] and tree.DV_passDistCut[idv]


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
    #print('next_dvTrks_len'+str(len(m_dvTrks)))
    for ii, trk1 in enumerate(m_dvTrks):
        totalAngleToOtherTracks = 0.
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
    return maxTotalAngleToOtherTracks/(m_DVnTrk-1.)


def dvBkgEst(trkTemplate, nTrkTemplates):
    global irandom

    # data
    m_BkgEst_data_iTrk_Region[m_DVnTrk][m_Region].Fill(m_tlvDV.M())
    max_average_opening_angle = getMaxTrkAngle()
    if (max_average_opening_angle < m_angleCut):
        m_BkgEst_data_NoCross_iTrk_Region[m_DVnTrk][m_Region].Fill(m_tlvDV.M())

    nLoops = m_DVnTrk-1 + (m_DVnTrk-2) * 5
    for _ in range(nLoops):
        # nominal template (delta track, delta R > 0.5)
        isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=True, useDeltaPhi=True, cut='dR')
        if isSampled:
            m_BkgEst_CrossDelta_DeltaR_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
        # using delta phi template (delta track, delta R > 0.5)
        isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, cut='dR')
        if isSampled:
            m_BkgEst_CrossDeltaPhi_DeltaR_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
        # using delta phi template (delta track, delta Eta > 0.5)
        isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, cut='dEta')
        if isSampled:
            m_BkgEst_CrossDeltaPhi_DeltaEta_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
        # using delta phi template (delta track, delta R > 0.5)
        isSampled, dvVtxCross = sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=True, cut='angle')
        if isSampled:
            m_BkgEst_CrossDeltaPhi_Angle_iTrk_Region[m_DVnTrk+1][m_Region].Fill(dvVtxCross.M(), 1./nLoops)
        #
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


def sample_random_track(trkTemplate, nTrkTemplates, useDeltaEta=False, useDeltaPhi=False, cut='dR'):
    global irandom
    isSampled = False
    nTries = 0
    random_track = TLorentzVector()
    while (not isSampled and nTries < 1000):
        nTries += 1
        if TMath.Abs(irandom - nTrkTemplates) < 1:
            irandom = int(gRandom.Uniform()*nTrkTemplates)
        # get the next tree in the chain and verify
        ientry = trkTemplate.LoadTree(irandom)
        # copy next entry into memory and verify
        nb = trkTemplate.GetEntry(irandom)
        irandom += 1
        if m_Region != trkTemplate.region:
            continue
        random_track_eta = trkTemplate.eta
        random_track_phi = trkTemplate.phi
        if useDeltaEta:
            random_track_eta = m_DVPV.Eta() + trkTemplate.d_eta
        if useDeltaPhi:
            random_track_phi = m_DVPV.Phi() + trkTemplate.d_phi
        random_track.SetPtEtaPhiM(trkTemplate.pt, random_track_eta, random_track_phi, m_massPion)
        if cut == 'dR' and (random_track.DeltaR(m_DVPV) > m_angleCut):
            return True, m_tlvDV+random_track
        elif cut == 'dEta' and (TMath.Abs(random_track.Eta() - m_DVPV.Eta()) > m_angleCut):
            return True, m_tlvDV+random_track
        elif cut == 'angle' and (random_track.Angle(m_DVPV.Vect()) > m_angleCut):
            return True, m_tlvDV+random_track
    print('Warning! A track was not sampled!')
    return False, m_tlvDV

    #print(entry, irandom, trkTemplate.pt, trkTemplate.eta, trkTemplate.phi)


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

    f = TFile('./DVtrkTemplate_v3.root', 'open')
    trkTemplate = f.Get('DVtrkTemplate')
    nTrkTemplates = trkTemplate.GetEntries()
    
    entries = chain.GetEntries()
    print('* Number of entries = {}'.format(entries))

    irandom = int(gRandom.Uniform()*nTrkTemplates)

    try:
        for entry in range(entries):
            if not entry % 10000:
                print('*** processed {0} out of {1} ({2}%)'.format(entry, entries, round(float(entry)/entries*100., 1)))
                irandom = int(gRandom.Uniform()*nTrkTemplates)
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
            event_weight = chain.McEventWeight * chain.PileupWeight * chain.ISRWeight
            if basic_event_selection(chain):
                m_posPV.SetXYZ(chain.PV_x, chain.PV_y, chain.PV_z)
                for idv in range(len(chain.DV_x)):
                    if basic_dv_selection(chain, idv) and chain.DV_nTracks[idv] < 6 and chain.DV_Region[idv] >= 0:
                        dvInfo(chain, idv)
                        #print('orig'+str(m_tlvDV.M()))
                        m_DVPV.SetVect(m_posDV - m_posPV)
                        
                        dvBkgEst(trkTemplate, nTrkTemplates)
                        irandom += 1
    except KeyboardInterrupt:
        pass
        
    output_root.cd()
    for itrk in range(3, 7):
        for region in range(12):
            m_BkgEst_Cross_NoLargeAngle_iTrk_Region[itrk][region].Write()
            m_BkgEst_Cross_LargeAngle_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_NoLargeAngle_iTrk_Region[itrk][region].Write()
            m_BkgEst_CrossDeltaPhi_LargeAngle_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDelta_DeltaR_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_DeltaR_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_DeltaEta_iTrk_Region[itrk][region].Write() 
            m_BkgEst_CrossDeltaPhi_Angle_iTrk_Region[itrk][region].Write() 
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
