 function [Synergy] = NNMF_Sync(EMG,k)


opt1        =	statset('MaxIter',100000,'Display','final', 'TolX', 1e-5,'TolFun', 1e-5);
[C1,U1]     =	nnmf(EMG,k,'replicates',25, 'options',opt1, 'algorithm','mult');

opt2        =	statset('MaxIter',100000,'Display','iter', 'TolX', 1e-5,'TolFun', 1e-5);
[C2,U2]     =	nnmf(EMG,k,'w0',C1,'h0',U1, 'options',opt2, 'algorithm','als');

Synergy.C   =   C2;
Synergy.U   =   U2;
Synergy.D   =   C2 * U2;
Synergy.EMG =   EMG;

Synergy.VAF =   Var_AF(EMG,Synergy);


 


 end

