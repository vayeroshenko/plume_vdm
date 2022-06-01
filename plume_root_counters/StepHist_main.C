// Author V. Balagura, balagura@cern.ch (Dec 2016)

#include <StepHist.h>
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>

inline void erase_i(ostream& os, int i) {
  if (i == 0) { os << "\b \b"; return; } // \b moves back, ' ' erases, \b moves back again
  while (i > 0) { os << "\b \b"; i /= 10; } // positive i: delete all digits
}

struct LumiCounters_ROOT {
  ULong64_t       EventInSequence;
  ULong64_t       EvtNumber;
  UInt_t          OrbitNumber;
  ULong64_t       RunNumber;
  UInt_t          bcid;
  ULong64_t       gpsTime;
  UShort_t        lumi_channel_0;
  UShort_t        lumi_channel_1;
  UShort_t        lumi_channel_2;
  UShort_t        lumi_channel_3;
  UShort_t        lumi_channel_4;
  UShort_t        lumi_channel_6;
  UShort_t        lumi_channel_7;
  UShort_t        lumi_channel_8;
  UShort_t        lumi_channel_9;
  UShort_t        lumi_channel_10;
  UShort_t        lumi_channel_12;
  UShort_t        lumi_channel_13;
  UShort_t        lumi_channel_14;
  UShort_t        lumi_channel_15;
  UShort_t        lumi_channel_16;
  UShort_t        lumi_channel_18;
  UShort_t        lumi_channel_19;
  UShort_t        lumi_channel_20;
  UShort_t        lumi_channel_21;
  UShort_t        lumi_channel_22;
  UShort_t        lumi_channel_24;
  UShort_t        lumi_channel_25;
  UShort_t        lumi_channel_26;
  UShort_t        lumi_channel_27;
  UShort_t        lumi_channel_28;
  UShort_t        lumi_channel_30;
  UShort_t        lumi_channel_31;
  UShort_t        lumi_channel_32;
  UShort_t        lumi_channel_33;
  UShort_t        lumi_channel_34;
  UShort_t        lumi_channel_36;
  UShort_t        lumi_channel_37;
  UShort_t        lumi_channel_38;
  UShort_t        lumi_channel_39;
  UShort_t        lumi_channel_40;
  UShort_t        lumi_channel_42;
  UShort_t        lumi_channel_43;
  UShort_t        lumi_channel_44;
  UShort_t        lumi_channel_45;
  UShort_t        lumi_channel_46;
  UShort_t        lumi_channel_48;
};

int main(int argc, char** argv) {

  if (argc != 2 && argc != 3 && argc != 4) {
    cerr << "usage: " << argv[0] << " <ROOT_file_with_lumi_counters> [int cut] [per_ee]\n"
	  << "If [cut] is not given (default), cut = 300 \n"
    << "If \"per_ee\" is not given (default), the empty-empty bunches are combined into bcid=10000\n";
    return 1;
  }

  UShort_t cut = 400;
  bool per_ee = false;

  if (argc > 2 && TString(argv[2]) != "per_ee") {
    cut = (int)(size_t)argv[2];
  }

  if (argc == 3 && TString(argv[2]) == "per_ee") {
    per_ee = true;
  } else if (argc == 4 && TString(argv[3]) == "per_ee") {
    per_ee = true;
  }

  TString file_name = argv[1];
  StepHist step_hist(cin);


  LumiCounters_ROOT r;
  TDirectoryFile *dirfile;
  TTree* tree;
  Long64_t nEntries;

  TFile* file = new TFile(file_name);

  TString
    tdir_name   = "PlumeTuple",
    ntuple_name = "Plume";

  dirfile =  (TDirectoryFile *)file->Get(tdir_name);
  tree = (TTree*)dirfile->Get(ntuple_name);

  // tree->Print();

  tree->SetMakeClass(1);
  tree->SetBranchAddress("RunNumber", &r.RunNumber);
  tree->SetBranchAddress("gpsTime", &r.gpsTime);
  tree->SetBranchAddress("EvtNumber", &r.EvtNumber);
  tree->SetBranchAddress("OrbitNumber", &r.OrbitNumber);
  tree->SetBranchAddress("EventInSequence", &r.EventInSequence);
  tree->SetBranchAddress("bcid", &r.bcid);
  tree->SetBranchAddress("lumi_channel_0", &r.lumi_channel_0);
  tree->SetBranchAddress("lumi_channel_1", &r.lumi_channel_1);
  tree->SetBranchAddress("lumi_channel_2", &r.lumi_channel_2);
  tree->SetBranchAddress("lumi_channel_3", &r.lumi_channel_3);
  tree->SetBranchAddress("lumi_channel_4", &r.lumi_channel_4);
  tree->SetBranchAddress("lumi_channel_6", &r.lumi_channel_6);
  tree->SetBranchAddress("lumi_channel_7", &r.lumi_channel_7);
  tree->SetBranchAddress("lumi_channel_8", &r.lumi_channel_8);
  tree->SetBranchAddress("lumi_channel_9", &r.lumi_channel_9);
  tree->SetBranchAddress("lumi_channel_10", &r.lumi_channel_10);
  tree->SetBranchAddress("lumi_channel_12", &r.lumi_channel_12);
  tree->SetBranchAddress("lumi_channel_13", &r.lumi_channel_13);
  tree->SetBranchAddress("lumi_channel_14", &r.lumi_channel_14);
  tree->SetBranchAddress("lumi_channel_15", &r.lumi_channel_15);
  tree->SetBranchAddress("lumi_channel_16", &r.lumi_channel_16);
  tree->SetBranchAddress("lumi_channel_18", &r.lumi_channel_18);
  tree->SetBranchAddress("lumi_channel_19", &r.lumi_channel_19);
  tree->SetBranchAddress("lumi_channel_20", &r.lumi_channel_20);
  tree->SetBranchAddress("lumi_channel_21", &r.lumi_channel_21);
  tree->SetBranchAddress("lumi_channel_22", &r.lumi_channel_22);
  tree->SetBranchAddress("lumi_channel_24", &r.lumi_channel_24);
  tree->SetBranchAddress("lumi_channel_25", &r.lumi_channel_25);
  tree->SetBranchAddress("lumi_channel_26", &r.lumi_channel_26);
  tree->SetBranchAddress("lumi_channel_27", &r.lumi_channel_27);
  tree->SetBranchAddress("lumi_channel_28", &r.lumi_channel_28);
  tree->SetBranchAddress("lumi_channel_30", &r.lumi_channel_30);
  tree->SetBranchAddress("lumi_channel_31", &r.lumi_channel_31);
  tree->SetBranchAddress("lumi_channel_32", &r.lumi_channel_32);
  tree->SetBranchAddress("lumi_channel_33", &r.lumi_channel_33);
  tree->SetBranchAddress("lumi_channel_34", &r.lumi_channel_34);
  tree->SetBranchAddress("lumi_channel_36", &r.lumi_channel_36);
  tree->SetBranchAddress("lumi_channel_37", &r.lumi_channel_37);
  tree->SetBranchAddress("lumi_channel_38", &r.lumi_channel_38);
  tree->SetBranchAddress("lumi_channel_39", &r.lumi_channel_39);
  tree->SetBranchAddress("lumi_channel_40", &r.lumi_channel_40);
  tree->SetBranchAddress("lumi_channel_42", &r.lumi_channel_42);
  tree->SetBranchAddress("lumi_channel_43", &r.lumi_channel_43);
  tree->SetBranchAddress("lumi_channel_44", &r.lumi_channel_44);
  tree->SetBranchAddress("lumi_channel_45", &r.lumi_channel_45);
  tree->SetBranchAddress("lumi_channel_46", &r.lumi_channel_46);

  nEntries = tree->GetEntriesFast();
  std::cout << nEntries << '\n';

  UShort_t
    ring_48 = 0,
    ring_49 = 0,
    ring_50 = 0,
    ring_51 = 0,
    ring_52 = 0;


  bool interactive = true;
  for (Long64_t iEntry=0; iEntry<nEntries; ++iEntry) {
    tree->GetEntry(iEntry);
    // Counters preserve the number of the first layer number of PLUME.
    step_hist.add(
      r.gpsTime,
      0,
      r.bcid,
      (r.lumi_channel_0 > cut && r.lumi_channel_24 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      1,
      r.bcid,
      (r.lumi_channel_1 > cut && r.lumi_channel_25 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      2,
      r.bcid,
      (r.lumi_channel_2 > cut && r.lumi_channel_26 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      3,
      r.bcid,
      (r.lumi_channel_3 > cut && r.lumi_channel_27 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      4,
      r.bcid,
      (r.lumi_channel_4 > cut && r.lumi_channel_28 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      6,
      r.bcid,
      (r.lumi_channel_6 > cut && r.lumi_channel_30 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      7,
      r.bcid,
      (r.lumi_channel_7 > cut && r.lumi_channel_31 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      8,
      r.bcid,
      (r.lumi_channel_8 > cut && r.lumi_channel_32 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      9,
      r.bcid,
      (r.lumi_channel_9 > cut && r.lumi_channel_33 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      10,
      r.bcid,
      (r.lumi_channel_10 > cut && r.lumi_channel_34 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      12,
      r.bcid,
      (r.lumi_channel_12 > cut && r.lumi_channel_36 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      13,
      r.bcid,
      (r.lumi_channel_13 > cut && r.lumi_channel_37 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      14,
      r.bcid,
      (r.lumi_channel_14 > cut && r.lumi_channel_38 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      15,
      r.bcid,
      (r.lumi_channel_15 > cut && r.lumi_channel_39 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      16,
      r.bcid,
      (r.lumi_channel_16 > cut && r.lumi_channel_40 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      18,
      r.bcid,
      (r.lumi_channel_18 > cut && r.lumi_channel_42 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      19,
      r.bcid,
      (r.lumi_channel_19 > cut && r.lumi_channel_43 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      20,
      r.bcid,
      (r.lumi_channel_20 > cut && r.lumi_channel_44 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      21,
      r.bcid,
      (r.lumi_channel_21 > cut && r.lumi_channel_45 > cut) ? 1 : 0
    );
    step_hist.add(
      r.gpsTime,
      22,
      r.bcid,
      (r.lumi_channel_22 > cut && r.lumi_channel_46 > cut) ? 1 : 0
    );


    if (
      r.lumi_channel_0 > cut && r.lumi_channel_24 > cut &&
      r.lumi_channel_6 > cut && r.lumi_channel_30 > cut &&
      r.lumi_channel_12 > cut && r.lumi_channel_36 > cut &&
      r.lumi_channel_18 > cut && r.lumi_channel_42 > cut
    ) {
      ring_48 = 1;
    }
    else {
      ring_48 = 0;
    }

    if (
      r.lumi_channel_1 > cut && r.lumi_channel_25 > cut &&
      r.lumi_channel_7 > cut && r.lumi_channel_31 > cut &&
      r.lumi_channel_13 > cut && r.lumi_channel_37 > cut &&
      r.lumi_channel_19 > cut && r.lumi_channel_43 > cut
    ) {
      ring_49 = 1;
    }
    else {
      ring_49 = 0;
    }

    if (
      r.lumi_channel_2 > cut && r.lumi_channel_26 > cut &&
      r.lumi_channel_8 > cut && r.lumi_channel_32 > cut &&
      r.lumi_channel_14 > cut && r.lumi_channel_38 > cut &&
      r.lumi_channel_20 > cut && r.lumi_channel_44 > cut
    ) {
      ring_50 = 1;
    }
    else {
      ring_50 = 0;
    }

    if (
      r.lumi_channel_3 > cut && r.lumi_channel_27 > cut &&
      r.lumi_channel_9 > cut && r.lumi_channel_33 > cut &&
      r.lumi_channel_15 > cut && r.lumi_channel_39 > cut &&
      r.lumi_channel_21 > cut && r.lumi_channel_45 > cut
    ) {
      ring_51 = 1;
    }
    else {
      ring_51 = 0;
    }

    if (
      r.lumi_channel_4 > cut && r.lumi_channel_28 > cut &&
      r.lumi_channel_10 > cut && r.lumi_channel_34 > cut &&
      r.lumi_channel_16 > cut && r.lumi_channel_40 > cut &&
      r.lumi_channel_22 > cut && r.lumi_channel_46 > cut
    ) {
      ring_52 = 1;
    }
    else {
      ring_52 = 0;
    }

    // Counters from 48 to 52 are asigned from the inner to the outer rings in PLUME.
    step_hist.add(r.gpsTime, 48, r.bcid, ring_48);
    step_hist.add(r.gpsTime, 49, r.bcid, ring_49);
    step_hist.add(r.gpsTime, 50, r.bcid, ring_50);
    step_hist.add(r.gpsTime, 51, r.bcid, ring_51);
    step_hist.add(r.gpsTime, 52, r.bcid, ring_52);

    // Counter 53 correspond to full detector

    step_hist.add(
      r.gpsTime,
      53,
      r.bcid,
      (ring_48 == 1 && ring_49 == 1 && ring_50 == 1 && ring_51 == 1 && ring_52 == 1) ? 1 : 0
    );


    if (interactive && iEntry % 10000 == 0) {
      erase_i(cerr, iEntry - 10000);
      cerr << iEntry;
    }
  }

  if (interactive) erase_i(cerr, nEntries);
  delete file;

  cout << step_hist;
  return 0;

}
