% read in seriers of images
% convert to grey scale
GI(i) = rgb2gray(CI(i)); 
% compute abs difference between two consective images
AD(i) = | GI(i+1) – GI(i) |
% display images 2-4