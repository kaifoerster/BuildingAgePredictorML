import gc
import logging
from functools import partial

import utils
import visualizations
import dataset
import preprocessing
import energy_modeling
from prediction import Predictor, Classifier, Regressor, PredictorComparison

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AgePredictor(Regressor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, target_attribute=dataset.AGE_ATTRIBUTE)


    def _pre_preprocess_analysis_hook(self):
        logger.info(f"Dataset standard deviation: {self.df[self.target_attribute].std()}")
        logger.info(f"Dataset mean age: {self.df[self.target_attribute].mean()}")
        logger.info(f'Training dataset length: {len(self.df_train)}')
        logger.info(f'Test dataset length: {len(self.df_test)}')
        logger.info(f'Test cities: {self.df_test["city"].unique()}')


    def _post_preprocess_analysis_hook(self):
        # The standard deviation in the test set gives us an indication of a
        # baseline. We want to be able to be substantially below that value.
        logger.info(f"Test dataset standard deviation after preprocessing: {self.df_test[self.target_attribute].std()}")
        logger.info(f"Test dataset mean age after preprocessing: {self.df_test[self.target_attribute].mean()}")
        logger.info(f'Training dataset length after preprocessing: {len(self.df_train)}')
        logger.info(f'Test dataset length after preprocessing: {len(self.df_test)}')


    def eval_metrics(self):
        eval_df = super().eval_metrics()

        r2, mape = self.energy_error()
        eval_df.at['total', 'energy_r2'] = r2
        eval_df.at['total', 'energy_mape'] = mape

        bins = [0, 5, 10, 20]
        hist = self.error_cum_hist(bins)

        for idx, bin in enumerate(bins[1:]):
            eval_df.at['total', f'within_{bin}_years'] = hist.flat[idx]

        if self.cross_validation_split:
            fold_histograms = self.error_cum_hist(bins, across_folds=True)
            fold_energy_errors = self.energy_error(across_folds=True)
            logger.info(fold_energy_errors)

            for fold, hist in enumerate(fold_histograms):
                eval_df.at[f'fold_{fold}', 'energy_r2'] = fold_energy_errors[fold][0]
                eval_df.at[f'fold_{fold}', 'energy_mape'] = fold_energy_errors[fold][1]

                for idx, bin in enumerate(bins[1:]):
                    eval_df.at[f'fold_{fold}', f'within_{bin}_years'] = hist.flat[idx]

        return eval_df


    def print_model_error(self):
        super().print_model_error()
        r2, mape = self.energy_error()
        print(f'R2: {r2:.4f}')
        print(f'MAPE: {mape:.4f}')


    def evaluate(self):
        self.print_model_error()
        _, axis = plt.subplots(2, 2, figsize=(14, 10), constrained_layout=True)
        visualizations.plot_regression_error(self.model, ax=axis[0, 0])
        visualizations.plot_histogram(
            self.y_test, self.y_predict, bins=utils.age_bins(self.y_predict), ax=axis[1, 0])
        visualizations.plot_relative_grid(self.y_test, self.y_predict, ax=axis[1, 1])
        plt.show()
        visualizations.plot_grid(self.y_test, self.y_predict)


    def evaluate_regression(self):
        self.evaluate()  # for backwards compatibility


    @Predictor.cv_aware
    def energy_error(self):
        y_true = pd.concat([self.y_test, self.aux_vars_test, self.X_test[['FootprintArea']]], axis=1, join="inner")
        y_pred = pd.concat([self.y_predict, self.aux_vars_test, self.X_test[['FootprintArea']]], axis=1, join="inner")
        try:
            return energy_modeling.calculate_energy_error(y_true, y_pred)
        except Exception as e:
            logger.error(f'Failed to calculate energy error: {e}')
            return np.nan, np.nan


class AgeClassifier(Classifier):

    def __init__(self, bins=[], bin_config=None, *args, **kwargs):

        if not bins and bin_config is None or bins and bin_config:
            logger.exception('Please either specify the bins or define a bin config to have them generated automatically.')

        self.bins = bins or utils.generate_bins(bin_config)

        super().__init__(*args, **kwargs, target_attribute=dataset.AGE_ATTRIBUTE,
                         labels=utils.generate_labels(self.bins), initialize_only=True)

        logger.info(f'Generated bins: {self.bins}')
        logger.info(f'Generated bins with the following labels: {self.labels}')

        self.metric_target_attribute = 'age_metric'
        self.preprocessing_stages.append(partial(preprocessing.categorize_age, bins=self.bins, metric_col=self.metric_target_attribute))

        self._e2e_training()


    def eval_metrics(self):
        eval_df = super().eval_metrics()

        if self.bins in dataset.TABULA_AGE_BINS.values():
            r2, mape = self.energy_error()
            eval_df.at['total', 'energy_r2'] = r2
            eval_df.at['total', 'energy_mape'] = mape

        if self.cross_validation_split:
            fold_energy_errors = self.energy_error(across_folds=True)
            for fold, energy_error in enumerate(fold_energy_errors):
                eval_df.at[f'fold_{fold}', 'energy_r2'] = energy_error[0]
                eval_df.at[f'fold_{fold}', 'energy_mape'] = energy_error[1]

        return eval_df


    def print_model_error(self):
        super().print_model_error()
        if self.bins in dataset.TABULA_AGE_BINS.values():
            r2, mape = self.energy_error()
            print(f'R2: {r2:.4f}')
            print(f'MAPE: {mape:.4f}')


    def evaluate(self):
        self.print_model_error()
        _, axis = plt.subplots(2, 2, figsize=(14, 10), constrained_layout=True)
        visualizations.plot_classification_error(self.model, multiclass=self.multiclass, ax=axis[0, 0])
        visualizations.plot_log_loss(self.model, multiclass=self.multiclass, ax=axis[0, 1])
        visualizations.plot_histogram(self.y_test, self.y_predict[[self.target_attribute]], bins=list(
            range(0, len(self.bins))), bin_labels=self.labels, ax=axis[1, 0])
        visualizations.plot_confusion_matrix(
            self.y_test, self.y_predict[[self.target_attribute]], class_labels=self.labels, ax=axis[1, 1])
        plt.show()


    def evaluate_classification(self):
        self.evaluate()  # for backwards compatibility


    @Predictor.cv_aware
    def energy_error(self):
        y_true = pd.concat([self.y_test, self.aux_vars_test, self.X_test[['FootprintArea']]], axis=1, join="inner")
        y_pred = pd.concat([self.y_predict, self.aux_vars_test, self.X_test[['FootprintArea']]], axis=1, join="inner")
        try:
            return energy_modeling.calculate_energy_error(y_true, y_pred, labels=self.labels)
        except Exception as e:
            logger.error(f'Failed to calculate energy error: {e}')
            return np.nan, np.nan


class AgePredictorComparison(PredictorComparison):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, predictor=AgePredictor)


    def evaluate(self, include_plot=False, include_error_distribution=False, include_energy_error=False, include_spatial_autocorrelation=False):
        age_distributions = {}
        comparison_metrics = []
        for name, predictors in self.predictors.items():
            # average eval metrics across seeds
            eval_metrics = {}
            eval_metrics['name'] = name
            eval_metrics['R2'] = self._mean(predictors, 'r2')
            eval_metrics['R2_std'] = self._std(predictors, 'r2')
            eval_metrics['MAE'] = self._mean(predictors, 'mae')
            eval_metrics['MAE_std'] = self._std(predictors, 'mae')
            eval_metrics['RMSE'] = self._mean(predictors, 'rmse')
            eval_metrics['RMSE_std'] = self._std(predictors, 'rmse')

            bins = [0, 5, 10, 20]
            hist = self._mean(predictors, 'error_cum_hist', bins)

            for idx, bin in enumerate(bins[1:]):
                eval_metrics[f'within_{bin}_years'] = hist.flat[idx]

            for seed, predictor in enumerate(predictors):
                eval_metrics[f'R2_seed_{seed}'] = predictor.r2()

            if include_error_distribution:
                eval_metrics['skew'] = self._mean(predictors, 'skew')
                eval_metrics['kurtosis'] = self._mean(predictors, 'kurtosis')

            if include_energy_error:
                r2, mape = self._mean(predictors, 'energy_error')
                eval_metrics['energy_r2'] = r2
                eval_metrics['energy_mape'] = mape

            if include_spatial_autocorrelation:
                eval_metrics['residuals_moranI_KNN'] = predictors[0].spatial_autocorrelation_moran('error', 'knn').I
                eval_metrics['residuals_moranI_block'] = predictors[0].spatial_autocorrelation_moran('error', 'block').I
                eval_metrics['residuals_moranI_distance'] = predictors[0].spatial_autocorrelation_moran('error', 'distance').I
                eval_metrics['prediction_moranI_KNN'] = predictors[0].spatial_autocorrelation_moran(predictors[0].target_attribute, 'knn').I
                eval_metrics['prediction_moranI_block'] = predictors[0].spatial_autocorrelation_moran(predictors[0].target_attribute, 'block').I
                eval_metrics['prediction_moranI_distance'] = predictors[0].spatial_autocorrelation_moran(predictors[0].target_attribute, 'distance').I

            if include_plot:
                age_distributions[f'{name}_predict'] = predictors[0].y_predict[predictors[0].target_attribute]
                age_distributions[f'{name}_test'] = predictors[0].y_test[predictors[0].target_attribute]

            comparison_metrics.append(eval_metrics)

        if include_plot:
            visualizations.plot_distribution(age_distributions)

        return pd.DataFrame(comparison_metrics).sort_values(by=['R2'])


    def evaluate_comparison(self, *args, **kwargs):
        return self.evaluate(*args, **kwargs)  # for backwards compatibility


    def determine_predictor_identifier(self, param_name, param_value, baseline_value):
        if param_name == 'preprocessing_stages':
            additional_stages = list(set(param_value) - set(baseline_value))
            stage_names = [getattr(stage, '__name__', stage) for stage in additional_stages]
            return f'add_preprocessing:{stage_names}'

        return f'{param_name}_{param_value}'


class AgeClassifierComparison(PredictorComparison):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, predictor=AgeClassifier)


    def evaluate(self, include_plot=False, include_energy_error=False):
        evals_results = {}
        comparison_metrics = []
        for name, predictors in self.predictors.items():
            # average eval metrics across seeds
            eval_metrics = {}
            eval_metrics['name'] = name
            eval_metrics['MCC'] = self._mean(predictors, 'mcc')
            eval_metrics['MCC_std'] = self._std(predictors, 'mcc')
            eval_metrics['F1'] = self._mean(predictors, 'f1')
            eval_metrics['F1_std'] = self._std(predictors, 'f1')

            for idx, label in enumerate(predictors[0].labels):
                eval_metrics[f'Recall_{label}'] = self._mean(predictors, 'recall', idx)

            for seed, predictor in enumerate(predictors):
                eval_metrics[f'MCC_seed_{seed}'] = predictor.mcc()

            if include_energy_error:
                r2, mape = self._mean(predictors, 'energy_error')
                eval_metrics['energy_r2'] = r2
                eval_metrics['energy_mape'] = mape

            comparison_metrics.append(eval_metrics)

            if include_plot:
                eval_metric = 'merror' if predictors[0].multiclass else 'error'
                evals_results[f'{name}_train'] = predictors[0].evals_result['validation_0'][eval_metric]
                evals_results[f'{name}_test'] = predictors[0].evals_result['validation_1'][eval_metric]

        if include_plot:
            _, axis = plt.subplots(figsize=(6, 6), constrained_layout=True)
            visualizations.plot_models_classification_error(evals_results, ax=axis)
            plt.show()

        return pd.DataFrame(comparison_metrics).sort_values(by=['MCC'])


    def evaluate_comparison(self):
        return self.evaluate()  # for backwards compatibility
