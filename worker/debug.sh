docker build -f ./Dockerfile -t textise_worker:3.0.0 .

WORKER_GROUP=Hangzhou
WORKER_KEY=testkey12345
WORKER_ROLE=textise

WORKER_ID=debug
WORKER_NAME=Hangzhou-Prod-worker-node-debug
WORKER_LOCATION=杭州

JOBCENTER_SERVER=127.0.0.1:2020

nvidia-docker run \
--name textise_worker_debug \
--network=host \
-e JOBCENTER_SERVER=${JOBCENTER_SERVER} \
-e WORKER_GROUP=${WORKER_GROUP} \
-e WORKER_KEY=${WORKER_KEY} \
-e WORKER_ROLE=${WORKER_ROLE} \
-e WORKER_ID=${WORKER_ID} \
-e WORKER_NAME=${WORKER_NAME} \
-e WORKER_LOCATION=${WORKER_LOCATION} \
-v /data/yn/dzjz/:/juanzong \
-it textise_worker:3.0.0 \
bash
