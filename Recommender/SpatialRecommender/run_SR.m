

function run_SR
% wrapper function for running Spatial Recommender (SR)

    rand('twister',0);
    
    % generate toy example
    [adj,X] = generate_toy_example(3000,40,800:1000);
    % normalization
    X = X./repmat(sqrt(sum(X.*X,2)),1,size(X,2));
    
    
    % learning parameter
    options = [];
    options.maxIter = 50;
    nClass = 20;
    
    % NMF learning
    options.alpha = 0;
    [Un,Vn] = GNMF(X,nClass,[],options);
    XpNMF = Un*Vn';    
    XdNMF = XpNMF;
    XdNMF(X~=0) = 0;
    
    % SNMF learning
	options.alpha = 0.9;
    [Us,Vs] = GNMF(X,nClass,adj,options);
    XpSNMF = Us*Vs';    
    XdSNMF = XpSNMF;
    XdSNMF(X~=0) = 0;

    
    
    
    % define background color
    j = colormap;
    j(1,:) = [ 1 1 1 ];
    colormap(j);
    % plot learning result
    % NMF
    subplot(2,5,1);imagesc(X);title('X');xlabel('Nodes');ylabel('User');
    subplot(2,5,2);imagesc(XpNMF);title('Xp, NMF');
    subplot(2,5,3);imagesc(XdNMF);title('Xp-X, NMF');
    subplot(2,5,4);imagesc(Un);title('U');xlabel('Preference');ylabel('User');
    subplot(2,5,5);imagesc(Vn);title('V');xlabel('Preference');ylabel('Nodes');
    % SNMF
    subplot(2,5,6);imagesc(X);title('X');xlabel('Nodes');ylabel('User');
    subplot(2,5,7);imagesc(XpSNMF);title('Xp, SNMF');
    subplot(2,5,8);imagesc(XdSNMF);title('Xp-X, SNMF');
    subplot(2,5,9);imagesc(Us);title('U');xlabel('Preference');ylabel('User');
    subplot(2,5,10);imagesc(Vs);title('V');xlabel('Preference');ylabel('Nodes');
    
end