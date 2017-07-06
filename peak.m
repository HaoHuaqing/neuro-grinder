clear;
Files = dir(strcat('C:\code\EEG_Motion\pro_data\s07\LR'));
LengthFiles = length(Files);
fs=1000;
emgnum=7;
peak_v = [];
for i = 3:LengthFiles;
    data = csvread(strcat('C:\code\EEG_Motion\pro_data\s07\LR\',Files(i).name),1,1);
    x=data(:,20);
    y=data(:,21);
    diffx = diff(Filter_LowPass(x,10,20,fs));
    diffy = diff(Filter_LowPass(y,10,20,fs));
    velxy = sqrt((diffx.^2+diffy.^2))*fs;
    max_v = max(velxy);
    peak_v = cat(1, peak_v, max_v);
    plot(velxy,'linewidth',2)
    hold on
end
% title('velxy','FontSize',20)
% legend({'trial1','trial2','trial3','trial4','trial5','trial6','trial7','trial8','trial9','trial10'},'FontSize',20)
csvwrite('s07_pre_lr_pkvel.csv',peak_v)
disp(length(peak_v))