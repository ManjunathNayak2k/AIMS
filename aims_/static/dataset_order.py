import os 
import argparse
# Function to rename multiple files 
def main(): 
    i = 1   # or set to appropriate start 
    for filename in os.listdir("invoices"): 
        dst = str(i) + ".jpg"
        src = 'invoices/'+ filename 
        dst ='invoices/invoice-'+ dst 
          
        # rename() function will 
        # rename all the files 
        os.rename(src, dst) 
        i += 1
  
# Driver Code
if __name__ == '__main__': 
    main()