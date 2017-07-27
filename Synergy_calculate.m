clear;
num_choose = '11';
LR_FR = '\LR\';
Files = dir(strcat('C:\data\pro_data2\s',num_choose,LR_FR));
LengthFiles = length(Files);
fs=1000;
mid=400;
emgnum=7;
EMGMatrix = [];
for i = 3:LengthFiles;
    data = csvread(strcat('C:\data\pro_data2\s',num_choose,LR_FR,Files(i).name),1,1);
    x=data(:,20);
    y=data(:,21);
    diffx = diff(Filter_LowPass(x,10,20,fs));
    diffy = diff(Filter_LowPass(y,10,20,fs));
    velxy = sqrt((diffx.^2+diffy.^2))*fs;
    [max_v,position] = max(velxy);
    mid_velxy = velxy(position-mid:length(velxy));
    IniNum = find(mid_velxy > 0.1 * max_v);
    start = IniNum(1);
    EMG = data(position-700+start:position+900+start,1:7);
    EMG_p(:,1) = EMG(:,5);
    EMG_p(:,2) = EMG(:,7);
    EMG_p(:,3) = EMG(:,6);
    EMG_p(:,4) = EMG(:,4);
    EMG_p(:,5) = EMG(:,2);
    EMG_p(:,6) = EMG(:,3);
    EMG_p(:,7) = EMG(:,1);
    [EMG_bp,EMG_rt,EMG_lp_20,EMG_lp_6] = EMG_Process(1000*EMG_p,100, 1000, 2);
    EMGMatrix = cat(1, EMGMatrix, EMG_lp_20);
end
for k = 1:1:emgnum
    [Synergy_S(1,k)] = NNMF_Sync(abs(EMGMatrix),k);
end

