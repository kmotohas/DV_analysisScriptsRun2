from ROOT import *

import mc

#isData = False
isData = True
isMC = not isData

h_evt = TH1F()
h_vx = TH1F()
tfile = TFile()

e_cutflow = [
           "Initial Events",
           #"Jet+MET Trigger",
           "MET Trigger",
           #"Meff filter",
           "MET filter",
           "Event cleaning",
           "Good Runs List",
           "Primary vertex",
           "Offline MET cut",
           "DV selection"
           ]
v_cutflow = [
            "Reco DVs",
            "Event cuts",
            "Fiducial acceptance",
            "DV displacement",
            "Fit quality",
            "Material veto",
            "DV nTrk",
            "DV mass"
            ]

#dM = ["30","50","80","130","1100"]
#l_met = ["100","110","120","130","140","150"]
#l_meff = ["1000","1100","1200","1300","1400","1500"]

#ld = open("./hists_mc.list")
#files = ld.readlines()
#ld.close()

#for dsid in range(402715,402720):
for dsid in range(402700,402740):
            #met = 200
            #mgluino = 600 + 200 * int((dsid - 402700) / 5)
            mgluino = mc.parameters[dsid]['g']
            dM = mgluino - mc.parameters[dsid]['chi0']
    #for met in range(100,101,10):
        #for meff in range(1000,1001,100):
            print "%"
            if isData:
                #if dsid != 402715:
                #tfile = TFile("../plots_maker_systTree_hadd_PeriodA-I.root")
                #tfile = TFile("../plots_maker_systTree_hadd_PeriodK-L.root")
                tfile = TFile("../plots_maker_systTree_hadd_PeriodALL_v22.root")
                print "% cut flow of data"
            elif isMC:
                #tfile = TFile("../hist/hist_" + str(dsid) + "_" + str(meff) + "_" + str(met) + ".root","open")
                #tfile = TFile("../hist/hist_" + str(dsid) + "_" + str(met) + ".root","open")
                #tfile = TFile("../hist/hist_" + str(dsid) + "_" + str(met) + ".root","open")
                filepath = ""
                for tmp_file in files:
                    if tmp_file.find("run" + str(dsid)) is not -1:
                        filepath = tmp_file[:-1]
                #tfile = TFile("../submitDir_LSF/mc/hist_DVPlusMETEff,DVPlusMETCutFlow/hist_" + str(dsid) + ".root","open")
                if filepath is "":
                    continue
                tfile = TFile(filepath,"open")
                print "% cut flow of DSID" + str(dsid)
            print "%"

            #tfile.GetObject("evt_cuts_DVPlusMET",h_evt)
            #tfile.GetObject("vx_cuts_DVPlusMET",h_vx)
            tfile.GetObject("cut_flow_event",h_evt)
            tfile.GetObject("cut_flow_dv",h_vx)

            print "\\begin{table}[hp]"
            print "\\begin{center}"
            if isData:
                print "  \\caption{Cut flow table for 2015 data of the DESDM\\_RPVLL stream for DV$+E^\\mathrm{miss}_T$ channel.}"
                print "  \\label{tab:cutflow_data}"
            elif isMC:
                print "  \\caption{Cut flow table for MC ($\\mathrm{DSID}=" + str(dsid) + "$, $M_{\\tilde{g}}=" + str(mgluino) + "\\,\\mathrm{[GeV]}$, $dM=" + dM  + "\\,\\mathrm{[GeV]}$) for DV$+E^{\\mathrm{miss}}_T$ channel.}"
                print "  \\label{tab:cutflow_dsid" + str(dsid) + "}"
            print "\small"
            print "  \\begin{tabular}{cccc} \\hline"
            print "    \multicolumn{4}{c}{Event Selection Cuts} \\\\ \\hline \\hline"
            print "     & Number of Events & Relative Efficiency [\%] & Overall Efficiency [\%] \\\\ \\hline"
            count = 1
            for cf in e_cutflow:
                if count == 1:
                    print "    " + cf + " & " + str(int(h_evt.GetBinContent(count))) + " & 100 & 100 " + "\\\\"
                elif (cf is "DV selection") and isData:
                    print "    " + cf + " & blinded & blinded & blinded " + "\\\\"
                else:
                    if h_evt.GetBinContent(count-1) == 0:
                        print "    " + cf + " & " + str(int(h_evt.GetBinContent(count))) + " & " + '%03.3f' % float(0.) + " & " + '%03.3f' % float(h_evt.GetBinContent(count)/h_evt.GetBinContent(1) * 100) + " \\\\"
                    else:
                        print "    " + cf + " & " + str(int(h_evt.GetBinContent(count))) + " & " + '%03.3f' % float(h_evt.GetBinContent(count)/h_evt.GetBinContent(count-1) * 100) + " & " + '%03.3f' % float(h_evt.GetBinContent(count)/h_evt.GetBinContent(1) * 100) + " \\\\"
                count += 1
            print "    \\hline"
            print "    \multicolumn{4}{c}{Vertex Selection Cuts} \\\\ \\hline \\hline"
            print "     & Number of DVs & Relative Efficiency [\%] & Overall Efficiency [\%] \\\\ \\hline"
            count = 1
            for cf in v_cutflow:
                if count == 1:
                    print "    " + cf + " & " + str(int(h_vx.GetBinContent(count))) + " & 100 & 100 " + "\\\\"
                elif ((cf is "DV nTrk") or (cf is "DV mass")) and isData:
                    print "    " + cf + " & blinded & blinded & blinded " + "\\\\"
                else:
                    if h_vx.GetBinContent(count-1) == 0:
                        print "    " + cf + " & " + str(int(h_vx.GetBinContent(count))) + " & " + '%03.3f' % float(0.) + " & " + '%03.3f' % float(h_vx.GetBinContent(count)/h_vx.GetBinContent(1) * 100) + " \\\\"
                    else:
                        print "    " + cf + " & " + str(int(h_vx.GetBinContent(count))) + " & " + '%03.3f' % float(h_vx.GetBinContent(count)/h_vx.GetBinContent(count-1) * 100) + " & " + '%03.3f' % float(h_vx.GetBinContent(count)/h_vx.GetBinContent(1) * 100) + " \\\\"
                count += 1
            print "    \\hline"
            print "  \\end{tabular}"
            print "\\end{center}"
            print "\\end{table}"
            print ""
            if isData:
                return
