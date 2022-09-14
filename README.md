# Hedera NFT generator (Python)
This project has been Dockerized to simplify system set up.
***
***

## Prerequisites
* [Docker & Docker Compose](https://docs.docker.com/desktop/) (<span style="color:orange">Local Development with Docker</span> only)
* [Hedera testnet credentials](https://portal.hedera.com/register)

***
***

## Repository
Clone or pull from the main branch before you begin coding.
```
#option 1 - SSH
git clone git@github.com:bobby-didcoding/hedera_nft_generator.git .

#option 2 - Github CLI
gh repo clone bobby-didcoding/hedera_nft_generator .

#option 3 - HTTPS
git clone https://github.com/bobby-didcoding/hedera_nft_generator.git .
```

***
***

## Celery Logs
Celery logs are kept away from GitHub. Therefore, we need to create the necessary directories.
```
cd logs && echo This is our celery log > celery.log
cd ../..
```

***
***

## Environment variable and secrets
1. Create a .env file from .env.template
    ```
    #Unix and MacOS
    cp .env.template .env

    #windows
    copy .env.template .env
    ```

2. Update your new .env file. Work your way down the .env file and add secrets where necessary.

***
***

## Fire up Docker:

>Note: You will need to make sure Docker is running on your machine!

Use the following command to build the docker images:
```
docker-compose up -d --build
```

### Finished
You should now be up and running!

* Your database instances are accessible at [http://localhost:5050](http://localhost:5050)
* The web app is running on  http://localhost:8000
* Flower is running on  http://localhost:5555
* IPFS is running on http://localhost:5001/webui

>Note: You can connect to the database in [http://localhost:5050](PGAdmin). All you need is the IP addresses and database names.

***
***
