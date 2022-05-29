import getopt
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import pandas
import statsmodels.api as sm
import numpy as np


def r_squared(df_in):
    row_index = column_index = 0
    np_data = np.empty([0, df_in.columns.size], dtype=float)

    for column_x in df_in.columns:
        row_data = []
        for column_y in df_in.columns:
            if column_x == column_y:
                print("(" + str(row_index) + "/" + str(
                    column_index) + ")" + " " + column_x + " | " + column_y + " >> " + "skipping")
                row_data.append(1)
            else:
                rr = sm.OLS(df_in[column_x], df_in[column_y]).fit().rsquared
                row_data.append(rr)
                print("(" + str(row_index) + "/" + str(
                    column_index) + ")" + " " + column_x + " | " + column_y + " >> " + str(rr))
            column_index += 1

        np_data = np.vstack((np_data, np.array(row_data)))
        row_index += 1
        column_index = 0

    return pandas.DataFrame(np_data, index=df_in.columns, columns=df_in.columns)


def show(corr_matrix_in, title):
    sns.heatmap(corr_matrix_in, annot=True)
    plt.title(title)
    plt.show()


if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["ifile=", "corr=", "sheet="])
        print(opts)
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    file = None
    corr = None
    sheet = None

    for opt, arg in opts:
        if opt == "--ifile":
            file = arg
        if opt == "--corr":
            corr = arg
        if opt == "--sheet":
            sheet = arg

    if file is None:
        print("--ifile parameter missing")

    if sheet is None:
        print("--sheet parameter missing")

    if corr is None:
        print("--corr parameter missing")

    if corr not in ["pearson", "kendall", "spearman", "rsquared"]:
        print("Correlation must be one of \"pearson\", \"kendall\", \"spearman\", \"rsquared\"")
        sys.exit(1)

    print("Reading ", file)
    df = pandas.read_excel(file, sheet_name=sheet)
    df.drop(labels='Dates', axis=1, inplace=True)

    if corr in ["pearson", "kendall", "spearman"]:
        corr_matrix = df.corr(corr)
        show(corr_matrix, corr)
        sys.exit(0)
    if corr in ["rsquared"]:
        corr_matrix = r_squared(df)
        show(corr_matrix, corr)
        sys.exit(0)


