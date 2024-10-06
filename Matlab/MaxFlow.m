s = [7 7 7 1 1 2 3 3 4 4 5 5];
t = [1 3 4 2 3 6 2 5 3 5 2 6];
weights = [1 1 6 0 1 1 1 2 1 2 0 5];
G = digraph(s,t,weights);
[mf,GF,cs,ct] = maxflow(G,7,6,'augmentpath');
H=plot(GF,'-or','EdgeLabel',GF.Edges.Weight,'Layout','layered');
highlight(H,cs,'NodeColor','red');
highlight(H,ct,'NodeColor','green');
disp(mf)

