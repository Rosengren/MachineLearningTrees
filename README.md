# Machine Learning Trees
##### Decision and Dependence Trees

## Bayesian Classifier

<p>The bayesian classifier is a machine learning technique which learns to classify different data points based on what has been learned through a training set. The optimal Bayesian classifier works by determining the probability that a data point will fall into a specific class. That is, the classifier will classify the data point based on the most likely category. The probability is calculated using Bayes’ theorem.</p>

### Results

<p>After running several tests with randomly generated dependent data, using 8-fold cross validation, the classifier had an average accuracy of <b>70%</b>.</p>

<p>Since the Real-Life data sets were not binary values, thresholds needed to be applied. For these data sets, the test data was compared against thresholds instead of expecting a one or a zero. The results were thus the following:</p>

#### Sample Outputs:

<b>Heart Disease</b>

53.872 percent Accuracy<br/>
total of 297 instances<br/>

<b>Iris</b>

91.333 percent Accuracy<br/>
total of 150 instances<br/>

<b>Wine</b>

98.315 percent Accuracy<br/>
total of 178 instances<br/>

<p>From the above, we see that the Optimal Bayes Classifier was very accurate for the Iris and Wine data sets but was not very effective in classifying the Heart Disease data set.</p>

## Bayesian Classifier with Dependence

<p>As noted in the Dependence Tree section, the algorithm could not be implemented due to the poor dependence tree generation. However, because the optimal Bayesian classifier is designed for handling independent data, it is safe to say that adding a dependence tree element to the algorithm would in fact hinder its accuracy. In many cases, the bayesian classifier comes close to, and often surpasses, the accuracy of algorithms which aim to find relationships between dimensions. There have been many scholarly articles written on the subject of the high classification accuracy when the algorithm assumes that the dimensions are independent.</p>

## Decision Tree

<p>The Decision tree was effective in predicting the outcome of discrete values such as predicting which class a data point belongs to based on the given dimensions. However, the decision tree is not exceptional with handling continuous data. If good thresholds are not chosen for the classification of dimensions, the accuracy suffers. Poor thresholds cause certain data points to be misclassified because the outcomes don’t perfectly separate each class. When the dimensions of each class overlap with each other, it becomes very difficult to accurately set thresholds. If two classes perfectly overlap, the decision tree becomes very ineffective in classifying the testing dataset. The accuracy of the randomly generated dataset was about <b>80%</b>.</p>

<p>The accuracy of the Iris dataset was about <em>95.3%</em> which makes sense considering that the classes have very little overlap in terms of their dimensions</p>

<p>The accuracy of the Wine dataset was about <em>85.6%</em>. The Wine data set is another example of a set that has a relatively low overlap between classes in terms of their dimensions. It does, however, have more overlap than the Iris dataset which explains the lower accuracy.</p>

<p>The decision tree had about <em>85%</em> accuracy in classifying the Heart Disease test data. This dataset was also fairly accurately classify do mainly because of the low level of overlap between each class dimension.</p>


## Dependence Tree

<p>Despite the weights being accurately calculated according to the mutual information equation below, the original dependence tree could not be generated.</p>

<p>Even when increasing the number of training samples to 100, 000 data points, the generated results were no better than a randomly generated tree. It is, however, possible that the data being properly generated so as to be dependent.</p>

<p>Without a functional algorithm, it’s hard to determine the accuracy. That being said, the accuracy of the algorithm is dependent on the number of dimensions, classes, and number of samples. The most significant factor is the size of the training set. While it is possible to improve accuracy through tweaking elements such as the thresholds, the number of data points will have the most dramatic effect. As the number of dimension and classes grow, the harder it becomes to generate the original tree.</p>

<p>One major challenge with the dependence tree is choosing the thresholds for each dimension. That is, the accuracy of a dependence tree is not as accurate for continuous data versus discrete data sets.</p>

<p>Finally, the dependence tree is not as effective as the optimal Bayes classifier when handling independent data because this algorithm will determine relationships between dimensions whether or not they exist.</p>

## Conclusion

<p>In terms of classifying the real-life data sets, the Decision Tree algorithm and the Optimal Bayes Classifier both performed very well for the most part. According to the data collected, the Decision Tree was much more accurate in classifying. It makes sense that the DT algorithm outperformed Bayes Classifier in the Iris dataset because their exists a relationship between the attributes which Bayes does not account for. When classifying the generated data, DT also performed slightly better than the Optimal Bayes Classifier. This makes sense for two main reasons; the generated data was dependent, which Bayes ignores, and the data was binary which means the DT algorithm did not need to create thresholds. Thresholds weren’t needed because the dimensions were binary. Unfortunately, due to the lack of a proper implementation of the dependence tree algorithm, it is hard to quantify its accuracy. However, given that the proper implementation nearly guarantees the reconstruction of the original dependence tree, it is likely that this algorithm would perform fairly well.</p>
