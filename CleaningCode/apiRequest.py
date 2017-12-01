import requests, csv
from sets import Set
from marcxml_parser import MARCXMLRecord

"""
@authors Julian DeGroot-Lutzner & Sydney Smith
@date Fall 2017

This code cleans the original dataset provided by the library. The code iterates
through each entry in the input file and makes a request based on the OCLC
number to the WorldCat Search API.

We wrote code to try and find the OCLC number if it was not given to us. The
functions name is 'searchForOCLC' but it needs more work before we can use it
confidently. To make it work we need to cross-reference the other fields to see
if the entry matches the original book in the database. Additionally, some work
needs to be done to search a substring of a title. For example, the title might
be messy but if we search a smaller piece of it we could find the right book.
We may want to also check if the given OCLC number matches with the entry
described in the original dataset. What if the OCLC number got messed up?
"""
OCLC_LOCATION = 1
BIBLIO_LOCATION = 2
TITLE_LOCATION = 3
CALL_LOCATION = 7
LANG_LOCATION = 8
LOCATION_LOCATION = 9
SUBJECT_LOCATION = 13
WORKING_STATUS_CODE = 200
WSKEY = "O8GluIEWJd5raVAqgurXR0OqeJsAFpHK4oaa1nbU2kxeMmA4e6aZhGTMS0FcyH0LjRLCc3uXAFHFO8PU"

def requestOpenSearch( query ):
    """ Returns the response from the API given the title """
    response = requests.get(
    "http://www.worldcat.org/webservices/catalog/search/worldcat/opensearch?q=" +
                            query + "&wskey=" + WSKEY)
    return response

def requestOCLC( OCLC ):
    """ Returns the response from the API given the OCLC """
    response = requests.get(
    "http://www.worldcat.org/webservices/catalog/content/" +
                            OCLC + "?wskey=" + WSKEY)
    return response

def searchForOCLC( line ):
    """" Uses the other information in the entry to try and return the OCLC.
    If no OCLC number is found return an OCLC value of '0'.
    This function is not finished yet because it does not cross-reference the
    information to see if the book matches the one in the input file """
    request = requestOpenSearch(line[TITLE_LOCATION])
    #request = requestOpenSearch(line[BIBLIO_LOCATION])
    # the Biblio search was not returning anything so I commented it out
    if(request.status_code != WORKING_STATUS_CODE):
        return "0" # return 0 if the request does not work
    text = request.text.encode('UTF-8')
    oclcStringLocater = "<oclcterms:recordIdentifier>"
    text = text.split(oclcStringLocater, 1)
    if(len(text) == 2):        #if the text split
        text = text[1].split("<",1)
        oclc = text[0]
    else:
        #print(requestBiblio(line[2]).text.encode('UTF-8'))
        oclc = "0" #return 0 if the oclc is not found
    return oclc


def helper(array):
    ''' puts author into the correct format for our csv output '''
    text = Set()
    for a in array:
        author = str(a)
        author = author.replace("Person(name=", '')
        author = author.replace(', second_name=', '')
        author = author.replace(", surname=", '')
        author = author.replace(", title=", '')
        text.add(author)
    author = str(list(text))
    #author = author.replace('["'''''''')",','')
    author = author.replace(",", ' ')
    author = author.replace('",',' ')
    author = author.replace('"', '')
    author = author.replace("'", '')
    author = author.replace("[)", '')
    author = author.replace("[", '')
    author = author.replace(")]", '')
    author = author.replace("]", '')
    author = author.replace(".", ' ')
    author = author.replace(")", ',')
    return author

def createRow( oclc_number, line , api_response_text ):
    ''' Creates a list of book info that will be written to the csv file.
    If there is no relevant information from the category it will return an
    empty spot in the array. '''
    # format: ["OCLC", "TITLE", "AUTHORS", "PUB_DATE", "PUBLISHER", "GENRE",
    #           "SUMMARY", "FORMAT", "RECORD #(BIBLIO)", "CALL #(BIBLIO)",
    #            "LANG", "LOCATION", "SUBJECT"]
    record = MARCXMLRecord(api_response_text)
    row = [oclc_number]                                      # Add OCLC
    row.append(record.get_name())                                   # Add title
    row.append(helper(record.get_authors()))                       # Add authors
    row.append(record.get_pub_date())                      # Add publishing date
    row.append(record.get_publisher())                           # Add publisher
    row.append(helper(record.get_subfields(
    "655", "a", i1=" ", i2="7", exception=False)))                  # Add genre
    row.append(helper(record.get_subfields(
    "520", "a", i1=" ", i2=" ", exception=False)))                 # Add summary
    row.append(record.get_format())                                # Add format
    # Add fields from original input
    row.append(line[BIBLIO_LOCATION])
    row.append(line[CALL_LOCATION])
    row.append(line[LANG_LOCATION])
    row.append(line[LOCATION_LOCATION])
    row.append(line[SUBJECT_LOCATION])
    return row

def main():
    # load in csv file with OCLC
    input_file = open('input2.csv', 'r')
    csv_input_file = csv.reader(input_file)

    # set up output csv file
    output_file = open('cleaned_data2.csv', 'w')
    csv_output_writer = csv.writer(output_file)
    csv_output_writer.writerow(
    ["OCLC", "TITLE", "AUTHORS", "PUB_DATE", "PUBLISHER", "GENRE",
    "SUMMARY", "FORMAT", "RECORD #(BIBLIO)", "CALL #(BIBLIO)",
    "LANG", "LOCATION", "SUBJECT"])
    # set up file to store failed entry requests
    rejects_file = open('uncleaned_data2.csv', 'w')
    csv_rejects_writer = csv.writer(rejects_file)
    # write the header of the input to the reject file / skip the header line
    csv_rejects_writer.writerow(csv_input_file.next())

    # Iterate through each row of the input csv file and write to cor. output
    for line in csv_input_file:         # iterate through each line in the input
        OCLC_number = line[OCLC_LOCATION]               # return the OCLC number
        if(OCLC_number == ""):
            csv_rejects_writer.writerow(line)
        # The OCLC number returned by searching for the title does not match
        # with the books in the original database. The searchForOCLC needs more
        # work before we can use it confidently.
        # if(OCLC_number == ""):                    # if the OCLC field is empty
        #    OCLC_number = searchForOCLC(line)              # search for the OCLC
        # if(OCLC_number == "0" or OCLC_number == ""):# if no OCLC number is found
        #    csv_rejects_writer.writerow(line)         # write to the reject file
        else:                                        # if we have an OCLC number
         result = requestOCLC(OCLC_number)           # request info from the API
         if(result.status_code == WORKING_STATUS_CODE):  # if the request worked
            text = result.text.encode('UTF-8')
            if(text.find("<record") >= 0):
                csv_output_writer.writerow(
                createRow(OCLC_number, line, text))       # write row to output
            else:
                csv_rejects_writer.writerow(line)
         else:                                     # if the request did not work
            csv_rejects_writer.writerow(line)         # write to the reject file

    # close files
    input_file.close()
    output_file.close()
    rejects_file.close()

main()
