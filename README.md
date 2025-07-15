# AI Web Scrapper

## Pre-requisites
- Docker is required to build and run the application containers. Make sure you **start the Docker Engine before running the commands**.
- Ensure that ports `8000` (for the web server) and `27017` (for the database) are available and not in use by other applications.

## Introduction
This project is a Web Scraper powered by AI, designed to extract product information from e-commerce websites. 
It uses Python with FastAPI for the web server and MongoDB to store the LLM model history for a better model performane.

## Design Architecture
- This app is a combination of google search with AI model scrapping.
  1. **Google Search**: All the top product URLs are fetched by google using the query and country from the request.
  2. **AI Scrapping**: All the fetched URLs are provided to the LLM for scrapping. The main reason to involve AI for scrapping is due to the broader problem statemnet. A single scrapper cannot fetch various product details globally. This is humanly not possible and requires a lot of coding. Hence leveraging AI for this use case seems valid.
- MongoDB is introduced to store the history of the previous chat sessions for a better LLM model performance.

## Steps to start up the application
1. Clone the repository:
   ```bash
   git clone https://github.com/abhiramd09/stealth-ai-x-commerce-hiring-assignment.git
   ```
   
2. Navigate to the project directory and then build the Docker containers:
   ```bash
    docker-compose up --build
    ```
   If these logs appear, it means the application has started successfully and is ready to consume requests
   ```
   ai_webscrapper_app | INFO:     Started server process [1]
   ai_webscrapper_app | INFO:     Waiting for application startup.
   ai_webscrapper_app | INFO:     Application startup complete.
   ai_webscrapper_app | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

3. The pervious command will build the Docker images and start the containers. :
   - The web server will be accessible at `http://localhost:8000`.
     1. The webserver exposes the endpoint `GET /get-product-details`
     2. This endpoint accepts a request with the following JSON body.
         ```json
        {
          "country": "UK",
          "query": "apple ipad pro"
        }
        ```
     3. The endpoint returns a list of product details such as product link, price etc.
   - The MongoDB database will be running on `mongodb://mongod:27017`.
4. To stop the application, you can use the following commands:
    - This command will stop the containers and **remove the networks** created by `docker-compose up`.
      ```bash
       docker-compose down
      ```
    - If you want to stop the containers without removing them, you can use:
      ```bash
       docker-compose stop
      ```
    - **Note:** When you stop the containers and restart them, the network ip gets changed. You have to manually remove the old network ip. The error looks like `ERROR: Network "stealth-ai-x-commerce-hiring-assignment_default" needs to be recreated - option "com.docker.network.enable_ipv6" has changed
`In such cases, you can remove the network by running:
      ```bash
       docker network rm stealth-ai-x-commerce-hiring-assignment_default
      ```

5. To start the containers again, you can use:
      ```bash
       docker-compose up
      ```

## Note
- In some responses there might be a slight variation in the price you see in the response and in the product link. This is due to the dynamic nature of e-commerce websites where prices can change frequently and each user can see a different price of the same product.

## Scope of Improvements
- The model used is very generic which is trained on previous data. The pricing number in the response can vary 10 to 20% with the actual price on the website. This can be improved by training a custom model specific for scrapping purpose.
- The model can be experimented with different types of prompts which might generate more accurate results.

## Working Video Proof
This video demonstrates how to start the application locally and run various example queries. As displaying a video in `Readme.md` is  not supported yet, the video can be found in the projects root directory as `/working-video-proof.mp4`.
