function [EMG_bp,EMG_rt,EMG_lp_20,EMG_lp_6] = EMG_Process( originEMG,trignum_e, fs, state)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

%EMG bandstop
    star  = - 0.6;
    stop  = - 0.1;
    
    
    switch state                  % time before trigger as steady state;  2 % time  of initial state
        case 1
             EMG_NoBias                = originEMG - mean(originEMG(trignum_e + fs * star : trignum_e + fs * stop));
        case 2
             EMG_NoBias                = originEMG - mean(originEMG( -fs * stop : - fs * star));
    end
    
    a                         = Filter_BandStop(50,EMG_NoBias,fs);
for ratio1=2:1:9
    b                         = Filter_BandStop(50*ratio1,a,fs);
    a                         = b;
end

for ratio2=1:1:4
    EMG_bs                    = Filter_BandStop(120*ratio2,b,fs);
    b                         = EMG_bs;
end

%EMG bandpass
    EMG_bp                     = Filter_BandPass(20,400,EMG_bs,fs);
    EMG_bp(1:200)             = [0];
    EMG_bp(end-200:end)       = [0];
    
%EMG rectify
    EMG_rt=abs(EMG_bp);
    
%EMG lowpass
%     EMG_lp_50                  = Filter_LowPass(EMG_rt,40,50,fs);
%     EMG_lp_50(1:200)          = [0];
%     EMG_lp_50(end-200:end)    = [0];

    EMG_lp_20                  = Filter_LowPass(EMG_rt,20,30,fs);
    EMG_lp_20(1:200,:)          = 0;
    EMG_lp_20(end-200:end,:)    = 0;
    
    EMG_lp_6                   = Filter_LowPass(EMG_rt,5,6,fs);
    EMG_lp_6(1:200,:)           = 0;
    EMG_lp_6(end-200:end,:)     = 0;
    
    clear a;clear b;
end

