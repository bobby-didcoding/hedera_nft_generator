# [Hedera](https://hedera.com/) NFT generator (Python)
This project has been developed to help you create and mint NFT's on the [Hedera](https://hedera.com/) network.

This is a [Dockerized](https://www.docker.com/) app that uses the following stack:
- Hedera [JAVA SDK](https://docs.hedera.com/guides/docs/sdks) with a [python wrapper](https://pypi.org/project/hedera-sdk-py/)
- [Django web framework](https://www.djangoproject.com/)
- [Celery](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html)
- [Redis](https://redis.io/)
- [IPFS](https://ipfs.tech/)
- [Flower](https://flower.readthedocs.io/en/latest/)

***
***

## Prerequisites
* [Hedera](https://hedera.com/) credentials. You can sign up [here](https://portal.hedera.com/register).
> Please use testnet credentials!
* [Docker & Docker Compose](https://docs.docker.com/desktop/)
* Some artwork would be great :)


***
***

## Repository
Clone or pull from the main branch before you begin coding. Download the zip file if you do not have a GitHub Account.
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
Celery logs are kept away from GitHub. Therefore, we need to create the necessary directories. We also need to create the mediafiles directory
```
mkdir logs
cd logs && echo This is our celery log > celery.log
cd ..
copy media mediafiles
```

***
***

## Environment variable and secrets
1. Create a .env file from .env.template
```
copy .env.template .env
```

2. Update your new .env file with OPERATOR_ID (Public key), OPERATOR_KEY (Secret key), TRAITS (The trait categories i.e. hair or eyes) and TRAIT_QUANTITY (How many images options do you need for each trait?)
```
export OPERATOR_ID=***User your credentials***
export OPERATOR_KEY=***User your credentials***
##name of each trait category separated with a space
export TRAITS=Base Body Pants
export TRAIT_QUANTITY=10
```

***
***

## Fire up Docker:

>Note: You will need to make sure Docker is running on your machine!

Use the following command to build the docker images:
> Note: this command will create the Docker containers and configure everything you need to get started.
```
docker-compose up -d --build
```

### Access
You should now be up and running!

* Your database instances are accessible at [http://localhost:5050](http://localhost:5050)
>Note: You can connect to the database in [PGAdmin](http://localhost:5050). service name is 'db'. database name, username and passwords are all 'hedera' as default.

* The web app is running on  [http://localhost:8000](http://localhost:8000)
* The built in admin page can be found on [http://localhost:8000/admin](http://localhost:8000/admin)
> Note: username is 'demo@hedera-didcoding.com' and password is 'hedera' as default.
* Flower is running on  [http://localhost:5555](http://localhost:5555)

* The IPFS web UI is running on [http://localhost:5001/webui](http://localhost:5001/webui)

***
***

### Add artwork
visit the trait table in the built-in admin page to add the names and artwork for your project.