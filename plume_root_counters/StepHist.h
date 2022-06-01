#ifndef StepHist_h
#define StepHist_h 1

#include <vector>
#include <map>
#include <set>
#include <iostream>
#include <climits>
#include <cmath>
#include <iomanip> // for setprecision

using namespace std;

struct Hist : public map<unsigned int, unsigned int> { // histogram: (*this)[bin] = content
  friend ostream& operator<<(ostream& os, const Hist& h);
};
struct BX : public map<unsigned int, Hist> { // [bxID][bin]
};
struct Counter : public map<unsigned int, BX> { // [i_lumiCounter][bxID][bin]
  unsigned long long tmin;
};
struct StepHist : public map<unsigned long long, Counter> { // [tmax][i_Counter][bxID][bin],
  //  i_Counter =  0     1       2        3     4     6     7      8    11     14     106
  //  name      = PU  RZVelo  RZVeloBW  Velo  Muon  SPD  CaloEt  TTIP  PV3D  Vertex  SPD+CaloEt
  // bxID=0 means all empty-empty, bxID<0 all be,eb
  //
  // Initialize from the file describing the step timing with the format
  // tmin1 tmax1
  // tmin2 tmax2
  // ...
  // where all tmin/tmax are gps from ODIN bank, ie. UNIX time in microseconds (64 bit)
  StepHist(istream& is);
  // print the results in the format
  // tmin1 tmax1 counter1 bxID1 bin1 content1
  // ...
  friend ostream& operator<<(ostream& os, const StepHist& s);
  // if "time" is in one of the step periods, add "value" to the histogram of
  // the "counter", "bxID"
  void add(unsigned long long time, unsigned int counter, unsigned int bxID, unsigned int value);
};

StepHist::StepHist(istream& is) {
  long double tmin, tmax; // accept in fractional UNIX seconds but store in integer microseconds
  while (is >> tmin >> tmax) (*this)[(unsigned long long)(tmax * 1e6)].tmin = (unsigned long long)(tmin * 1e6);
}
void StepHist::add(unsigned long long time, unsigned int counter, unsigned int bxID, unsigned int value) {
  // lower_bound name is misleading: "it" will point to the first tmax for which time <= tmax,
  // ie. lower_bound == the lowest among "upper" (greater or equal) bounds
  auto it = lower_bound(time);
  if (it != end() && it->second.tmin <= time) // finally accept iff tmin<=time<=tmax
    ++it->second[counter][bxID][value];  // automatically create all non-existing map elements
}
inline ostream& operator<<(ostream& os, const StepHist& s) {
  // format: "tmin counter bx bin value"
  for (const auto& step : s)
    for (const auto& counter : step.second)
      for (const auto& bx : counter.second) {
	for (const auto& bin : bx.second)
	  os << ' ' << fixed << setprecision(6) << step.second.tmin / (long double)(1e6) // back to UNIX sec
	     << ' ' << counter.first << ' ' // note ' ' in front
	     << bx.first << ' ' << bin.first << ' ' << bin.second << '\n';
      }
  return os;
}

#endif
