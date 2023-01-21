<h1>Capital Gains Tax Software</h1>

<h2>Contributing</h2>
As of now this software allows aggregation of Coinbase and Coinbase Pro transactions based off of their csv file format.
Contributions are encouraged if you're interested, the goal is to allow this to work for many platforms and DEFI platforms concurrently.
To Contribute create a PR.

<h2>Instructions</h2>
<ol>
  <li>Create an input directory in the base directory and place your Coinbase trades CSV file and your Coinbase Pro trades CSV files. In further iterations other trading csv types will be able to be accomodated</li>
  <li>Make sure python > 3.7 is installed.</li>
  <li>Open a command prompt and navigate to the root directory of the project.</li>
  <li>Run the command "python ProcessData.py" this will take your files in the input folder combine them based off the current Coinbase csv format and calculate based off the HIFO method a sample csv in a capital gains format.</li>
  <li>The output will be a series of CSV files in the "output" directory. These files will contain your calculated capital gains, sorted by year, using the HIFO method.</li>
</ol>
<p>Please note that this software is intended to be used as a tool to assist you in calculating your capital gains tax. It is important that you consult with a tax professional to ensure that you are properly reporting your gains and losses.</p>
<h2>Support</h2>
<p>If you have any questions or issues with this software, please contact me on github or raise an issue</p>
</br>
