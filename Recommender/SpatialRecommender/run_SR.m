

function [X,XpNMF,XdNMF] = run_SR
% wrapper function for running Spatial Recommender (SR)

    % generate toy example
    [adj,X] = generate_toy_example();
    
    % NMF learning
    options = [];
    options.maxIter = 100;
    options.alpha = 0;
    nClass = 10;
    [U,V] = GNMF(X,nClass,[],options);
    XpNMF = U*V';    
    XdNMF = XpNMF;
    XdNMF(X==1) = 0;
    
    % SNMF learning
	options = [];
    options.maxIter = 100;
    options.alpha = 0;
    nClass = 10;
    [U,V] = GNMF(X,nClass,adj,options);
    XpSNMF = U*V';    
    XdSNMF = XpSNMF;
    XdSNMF(X==1) = 0;

    % define background color
    j = colormap;
    j(1,:) = [ 1 1 1 ];
    colormap(j);
 
    % plot learning result
    subplot(1,7,1);imagesc(X);title('X');xlabel('Nodes');ylabel('User');
    subplot(1,7,2);imagesc(U);title('U');xlabel('Preference');ylabel('User');
    subplot(1,7,3);imagesc(V);title('V');xlabel('Preference');ylabel('Nodes');
    subplot(1,7,[4,5]);imagesc([XpNMF,XdNMF]);title('NMF');
    subplot(1,7,[6,7]);imagesc([XpSNMF,XdSNMF]);title('SNMF');
    colorbar;
    
    
end