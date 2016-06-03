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
* After computing the list of potential stripes we recursively remove all stripes that have no piece wise separating lines.

##Character Segmentation
Character segementation is doen with the method described in Lee, Hong, and Brijesh Verma. "Binary segmentation algorithm for English cursive handwriting recognition." Pattern Recognition 45.4 (2012): 1306-1317. With the following changes:

* Instead of using the method described by H. Lee and B.Verma to compute the baseline we use the horizontal pixel density histogram. 
* H. Lee and B.Verma compute the `segment_criterion` as `segement_criterion_factor * stroke_width` with `segment_criterion_factor = 2`. In our case this gave zero suspicious regions for some images, thus we start of with `segment_criterion = segment_criterion_factor * stroke_width` and increase the `segment_criterion_factor` until the number of suspicious regions is greater than or equal to the length of the longest word. The `segment_criterion_factor` is initialized on the parameter `initial_segment_criterion_factor`.