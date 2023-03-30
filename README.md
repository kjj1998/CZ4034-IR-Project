# CZ4034 Information Retrieval Project

## Set up

### Set up project

Install required libraries and dependencies

``` bash
pip install -r requirements.txt
```

### Set up Solr and create Solr core

1. Navigate to your local installation of Solr (Note: An existing  Java SDK installation is required) </br>

    ``` bash
    cd <your path to solr>/solr-9.1.1
    ```

2. Start Solr

    ``` bash
    bin/solr start
    ```

3. Create Solr core

    ``` bash
    bin/solr create -c mobileaccessories
    ```

### Configure Solr core

1. Navigate to the data folder of this project

    ```bash
    cd <your path>/CZ4034-IR-Project/data
    ```

2. Run the script to configure Solr core

    ```bash
    python configure_solr_core.py
    ```

### Generate embeddings for images

Note: The repo comes with pre-generated embeddings, so you can skip to the next step

1. Navigate to the data folder of this project

    ```bash
    cd <your path>/CZ4034-IR-Project/data
    ```

2. Run the script to generate embeddings

    ```bash
    python generate_embeddings.py
    ```

### Index data into Solr core

1. Navigate to the data folder of this project

    ```bash
    cd <your path>/CZ4034-IR-Project/data
    ```

2. Run the script to index data into Solr core

    ```bash
    python index_data_into_solr.py
    ```

### Run the application

1. Navigate to the root of this project

    ```bash
    cd <your path>/CZ4034-IR-Project
    ```

2. Start the application

    ```bash
    python app.py
    ```

3. Navigate to <http://127.0.0.1:5000> to access the search app
