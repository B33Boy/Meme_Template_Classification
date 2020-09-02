'''
    Script that will modify the original "memes_data.tsv" to our required form.
    Will use the save_image_from_url.py to help generate the data

    inputs:
        path_original_data (memes_data.tsv) ->  string
        path_new_data (updated path to root folder) -> string
        (idea here is to seperate the classes into different folders, this makes it easy
        code the classificaion model in tensor flow)

    output:
        creates a fo -> 0 for fail, 1 for success

    sample error handling cases:
        - path does not exist

'''