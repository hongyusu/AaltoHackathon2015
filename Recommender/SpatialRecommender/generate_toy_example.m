




function [adj,X] = generate_toy_example
    % this function is to generate data for the toy example
    
    % define random seed
    rand('twister',0)
    
    % number of vertices in the graph
    vNum = 5000;
    % number of record
    recordNum = 40;
    
    % generate adjacenty matrix
    adj = zeros(vNum,vNum);
    for i=1:(vNum-1)
        adj(i,i+1) = 1;
    end
    adj(vNum/2,vNum/2+1) = 0;
    
    % generate running record
    X = zeros(recordNum,vNum);
    for i=1:recordNum
        for k=1:2
            if i<=recordNum/2
                posStart = randsample(1:(vNum/2-100),1);
            else
                posStart = randsample((vNum/2+1):(vNum-100),1);
            end
            posEnd   = posStart + randsample(100:200,1);
            X(i,posStart:posEnd) = ones(1,posEnd-posStart+1);
        end
    end
    
end