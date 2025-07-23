import pandas as pd

df1 = pd.DataFrame({"Name": ["田中", "鈴木", "柴田"], 
                    "Group": ["A", "A", "B"],
                    "Point": [1, 2, 2]})

df2 = pd.DataFrame({"Name": ["松井", "柴田"], 
                    "Group": ["A", "B"],
                    "Point": [0, 4]})

df3 = pd.DataFrame({"Name": ["田中", "鈴木", "柴田"],  
                    "Address": ["東京", "大阪", "北海道"]})

df4 = pd.DataFrame({"Name": ["田中", "鈴木", "大井"],  
                    "Address": ["東京", "大阪", "福岡"]})
concat_df = pd.concat([df1, df2], axis=1)

concat_df.to_csv("concat_output.csv", index=True,index_label="No.")