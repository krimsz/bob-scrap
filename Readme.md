# Description

The project contains 2 different, clearly separated areas:
  
  - Scrapping and processing, contained in the `scrap` folder
    - `spider.py` contains the logic to parse the webpages and store the results in local files (raw original html and processed JSON files)
    - `sanitize_and_restructure_json.py` contains the logic to enhance the data with fields for easy indexing by elasticsearch and create a new structure of directories with only the JSON files for convenience
    - `insert_elasticsearch.py` contains the logic to read all the json files saved by the previous script and store them in a local elasticsearch
    
  - Display of the information, contained in the `front` folder
    - This is a web application written with Angular in Typescript that will straight away consume the elasticsearch
    
## How to run the project locally

### Get the data
First thing that needs to happen is that you have the data loaded in a elasticsearch instance. In order to do this, please run in order the following scripts
    - `spider.py`. This will take several hours. The path for downloads specified inside must exist beforehand (by default, create a `scrapped_data` folder from the context path where you are executing the python command)
    - `sanitize_and_restructure_json.py`. This will take several minutes and has a requirement the execution the previous script and the existance of the folder `json_posts`

### Startup elasticsearch
After this ran correctly, it's time to upload the data to an elasticsearch instance. To run one locally, assuming you have docker installed please run
    - `docker-compose up` Needs to be run from the root level, where the `docker-compose.yml` file is located

This will start a local elasticsearch and store the data in a named volume. If you want to reuse the data once its loaded there, please point the volume to a local directory and reuse it later. If the elasticsearch instance in the docker can access the indexes stored in the docker path `/usr/share/elasticsearch/data` then the docker can be considered prepopulated.
    
### Populate data inside elasticsearch
Simply use the script `insert_elasticsearch.py` that assumes that you have elasticsearch reachable on `localhost:9200`

### Configure and run the front
Install the dependencies
    - `npm install` from the directory `front/bob-future`. You will need to have `npm` installed beforehand
Edit the contents of `front/bob-future/src/environments`.
    - If you plan to just run it locally
        - Edit `environment.ts` if needed and point it to the right host where elastic is running
        - Run the development server using `ng serve`
    - If you plan to deploy it somewhere, you'll probably need to build and transpile TS to JS
        - Edit `environment.prod.ts` if needed and point it to the right host where elastic is running
        - Run the development server using `ng build --prod`
        - Place the content of the generated `front/bob-future/dist/bob-future` in your web server of choice

### Running all together

If you want to run it all in one, there is also the file `docker-compose-with-front.yml` that assumes that the build for production for the front has already happened.
  - `docker-compose -f docker-compose-with-front.yml up`
