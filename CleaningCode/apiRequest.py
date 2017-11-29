import requests, csv
from sets import Set
from marcxml_parser import MARCXMLRecord

"""
TODO:
    - Questions
        - What are we going to do if the row does not have an OCLC number?
            Maybe we could search by title, then get the OCLC num of the first
            result
        - What should we do with repeats of books in the current cleaned file?
            Why are there repeats?
        -
    - Jobs related to createRow function
        - Helper function for authors (parser currently returns as array)
        - How do we return subject, Sub-subject, and notes? These are all
            available from API and will be crucial in future text analysis
        - Helper function for type of entry (book, movie, etc.)
        - The formats aren't all the same! We might have to parse them more?

    TODO: Should we make a check to see if the given OCLC number matches up with
    the given title? For example, what if the given OCLC number is a different
    book than what is currently stored in the title and author spot.

"""
OCLC_LOCATION = 1
BIBLIO_LOCATION = 2
TITLE_LOCATION = 3
WORKING_STATUS_CODE = 200
WSKEY = "vA6NzAaEVpE2Vt3Yh8Bl6wxJc2CKXCrmupTTEdFt2Ezo0lLqnzX9DxjZzhJnhQWps3VwuieCA8T5orBf"

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
    If no OCLC number is found return an OCLC value of '0' """
    request = requestOpenSearch(line[TITLE_LOCATION])
    #request = requestOpenSearch(line[BIBLIO_LOCATION])
    # the Biblio search was not returning anything so I commented it out
    if(request.status_code != WORKING_STATUS_CODE):
        return "0" # return 0 if the request does not work
    text = request.text.encode('UTF-8')
    oclcStringLocater = "<oclcterms:recordIdentifier>"
    text = text.split(oclcStringLocater, 1)
    if(len(index) == 2):        #if the text split
        text = text[1].split("<",1)
        oclc = oclc[0]
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

def createRow( OCLC , api_response ):
    ''' Creates a list of book info that will be written to the csv file.
    If there is no relevant information from the category it will return an
    empty spot in the array. '''
    # format: [OCLC, title, authors, pub_date, publisher, genre, summary]
    record = MARCXMLRecord(api_response.text.encode('UTF-8'))
    row = [OCLC]                                                     # Add OCLC
    row.append(record.get_name())                                   # Add title
    row.append(helper(record.get_authors()))                       # Add authors
    row.append(record.get_pub_date())                      # Add publishing date
    row.append(record.get_publisher())                           # Add publisher
    row.append(helper(record.get_subfields(
    "655", "a", i1=" ", i2="7", exception=False)))                  # Add genre
    row.append(helper(record.get_subfields(
    "520", "a", i1=" ", i2=" ", exception=False)))                 # Add summary
    return row

def main():
    # load in csv file with OCLC
    input_file = open('sampleInput.csv', 'r')
    csv_input_file = csv.reader(input_file)

    # set up output csv file
    output_file = open('output.csv', 'w')
    csv_output_writer = csv.writer(output_file)
    csv_output_writer.writerow(
    ["OCLC", "TITLE", "AUTHORS", "PUB_DATE", "PUBLISHER", "GENRE", "SUMMARY"])
    # RECORD #(BIBLIO)      2
    # CALL #(BIBLIO)        7
    # LANG                  8
    # LOCATION              9
    # SUBJECT               13
    # set up file to store failed entry requests
    rejects_file = open('rejects.csv', 'w')
    csv_rejects_writer = csv.writer(rejects_file)
    # write the header of the input to the reject file / skip the header line
    csv_rejects_writer.writerow(csv_input_file.next())

    # Iterate through each row of the input csv file and write to cor. output
    for line in csv_input_file:         # iterate through each line in the input
        OCLC_number = line[OCLC_LOCATION]               # return the OCLC number
        if(OCLC_number == ""):                      # if the OCLC field is empty
            OCLC_number = searchForOCLC(line)              # search for the OCLC
        if(OCLC_number == "0" or OCLC_number == ""):# if no OCLC number is found
            csv_rejects_writer.writerow(line)         # write to the reject file
        else:                                        # if we have an OCLC number
         result = requestOCLC(OCLC_number)           # request info from the API
         if(result.status_code == WORKING_STATUS_CODE):  # if the request worked
            csv_output_writer.writerow(
            createRow(OCLC_number, result))                # write row to output
         else:                                      # if the request did not work
            csv_rejects_writer.writerow(line)         # write to the reject file

    # close files
    input_file.close()
    output_file.close()
    rejects_file.close()


def test_parsing_calls():
    ''' This function shows an example of what each highlevel getter returns
    for the marcxml_parser. Here is the complete API request to see all the
    information that the worldcat database has available.
     http://www.worldcat.org/webservices/catalog/content/82671871?wskey=vA6NzAaEVpE2Vt3Yh8Bl6wxJc2CKXCrmupTTEdFt2Ezo0lLqnzX9DxjZzhJnhQWps3VwuieCA8T5orBf
    As you can see, we still have work to do.
    '''
    OCLC = "82671871"
    request = requestOCLC(OCLC)
    record = MARCXMLRecord(request)
    print(record.get_name())
    print(record.get_subname())
    print(record.get_price())
    print(record.get_part())
    print(record.get_part_name())
    print(record.get_publisher())
    print(record.get_pub_date())
    print(record.get_pub_order())
    print(record.get_pub_place())
    print(record.get_format())
    print(record.get_authors())
    print(record.get_corporations())
    print(record.get_distributors())
    print(record.get_ISBNs())
    print(record.get_binding())
    print(record.get_originals())

def testingTitle():
    sampleLine = ["","","","The unwinding: an inner history of the new America"]
    searchForOCLC(sampleLine)

def test():
    text = "yabadaba<oclcterms:recordIdentifier>10<adsfasd"
    oclcStringLocater = "<oclcterms:recordIdentifier>"
    text = text.split(oclcStringLocater, 1)
    print(text[0], text[1])
    text = text[1].split("<", 1)
    print(text[0] == "9" or text[0] == "10")
#main()
test()
