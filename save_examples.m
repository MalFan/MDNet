function [] = save_examples( images, datasetName, seqName, init_pos_examples, init_neg_examples, total_pos_examples, total_neg_examples )
    mkdir(fullfile('result', datasetName, seqName, 'init_pos_examples'));
    mkdir(fullfile('result', datasetName, seqName, 'init_neg_examples'));
    
    csvwrite(fullfile('result', datasetName, seqName, 'init_pos_examples.txt'), init_pos_examples)
    % csvwrite(fullfile('result', datasetName, seqName, 'init_neg_examples.txt'), init_neg_examples)


    % img = imread(images{1});
    % if(size(img,3)==1), img = cat(3,img,img,img); end

    % for bbox_idx = 1:size(init_pos_examples, 1)
    %     bbox = init_pos_examples(bbox_idx, :);
    %     crop = imcrop(img, bbox);

    %     bbox_idx
    %     imwrite(crop, fullfile('result', datasetName, seqName, 'init_pos_examples', sprintf('%04d.png', bbox_idx)), 'png')
    % end

    % for bbox_idx = 1:size(init_neg_examples, 1)
    %     bbox = init_neg_examples(bbox_idx, :);
    %     crop = imcrop(img, bbox);

    %     bbox_idx
    %     imwrite(crop, fullfile('result', datasetName, seqName, 'init_neg_examples', sprintf('%04d.png', bbox_idx)), 'png')
    % end



    nFrames = size(total_pos_examples);

    for To = 1:nFrames
        mkdir(fullfile('result', datasetName, seqName, 'cur_pos_examples', sprintf('%d', To)));
        mkdir(fullfile('result', datasetName, seqName, 'cur_neg_examples', sprintf('%d', To)));

        csvwrite(fullfile('result', datasetName, seqName, 'cur_pos_examples', sprintf('%d.txt', To)), total_pos_examples{To})
        % csvwrite(fullfile('result', datasetName, seqName, 'cur_neg_examples', sprintf('%d.txt', To)), total_neg_examples{To})

        % img = imread(images{To});
        % if(size(img,3)==1), img = cat(3,img,img,img); end

        % cur_pos_examples = total_pos_examples{To};
        % cur_neg_examples = total_neg_examples{To};

        % for bbox_idx = 1:size(cur_pos_examples, 1)
        %     bbox = cur_pos_examples(bbox_idx, :);
        %     crop = imcrop(img, bbox);

        %     bbox_idx
        %     imwrite(crop, fullfile('result', datasetName, seqName, 'cur_pos_examples', sprintf('%d', To), sprintf('%04d.png', bbox_idx)), 'png')
        % end

        % for bbox_idx = 1:size(cur_neg_examples, 1)
        %     bbox = cur_neg_examples(bbox_idx, :);
        %     crop = imcrop(img, bbox);

        %     bbox_idx
        %     imwrite(crop, fullfile('result', datasetName, seqName, 'cur_neg_examples', sprintf('%d', To), sprintf('%04d.png', bbox_idx)), 'png')
        % end

    end
end
