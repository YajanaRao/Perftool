# Perftool

The ``perftool`` module helps Analyse the performance of command line execution.

The goal of the ``perftool`` module is to allow you to understand the performance of any command line execution, it is compactable with Python 2 and 3.
alongside a Python 2 stack of dependencies.

It is designed to be used as follows:::

	# Interactive console
    python perftool 

	# For Command execution
	python perftool netstat

	# Without reports
	python perftool netstat --report False 

	# For Debug
	python perftool netstat --DEBUG

	# For Multiword commands
	python perftool "netstat -an"
    



Features
Measure the time taken for the execution of system commands and record the performance while executing

## Interactive console for instant report:

![alt text](https://raw.githubusercontent.com/YajanaRao/Perftool/b52d3533/site/images/console.PNG)

&nbsp;
## Detailed Reporting 

## Live Demo
[a link](http://htmlpreview.github.io/?https://github.com/YajanaRao/Perftool/blob/master/site/2018-05-02_19-40-34/index.html)


Example
![alt text](https://raw.githubusercontent.com/YajanaRao/Perftool/261d4034/site/images/PerformanceReport.png)

# Environment
	Windows 10
	Ubuntu 16
	Ubuntu 17
