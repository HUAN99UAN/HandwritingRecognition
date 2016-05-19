#Cropper
The commend line interface can be used by calling ``python ./cropper/cli.py ...`` with the correct arguments. See ``python ./cropper/cli.py -h`` for the arguments. 

Interfacing with ``cropper`` from other scriptss can be via the ``cropper.dataset`` module. Note that there are still some problem caveats when using this approach, see these issues: 
[1](https://github.com/Twinblade/HandwritingRecognition/issues/1),
[2](https://github.com/Twinblade/HandwritingRecognition/issues/2),
[3](https://github.com/Twinblade/HandwritingRecognition/issues/3).

#Noise Removal

#Segmenter
Handles the segmentation of a textblock into lines, words and characters. 
	
##Line Segmentation
Line segmentation is done with the method described in Tripathy, Nilamadhaba, and Umapada Pal. "Handwriting segmentation of unconstrained Oriya text." Sadhana 31.6 (2006): 755-769. With the following changes:

* Instead of choosing the mode of the lineheights we use the min of the n most frequent line heights. Ussing the mode of the line heights, removed nearly all piece wise separating lines.