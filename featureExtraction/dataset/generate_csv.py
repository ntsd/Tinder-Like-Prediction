import pandas as pd
import sys

if __name__ == "__main__":
    df = pd.read_csv("All_Ratings.csv")
    df = df[df.Filename.str.contains("AF")] # only asian female
    df = df.loc[(df['Rating'] == 1) | (df['Rating'] == 5)] # filter only 1 and 5
    # get all rating
    df.Filename = './dataset/Images/' + df.Filename # add path to Filename
    df = df.filter(items=['Filename', 'Rating']) #filter only Filename Rating column
    df = df.drop_duplicates('Filename') # use drop duplicate file name
    df.columns = ['path', 'class'] # rename column
    df.to_csv('af1and5.csv')
    sys.exit(0)

    # get mean rating of reviewer
    filenames = df.Filename.unique() # one image has arround 60 reviewer
    lis = []
    for filename in filenames:
        lis.append( (filename, df[df.Filename == filename].Rating.mean()) )

    # write to file
    '''
    please download dataset @ https://github.com/HCIILAB/SCUT-FBP5500-Database-Release 
    and place folder `Images` in image in to dataset sub directory 
    '''
    with open("all.csv", 'w') as myfile:
        myfile.write("path,class\n")
        for i in lis:
            myfile.write("./dataset/Images/{},{}\n".format(i[0], i[1]))