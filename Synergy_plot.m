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
subplot(2,2,3)
bar(Synergy_S(2).U(end,:),'y','Horizontal','on')
subplot(2,2,2)
plot(average_2/(LengthFiles-2),'Color',[1 0 0], 'LineWidth',4)
subplot(2,2,4)
plot(average_4/(LengthFiles-2),'Color',[1 0 0], 'LineWidth',4)
h = suptitle('S11 LR PRE');
set(h,'Fontsize',30);