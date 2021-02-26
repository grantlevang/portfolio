# Project: Education - College Admission
# Set working directory

## PREDICTIVE COMPONENT
# Read in the data
df = data.table::fread("US_college_dataset.csv", header=T)
head(df)

# Looking at the structure of the data
str(df)

# Admit, ses, Gender_Male, Race and rank need to be categorical variables
df = as.data.frame(df)
for (col in names(df)[c(1,4:7)]){
  df[,col] = as.factor(df[,col])
}

# Check data structure now - all categorical variables are now factors
str(df)

# Any missing values?
apply(df, 2, function(x) sum(is.na(x)))
# No missing values

# Some quick exploratory data analysis
library(ggplot2)
ggplot(data = df, aes(x=admit, y=gpa, color=ses)) + geom_boxplot() + ggtitle("GPA vs admission by socio-economic class")

ggplot(data = df, aes(x=admit, y=gre, color=ses)) + geom_boxplot() + ggtitle("GRE vs admission by socio-economic class")

admit_rank = table(df$admit, df$rank)
names(dimnames(admit_rank)) = c("Admitted", "University Rank")
admit_rank

admit_race = table(df$admit, df$Race)
names(dimnames(admit_race)) = c("Admitted", "Race")
admit_race

admit_gender = table(df$admit, df$Gender_Male)
names(dimnames(admit_gender)) = c("Admitted", "Male")
admit_gender


# Split the data into a training and testing set - using a 80-20 split
set.seed(100) # set seed to reproduce the results
train_rows = sample(nrow(df), size=floor(0.8*nrow(df)), replace=F)
df_train = df[train_rows, ]
df_test = df[-train_rows, ]

# Fit logistic model
model = glm(admit~., family=binomial(link="logit"), data=df_train)
summary(model)

# ses is least significant - refit with this dropped
model = glm(admit~. - ses, family=binomial(link="logit"), data=df_train)
summary(model)

# drop gender
model = glm(admit~. - ses - Gender_Male, family=binomial(link="logit"), data=df_train)
summary(model)

# drop gre
model = glm(admit~. - ses - Gender_Male - gre, family=binomial(link="logit"), data=df_train)
summary(model)

# Leave race in the model for now

# Predict with this model and check accuracy
predictions = predict(model, df_train, type="response")
predictions = as.factor(ifelse(predictions > 0.5, 1, 0))
library(e1071)
library(caret)
confusionMatrix(predictions, df_train$admit, positive='1')
# accuracy of 0.7188 - confusion matrix shows this model is not great at predicting admissions
# i.e. 77 admissions were predicted as non-admissions resulting in a sensitivity of 0.2376.

# Try with a model not inclusive of race
model = glm(admit~. - ses - Gender_Male - gre - Race, family=binomial(link="logit"), data=df_train)
summary(model)
# slightly lower AIC which is good

# Predict with this model and check accuracy
predictions = predict(model, df_train, type="response")
predictions = as.factor(ifelse(predictions > 0.5, 1, 0))

confusionMatrix(predictions, df_train$admit, positive='1')
# model has an accuracy of 0.7094 and a sensitivity of 0.21782. AIC is lower but the predictions are
# not as good - leave race in the model.

# Try a decision tree classification approach
df_train = tibble::as_tibble(df_train)
library(rpart)
tree = rpart(admit~., data=df_train, method="class")
tree # view model

# Visualize the resultant model
plot(tree, main="Classification Tree for College Admission")
text(tree, use.n=T, all=T, cex=0.8)

printcp(tree)
# actual variables used are gpa, gre and rank

# Confusion matrix
confusionMatrix(predict(tree, type = "class", df_train), df_train$admit, positive='1')
# Accuracy of 0.7719 - better than the first models. The conf. matrix shows this is also 
# not the best at predicting although it is a lot better than the other models we have so far. 

#Let's try pruning the tree to the lowest relative error.

# Picking the tree size which minimizes prediction error
plotcp(tree)
bestcp = tree$cptable[which.min(tree$cptable[,"xerror"]),"CP"]

# Tree pruning
pruned_tree = prune(tree, cp=bestcp)
pruned_tree # view model

printcp(pruned_tree) #actual variables used are gpa and rank

#Visualize pruned tree
plot(pruned_tree, main="Classification Tree for College Admission")
text(pruned_tree, use.n=T, all=T, cex=0.8)

# Confusion matrix on the pruned tree
confusionMatrix(predict(pruned_tree, type = "class", df_train), df_train$admit, positive='1')
# accuracy score - 0.7219 - model seems worse than the unpruned tree - let's try SVM

# SVM
svm_model = svm(admit~., kernel="linear", data=df_train)
svm_model
confusionMatrix(predict(svm_model), df_train$admit, positive='1')
# accuracy of 0.7031, sensitivity of 0.25743

# let's try tuning the SVM
tuned_parameters = tune.svm(admit~., data=df_train, kernel="linear", gamma = 10^(-5:-1), cost = 10^(-3:1))
summary(tuned_parameters)

# best parameters --> gamma = 0.00001 , cost = 10
svm_tuned = svm(admit~., data=df_train, kernel="linear", gamma=0.00001, cost=10)
confusionMatrix(predict(svm_tuned), df_train$admit, positive='1')
# model is the same when tuned

# Validating each of the models on the test set
# Logistic regression model
model = glm(admit~. - ses - Gender_Male - gre, family=binomial(link="logit"), data=df_train)
predictions = predict(model, df_test, type="response")
predictions = as.factor(ifelse(predictions > 0.5, 1, 0))
logistic_cm = confusionMatrix(predictions, df_test$admit, positive='1')

# Decision tree model
tree = rpart(admit~., data=df_train, method="class")
tree_cm = confusionMatrix(predict(tree, type = "class", df_test), df_test$admit, positive='1')

# SVM 
svm_model = svm(admit~., kernel="linear", data=df_train)
predictions_svm = predict(svm_model, df_test)
svm_cm = confusionMatrix(predictions_svm, df_test$admit, positive='1')

# Obtaining a scatterplot of accuracy and sensitivity and choosing the best pair as the champion
accuracies = c(logistic_cm$overall["Accuracy"], tree_cm$overall["Accuracy"], svm_cm$overall["Accuracy"])
sensitivities = c(logistic_cm$byClass["Sensitivity"], tree_cm$byClass["Sensitivity"], svm_cm$byClass["Sensitivity"])
plot(accuracies, sensitivities, main="Model accuracy vs model sensitivity", xlab="Accuracy", ylab="Sensitivity", ylim=c(0,0.5))
text(accuracies, sensitivities, labels = c("Logistic", "Tree", "SVM"), cex=0.7, pos=3)

# Most accurate model is Logistic, most sensitive is decision tree. Decision tree has a good balance of accuracy and sensitivity
# Champion model --> Decision Tree model

# Other ML techniques that could be applied:
# - Linear Discriminant Analysis
# - Quadratic Discriminant Analysis
# - KNN
# - Naive Bayes classifier
# - Random forest classifier

## DESCRIPTIVE COMPONENT
# Obtain admission probability percentages
model = glm(admit~. - ses - Gender_Male - gre, family=binomial(link="logit"), data=df)
predictions = predict(model, df, type="response")
predictions

df$gre_category = as.factor(sapply(df$gre, function(x) ifelse(x<440, "Low", ifelse(x>=440 & x<580, "Medium", "High"))))

ggplot(data = df, aes(x=gre_category, y=predictions, color=gre_category)) + geom_point()
library(sinaplot)
sinaplot(groups = df$gre_category, x=predictions, col = c("#c63a1d", "#d8bd34", "#dd8c1a"), pch=20, main="Prediction probability per grade point average class", xlab = "Grade point average classes", ylab="Prediction probability")

  
