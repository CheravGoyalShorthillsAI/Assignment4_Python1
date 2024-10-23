from data_extractor.data_extractor.extractorHelper import ExtractData
from data_extractor.storage.save_data import SaveData

def main():
    # Get the file path
    file_path = input("Enter the file path: ")
    
    # check if empty string is given as the file path
    if not file_path:
        raise ValueError("FILE_PATH is not given.")

    # Extract the data
    helper = ExtractData(file_path)
    data = helper.extractData()

    # Save the extracted data
    saving_strategies = [SaveData.saveToLocal, SaveData.saveToSQLDatabase]

    # Save using each strategy
    saver = SaveData(data, file_path)
    for strategy in saving_strategies:
        strategy(saver)

if __name__ == "__main__":
    main()
