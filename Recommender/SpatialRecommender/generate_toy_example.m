




function [adj,X] = generate_toy_example
    % this function is to generate data for the toy example
    
    % define random seed
    rand('twister',0)
    
    % generate adjacenty matrix
    adj = zeros(2000,2000);
    for i=1:2000
        adj(i,i+1) = 1;
    end
    adj(1000,1001) = 0;
    
    % generate running record
    X = zeros(200,2000);
    for i=1:size(X,1)
        if i<=100
            posStart = randsample(1:500,1);
        else
            posStart = randsample(1001:1500,1);
        end
        posEnd   = posStart + randsample([100:200],1);
        X(i,posStart:posEnd) = ones(1,posEnd-posStart+1);
    end
    
end