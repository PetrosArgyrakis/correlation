import getopt
import sys
import seaborn as sns
import matplotlib.pyplot as plt

import pandas

if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["ifile=", "corr="])
        print(opts)
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    corr = "pearson";

    for opt, arg in opts:
        if opt == "--ifile":
            print("Reading ", arg)
            df = pandas.read_csv(arg, delimiter=';')
        if opt == "--corr":
            corr = arg
            if corr not in ["pearson", "kendall", "spearman"]:
                print("Correlation must be one of \"pearson\", \"kendall\", \"spearman\"")
                sys.exit(2)

    df.drop(columns=['Dates'], inplace=True)
    corr_matrix = df.corr(corr)
    sns.heatmap(corr_matrix, annot=True)
    plt.show()

    print("Done")
