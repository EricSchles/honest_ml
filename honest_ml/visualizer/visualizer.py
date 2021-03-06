import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

class Visualizer:
    def __init__(self, model_instances, model_type, coef_names=[]):
        self.model_instances = model_instances
        self.model_type = model_type
        self.regression_metrics = [
            "mse", "max_error", "mae"
        ]
        if 'coef' in list(model_instances[0].keys()):
            self.coefs = self._get_coefs(model_instances, coef_names)
        else:
            self.coefs = None

        if model_type == "classification":
            classes = list(model_instances[0].keys())
            classes.remove("accuracy")
            classes.remove("mask")
            classes.remove("seed")
            classes.remove("hyperparameters")
            classes.remove("coef")
            self.classes = classes
            self.classification_metrics = [
                "precision", "recall", "f1-score", "support"
            ]
    def _get_coefs(self, model_instances, coef_names):
        coefs = {}.fromkeys(coef_names)
        for coef in coefs:
            coefs[coef] = []
        for run in model_instances:
            for coef in run['coef']:
                for index in range(len(coef_names)):
                    key = coef_names[index]
                    coefs[key].append(coef[index])
        return coefs

    def visualize_coeficients(self, **kwargs):
        if self.coefs:
            for coeficient_name in self.coefs:
                coef = self.coefs[coeficient_name]
                plt.hist(coef, **kwargs)
                plt.xlabel(coeficient_name)
                plt.ylabel("magnitude")
                plt.show()
            
    def visualize_regression(self, **kwargs):
        for metric in self.regression_metrics:
            metrics = [model_instance[metric] for model_instance in self.model_instances]
            plt.hist(metrics, **kwargs)
            plt.xlabel(metric)
            plt.ylabel("magnitude")
            plt.show()

    def visualize_classification(self, **kwargs):
        for _class in self.classes:
            for metric in self.classification_metrics:
                metrics = [
                    model_instance[_class][metric]
                    for model_instance in self.model_instances
                ]
                plt.hist(metrics, **kwargs)
                plt.xlabel(metric)
                plt.ylabel("magnitude")
                if "avg" in _class:
                    plt.title(_class)
                else:
                    plt.title(f"class {_class}")
                plt.show()

    def visualize_confusion_matrix(self, **kwargs):
        for _class in self.classes:
            precision = [
                model_instance[_class]["precision"]
                for model_instance in self.model_instances
            ]
            recall = [
                model_instance[_class]["recall"]
                for model_instance in self.model_instances
            ]
            _data = pd.DataFrame()
            _data[f"precision_class_{_class}"] = precision
            _data[f"recall_class_{_class}"] = recall
            sns.jointplot(
                data=_data,
                x=f"precision_class_{_class}",
                y=f"recall_class_{_class}"
            )
            plt.show()
            
