function [] = save_result_seq( datasetName )
    datasetName
    switch(datasetName)
        case '92-2'
            seqList = {'92-2-1','92-2-2','92-2-4','92-2-5','92-2-6','92-2-7','92-2-8','92-2-9','92-2-10','92-2-11'}
        case 'otb'
            fileID = fopen('tb_100.txt', 'r');
            seqList = textscan(fileID, '%s');
            fclose(fileID);
            seqList = seqList{1};
    end

    for seqIdx = 1:length(seqList) 

        
        seqName = seqList{seqIdx};
        conf = genConfig(datasetName, seqName);
        images = conf.imgList;

        nFrames = length(images);

        bbox_tracking_result = csvread(fullfile('result', datasetName, seqName, sprintf('result_mdnet_%s.txt', seqName)));
        % bbox_groundtruth = csvread(fullfile('dataset', datasetName, seqName, 'groundtruth_rect.txt'));
        bbox_groundtruth = conf.gt;

        fileID = fopen(fullfile('result', datasetName, seqName,sprintf('fsa_seq_mdnet_%s.txt', seqName)), 'r');
        fsa_seq_result = textscan(fileID, '%s');
        fclose(fileID);
        fsa_seq_result = fsa_seq_result{1};
        
        % % First frame
        figure(1);
        set(gcf,'Position',[200 100 600 400],'MenuBar','none','ToolBar','none');
        
        img = imread(images{1});
        hd = imshow(img,'initialmagnification','fit'); hold on;
        % rectangle('Position', bbox_tracking_result(1,:), 'EdgeColor', [1 0 0], 'Linewidth', 3);
        rectangle('Position', bbox_groundtruth(1,:), 'EdgeColor', [0 1 0], 'Linewidth', 3);
        set(gca,'position',[0 0 1 1]);
        
        text(10,20,fsa_seq_result{1},'Color','r', 'HorizontalAlignment', 'left', 'FontWeight', 'bold', 'FontSize', 20, 'Interpreter', 'none'); 
        hold off;
        drawnow;

        % Frame to img, then imwrite
        f = getframe(gca);
        [X, map] = frame2im(f);

        mkdir(fullfile('result', datasetName, seqName, 'img_w_bbox'))

        img_name = strsplit(images{1}, '/');
        img_name = img_name(end);
        img_name = img_name{1};
        img_name_idx = strsplit(img_name, '.');
        img_name_idx = img_name_idx(1);
        img_name_idx = img_name_idx{1};
        imwrite(X, fullfile('result', datasetName, seqName, 'img_w_bbox', sprintf('%04d.png', int32(str2num(img_name_idx)))), 'png')


        % The rest frames
        for To = 2:nFrames
            sprintf('%d/%d', To, nFrames)

            img = imread(images{To});

            hc = get(gca, 'Children');
            delete(hc(1:end-1));
            set(hd,'cdata',img); 
            hold on;
            
            rectangle('Position', bbox_tracking_result(To,:), 'EdgeColor', [1 0 0], 'Linewidth', 3);
            rectangle('Position', bbox_groundtruth(To,:), 'EdgeColor', [0 1 0], 'Linewidth', 3);
            set(gca,'position',[0 0 1 1]);
            
            text(10,20,fsa_seq_result{To},'Color','r', 'HorizontalAlignment', 'left', 'FontWeight', 'bold', 'FontSize', 20, 'Interpreter', 'none'); 
            hold off;
            drawnow;

            % Frame to img, then imwrite
            f = getframe(gca);
            [X, map] = frame2im(f);

            img_name = strsplit(images{To}, '/');
            img_name = img_name(end);
            img_name = img_name{1};
            img_name_idx = strsplit(img_name, '.');
            img_name_idx = img_name_idx(1);
            img_name_idx = img_name_idx{1};
            imwrite(X, fullfile('result', datasetName, seqName, 'img_w_bbox', sprintf('%04d.png', int32(str2num(img_name_idx)))), 'png')

        end
    end
end
