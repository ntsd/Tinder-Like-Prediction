import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("All_Ratings.csv")
    df = df[df.Filename.str.contains("AF")]
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