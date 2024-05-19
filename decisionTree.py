import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_wine, load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# Load the datasets
wine = load_wine() 
digits = load_digits()  

class DecisionTreeExperiment:
    def __init__(self, dataset, criterion, testSize):

        self.dataset = dataset
        self.criterion = criterion

        # Split the dataset into training and testing data
        self.xTrain, self.xTest, self.yTrain, self.yTest = (
            train_test_split(
                self.dataset.data,
                self.dataset.target,
                test_size=testSize, 
                random_state=42
            )
        )        
        self.decisionTreeClassifier = DecisionTreeClassifier(criterion=self.criterion)  # Create a decision tree classifier

    def createClassificationReport(self):

        #Initialise arrays to store the precision, recall and f1-score for each class
        precision = []
        recall = []
        f1Score = []

        self.decisionTreeClassifier.fit(self.xTrain, self.yTrain)  # Fit the decision tree classifier on the training data
        yPred = self.decisionTreeClassifier.predict(self.xTest)  # Predict the true values for the testing data

        report = classification_report(self.yTest, yPred, output_dict=True) # Generate the classification report

        #Store the precision, recall and f1-score for each class
        classes = list(report.keys())[:-3]
        for c in classes:
            precision.append(report[c]['precision'])
            recall.append(report[c]['recall'])
            f1Score.append(report[c]['f1-score'])

        # Store the macro and weighted averages for precision, recall and f1-score
        macroAvgPrecision = report['macro avg']['precision']
        macroAvgRecall = report['macro avg']['recall']
        macroAvgF1Score = report['macro avg']['f1-score']

        weightedAvgPrecision = report['weighted avg']['precision']
        weightedAvgRecall = report['weighted avg']['recall']
        weightedAvgF1Score = report['weighted avg']['f1-score']

        fig, ax = plt.subplots(1, 3, figsize=(15, 5))
        ax[0].bar(classes, precision)
        ax[0].set_title('Precision')
        ax[0].set_xlabel('Class')
        ax[0].set_ylabel('Precision')

        #Add a line in the bar chart to show the macro and weighted averages for the Precision
        ax[0].axhline(macroAvgPrecision, color='r', linestyle='--', label='Macro Average')
        ax[0].axhline(weightedAvgPrecision, color='g', linestyle='--', label='Weighted Average')


        ax[1].bar(classes, recall)
        ax[1].set_title('Recall')
        ax[1].set_xlabel('Class')
        ax[1].set_ylabel('Recall')

        #Add a line in the bar chart to show the macro and weighted averages for the Recall
        ax[1].axhline(macroAvgPrecision, color='r', linestyle='--', label='Macro Average')
        ax[1].axhline(weightedAvgPrecision, color='g', linestyle='--', label='Weighted Average')

        ax[2].bar(classes, f1Score)
        ax[2].set_title('F1-Score')
        ax[2].set_xlabel('Class')
        ax[2].set_ylabel('F1-Score')

        #Add a line in the bar chart to show the macro and weighted averages for the F1-Score
        ax[2].axhline(macroAvgPrecision, color='r', linestyle='--', label='Macro Average')
        ax[2].axhline(weightedAvgPrecision, color='g', linestyle='--', label='Weighted Average')
        
        fig.suptitle(f'Criterion: {self.criterion} Classification Report')
        plt.show()


        #Print out the averages in the terminal
        print(f'Precision Macro Average: {macroAvgPrecision:.2f}')
        print(f'Precision Weighted Average: {weightedAvgPrecision:.2f} \n')

        print(f'Recall Macro Average: {macroAvgRecall:.2f}')
        print(f'Recall Weighted Average: {weightedAvgRecall:.2f} \n')

        print(f'F1-Score Macro Average: {macroAvgF1Score:.2f}')
        print(f'F1-Score Weighted Average: {weightedAvgF1Score:.2f} \n') 


    def createConfusionMatrix(self):
        self.decisionTreeClassifier.fit(self.xTrain, self.yTrain)
        yPred = self.decisionTreeClassifier.predict(self.xTest)
        confusionMatrix = confusion_matrix(self.yTest, yPred) # Generate the confusion matrix
        fig = plt.figure(figsize=(10, 8))
        sns.heatmap(confusionMatrix, annot=True, cmap='Blues') # Create a heatmap of the confusion matrix
        plt.xlabel('Predicted')
        plt.ylabel('True')
        fig.suptitle(f'Criterion: {self.criterion} Confusion Matrix')
        plt.show()

    def calculateAccuracy(self):
        self.decisionTreeClassifier.fit(self.xTrain, self.yTrain) 
        yPred = self.decisionTreeClassifier.predict(self.xTest)  

        print(f"Accuracy: {accuracy_score(self.yTest, yPred):.2f}", '\n')  # Print the accuracy score


criteria = ['gini', 'log_loss']  #Array of the criteria to test
for crit in criteria:
    wineAnalysis = DecisionTreeExperiment(wine, crit, 0.2) 
    print("Wine dataset:", '\n')

    #Generate the visualisations for the features for the wine dataset
    wineAnalysis.createClassificationReport()
    wineAnalysis.createConfusionMatrix()
    wineAnalysis.calculateAccuracy()

    digitsAnalysis = DecisionTreeExperiment(digits, crit, 0.2) 
    print("Digits dataset:", '\n')

    #Generate the visualisations for the features for the digits dataset
    digitsAnalysis.createClassificationReport()
    digitsAnalysis.createConfusionMatrix()
    digitsAnalysis.calculateAccuracy()