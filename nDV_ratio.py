from ROOT import *
import utils

tfile = utils.open_tfile('../output_systTree_PeriodA-I.root')
#tfile = utils.open_tfile('../all_2016.root')
#tfile = utils.open_tfile('../all_2016.root')

h = [[TH1F() for _ in range(12)] for __ in range(5)]
h_nolarge = [[TH1F() for _ in range(12)] for __ in range(5)]
h_large = [[TH1F() for _ in range(12)] for __ in range(5)]
h_cross = [[TH1F() for _ in range(12)] for __ in range(5)]

for ntrk in [2, 3, 4]:
    for reg in range(12):
        tfile.GetObject('BkgEst_data_{0}Trk_Region{1}_DVMultiTrkBkg'.format(ntrk, reg), h[ntrk][reg])
        #tfile.GetObject('BkgEst_Cross_NoLargeAngle_{0}Trk_Region{1}_DVMultiTrkBkg'.format(ntrk, reg), h_nolarge[ntrk][reg])
        #tfile.GetObject('BkgEst_Cross_LargeAngle_{0}Trk_Region{1}_DVMultiTrkBkg'.format(ntrk, reg), h_large[ntrk][reg])
        #tfile.GetObject('BkgEst_Cross_{0}Trk_Region{1}_DVMultiTrkBkg'.format(ntrk, reg), h_cross[ntrk][reg])

bin8 = h[2][0].FindBin(4)
bin2 = h[2][0].FindBin(6)
bin4 = h[2][0].FindBin(3.6)
bin10 = h[2][0].FindBin(10)
print(bin10)
l = []
l2 = []
for reg in range(12):
    print('Region: ' + str(reg))
    #print float(h_large[3][reg].GetEntries()) / h[2][reg].GetEntries()
    #print float(h_cross[4][reg].GetEntries()) / h[3][reg].GetEntries()
    #print float(h_large[3][reg].GetEntries()) / h_nolarge[3][reg].GetEntries()
    #print float(h_large[4][reg].GetEntries()) / h_nolarge[4][reg].GetEntries()
    #print h[2][reg].GetEntries() * h[4][reg].GetEntries() / h[3][reg].GetEntries() ** 2 
    #l.append(round(h[2][reg].GetEntries() * h[4][reg].GetEntries() / h[3][reg].GetEntries() ** 2, 2) )
    #l2.append(round(h[2][reg].GetEntries() * h[4][reg].GetEntries() / h[3][reg].GetEntries() ** 2, 2) )
    #if reg == 2 or reg == 4:
    #    l.append(round(float(h[2][2].GetEntries()+h[2][4].GetEntries()) / 
    #                        (h[3][2].Integral(bin4, -1)+h[3][4].Integral(bin4, -1)) * 
    #                        (h[4][2].Integral(bin4, -1)+h[4][4].Integral(bin4, -1)) / 
    #                        (h[3][2].GetEntries()+h[3][4].GetEntries()), 4) )
    #else:
    #    l.append(round(float(h[2][reg].GetEntries()) / h[3][reg].Integral(bin8, -1) * h[4][reg].Integral(bin2, -1) / h[3][reg].GetEntries(), 4) )
    #print(h[4][reg].Integral(h[4][reg].FindBin(10), -1))
    l.append(round(float(h[2][reg].GetEntries()) / h[3][reg].Integral(h[3][reg].FindBin(6), -1) * h[4][reg].Integral(h[4][reg].FindBin(6), -1) / h[3][reg].GetEntries(), 3) )
    #l2.append(round(h[2][reg].GetEntries() * h[4][reg].GetEntries() / h[3][reg].GetEntries() ** 2, 2) )
    #print h[2][reg].Integral(bin4, -1) * h[4][reg].Integral(bin4, -1) / h[3][reg].Integral(bin4, 0) ** 2 
print  l
