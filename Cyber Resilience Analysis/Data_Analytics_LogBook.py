# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 09:05:09 2025

@author: Mwang002
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import time


#Reading the experiment Log Book
log_book = pd.read_csv('Experiment_Log_Book.csv')

df = log_book
# Clean and preprocess the data
df['Mutation Triggered?'] = df['Mutation Triggered?'].str.strip().str.lower()
df['Classified Correctly?'] = df['Classified Correctly?'].str.strip().str.lower()
df['Threat contained?'] = df['Threat contained?'].str.strip().str.lower()

# Diagnostic 1: Containment success rate by severity
containment_by_severity = df.groupby('CVSS Severity')['Threat contained?'].value_counts(normalize=True).unstack().fillna(0) * 100

# Diagnostic 2: Containment success based on mutation
containment_by_mutation = df.groupby('Mutation Triggered?')['Threat contained?'].value_counts(normalize=True).unstack().fillna(0) * 100

# Diagnostic 3: Containment success based on classification
containment_by_classification = df.groupby('Classified Correctly?')['Threat contained?'].value_counts(normalize=True).unstack().fillna(0) * 100

# Combine all diagnostics into a dictionary
diagnostic_results = {
    'Containment by CVSS Severity (%)': containment_by_severity.round(2),
    'Containment by Mutation Triggered (%)': containment_by_mutation.round(2),
    'Containment by Classification Accuracy (%)': containment_by_classification.round(2)
}

df_diagnostics = pd.concat(diagnostic_results, axis=1)
print(df_diagnostics)
df_diagnostics.style.format("{:.2f}")

# Set up plots for the diagnostics
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Bar plot 1: Containment by Severity
diagnostic_results['Containment by CVSS Severity (%)'].plot.bar(ax=axes[0])
axes[0].set_title('Containment by CVSS Severity')
axes[0].set_ylabel('Percentage (%)')
axes[0].set_xlabel('Severity Level')
axes[0].legend(title='Threat Contained?')

# Bar plot 2: Containment by Mutation Triggered
diagnostic_results['Containment by Mutation Triggered (%)'].plot.bar(ax=axes[1])
axes[1].set_title('Containment by Mutation Triggered')
axes[1].set_ylabel('Percentage (%)')
axes[1].set_xlabel('Mutation Triggered')
axes[1].legend(title='Threat Contained?')

# Bar plot 3: Containment by Classification Accuracy
diagnostic_results['Containment by Classification Accuracy (%)'].plot.bar(ax=axes[2])
axes[2].set_title('Containment by Classification Accuracy')
axes[2].set_ylabel('Percentage (%)')
axes[2].set_xlabel('Classified Correctly')
axes[2].legend(title='Threat Contained?')

plt.tight_layout()
plt.show()
