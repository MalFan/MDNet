%DEMO_TRACKING
%
% Running the MDNet tracker on a given sequence.
%
% Hyeonseob Nam, 2015
%

setup_mdnet;

clear;

datasetName = '92-2';
seqList = {'92-2-1','92-2-2','92-2-4','92-2-5','92-2-6','92-2-7','92-2-8','92-2-9','92-2-10','92-2-11'}
% seqList = {'92-2-2'}
% seqList = {'92-2-1','92-2-4','92-2-5','92-2-6','92-2-7','92-2-8','92-2-9','92-2-10','92-2-11'}
% seqList = {'92-2-1','92-2-4'}


for i = 1:length(seqList)
    seqName = seqList{i}

    conf = genConfig('92-2', seqName);
% conf = genConfig('vot2015','ball1');

    switch(conf.dataset)
        case {'otb','92-2'}
            net = fullfile('models','mdnet_vot-otb.mat');
        case 'vot2014'
            net = fullfile('models','mdnet_otb-vot14.mat');
        case 'vot2015'
            net = fullfile('models','mdnet_otb-vot15.mat');
    end

    [result, fsa_seq_str, init_pos_examples, init_neg_examples, total_pos_examples, total_neg_examples] = mdnet_run(conf.imgList, conf.gt(1,:), net);
    
    
    save_examples(conf.imgList, datasetName, seqName, init_pos_examples, init_neg_examples, total_pos_examples, total_neg_examples);

    % mkdir(fullfile('result', datasetName, seqName))

    % csvwrite(fullfile('result', datasetName, seqName, sprintf('result_mdnet_%s.txt', seqName)), result)
    
    % fileID = fopen(fullfile('result', datasetName, seqName, sprintf('fsa_seq_mdnet_%s.txt', seqName)),'w');
    % fprintf(fileID, fsa_seq_str);
    % fclose(fileID);    

end

% close all;
% save_result_seq(datasetName);
