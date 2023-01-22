# Capital Gains Tax Software

## Contributing
As of now this software allows aggregation of Coinbase and Coinbase Pro transactions based off of their csv file format.
Contributions are encouraged if you're interested, the goal is to allow this to work for many platforms and DEFI platforms concurrently.
To Contribute create a PR.

## Instructions
1. Create an input directory in the base directory and place your Coinbase trades CSV file and your Coinbase Pro trades CSV files. In further iterations other trading csv types will be able to be accomodated
*Make sure python > 3.7 is installed.*
2. Open a command prompt and navigate to the root directory of the project.
3. Run the command "python ProcessData.py" this will take your files in the input folder combine them based off the current Coinbase csv format and calculate based off the HIFO method a sample csv in a capital gains format.
4. The output will be a series of CSV files in the "output" directory. These files will contain your calculated capital gains, sorted by year, using the HIFO method.

**Please note that this software is intended to be used as a tool to assist you in calculating your capital gains tax. It is important that you consult with a tax professional to ensure that you are properly reporting your gains and losses.**

## Support
If you have any questions or issues with this software, please contact me on github or raise an issue.
 