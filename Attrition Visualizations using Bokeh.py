"""
MFG: 598
Engineering Computing with Python
Final Project

Author: Nishad Kale
ASU ID: 1226362919

Description: This is an advanced visualization of the Employee attrition dataset using Bokeh.
Total of 6 plots are shown for analysis.
"""

# imports
import math
from math import pi
import numpy as np
import pandas as pd
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper, ColorBar, BasicTicker
from bokeh.palettes import Category20c, Magma256
from bokeh.transform import factor_cmap, transform, cumsum
from bokeh.plotting import figure, show

# Load the dataset
df = pd.read_csv('attrition.csv')

#######################################################################################################################

# 1. SCATTER PLOT

# Define the data source for the scatter plot
scatter_source = ColumnDataSource(data=dict(age=df['Age'], income=df['MonthlyIncome'], attrition=df['Attrition']))
colors = factor_cmap('attrition', palette=['green', 'red'], factors=['Yes', 'No'])

#  Age vs MonthlyIncome plot
scatter_plot = figure(title="Age vs. Monthly Income with Attrition", tools="")
scatter_plot.scatter(x='age', y='income', source=scatter_source, size=8, color=colors, legend_field='attrition', )

# Add hover tool to show the details
hover = HoverTool(tooltips=[("Age", "@age"), ("Monthly Income", "@income"), ("Attrition", "@attrition"), ])
scatter_plot.add_tools(hover)

# Styling the plot
scatter_plot.xaxis.axis_label = "Age"
scatter_plot.yaxis.axis_label = "Monthly Income"
scatter_plot.legend.location = "top_left"

#####################################################################################################################

# 2. DONUT CHART

# getting values based on conditions to plot donut chart

ls_yes = len(df[(df['EducationField'] == 'Life Sciences') & (df['Attrition'] == 'Yes')])
ls_no = len(df[(df['EducationField'] == 'Life Sciences') & (df['Attrition'] == 'No')])

other_yes = len(df[(df['EducationField'] == 'Other') & (df['Attrition'] == 'Yes')])
other_no = len(df[(df['EducationField'] == 'Other') & (df['Attrition'] == 'No')])

medical_yes = len(df[(df['EducationField'] == 'Medical') & (df['Attrition'] == 'Yes')])
medical_no = len(df[(df['EducationField'] == 'Medical') & (df['Attrition'] == 'No')])

market_yes = len(df[(df['EducationField'] == 'Marketing') & (df['Attrition'] == 'Yes')])
market_no = len(df[(df['EducationField'] == 'Marketing') & (df['Attrition'] == 'No')])

tech_yes = len(df[(df['EducationField'] == 'Technical Degree') & (df['Attrition'] == 'Yes')])
tech_no = len(df[(df['EducationField'] == 'Technical Degree') & (df['Attrition'] == 'No')])

hr_yes = len(df[(df['EducationField'] == 'Human Resources') & (df['Attrition'] == 'Yes')])
hr_no = len(df[(df['EducationField'] == 'Human Resources') & (df['Attrition'] == 'No')])

# store all values in array
values = [ls_no, ls_yes, other_yes, other_no, market_yes, market_no, hr_yes, hr_no, tech_yes, tech_no, medical_yes,
          medical_no]
labels = ['Yes: Life Sci', 'No: Life Sci', 'Yes: Other', 'No: Other', 'Yes: Medical', 'No: Medical',
          'Yes: Marketing', 'No: Marketing', 'Yes: Technical degree', 'No: Technical degree',
          'Yes: HR', 'No: HR']

# create dictionary to map index to label
label_dict = {i: label for i, label in enumerate(labels)}

# create data source
data = {'values': values, 'angle': [v / sum(values) * 2 * pi for v in values],
        'color': Category20c[len(values)],
        'label': [label_dict[i] for i in range(len(values))]}

# create figure and donut chart
donut_plot = figure(title="Donut Chart", toolbar_location=None,
                    tools="hover", tooltips="@label: @values", )

# create inner and outer wedge for donut shape
donut_plot.wedge(x=0, y=1, radius=0.9,
                 start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                 line_color="white", fill_color='color', legend_field='label', source=data)

donut_plot.wedge(x=0, y=1, radius=0.7,
                 start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), color='white',
                 line_color="white", source=data)

# update legend
donut_plot.legend.label_text_font_size = "8pt"
donut_plot.legend.label_text_font_style = "bold"
donut_plot.legend.location='center'
donut_plot.legend.label_width = 40
donut_plot.legend.glyph_width = 10

donut_plot.xaxis.visible = False
donut_plot.yaxis.visible = False
donut_plot.outline_line_color = None
donut_plot.ygrid.grid_line_color = None
donut_plot.xgrid.grid_line_color = None
donut_plot.xaxis.minor_tick_line_color = None


########################################################################################################################

# 3. STACKED BAR CHART

# create a new column in the dataframe to indicate the combined EducationField and Attrition status
df['JobRole_Attrition'] = df['JobRole'].astype(str) + '_' + df['Attrition'].astype(str)

# group the data by EducationField_Attrition and count the number of occurrences
grouped = df.groupby('JobRole_Attrition').count()['Attrition']

# calculate the proportion of each EducationField_Attrition combination that has left the company
yes_prop = []
no_prop = []
fields = df['JobRole'].unique()
# print(fields)
for i, field in enumerate(fields):
    yes_prop.append(grouped[f'{field}_Yes'] / (grouped[f'{field}_Yes'] + grouped[f'{field}_No']))
    no_prop.append(grouped[f'{field}_No'] / (grouped[f'{field}_Yes'] + grouped[f'{field}_No']))

# create a ColumnDataSource object for the stacked bar chart
source = ColumnDataSource(data=dict(fields=fields, yes_prop=yes_prop, no_prop=no_prop))

# create the figure object for the stacked bar chart
stacked_bar = figure(x_range=fields, title="Proportion of employees by JobRole and Attrition Status",
                     toolbar_location=None, tools="")

# add the stacked bar chart glyphs to the figure
stacked_bar.vbar(x='fields', top='yes_prop', width=0.5, source=source, color='green', legend_label='Yes')
stacked_bar.vbar(x='fields', top='no_prop', width=0.5, source=source, color='red', legend_label='No', bottom='yes_prop')

# format the axes and legend
stacked_bar.xaxis.axis_label = "Job Role"
stacked_bar.xaxis.major_label_orientation = math.pi/3
stacked_bar.yaxis.axis_label = "Proportion"
stacked_bar.xgrid.grid_line_color = None
stacked_bar.legend.location = "top_right"
stacked_bar.legend.label_text_font_size = "8pt"

########################################################################################################################

# 4. HEAT MAP of all number fields

# Select only the desired columns: based on numerical values
selected_columns = ['Age', 'DailyRate', 'DistanceFromHome', 'Education', 'HourlyRate', 'JobInvolvement',
                    'WorkLifeBalance', 'EnvironmentSatisfaction', 'YearsAtCompany', 'RelationshipSatisfaction',
                    'JobLevel', 'MonthlyIncome', 'YearsSinceLastPromotion', 'NumCompaniesWorked', 'MonthlyRate',
                    'PercentSalaryHike', 'PerformanceRating', 'StockOptionLevel', 'TotalWorkingYears',
                    'TrainingTimesLastYear']
df_selected = df[selected_columns]

# Compute the correlation matrix
corr_matrix = df_selected.corr()

# Get the column and row names
cols = corr_matrix.columns.tolist()
rows = corr_matrix.index.tolist()

# Reshape the correlation matrix into a long-form dataframe
df_corr = pd.DataFrame(corr_matrix.stack(), columns=['correlation']).reset_index()
df_corr.columns = ['variable_x', 'variable_y', 'correlation']

# Create a color mapper
color_mapper = LinearColorMapper(palette=Magma256[::-1], low=df_corr.correlation.min(), high=df_corr.correlation.max())

# Create the figure
heat_map = figure(title='Correlation Heatmap', x_range=cols, y_range=rows, x_axis_location="above",
                  tools="hover,save")

# Add the rectangles representing the correlation values
heat_map.rect(x="variable_x", y="variable_y", width=1, height=1,
              source=ColumnDataSource(df_corr),
              line_color=None, fill_color=transform('correlation', color_mapper))

# Add the color bar
color_bar = ColorBar(color_mapper=color_mapper, ticker=BasicTicker(),
                     label_standoff=12, border_line_color=None, location=(0, 0))
heat_map.add_layout(color_bar, 'right')

# Set the axis properties
heat_map.axis.axis_line_color = None
heat_map.axis.major_tick_line_color = None
heat_map.axis.major_label_text_font_size = "7pt"
heat_map.axis.major_label_standoff = 0
heat_map.xaxis.major_label_orientation = 1.0

########################################################################################################################

# 5.  HISTOGRAM

# mapping categorical data to 1-0 encoding
df['Attrition'] = df['Attrition'].map({'Yes': 1, 'No': 0})

# load data
df = pd.read_csv('attrition.csv')

# create a histogram plot
hist_male, edges = np.histogram(df[df['Gender'] == 'Male']['Age'], bins=10)
hist_female, _ = np.histogram(df[df['Gender'] == 'Female']['Age'], bins=edges)
source = ColumnDataSource(data=dict(hist_male=hist_male, hist_female=hist_female,
                                    left=edges[:-1], right=edges[1:]))

plot_histogram = figure(title='Age and Gender Distribution of Employees',
                        x_axis_label='Age', y_axis_label='Count')
plot_histogram.quad(top='hist_male', bottom=0, left='left', right='right', source=source,
                    fill_color='#083dff', line_color='white', alpha=0.7, legend_label='Male')
plot_histogram.quad(top='hist_female', bottom='hist_male', left='left', right='right', source=source,
                    fill_color='#fa16a6', line_color='white', alpha=0.7, legend_label='Female')
plot_histogram.legend.location = 'top_right'

# add hover tool
hover = HoverTool(tooltips=[('Age Range', '@left to @right'),
                            ('Male Count', '@hist_male'),
                            ('Female Count', '@hist_female')])
plot_histogram.add_tools(hover)

# #####################################################################################################################

# 6. LINE CHARTS

# Load the Attrition dataset into a pandas dataframe
df = pd.read_csv("attrition.csv")

# Filter the dataset to include only relevant columns
df = df[["YearsAtCompany", "MonthlyIncome", "Attrition"]]

# Create separate dataframes for employees with and without attrition
df_yes = df[df["Attrition"] == "Yes"]
df_no = df[df["Attrition"] == "No"]

# Create ColumnDataSource objects for each dataframe
source_yes = ColumnDataSource(df_yes)
source_no = ColumnDataSource(df_no)

# Group the data by years at company
grouped_yes = df_yes.groupby("YearsAtCompany")
grouped_no = df_no.groupby("YearsAtCompany")

# Calculate the median monthly income for each group
med_monthly_income_yes = grouped_yes["MonthlyIncome"].median()
med_monthly_income_no = grouped_no["MonthlyIncome"].median()

# Create the figure
line_plot = figure(title="Monthly Income by Years at Company", x_axis_label="Years at Company",
                   y_axis_label="Monthly Income")

# Add the lines to the plot
line_plot.line(x=med_monthly_income_yes.index, y=med_monthly_income_yes.values, line_width=2, color="red",
               legend_label="Attrition = Yes")
line_plot.line(x=med_monthly_income_no.index, y=med_monthly_income_no.values, line_width=2, color="blue",
               legend_label="Attrition = No")

# Add a legend
line_plot.legend.location = "top_left"

####################################################################################################################

# grid plot
grid = gridplot([[scatter_plot, donut_plot, plot_histogram], [heat_map, stacked_bar, line_plot]], width=600,
                height=600)
show(grid)

# ---end----
