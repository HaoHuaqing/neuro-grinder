%%
clc;
clear;
cd  (['D:\Data\HaoHQ\synergy']);
S1 = load('Syn_Peak_Sync_Subject_16_EXP1.mat'); 
S2 = load('Syn_Peak_Sync_Subject_16_EXP2.mat'); 
Synergy_Sync = cat(1, S1.Synergy_Sync, S2.Synergy_S);
save(['Syn_Peak_Sync_Subject_16_EXP1_Hao.mat'],'Synergy_Sync'); 
cd .. 

%% output VAF
clear ;
clc;
type = 'Subject';
for sub = 16
        EXP = '1';              % 1 首评     %　2 尾评     % 3 二次入组首评    %  4 二次入组尾评
            if sub >= 10
            synmat = ['Syn_Peak_Sync_' type '_' num2str(sub) '_EXP' EXP '_Hao.mat'];
            else
                synmat = ['Syn_Peak_Sync_' type '_0' num2str(sub) '_EXP' EXP '_Hao.mat'];
            end
            cd  (['D:\Data\HaoHQ\synergy']);
            load (synmat);
 
        for task = 1:2 
                if type == 'Control'
                    for comp = 1:1:7
                     Syne_Cont{sub,task}.VAF(1,comp) = Synergy_Sync(task, comp).VAF;
                    end

                else
                    for comp = 1:1:7
                     Syne_Subj{sub,task}.VAF(1,comp) = Synergy_Sync(task, comp).VAF;
                    end

                end


        end
end

 save(['SynergySimilarity_Output_EXP' EXP '.mat'],'Syne_Subj'); 
 cd .. 
%% calculate similarity
clc;
cd  (['D:\Data\HaoHQ\synergy']);
 
load('Vel10perc_Syn_LR_4_C_ave_Control_01.mat'); % 与H01对比
Syn_H01 = Synergy_Sync;
clear Synergy_Sync;

comp (1,1) = 3; %两个task的synergy个数
comp (1,2) = 4;

point = 1000;   % synergy序列一个trial的点个数

type = 'Subject';
for sub = 16
        EXP = '1';              % 1 首评     %　2 尾评     % 3 二次入组首评    %  4 二次入组尾评
            if sub >= 10
                 synmat = ['Syn_Peak_Sync_' type '_' num2str(sub) '_EXP' EXP '_Hao.mat'];
            else 
                 synmat = ['Syn_Peak_Sync_' type '_0' num2str(sub) '_EXP' EXP '_Hao.mat'];
            end
            load (synmat);
            Syn_Each = Synergy_Sync;

for task = 1:1:2
            k_H01 = comp(1,task);
            k_Each = comp(1,task);  
    
     %%%%%%%%%% simi of vector (before weighted by lamda)
            
            for k1 = 1:1:k_H01
                for k2 = 1:1:k_Each
                    Matrix_V(k1,k2) = sum(Syn_H01(task, k_H01).U(k1,:).* Syn_Each(task, k_Each).U(k2,:))/(norm(Syn_H01(task, k_H01).U(k1,:))*norm(Syn_Each(task, k_Each).U(k2,:)));
                end
            end
                    for nn = 1:1:k_Each
                        [simi num] = max(Matrix_V(:,nn));
                        Syne_Subj{sub,task}.MatchNum(1,nn) = num;
                        Syne_Subj{sub,task}.MatchSimi_V(1,nn) = simi;
                    end

    %%%%%%%%%% simi of time profile (before weighted by lamda)  
            % step 1:get the average of time profile from all trials

                        tranum = len_trial(task);
                        for column = 1:1:comp(1,task)
                            for chan = 1:1:point
                                for tra = 1:1:tranum
                                    C_chan(chan,tra) = Synergy_Sync(task,comp(1,task)).C((tra-1)*point+chan,column);
                                end
                                C_ave(chan,column) = mean(C_chan(chan,:));
                            end
                        end
                            Syne_Subj{sub,task}.C_ave = C_ave;
                    
             %%step 2:calculate simi of averaged similarity    
            for k1 = 1:1:k_H01
                for k2 = 1:1:k_Each
                    Matrix_T(k1,k2) = sum(Syn_H01(task, k_H01).C_ave(:,k1).* Syne_Subj{sub,task}.C_ave(:,k2))/(norm(Syn_H01(task, k_H01).C_ave(:,k1))*norm(Syne_Subj{sub,task}.C_ave(:,k2)));
                end
            end
                    for nn = 1:1:k_Each
                       Syne_Subj{sub,task}.MatchSimi_T(1,nn) =  Matrix_T(Syne_Subj{sub,task}.MatchNum(1,nn),nn);   % Matchnumber decided by V
                    end
                    
   %%%%%%%%%%%%%%%%%%%%%%%% get contribution of time profile form C_ave
     % contribution of eigen value
            Eigen   = zeros(1,comp(1,task));
            Contrib = zeros(1,comp(1,task));
            X       = Syne_Subj{sub,task}.C_ave;
            [coeff,score,latent]    = pca(X);
            Eigen(1,1:comp(1,task)) = latent;
            SUM     = sum(Eigen(1,1:comp(1,task)));
            for nn  = 1:comp(1,task)
                Syne_Subj{sub,task}.Contrib(1,nn) = Eigen(1,nn)/SUM;
            end
      % weighted similarity (= simi of Li et al., 2017)
            Syne_Subj{sub,task}.SV = sum(Syne_Subj{sub,task}.MatchSimi_V .* Syne_Subj{sub,task}.Contrib);
            Syne_Subj{sub,task}.ST = sum(Syne_Subj{sub,task}.MatchSimi_T .* Syne_Subj{sub,task}.Contrib);
            Syne_Subj{sub,task}.SCOM = 0.5 * (Syne_Subj{sub,task}.SV + Syne_Subj{sub,task}.ST);
end
end
%%
cd  (['D:\Data\HaoHQ\result']);
save(['SynergySimilarity_Output_EXP' EXP '_Hao.mat'],'Syne_Subj'); 
cd ..
%% save to excel
clc; close all;clear all;
EXP = '1';
cd  (['D:\Data\HaoHQ\result']);
load(['SynergySimilarity_Output_EXP' EXP '_Hao.mat']);
filename = (['SynergySimilarity_Output_EXP' EXP '_Hao.xlsx']);
% group = 'Control';
  group = 'Subject';
comp (1,1) = 3; %两个task的synergy个数
comp (1,2) = 4;

  for sub = 16     
      for task = 1:2
        % export
        sheet = ['Task' num2str(task)'];
        SUBlist = ['BCDEFGHIJKLMNOPQRSTUVWXYZ'];
        xlRange = [SUBlist(sub-3)];
        data=[sub';task';comp(1,task)';Syne_Subj{sub,task}.VAF(1,comp(1,task))';Syne_Subj{sub,task}.SV';Syne_Subj{sub,task}.ST'';Syne_Subj{sub,task}.SCOM'';];
        [m,n]=size(data);
        data_cell = mat2cell(data, ones(m,1), ones(n,1));    
        title = {'sub';'task';'COMP';'VAF';'SV';'ST';'SCOM'};     
%         result= [title, data_cell];    % 第一次输出时需要titile,后面无需
        result= [data_cell];   
        xlswrite(filename,result,sheet,xlRange);
      end
    end