# Module 5: Diagnostic Systems

Implement and evaluate the following classifiers in the task of assigning the diagnosis malignant or benign:

1. A rule-based classifier which follows the following form:
  * If [cell size is abnormal]:
  * or [cell shape is abnormal]
  * or [cell texture is abnormal]
  * or [cell similarity/homogeneity is abnormal], Clarification: There is not a direct link between the Eickhoff summary and the features—you must interpret what these rules should be in the context of the available data. 
  * then: diagnosis is malignant, 
  * otherwise: diagnosis is benign.
2. A random forest classifier using the sklearn framework applied to the features given in the supplied dataset.  
3. A classifier of your own design which attempts to trade off interpretability and classification performance. Clarification: This can build on existing models but the choice/design should focused on the mentioned trade off.  

For the first classifier, it is up to you to define the appropriate variables and the notion of abnormal, based on the supplied data. Motivate your choices. There is not only one solution to this problem. The purpose is to translate medical insights into a model based on available data, and to provide a baseline for other classifiers. 
Compare the classification performance of the three classifiers and comment on their interpretability, from your perspective. (Note that your interpretation may differ from that of a physician). Are there notable interactions between features? 
