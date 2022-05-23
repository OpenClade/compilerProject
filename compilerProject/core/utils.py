import difflib
# check plagiarism of 2 strings in percent
def plagiarism(str1, str2):
    seq = difflib.SequenceMatcher(None, str1, str2)
    return seq.ratio() * 100

 