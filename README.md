# rahti2-fastapi 

## Deploy PostgreSQL to OpenShift

The best way to get a modern PostgreSQL Server for your OpenShift (CSC Rahti) project is using a custom YAML. Check here: https://github.com/fw-teaching/rahti-openshift-yaml


### For push-to-deploy to Rahti2

- Copy the GitHub Webhook url from the BuildConfig of the app instance (cklick the instance, select the Build)
- Set up the Webhook on GitHub (remember application/json)

Note: OpenShift wants the main branch to be named *master* by default, you have two options:
1. Push to origin/master to deploy
2. Change the setting in Openshift to *main*:    
    Edit BuildConfig ==> Show advanced git options ==> Git reference: `main`

See also: https://fastapi.tiangolo.com/deployment/docker/


### For local real-time development using docker-compose

The included compose file will also set up a local DB. 

Rename `.env-example` to `.env` to override the `MODE=production`set in the `Dockerfile`. Note that this needs a valueless declaration of `MODE` in `docker-compose.yml`

To run the container locally:
`docker-compose up --build`
