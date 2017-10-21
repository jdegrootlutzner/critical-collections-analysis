# Critical Collections Analysis
**Final Project for CS181** *(Fall Semester 2017)*

*Team Members:* Julian DeGroot-Lutzner, Sydney Smith, Corbin Bethurem, Julia Seacat

## Background & Motivation 
*What is the problem you are solving?
What is the goal of this project?
Why is your project important?
Why is it interesting as a Big Data problem and who would use it if it were solved?*

Madelynn Dickerson, the information resources coordinator at the Claremont Colleges Library, approached our professor, Mariam Salloum, about having students expand upon a research project within the class Big Data: Applications/Platforms. Dickerson and other librarians piloted a project [described here](http://madelynndickerson.wixsite.com/dh4collections) that could be greatly aided by the tools of Big Data. Dickerson described the project as such:

> \[The Critical Collection Analysis Project] was a pilot study of the ways in which text analysis and other digital humanities tools could be used to understand and evaluate library collections. A team of four librarians collected data about book records created and added to Claremont’s library management system between 1995 – 2015.  The initial study focused on identifying trends in collecting practices of print books related to terrorism.  Book records were downloaded and title information was uploaded to Voyant Tools for text analysis in order to answer questions about how print collecting in terror studies has changed over time. In addition, timelines were created to understand how the library’s collecting patterns aligned to changes in the national political landscape. Our goal for taking this project to the next level is to build a functional, sustainable and user-friendly database of historic library book records for future study.

The pilot project is where our project begins. But first, why is a project like the Critical Collection Analysis project important?

Libraries are flexible spaces that allow people to explore an inclusive range of resources. As such, it is important for a library to have diverse perspectives on an issue so people can create well-rounded opinions. Curators of libraries decide what information is available for its attendants. uman bias is inherent and unavoidable in the resource acquisition process. The project provides an easily executable way to examine possible biases in library collections. Once aggregated and accessible in a database, users can compare the collections of a library to those of other libraries. Additionally, librarians can use text analysis to find to analyze the sentiment and perspective towards a specific topic. Text analysis has its limitations; it is reductivist in the sense that it simplifies an author’s argument, and it is also limited by the human bias of the software developer. However simple, our project is important because text analysis would provide a way to analyze the bias of large library collections quickly and with little effort. 

Much of Big Data is often the process of cleaning and wrangling data. The library's current dataset is unworkably dirty since it comes from two databases, one of which is outdated. Much of the libraries work on the pilot project involved **manually** cleaning the dataset. We will first clean the dataset by using an API to retrieve clean information about all of the recorded books. We will then quantify the amount of books on a given topic and compare it to the amount of books on the same topic at a different liberal arts college's library. Our high reach goal for this semester is to use text analysis on excerpts of books from a specific topic to analyze the bias, if any, of the collection at the Claremont Colleges Library.

## Description of Dataset
![alt text](https://github.com/jdegrootlutzner/critical-collections-analysis/blob/master/original-data-screenshot.png)

The dataset has several variables and only a few will be of interest to us including:

'OCLC'              - Will assist in finding the book in the API.

'RECORD #(BIBLIO)'  - Will assist in finding the book in the API.

'title'             - Many characters in titles were misprinted and this must be cleaned.

'author'            - The author takes has many formats and must be cleaned.

'IMPRINT'           - The published year and location. The data has many formats. Year may be used in analysis.

SUBJECT	            - The subject of the book. This will assist in analysis.

CALL #(BIBLIO)	    - Will assist in finding the book in the API

Other non-important variables are: 'STANDARD #,' 'LANG,' 'LOCATION,' 'MATTYPE,' 'BIBLVL,' 'FY,' 'NOTE,' 'ORD TYPE,' 'VENDOR,' 'Paid Date,' 'Invoice Date,' 'Invoice Num,' 'Amount Paid,' 'Voucher Num,' 'Copies,' 'Sub From,' 'Sub To,' and 'Note'

## Expected Work/Deliverables
Our first step will be to clean the dataset. We will use the book record fields from the original dataset to create a new cleaned dataset. We will need to write Java code in order to return the desired information from the API. The API returns XML code so we will need to write code in order to process the information into the format we want.

Our next step will be to analyze the collection from a quantitative perspective. For example, how many books does the library have on a specific topic? How does this compare with how many books another library has on the same topic or all books published on the topic? To do this we will need to write more code to handle the API and return information on topics. We will use R to visualize and interpret the data.

Our next goal is to use text analysis to analyze the sentiment of books from a certain topic. We are not sure what the specifics of the text analysis are yet. We will compare the text analysis of the books in our library to that of other libraries. 

We may also try to create a website in order to host and allow people to interact with the database.

## Project Enviornments
Java

Eclipse

API - https://platform.worldcat.org/api-explorer/apis/wcapi

R

IBM Watson

## Project Schedule

## Expected Background Materials
Pilot Project (http://madelynndickerson.wixsite.com/dh4collections)

The [original dataset](https://github.com/jdegrootlutzner/critical-collections-analysis/blob/master/7-2013%3D6-2014_books-1.xlsx), the [original "cleaned" dataset](https://github.com/jdegrootlutzner/critical-collections-analysis/blob/master/7-2013%3D6-2014_books-1%20clean-c.xlsx), [cleaning instructions](https://github.com/jdegrootlutzner/critical-collections-analysis/blob/master/DH%20Project%202016%20Data%20Clean%20Up%20Instructions.docx), and [grant proposal](https://github.com/jdegrootlutzner/critical-collections-analysis/blob/master/Collections%20as%20Data%20Sontag%20Grant%20App%202017.docx) are attached in the Github Document.
