%plot subjects
clear;
num_choose = '10_2';
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

average_2 = 0;
average_4 = 0;
for i = 1:LengthFiles-2;
    subplot(2,2,2)
    plot(Synergy_S(2).C(1600*(i-1)+1:1600*i,1),'Color',[96 96 96]/255);
    hold on
    subplot(2,2,4)
    plot(Synergy_S(2).C(1600*(i-1)+1:1600*i,end),'Color',[96 96 96]/255);
    hold on
    average_2 = average_2 + Synergy_S(2).C(1600*(i-1)+1:1600*i,1);
    average_4 = average_4 + Synergy_S(2).C(1600*(i-1)+1:1600*i,end);
end
subplot(2,2,1)
bar(Synergy_S(2).U(1,:),'y','Horizontal','on')
name = {'Tlt', 'BR', 'Tlh', 'BI','DP', 'DA', 'PC'};
set(gca, 'YTickLabel', name);
subplot(2,2,3)
bar(Synergy_S(2).U(end,:),'y','Horizontal','on')
set(gca, 'YTickLabel', name);
subplot(2,2,2)
plot(average_2/(LengthFiles-2),'Color',[1 0 0], 'LineWidth',4)
subplot(2,2,4)
plot(average_4/(LengthFiles-2),'Color',[1 0 0], 'LineWidth',4)
h = suptitle('S10 LR AFT');
set(h,'Fontsize',30);