import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
     print("Usage: python dna.py data.csv sequence.txt")
     return
    # TODO: Read database file into a variable
    suspects_list = []
    patern_list = []
    with open(sys.argv[1], "r") as file:
        reader = csv.reader(file)
        rows = list(reader)
        patern_list = rows[0]
    with open(sys.argv[1], "r") as fileb:
    # Read the file into a list of rows
        new_reader = csv.reader(fileb)
        new_rows = list(new_reader)
        for x in range(1, len(new_rows)):
            name = new_rows[x][0]
            suspect = {
                "name": name,
            }
            for y in range(1, len(new_rows[0])):
                suspect_ = {
                    new_rows[0][y]: new_rows[x][y],
                }
                suspect.update(suspect_)
            suspects_list.append(suspect)
    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as files:
        readers = csv.reader(files)
        sequence = list(readers)[0]
    # TODO: Find longest match of each STR in DNA sequence
    patern_list_2 = []
    patern = {}
    for l in range(1, len(patern_list)):
        patern = {
        patern_list[l]: longest_match(list(sequence), patern_list[l])
        }
        patern_list_2.append(patern)
    # TODO: Check database for matching profiles
    criminal = check_dna(suspects_list, patern_list_2, 0)
    if criminal == []:
        print("No match")
        return
    print(f"{criminal[0]['name']}")
    return

def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence[0])

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[0][start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run
def check_dna(suspects_list, patern_list, n):
    if n == len(patern_list):
        return suspects_list
    new_suspect_list = check_patern(suspects_list, patern_list[n])
    return check_dna(new_suspect_list, patern_list, n+1)
def check_patern(suspects_list, patern):
    suspects_list2 = []
    j = list(patern.keys())[0]
    for suspect in suspects_list:
        if int(suspect[j]) == patern[j]:
            suspects_list2.append(suspect)
    return suspects_list2

main()
