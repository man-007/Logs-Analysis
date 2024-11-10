from fetchFiles import fetchFiles
from process import process

if __name__ == "__main__":
    parent_folder = "/Users/manas/Downloads"

    #------------------------------------------------fetch All files----------------------------------------------
    fetch_files = fetchFiles(parent_folder)
    save_files = fetch_files.fetch()
    res = fetch_files.saveData("artifactInfo.json")
    print(res)

    #-------------------------------------process the files according to first Run/final Failures-----------------------

    process_file = process(parent_folder, res['keysInfo'], 2, True)

    resp = process_file.processArtifactsDirListData(res['fileName'])
    process_file.saveData(resp['data'], "artifactInfo.json")
    processResp = process_file.processFileData("artifactInfo.json")
    print(processResp)


    process_file.fileKeysInfo = processResp["keysInfo"]
    process_file.artifacts = {'data': {}}
    respo = process_file.processArtifactsDirListData("failures.json")
    process_file.saveData(respo['data'], "failures.json")


    #----------------------------------------Create an output-----------------------------------------------------------

    """
    TODO: for extension of the script
        1. Add the script to extract the failure reason and story it in csv/json file.
            a. Maybe extract the Assertion Failure.
        2. Add the script/ML model to process the jenkins Logs/failures and put it in some catageory
        3. 
    """
