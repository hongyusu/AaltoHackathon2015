

function run_SR
% wrapper function for running Spatial Recommender (SR)

    % generate toy example
    [adj,X] = generate_toy_example();

    fea = randn(1000,2000);
    fea = fea - min(min(fea));

    %NMF learning
    options = [];
    options.maxIter = 100;
    options.alpha = 0;
    %when alpha = 0, GNMF boils down to the ordinary NMF.
    nClass = 20;
    [U,V] = GNMF(fea',nClass,[],options); %'

    size(fea)
    size(U)
    size(V)
    
end