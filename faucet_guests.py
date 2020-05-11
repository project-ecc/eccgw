import pathlib
import pickle
import sys

################################################################################

faucetFileNameAddresses = 'faucet/addresses.dat'
faucetFileNameNodes     = 'faucet/nodes.dat'

faucetAddresses = []
faucetNodes     = []

############################################################

def loadListFile(filePath = ''):

    nullList = []

    if not pathlib.Path(filePath).is_file():

        with open(filePath, 'wb') as f:

            pickle.dump(nullList, f)

            f.close()

            return nullList

    else:

        with open(filePath, 'rb') as f:

            return pickle.load(f)

############################################################

def loadFaucetFiles():

    global faucetAddresses
    global faucetNodes

    faucetAddresses = loadListFile(faucetFileNameAddresses)
    faucetNodes     = loadListFile(faucetFileNameNodes)

############################################################

def saveListFile(list = [], filePath = ''):

    with open(filePath, 'wb') as f:

        pickle.dump(list, f)

        f.close()

############################################################

def saveFaucetFiles():

    saveListFile(faucetAddresses, faucetFileNameAddresses)
    saveListFile(faucetNodes,     faucetFileNameNodes)

################################################################################

################################################################################
### Main program ###############################################################
################################################################################

def main():

    loadFaucetFiles()

    print("Addresses %d" % len(faucetAddresses))
    print("Nodes     %d" % len(faucetNodes))

################################################################################

if __name__ == "__main__":

    main()

################################################################################
