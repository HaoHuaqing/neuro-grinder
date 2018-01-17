%% initial load
clear ;
clc;
close all;
type = 'Subject'; 
cd  (['X:\Synergy_Analysis\NewSubject\Synergy_Kine_Analysis\Result']);

EXP = '2';  
comp(1,1) = 3;
comp(1,2) = 4;
emgnum = 7;
load (['SynergySimilarity_Output_EXP' EXP '.mat']);
for sub = 16
                    % 1 首评     %　2 尾评     % 3 二次入组首评    %  4 二次入组尾评
            if sub >= 10
            synmat = ['Syn_Peak_Sync_' type '_' num2str(sub) '_EXP' EXP '.mat'];
            else
                synmat = ['Syn_Peak_Sync_' type '_0' num2str(sub) '_EXP' EXP '.mat'];
            end
             load (synmat);
             cd .. 
             
       %%%%%%%%
       for task = 1:2

          
          switch task 
              case 1
                        colo = [226/255 175/255 45/255;
                                119/255 181/255 53/255;
                                217/255 113/255 110/255];
         
                        input = figure;

                        xSize_i  = 6;   % 图片宽,英寸
                        ySize_i  = 3; % 高,英寸
                        xLeft_i  = 3;
                        yTop_i   = 3;
                        set(input, 'Units', 'inches');  %  'centimeters'
                        set(input, 'Position', [xLeft_i yTop_i xSize_i ySize_i]);
                        set(input, 'PaperUnits', 'inches');  %  'centimeters'
                        set(input, 'PaperPosition', [xLeft_i yTop_i xSize_i ySize_i]);

                        Position(1:2*comp(1,task),1:4) = [0.05 0.1  0.12 0.7;
                                                          0.21 0.1  0.12 0.7;
                                                          0.37 0.1  0.12 0.7;
                                                          0.6 0.67  0.35 0.13;
                                                          0.6 0.385 0.35 0.13;
                                                          0.6 0.1   0.35 0.13];
                            
              case 2
                       colo = [204/255 0/255   0/255;
                               173/255 119/255 8/255;
                               0/255   127/255 0/255;
                               0/255   0/255 250/255]; % colo of template (H01)
                           
                        input = figure;
                        xSize_i  = 7.2;   % 图片宽,英寸
                        ySize_i  = 3; % 高,英寸
                        xLeft_i  = 3;
                        yTop_i   = 3;
                        set(input, 'Units', 'inches');  %  'centimeters'
                        set(input, 'Position', [xLeft_i yTop_i xSize_i ySize_i]);
                        set(input, 'PaperUnits', 'inches');  %  'centimeters'
                        set(input, 'PaperPosition', [xLeft_i yTop_i xSize_i ySize_i]);
                         
                        Position(1:2*comp(1,task),1:4) = [0.05 0.1  0.1 0.7;
                                                          0.185 0.1  0.1 0.7;
                                                          0.32 0.1  0.1 0.7;
                                                          0.455 0.1  0.1 0.7;
                                                          0.65 0.67  7/24 0.13;
                                                          0.65 0.48  7/24 0.13;
                                                          0.65 0.29 7/24 0.13;
                                                          0.65 0.1  7/24 0.13];

          end
                        for row = 1:comp(1,task)
                             subplot('position',Position(row,:));
                             h1 = barh(Synergy_Sync(task,comp(1,task)).U(row,emgnum:-1:1),'FaceColor',colo(Syne_Subj{sub,task}.MatchNum(1,row),:),'EdgeColor',colo(Syne_Subj{sub,task}.MatchNum(1,row),:),'LineWidth',1);
%                              set(get(h1(1),'BaseLine'),'Visible','off');
                             set(gca, 'YTick',[],'XTick',[0 1],'FontSize',9);     
                             xlim([0 1]);
                             ylim([0.5 emgnum+0.41]);
                             titlestr = [num2str(round(Syne_Subj{sub,task}.MatchSimi_V(1,row)*100)/100) ' (' num2str(Syne_Subj{sub,task}.MatchNum(1,row)) ')'];
                             title(titlestr);
                        end
                        
                        for column = 1:comp(1,task)
                             subplot('position',Position(column+comp(1,task),:));
                             C_xlim = max(max(Syne_Subj{sub,task}.C_ave));
                             area(Syne_Subj{sub,task}.C_ave(:,column),'FaceColor',colo(Syne_Subj{sub,task}.MatchNum(1,column),:),'EdgeColor',colo(Syne_Subj{sub,task}.MatchNum(1,column),:),'LineWidth',1);
                             set(gca, 'YTick',[],'XTick',[0 1000],'FontSize',9);  
                             ylim([0 C_xlim*1.1]);
                             titlestr = [num2str(round(Syne_Subj{sub,task}.MatchSimi_T(1,column)*100)/100) ' (' num2str(Syne_Subj{sub,task}.MatchNum(1,column)) ')'];
                             title(titlestr);
                        end
                        
                          annotation('textbox',...
                          [0.40 0.88 0.10 0.10],...
                          'String',{['Subj ' num2str(sub) ' Task ' num2str(task) ' EXP ' num2str(EXP)]}','LineStyle','none');
                      
            cd  (['X:\Synergy_Analysis\NewSubject\Synergy_Kine_Analysis\Result']);
            s = ['Subj ' num2str(sub) ' Task ' num2str(task) ' EXP ' num2str(EXP)];
            print(gcf,'-dbmp',s);
            cd ..
            
       end
end

%% DRAW TEMPLATE OF H01
% initial load
clear;
clc;
close all;

cd  (['X:\Synergy_Analysis\NewSubject\Synergy_Kine_Analysis\Result']);
load('Vel10perc_Syn_LR_4_C_ave_Control_01.mat'); % 与H01对比

comp (1,1) = 3; %两个task的synergy个数
comp (1,2) = 4;

point = 1000;   % synergy序列一个trial的点个数
emgnum = 7;    

       %%%%%%%%
       for task = 1:2

          
          switch task 
              case 1
                        colo = [226/255 175/255 45/255;
                                119/255 181/255 53/255;
                                217/255 113/255 110/255];      
         
                        input = figure;

                        xSize_i  = 6;   % 图片宽,英寸
                        ySize_i  = 3; % 高,英寸
                        xLeft_i  = 3;
                        yTop_i   = 3;
                        set(input, 'Units', 'inches');  %  'centimeters'
                        set(input, 'Position', [xLeft_i yTop_i xSize_i ySize_i]);
                        set(input, 'PaperUnits', 'inches');  %  'centimeters'
                        set(input, 'PaperPosition', [xLeft_i yTop_i xSize_i ySize_i]);

                        Position(1:2*comp(1,task),1:4) = [0.05 0.1  0.12 0.7;
                                                          0.21 0.1  0.12 0.7;
                                                          0.37 0.1  0.12 0.7;
                                                          0.6 0.67  0.35 0.13;
                                                          0.6 0.385 0.35 0.13;
                                                          0.6 0.1   0.35 0.13];
                            
              case 2
                       colo = [204/255 0/255   0/255;
                               173/255 119/255 8/255;
                               0/255   127/255 0/255;
                               0/255   0/255 250/255]; % colo of template (H01)
                        input = figure;
                        xSize_i  = 7.2;   % 图片宽,英寸
                        ySize_i  = 3; % 高,英寸
                        xLeft_i  = 3;
                        yTop_i   = 3;
                        set(input, 'Units', 'inches');  %  'centimeters'
                        set(input, 'Position', [xLeft_i yTop_i xSize_i ySize_i]);
                        set(input, 'PaperUnits', 'inches');  %  'centimeters'
                        set(input, 'PaperPosition', [xLeft_i yTop_i xSize_i ySize_i]);
                         
                        Position(1:2*comp(1,task),1:4) = [0.05 0.1  0.1 0.7;
                                                          0.185 0.1  0.1 0.7;
                                                          0.32 0.1  0.1 0.7;
                                                          0.455 0.1  0.1 0.7;
                                                          0.65 0.67  7/24 0.13;
                                                          0.65 0.48  7/24 0.13;
                                                          0.65 0.29 7/24 0.13;
                                                          0.65 0.1  7/24 0.13];

          end
                        for row = 1:comp(1,task)
                             subplot('position',Position(row,:));
                             h1 = barh(Synergy_Sync(task,comp(1,task)).U(row,emgnum:-1:1),'FaceColor',colo(row,:),'EdgeColor',colo(row,:),'LineWidth',1);
%                              set(get(h1(1),'BaseLine'),'Visible','off');
                             set(gca, 'YTick',[],'XTick',[0 1],'FontSize',9);     
                             xlim([0 1]);
                             ylim([0.5 emgnum+0.41]);
                             titlestr = ['V' num2str(row)];
                             title(titlestr);
                        end
                        
                        for column = 1:comp(1,task)
                             subplot('position',Position(column+comp(1,task),:));
                             C_xlim = max(max(Synergy_Sync(task, comp(1,task)).C_ave));
                             area(Synergy_Sync(task, comp(1,task)).C_ave(:,column),'FaceColor',colo(column,:),'EdgeColor',colo(column,:),'LineWidth',1);
                             set(gca, 'YTick',[],'XTick',[0 1000],'FontSize',9);  
                             ylim([0 C_xlim*1.1]);
                             titlestr = ['T' num2str(column)];
                             title(titlestr);
                        end
                        
                          annotation('textbox',...
                          [0.40 0.88 0.10 0.10],...
                          'String',{['HealthyControl H01 Task ' num2str(task) ]}','LineStyle','none');
           
       
end