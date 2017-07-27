clear;
num_choose = '16';
pre_str = strcat('C:\data\pro_data2\s',num_choose,'\LR\');
aft_str = strcat('C:\data\pro_data2\s',num_choose,'_2\LR\');
Files = dir(pre_str);
LengthFiles = length(Files);
fs=1000;
emgnum=7;
peak_v = [];
mid = 400;
figure;
for i = 3:LengthFiles;
    data = csvread(strcat(pre_str,Files(i).name),1,1);
    x=data(:,20);
    y=data(:,21);
    diffx = diff(Filter_LowPass(x,10,20,fs));
    diffy = diff(Filter_LowPass(y,10,20,fs));
    pre_velxy = sqrt((diffx.^2+diffy.^2))*fs;
    [max_v,position] = max(pre_velxy(1:length(pre_velxy)-500));
    mid_velxy = pre_velxy(position-mid:length(pre_velxy));
    IniNum = find(mid_velxy > 0.1 * max_v);
    start = IniNum(1);
    pre_velxy = pre_velxy(position-700+start:position+900+start);
    peak_v = cat(1, peak_v, max_v);
    h1 = plot(pre_velxy,'Color',[0 0 1]);
    hold on
end
LR_title = strcat('Subject ',num_choose, 'LR Velocity');
title(LR_title,'FontSize',20)
ylim([0,2])
% legend({'trial1','trial2','trial3','trial4','trial5','trial6','trial7','trial8','trial9','trial10'},'FontSize',20)
% csvwrite('s20_pre_lr_pkvel.csv',peak_v)
% disp(length(peak_v))
Files = dir(aft_str);
LengthFiles = length(Files);
fs=1000;
emgnum=7;
peak_v = [];
for i = 3:LengthFiles;
    data = csvread(strcat(aft_str,Files(i).name),1,1);
    x=data(:,20);
    y=data(:,21);
    diffx = diff(Filter_LowPass(x,10,20,fs));
    diffy = diff(Filter_LowPass(y,10,20,fs));
    aft_velxy = sqrt((diffx.^2+diffy.^2))*fs;
    [max_v,position] = max(aft_velxy);
    mid_velxy = aft_velxy(position-mid:length(aft_velxy));
    IniNum = find(mid_velxy > 0.1 * max_v);
    start = IniNum(1);
    aft_velxy = aft_velxy(position-700+start:position+900+start);
    peak_v = cat(1, peak_v, max_v);
    h2 = plot(aft_velxy,'Color',[1 0 0]);
    hold on
end
h = legend([h1,h2],'PRE', 'AFT');
set(h,'Fontsize',20);



pre_str = strcat('C:\data\pro_data2\s',num_choose,'\FR\');
aft_str = strcat('C:\data\pro_data2\s',num_choose,'_2\FR\');
Files = dir(pre_str);
LengthFiles = length(Files);
fs=1000;
emgnum=7;
peak_v = [];
figure;
for i = 3:LengthFiles;
    data = csvread(strcat(pre_str,Files(i).name),1,1);
    x=data(:,20);
    y=data(:,21);
    diffx = diff(Filter_LowPass(x,10,20,fs));
    diffy = diff(Filter_LowPass(y,10,20,fs));
    pre_velxy = sqrt((diffx.^2+diffy.^2))*fs;
    [max_v,position] = max(pre_velxy);
    mid_velxy = pre_velxy(position-mid:length(pre_velxy));
    IniNum = find(mid_velxy > 0.1 * max_v);
    start = IniNum(1);
    pre_velxy = pre_velxy(position-700+start:position+900+start);
    peak_v = cat(1, peak_v, max_v);
    h1 = plot(pre_velxy,'Color',[0 0 1]);
    hold on
end
FR_title = strcat('Subject ',num_choose, 'FR Velocity');
title(FR_title,'FontSize',20)
ylim([0,2])
% legend({'trial1','trial2','trial3','trial4','trial5','trial6','trial7','trial8','trial9','trial10'},'FontSize',20)
% csvwrite('s20_pre_lr_pkvel.csv',peak_v)
% disp(length(peak_v))
Files = dir(aft_str);
LengthFiles = length(Files);
fs=1000;
emgnum=7;
peak_v = [];
for i = 3:LengthFiles;
    data = csvread(strcat(aft_str,Files(i).name),1,1);
    x=data(:,20);
    y=data(:,21);
    diffx = diff(Filter_LowPass(x,10,20,fs));
    diffy = diff(Filter_LowPass(y,10,20,fs));
    aft_velxy = sqrt((diffx.^2+diffy.^2))*fs;
    [max_v,position] = max(aft_velxy);
    mid_velxy = aft_velxy(position-mid:length(aft_velxy));
    IniNum = find(mid_velxy > 0.1 * max_v);
    start = IniNum(1);
    aft_velxy = aft_velxy(position-700+start:position+900+start);
    peak_v = cat(1, peak_v, max_v);
    h2 = plot(aft_velxy,'Color',[1 0 0]);
    hold on
end
h = legend([h1,h2],'PRE', 'AFT');
set(h,'Fontsize',20);
