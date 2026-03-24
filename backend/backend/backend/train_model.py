import pandas as pd 
from sklearn.model_selection import train_test_split 
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
from sklearn.linear_model import LogisticRegression 
from sklearn.svm import SVC 
from sklearn.tree import DecisionTreeClassifier 
from sklearn.metrics import classification_report, f1_score
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np
import joblib                              

data = pd.read_csv(r'C:\Users\ASUS\Downloads\student_exam_data_new.csv') 

X = data[['Study Hours','Previous Exam Score']] 
y = data['Pass/Fail'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) 

results = {}                      

log_model = LogisticRegression() 
log_model.fit(X_train, y_train)
log_preds = log_model.predict(X_test)
log_acc = accuracy_score(y_test, log_preds)
results['Logistic Regression'] = (log_acc, log_model)

svm_model = SVC(kernel='linear')
svm_model.fit(X_train, y_train)
svm_preds = svm_model.predict(X_test)
svm_acc = accuracy_score(y_test, svm_preds)
results['SVM'] = (svm_acc, svm_model)

tree_model = DecisionTreeClassifier(random_state=42)
tree_model.fit(X_train, y_train)
tree_preds = tree_model.predict(X_test)
tree_acc = accuracy_score(y_test, tree_preds)
results['Decision Tree'] = (tree_acc, tree_model)

for name, (acc, _) in results.items():
    print(f"{name} Accuracy: {acc:.4f}")

best_model_name = max(results, key=lambda x: results[x][0])
best_model = results[best_model_name][1]
joblib.dump(best_model, 'student_model.pkl')
print(f"\nBest model: {best_model_name} saved as 'student_model.pkl'")

y_pred = best_model.predict(X_test)
print("F1 Score:", f1_score(y_test, y_pred, average='weighted'))
print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.show()
   