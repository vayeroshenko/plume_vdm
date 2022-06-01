step_hist : StepHist.h StepHist_main.C
	g++ StepHist_main.C -std=c++17 -I. -O3 \
            -I`root-config --incdir` `root-config --libs` -lz -o step_hist

clean: 
	rm step_hist

# at lxplus c++17 is not supported by default, otherwise one can use instead:
#	g++ StepHist_main.C -std=c++17 -I. -O3 \
