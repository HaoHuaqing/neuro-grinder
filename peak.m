clear;
num_choose = '07';
pre_str = strcat('C:\data\pro_data\s',num_choose,'\LR\');
aft_str = strcat('C:\data\pro_data\s',num_choose,'_2\LR\');
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
    max_v = max(pre_velxy);
    IniNum = find(pre_velxy > 0.1 * max_v);
    start = IniNum(1);
    pre_velxy = pre_velxy(start-200:start+1300);
    peak_v = cat(1, peak_v, max_v);
    h1 = plot(pre_velxy,'Color',[0 0 1]);
    hold on
end
title('velxy','FontSize',20)
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
    max_v = max(aft_velxy);
    IniNum = find(aft_velxy > 0.1 * max_v);
    start = IniNum(1);
    aft_velxy = aft_velxy(start-200:start+1300);
    peak_v = cat(1, peak_v, max_v);
    h2 = plot(aft_velxy,'Color',[1 0 0]);
    hold on
end
h = legend([h1,h2],'PRE', 'AFT');
set(h,'Fontsize',20);



pre_str = 'C:\data\pro_data\s07\FR\';
aft_str = 'C:\data\pro_data\s07_2\FR\';
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
    max_v = max(pre_velxy);
    IniNum = find(pre_velxy > 0.1 * max_v);
    start = IniNum(1);
    pre_velxy = pre_velxy(start-200:start+1300);
    peak_v = cat(1, peak_v, max_v);
    h1 = plot(pre_velxy,'Color',[0 0 1]);
    hold on
end
title('velxy','FontSize',20)
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
    max_v = max(aft_velxy);
    IniNum = find(aft_velxy > 0.1 * max_v);
    start = IniNum(1);
    aft_velxy = aft_velxy(start-200:start+1300);
    peak_v = cat(1, peak_v, max_v);
    h2 = plot(aft_velxy,'Color',[1 0 0]);
    hold on
end
h = legend([h1,h2],'PRE', 'AFT');
set(h,'Fontsize',20);
