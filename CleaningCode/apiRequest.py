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
"""
def requestTitle( title ):
    """ Returns the response from the API given the title """
    # key for permission
    wskey = "vA6NzAaEVpE2Vt3Yh8Bl6wxJc2CKXCrmupTTEdFt2Ezo0lLqnzX9DxjZzhJnhQWps3VwuieCA8T5orBf"
    # call request using
    response = requests.get("http://www.worldcat.org/webservices/catalog/search/worldcat/opensearch?q=" +
                            title + "&wskey=" + wskey)
    return response


def searchForOCLC( line ):
    """" Uses the other information in the entry to try and return the OCLC,
    if this fails return something that will tell me to write to rejects"""
    title = line[3]
    request = requestTitle(title)
    if(request.status_code != 200):
        return 0 # return 0 if the request does not work
    text = request.text.encode('UTF-8')
    #print(text)
    oclcStringLocater = "<oclcterms:recordIdentifier>"
    index = text.split(oclcStringLocater, 1)
    if(len(index) > 1):
        print(len(index))
        print("  ")
        oclc = index[1][1:-2]
        oclc = oclc.split("<",1)
        oclc = oclc[0]
    else:
        oclc = 0 #return 0 if the oclc is not found
    return oclc


def requestOCLC( OCLC ):
    """ Returns the response from the API given the OCLC """
    # key for permission
    wskey = "vA6NzAaEVpE2Vt3Yh8Bl6wxJc2CKXCrmupTTEdFt2Ezo0lLqnzX9DxjZzhJnhQWps3VwuieCA8T5orBf"
    # call request using
    response = requests.get("http://www.worldcat.org/webservices/catalog/content/" +
                            OCLC + "?wskey=" + wskey)
    return response

def helper(array): #puts author into the correct format for our csv output
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

# Possible format for final file
# OCLC, title, authors, publication date, publisher, type (book, movie, etc.), ISBN (from original document), Subject[s], Sub-subject?,
def createRow( OCLC , api_response ):
    ''' Creates a list of book info that will be written to the csv file. If
    there is no relevant information from the category it should return an
    empty spot in the array. '''
    # parse api_response
    record = MARCXMLRecord(api_response.text.encode('UTF-8'))
    #print(record)
    row = [OCLC] #i nitialize list with just OCLC number
    row.append(record.get_name()) # add title
    row.append(helper(record.get_authors())) #add authors
    # TODO: add authors - this needs a helper function bc authors are currently
    # returned as an array
    row.append(record.get_pub_date()) # add publishing date
    row.append(record.get_publisher()) # add publisher
    row.append(helper(record.get_subfields("655", "a", i1=" ", i2="7", exception=False))) #add genre
    row.append(helper(record.get_subfields("520", "a", i1=" ", i2=" ", exception=False))) #add summary
    return row

def main():
    # load in csv file with OCLC
    input_file = open('sampleInput.csv', 'r')
    csv_input_file = csv.reader(input_file)
    # TODO: could use 'csv.DictReader' instead of 'csv.reader', then we can call
    # on data by column name, so by OCLC, ISBN, title, etc.

    # set up output csv file
    output_file = open('output.csv', 'w')
    csv_output_writer = csv.writer(output_file)

    # TODO: Add the 'header' to the cvs_output_writer an array of all the titles

    # set up file to store list of OCLCs that failed the API request
    rejects_file = open('rejects.csv', 'w')
    csv_rejects_writer = csv.writer(rejects_file)

    # TODO: Add the 'header' to the cvs_rejects_writer an array of all the titles

    ''' Iterate through each row of the input csv file.
    TODO: For now I have the input file as just a single column of OCLC numbers,
    which is called 'sampleOCLC.csv.' In the future we can change it to the
    complete 'cleaned' CSV file.

    TODO: Should we make a check to see if the given OCLC number matches up with
    the given title? For example, what if the given OCLC number is a different
    book than what is currently stored in the title and author spot.
    '''
    csv_input_file.next() #skip header
    for line in csv_input_file:
        OCLC_number = line[1]
        if(OCLC_number == ""):
            OCLC_number = searchForOCLC(line)
        if(OCLC_number == 0):
            csv_rejects_writer.writerow([OCLC_number])
        else:     
         result = requestOCLC(OCLC_number)
         if(result.status_code == 200): # returns 200 if the request worked
            csv_output_writer.writerow(createRow(OCLC_number, result))
         else: # if the request returned a different status message
            csv_rejects_writer.writerow([OCLC_number])

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

main()
