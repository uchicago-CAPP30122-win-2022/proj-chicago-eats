PLATFORM=$(python3 -c 'import platform; print(platform.system())')

echo -e "1. Creating new virtual environment..."

# Remove the env directory if it exists
if [[ -d env ]]; then
    echo -e "\t--Replacing the virtual environment that already exists
                with a new one."
    rm -rf env
fi

python3 -m venv env 

if [[ ! -d env ]]; then
    echo -e "\t--Could not create virtual environment... Please make sure venv
                is installed."
    exit 1
fi

echo -e "2. Installing Requirements..."
if [[ ! -e "requirements.txt" ]]; then
    echo -e "\t--Directory does not contain requirements.txt to install
            packages."
    exit 1
fi

source env/bin/activate
pip install -r requirements.txt

# Fill in any additional libraries that need to be installed.  

deactivate 
echo -e "Install is complete."